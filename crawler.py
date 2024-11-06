import requests
from bs4 import BeautifulSoup
import random
import time
from sqlalchemy.exc import IntegrityError
import threading
import queue

from database import add_links_to_db, get_random_link_from_db, links_table,Session

def fetch_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        links = [link for link in links if link.startswith('http')]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return []

def is_valid_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def fetch_and_store_url_content(url):
    with Session() as session:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.string if soup.title else "No Title"
            h1_tags = " | ".join([h1.get_text() for h1 in soup.find_all('h1')])
            paragraphs = soup.find_all('p')
            important_paragraphs = " | ".join(
                [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
            )[:1000]

            keywords_tag = soup.find("meta", attrs={"name": "keywords"})
            keywords = keywords_tag["content"] if keywords_tag else ""

            stmt = links_table.insert().values(url=url, title=title, h1_tags=h1_tags, important_paragraphs=important_paragraphs, keywords=keywords)
            session.execute(stmt)
            session.commit()
            print(f"Added: {url} with title, content, and keywords.")
        except IntegrityError:
            session.rollback()
            print(f"The URL {url} is already present in the database.")
        except Exception as e:
            session.rollback()
            print(f"Error adding {url}: {e}")

def worker(url_queue, visited_urls):
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
    url_queue = queue.Queue()
    visited_urls = set()

    for url in seed_urls:
        url_queue.put(url)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(url_queue, visited_urls))
        thread.start()
        threads.append(thread)

    url_queue.join()

    for thread in threads:
        thread.join()