from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, func, delete, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import requests

from config import DATABASE_URL

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

embeddings_table = Table(
    'Embeddings', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('link_id', Integer, unique=True),
    Column('embedded_title', Text),
    Column('embedded_keywords', Text),
    Column('embedded_paragraphs', Text),
    Column('embedded_h1', Text),
    Column('domains', Text),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def clean_invalid_links():
    with Session() as session:
        links = session.query(links_table).all()
        total_links = len(links)
        deleted_count = 0

        for link in links:
            try:
                response = requests.get(link.url, timeout=5)
                response.raise_for_status()
                print(f"The link {link.url} is accessible.")
            except requests.RequestException:
                print(f"The link {link.url} is inaccessible, deleting.")
                stmt = delete(links_table).where(links_table.c.id == link.id)
                session.execute(stmt)
                session.commit()
                deleted_count += 1

        print(f"Cleanup finished. Total links deleted: {deleted_count}/{total_links}")


def add_links_to_db(links):
    with Session() as session:
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
                print(f"Duplicate link ignored: {link}")
        session.commit()
        return added_count


def get_random_link_from_db():
    with Session() as session:
        result = session.query(links_table).order_by(func.random()).first()
        if result:
            return result.url
        return None