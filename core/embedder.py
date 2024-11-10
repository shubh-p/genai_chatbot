from sentence_transformers import SentenceTransformer
import json

# Load a pre-trained embedding model from Hugging Face
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to get embeddings for text sections
def get_embeddings(texts):
    return embedding_model.encode(texts, convert_to_tensor=True)
