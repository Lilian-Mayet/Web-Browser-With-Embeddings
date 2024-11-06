import numpy as np
from sentence_transformers import SentenceTransformer
import json
from sqlalchemy import Table, create_engine, Column, Integer, String, MetaData, Text,delete
from database import links_table, Session, embeddings_table
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.exc import IntegrityError
from config import DOMAIN_CATEGORIES,EMBEDDINGS_MODEL
from typing import List, Dict, Set

# Load the model for generating embeddings
model = SentenceTransformer(EMBEDDINGS_MODEL)

def generate_domain_embeddings():
    """Generate embeddings for each domain category"""
    domain_embeddings = {}
    for domain, content in DOMAIN_CATEGORIES.items():
        # Create embedding from keywords and description
        text_to_embed = " ".join(content["keywords"]) + " " + content["description"]
        domain_embeddings[domain] = model.encode(text_to_embed)
    return domain_embeddings

def classify_content_domains(
    title_embedding: np.ndarray = None,
    keywords_embedding: np.ndarray = None,
    paragraphs_embedding: np.ndarray = None,
    h1_embedding: np.ndarray = None,
    similarity_threshold: float = 0.33
) -> Set[str]:
    """
    Classify content into domains based on embeddings
    Returns a set of matching domains
    """
    domain_embeddings = generate_domain_embeddings()
    matching_domains = set()
    
    # Combine all available embeddings
    content_embeddings = []
    if title_embedding is not None:
        content_embeddings.append(np.array(title_embedding))
    if keywords_embedding is not None:
        content_embeddings.append(np.array(keywords_embedding))
    if paragraphs_embedding is not None:
        content_embeddings.append(np.array(paragraphs_embedding))
    if h1_embedding is not None:
        content_embeddings.append(np.array(h1_embedding))
    
    if not content_embeddings:
        return matching_domains
    
    # Calculate average embedding for content
    average_embedding = np.mean(content_embeddings, axis=0)
    
    # Compare with each domain
    for domain, domain_embedding in domain_embeddings.items():
        similarity = cosine_similarity([average_embedding], [domain_embedding])[0][0]
        if similarity > similarity_threshold:
            matching_domains.add(domain)
    
    return matching_domains

def update_content_domains():
    """Update domains for all entries in the embeddings table"""
    with Session() as session:
        # Get all embeddings
        results = session.query(embeddings_table).all()
        total = len(results)
        
        for i, row in enumerate(results, 1):
            try:
                # Parse stored embeddings
                title_embedding = json.loads(row.embedded_title) if row.embedded_title else None
                keywords_embedding = json.loads(row.embedded_keywords) if row.embedded_keywords else None
                paragraphs_embedding = json.loads(row.embedded_paragraphs) if row.embedded_paragraphs else None
                h1_embedding = json.loads(row.embedded_h1) if row.embedded_h1 else None
                
                # Classify content
                domains = classify_content_domains(
                    title_embedding,
                    keywords_embedding,
                    paragraphs_embedding,
                    h1_embedding
                )
                
                # Update database using SQLAlchemy update statement
                if domains:
                    update_stmt = embeddings_table.update().where(
                        embeddings_table.c.link_id == row.link_id
                    ).values(
                        domains=json.dumps(list(domains))
                    )
                    session.execute(update_stmt)
                    session.commit()
                    print(f"Updated domains for ID {row.link_id} ({i}/{total}): {domains}")
                else:
                    print(f"No matching domains found for ID {row.link_id} ({i}/{total})")
                    
            except Exception as e:
                print(f"Error processing ID {row.link_id}: {str(e)}")
                session.rollback()
                continue


def get_embeddings_from_content(title, keywords, paragraphs, h1_tags):
    embeddings = {
        "title": model.encode(title) if title else None,
        "keywords": model.encode(keywords) if keywords else None,
        "paragraphs": model.encode(paragraphs) if paragraphs else None,
        "h1": model.encode(h1_tags) if h1_tags else None
    }
    return embeddings

def generate_and_store_embeddings():
    with Session() as session:
        existing_ids = {row[0] for row in session.query(embeddings_table.c.link_id).all()}
        links = session.query(links_table).filter(~links_table.c.id.in_(existing_ids)).all()
        total_links = len(links)
        completed = 0

        for link in links:
            title = link.title
            keywords = link.keywords
            paragraphs = link.important_paragraphs
            h1_tags = link.h1_tags

            embeddings = get_embeddings_from_content(title, keywords, paragraphs, h1_tags)

            if any(embedding is not None for embedding in embeddings.values()):
                try:
                    embedding_title = json.dumps(embeddings["title"].tolist()) if embeddings["title"] is not None else None
                    embedding_keywords = json.dumps(embeddings["keywords"].tolist()) if embeddings["keywords"] is not None else None
                    embedding_paragraphs = json.dumps(embeddings["paragraphs"].tolist()) if embeddings["paragraphs"] is not None else None
                    embedding_h1 = json.dumps(embeddings["h1"].tolist()) if embeddings["h1"] is not None else None

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
                    print(f"ID {link.id} added. Total completed: {completed}/{total_links}. Remaining: {total_links - completed}")
                except IntegrityError:
                    session.rollback()
                    print(f"The link with ID {link.id} already exists in the Embeddings table.")

def delete_orphan_links():
    with Session() as session:
        existing_link_ids = {row[0] for row in session.query(embeddings_table.c.link_id).all()}
        orphan_links = session.query(links_table).filter(~links_table.c.id.in_(existing_link_ids)).all()
        deleted_count = 0
        for link in orphan_links:
            stmt = delete(links_table).where(links_table.c.id == link.id)
            session.execute(stmt)
            session.commit()
            deleted_count += 1
            print(f"Link {link.url} deleted (ID {link.id}).")

        print(f"Cleanup finished. Total links deleted: {deleted_count}")