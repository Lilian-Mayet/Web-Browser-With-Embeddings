import json
import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity
from database import links_table, Session, embeddings_table
from embeddings import generate_domain_embeddings
from config import EMBEDDINGS_MODEL,DOMAIN_TRESHOLD
from sentence_transformers import SentenceTransformer



model = SentenceTransformer(EMBEDDINGS_MODEL)

def search_similar_links(user_query, top_n=10, use_query_domains=True):
    start_time = time.time()  # Start timer

    # Embedding du texte de la requête
    query_embedding = model.encode(user_query)
    detected_domains = get_query_domains(user_query)
    print(f"Domains detected in query: {detected_domains}\n")

    with Session() as session:
        query = session.query(
            links_table.c.id,
            links_table.c.url,
            links_table.c.title,
            embeddings_table.c.embedded_title,
            embeddings_table.c.embedded_keywords,
            embeddings_table.c.embedded_paragraphs,
            embeddings_table.c.embedded_h1,
            embeddings_table.c.domains
        ).join(
            embeddings_table,
            links_table.c.id == embeddings_table.c.link_id
        )

        results = query.all()
        similarities = []

        for result in results:
            if use_query_domains and detected_domains:
                result_domains = json.loads(result.domains) if result.domains else []
                if not any(domain in result_domains for domain in detected_domains):
                    continue

            embeddings = [
                json.loads(result.embedded_title) if result.embedded_title else None,
                json.loads(result.embedded_keywords) if result.embedded_keywords else None,
                json.loads(result.embedded_paragraphs) if result.embedded_paragraphs else None,
                json.loads(result.embedded_h1) if result.embedded_h1 else None,
            ]

            similarities_for_link = []
            for embedding in embeddings:
                if embedding is not None:
                    similarity = cosine_similarity(
                        [query_embedding], [np.array(embedding)]
                    )[0][0]
                    similarities_for_link.append(similarity)

            if similarities_for_link:
                avg_similarity = np.mean(similarities_for_link)
                similarities.append((result.id, avg_similarity, result))

        top_links = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]

        top_link_ids = [link[0] for link in top_links]
        closest_links = session.query(links_table).filter(links_table.c.id.in_(top_link_ids)).all()

        # Formatting results
        print("\n--- Similar Links Search Results ---\n")
        for _, similarity, result in top_links:
            result_domains = json.loads(result.domains) if result.domains else []
            matched_domains = [d for d in result_domains if d in detected_domains] if detected_domains else []

            print(f"ID: {result.id}")
            print(f"URL: {result.url}")
            print(f"Title: {result.title}")
            print(f"Similarity Score: {similarity:.4f}")
            print(f"Domains: {result_domains}")
            print(f"Matched Query Domains: {matched_domains}\n")
            print("-" * 40)

        end_time = time.time()  # End timer
        response_time = end_time - start_time
        print(f"\nQuery completed in {response_time:.2f} seconds")

        return {
            "results": [
                {
                    "id": result.id,
                    "url": result.url,
                    "title": result.title,
                    "similarity_score": float(similarity),
                    "domains": result_domains,
                    "matched_query_domains": matched_domains
                }
                for _, similarity, result in top_links
            ],
            "detected_domains": detected_domains,
            "total_results": len(top_links),
            "query": user_query,
            "response_time": response_time
        }

def get_query_domains(query):
    query_embedding = model.encode(query)
    domain_embeddings = generate_domain_embeddings()

    matching_domains = []
    for domain, domain_embedding in domain_embeddings.items():
        similarity = cosine_similarity([query_embedding], [domain_embedding])[0][0]
        if similarity > DOMAIN_TRESHOLD:
            matching_domains.append((domain, similarity))

    matching_domains.sort(key=lambda x: x[1], reverse=True)
    return [domain for domain, _ in matching_domains]

search_similar_links("I want to be an entrepreneur and open a restaurant",5,False)