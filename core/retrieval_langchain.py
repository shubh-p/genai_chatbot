from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import json
from sentence_transformers import SentenceTransformer
from core.logging_config import logger

def load_data_handbook():
    with open('data/gitlab_handbook.json', 'r') as f:
        handbook_data = json.load(f)
    return handbook_data

def load_data_direction():
    with open('data/gitlab_direction.json', 'r') as f:
        direction_data = json.load(f)
    return direction_data

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_vector_store(data, name):
    documents = [Document(page_content=f"{item['header']} - {item['content']}") for item in data]
    logger.info(f"Total documents indexed in {name}: {len(documents)}")
    vector_store = FAISS.from_documents(documents, hf_embeddings)
    return vector_store

# Build vector stores separately
vector_store_handbook = build_vector_store(load_data_handbook(), "handbook")
vector_store_direction = build_vector_store(load_data_direction(), "direction")

def retrieve_context(query):
    # Retrieve top 3 relevant documents from each vector store
    retriever1 = vector_store_handbook.as_retriever()
    results1 = retriever1.get_relevant_documents(query)[:3]
    retriever2 = vector_store_direction.as_retriever()
    results2 = retriever2.get_relevant_documents(query)[:3]
    
    # Log retrieved documents for debugging
    logger.info(f"Retrieved Documents for Query from handbook '{query}': {[doc.page_content for doc in results1]}")
    logger.info(f"Retrieved Documents for Query from direction '{query}': {[doc.page_content for doc in results2]}")

    # Combine the content of the retrieved documents
    combined_content = " ".join([doc.page_content for doc in results1 + results2])
    return combined_content
