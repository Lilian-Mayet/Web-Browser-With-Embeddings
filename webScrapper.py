import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, func,delete, Text
from sqlalchemy.orm import sessionmaker
import random
import time
from sqlalchemy.exc import IntegrityError
import threading
import queue

# Configuration de la base de données
DATABASE_URL = "mysql+pymysql://root:@localhost/webbrowser"

# Connexion à la base de données et création de la table Links si elle n'existe pas
engine = create_engine(DATABASE_URL)
metadata = MetaData()

links_table = Table(
    'Links', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('url', String, unique=True),
    Column('title', String),
    Column('h1_tags', Text),
    Column('important_paragraphs', Text),
    Column('keywords', Text),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def clean_invalid_links():
    # Récupérer tous les liens de la table Links
    links = session.query(links_table).all()
    total_links = len(links)
    deleted_count = 0

    for link in links:
        try:
            # Essayer d'ouvrir le lien
            response = requests.get(link.url, timeout=5)
            response.raise_for_status()  # Vérifier que la requête est réussie (code 200)
            print(f"Le lien {link.url} est accessible.")
        except requests.RequestException:
            # Si une erreur survient, supprimer le lien
            print(f"Le lien {link.url} est inaccessible, suppression en cours.")
            stmt = delete(links_table).where(links_table.c.id == link.id)
            session.execute(stmt)
            session.commit()
            deleted_count += 1

    print(f"Nettoyage terminé. Total de liens supprimés : {deleted_count}/{total_links}")


# Fonction pour extraire les liens d'une page web
def fetch_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        # Nettoyage et formatage des liens (absolus)
        links = [link for link in links if link.startswith('http')]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

# Fonction pour ajouter des liens à la base de données
def add_links_to_db(links):
    added_count = 0
    for link in links:
        try:
            session.execute(
                "INSERT INTO Links (url) VALUES (:url) ON DUPLICATE KEY UPDATE url=url",
                {"url": link}
            )
            added_count += 1
        except IntegrityError:
            session.rollback()
            print(f"Doublon ignoré : {link}")
    session.commit()
    return added_count

# Fonction pour récupérer un lien aléatoire dans la base de données
def get_random_link_from_db():
    result = session.query(links_table).order_by(func.random()).first()
    if result:
        return result.url
    return None

# Fonction principale pour continuer le crawling
def start_crawling(initial_url, max_sites=100000):
    queue = [initial_url]
    crawled_links = set()
    total_links_added = 0
    
    while total_links_added < max_sites:
        url = queue.pop(0)
        if url in crawled_links:
            continue
        
        print(f"Crawling: {url}")
        crawled_links.add(url)
        
        # Récupération et ajout des liens trouvés dans la base de données
        links = fetch_links(url)
        added_links = add_links_to_db(links)
        total_links_added += added_links
        
        print(f"Liens ajoutés: {added_links}, Total: {total_links_added}")
        
        # Ajouter de nouveaux liens à la file d'attente pour les futurs crawls
        for link in links:
            if link not in crawled_links:
                queue.append(link)
        
        # Si la file est vide, choisir un lien aléatoire dans la base de données
        if not queue:
            random_link = get_random_link_from_db()
            if random_link:
                queue.append(random_link)
        
        # Petite pause pour éviter de surcharger les serveurs
        time.sleep(1)

    print("Crawling terminé.")
    session.close()

def is_valid_url(url):
    """Vérifie si l'URL est valide et accessible."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def fetch_and_store_url_content(url):
    """Récupère le titre, les balises h1, les paragraphes importants et les mots-clés d'une URL et les stocke dans la base de données."""
    session = Session()  # Crée une nouvelle session par appel de fonction
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string if soup.title else "No Title"
        h1_tags = " | ".join([h1.get_text() for h1 in soup.find_all('h1')])
        paragraphs = soup.find_all('p')
        important_paragraphs = " | ".join(
            [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
        )[:1000]  # Limiter à 1000 caractères pour éviter les entrées trop longues

        # Récupérer les mots-clés de la balise meta
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords_tag["content"] if keywords_tag else ""

        # Insertion dans la base de données
        stmt = links_table.insert().values(url=url, title=title, h1_tags=h1_tags, important_paragraphs=important_paragraphs, keywords=keywords)
        session.execute(stmt)
        session.commit()
        print(f"Ajouté : {url} avec titre, contenu et mots-clés.")
    except IntegrityError:
        session.rollback()
        print(f"L'URL {url} est déjà présente dans la base de données.")
    except Exception as e:
        session.rollback()  # Rollback en cas d'erreur
        print(f"Erreur lors de l'ajout de {url}: {e}")
    finally:
        session.close()  # Toujours fermer la session après utilisation

def crawl_web(seed_urls, max_levels=3, max_urls_per_level=100):
    """Parcours récursif de niveaux de files d'attente pour crawler les sites Web."""
    current_queue = seed_urls
    visited_urls = set()

    for level in range(max_levels):
        print(f"--- Niveau {level + 1} ---")
        next_queue = []

        for url in current_queue:
            if url not in visited_urls and is_valid_url(url):
                fetch_and_store_url_content(url)
                visited_urls.add(url)

                try:
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        new_url = link['href']
                        if new_url.startswith('http') and new_url not in visited_urls:
                            next_queue.append(new_url)
                            if len(next_queue) >= max_urls_per_level:
                                break
                except requests.RequestException:
                    pass

            #if len(next_queue) >= max_urls_per_level:
            #    break

        # Passer à la nouvelle queue pour le prochain niveau

        current_queue = next_queue

        random.shuffle(current_queue)

        if not current_queue:
            print("Plus de liens à crawler.")
            break


def worker(url_queue, visited_urls):
    """Fonction de travail pour chaque thread."""
    while not url_queue.empty():
        url = url_queue.get()
        if url not in visited_urls and is_valid_url(url):
            fetch_and_store_url_content(url)
            visited_urls.add(url)
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    new_url = link['href']
                    if new_url.startswith('http') and new_url not in visited_urls:
                        url_queue.put(new_url)
            except requests.RequestException:
                pass
        url_queue.task_done()

def start_crawling(seed_urls, num_threads=5):
    """Démarre le crawling en utilisant plusieurs threads."""
    url_queue = queue.Queue()
    visited_urls = set()
    session = Session()

    # Ajoute les URL de départ dans la file d'attente
    for url in seed_urls:
        url_queue.put(url)

    # Crée et démarre les threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(url_queue, visited_urls))
        thread.start()
        threads.append(thread)
        # Attendre que toutes les tâches soient terminées


    # Attendre que toutes les tâches soient terminées
    url_queue.join()

    # Arrêter les threads
    for thread in threads:
        thread.join()

    session.close()


# Exemples de liens pour démarrer le crawler
seed_urls = [

           "https://www.britannica.com",          
    "https://www.buzzfeed.com",
        "https://www.shopify.com",              # E-commerce platform
    "https://www.codepen.io",               # Web development playground
    "https://www.entrepreneur.com",         # Business
    "https://www.investopedia.com",         # Finance and investment
    "https://www.zooniverse.org", 
        "https://www.bloomberg.com",            # Finance and news
    "https://www.tripadvisor.com",          # Travel and reviews
    "https://www.behance.net",              # Creative portfolio
    "https://www.deviantart.com",




]


random.shuffle(seed_urls)
start_crawling(seed_urls, num_threads=7)
