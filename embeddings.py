import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sqlalchemy import Table, create_engine, Column, Integer, String, MetaData, Text,delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configuration de la base de données
DATABASE_URL = "mysql+pymysql://root:@localhost/webbrowser"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Charger le modèle pour générer les embeddings
model = SentenceTransformer('all-mpnet-base-v2')

# Mise à jour de la table Embeddings avec de nouvelles colonnes
embeddings_table = Table(
    'Embeddings', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('link_id', Integer, unique=True),
    Column('embedded_title', Text),  # Embedding pour le titre
    Column('embedded_keywords', Text),  # Embedding pour les mots-clés
    Column('embedded_paragraphs', Text),  # Embedding pour les paragraphes importants
    Column('embedded_h1', Text),  # Embedding pour les balises H1
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

links_table = Table(
    'Links', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('url', String, unique=True),
    Column('title', String),
    Column('h1_tags', Text),
    Column('important_paragraphs', Text),
    Column('keywords', Text),
)

# Fonction pour récupérer le contenu et générer les embeddings spécifiques
def get_embeddings_from_content(title, keywords, paragraphs, h1_tags):
    embeddings = {
        "title": model.encode(title) if title else None,
        "keywords": model.encode(keywords) if keywords else None,
        "paragraphs": model.encode(paragraphs) if paragraphs else None,
        "h1": model.encode(h1_tags) if h1_tags else None
    }
    return embeddings

# Extraction des liens de la table Links et génération des embeddings
def generate_and_store_embeddings():
    with Session() as session:
        # Récupérer les IDs déjà présents dans Embeddings
        existing_ids = {row[0] for row in session.query(embeddings_table.c.link_id).all()}
        
        # Récupérer tous les liens et filtrer ceux qui ne sont pas dans Embeddings
        links = session.query(links_table).filter(~links_table.c.id.in_(existing_ids)).all()
        
        total_links = len(links)
        completed = 0
        
        for link in links:
            # Récupérer chaque élément de contenu
            title = link.title
            keywords = link.keywords
            paragraphs = link.important_paragraphs
            h1_tags = link.h1_tags
            
            # Générer les embeddings pour chaque partie
            embeddings = get_embeddings_from_content(title, keywords, paragraphs, h1_tags)
            
            # Vérifie que chaque embedding est présent sans évaluer les tableaux Numpy directement
            if any(embedding is not None for embedding in embeddings.values()):
                try:
                    # Conversion des embeddings en chaîne JSON pour chaque élément
                    embedding_title = json.dumps(embeddings["title"].tolist()) if embeddings["title"] is not None else None
                    embedding_keywords = json.dumps(embeddings["keywords"].tolist()) if embeddings["keywords"] is not None else None
                    embedding_paragraphs = json.dumps(embeddings["paragraphs"].tolist()) if embeddings["paragraphs"] is not None else None
                    embedding_h1 = json.dumps(embeddings["h1"].tolist()) if embeddings["h1"] is not None else None
                    
                    # Insérer dans la table Embeddings
                    stmt = embeddings_table.insert().values(
                        link_id=link.id,
                        embedded_title=embedding_title,
                        embedded_keywords=embedding_keywords,
                        embedded_paragraphs=embedding_paragraphs,
                        embedded_h1=embedding_h1
                    )
                    session.execute(stmt)
                    session.commit()
                    completed += 1
                    print(f"ID {link.id} ajouté. Total complété : {completed}/{total_links}. Restants : {total_links - completed}")
                except IntegrityError:
                    session.rollback()
                    print(f"Le lien avec ID {link.id} existe déjà dans la table Embeddings.")



def delete_orphan_links():
    # Récupérer tous les link_id présents dans Embeddings
    existing_link_ids = {row[0] for row in session.query(embeddings_table.c.link_id).all()}
    
    # Sélectionner les liens dans Links qui n'ont pas de correspondance dans Embeddings
    orphan_links = session.query(links_table).filter(~links_table.c.id.in_(existing_link_ids)).all()
    
    # Supprimer les liens orphelins
    deleted_count = 0
    for link in orphan_links:
        stmt = delete(links_table).where(links_table.c.id == link.id)
        session.execute(stmt)
        session.commit()
        deleted_count += 1
        print(f"Lien {link.url} supprimé (ID {link.id}).")

    print(f"Nettoyage terminé. Total de liens supprimés : {deleted_count}")

def search_similar_links(user_query, top_n=10):
    # Calculer l'embedding pour la recherche utilisateur
    query_embedding = model.encode(user_query)
    
    # Récupérer tous les embeddings stockés dans la base de données
    with Session() as session:
        results = session.query(
            embeddings_table.c.link_id,
            embeddings_table.c.embedded_title,
            embeddings_table.c.embedded_keywords,
            embeddings_table.c.embedded_paragraphs,
            embeddings_table.c.embedded_h1
        ).all()
        
        # Liste pour stocker les similitudes et les IDs des liens
        similarities = []
        
        for result in results:
            link_id = result.link_id
            embeddings = [
                json.loads(result.embedded_title) if result.embedded_title else None,
                json.loads(result.embedded_keywords) if result.embedded_keywords else None,
                json.loads(result.embedded_paragraphs) if result.embedded_paragraphs else None,
                json.loads(result.embedded_h1) if result.embedded_h1 else None,
            ]
            
            # Calcul de la similarité cosinus pour chaque embedding existant
            similarities_for_link = []
            for embedding in embeddings:
                if embedding is not None:
                    similarity = cosine_similarity(
                        [query_embedding], [np.array(embedding)]
                    )[0][0]
                    similarities_for_link.append(similarity)
            
            # Moyenne de la similarité pour ce lien (ignorer les valeurs None)
            if similarities_for_link:
                avg_similarity = np.mean(similarities_for_link)
                similarities.append((link_id, avg_similarity))
        
        # Trier les liens par similarité décroissante et prendre les top_n plus proches
        top_links = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]
        
        # Récupérer les informations des liens les plus proches
        top_link_ids = [link[0] for link in top_links]
        closest_links = session.query(links_table).filter(links_table.c.id.in_(top_link_ids)).all()
        
        # Renvoyer les informations des liens les plus similaires
        return [{"id": link.id, "url": link.url} for link in closest_links]


print(search_similar_links("I want to learn the wave management in LOL ",5))

