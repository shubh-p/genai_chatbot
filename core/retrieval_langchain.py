from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import json
from sentence_transformers import SentenceTransformer
from core.logging_config import logger

def load_data():
    with open('data/gitlab_handbook.json', 'r') as f:
        handbook_data = json.load(f)
    with open('data/gitlab_direction.json', 'r') as f:
        direction_data = json.load(f)
    #TODO:check why both of them dont work together and fix( already queried in gpt)
    return handbook_data + direction_data 

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_vector_store():
    data = load_data()
    # Combine header and content to form smaller, meaningful documents
    documents = [Document(page_content=f"{item['header']} - {item['content']}") for item in data]
    logger.info(f"Total documents indexed are : {len(documents)}")
    vector_store = FAISS.from_documents(documents, hf_embeddings)
    return vector_store

vector_store = build_vector_store()

def retrieve_context(query):
    retriever = vector_store.as_retriever()
    results = retriever.get_relevant_documents(query)
    
    # Log the retrieved documents for debugging
    logger.info(f"Retrieved Documents for Query '{query}': {[doc.page_content for doc in results[:3]]}")
    
    # Return joined content of top matches
    return " ".join([doc.page_content for doc in results[:3]])
