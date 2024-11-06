import time
from sentence_transformers import SentenceTransformer
from config import EMBEDDINGS_MODEL

start_time = time.time()  # Start timer


MODEL = SentenceTransformer(EMBEDDINGS_MODEL)



end_time = time.time()  # End timer
loading_time = end_time - start_time
print(f"\nModel Loaded in {loading_time:.2f} seconds")