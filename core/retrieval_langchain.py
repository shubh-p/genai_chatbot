from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import json
from sentence_transformers import SentenceTransformer
from core.logging_config import logger

TAG='retrieval_langchain.py'
def load_data_handbook():
    with open('data/gitlab_handbook.json', 'r') as f:
        handbook_data = json.load(f)
    return handbook_data

# def load_data_direction():
#     with open('data/gitlab_direction.json', 'r') as f:
#         direction_data = json.load(f)
#     return direction_data

def load_data_direction():
    with open('data/webpage_data.json', 'r') as f:
        direction_data = json.load(f)
    return direction_data

# def load_data_direction():
#     with open('data/webpage_data_hiearchial.json', 'r') as f:
#         direction_data = json.load(f)
#     return direction_data

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# def flatten_hierarchical_data(data, parent_header=""):
#     """
#     Recursively flatten hierarchical data into a list of documents with parent context.
#     """
#     documents = []
#     for item in data:
#         # Combine parent header with the current header for context
#         full_header = f"{parent_header} > {item['header']}".strip(" > ")
        
#         # Add the main content as a document
#         if item["content"]:
#             documents.append(Document(page_content=f"{full_header} - {item['content']}"))
        
#         # Add bullet points as individual documents (optional, depending on your use case)
#         if "bullet_points" in item:
#             for bullet in item["bullet_points"]:
#                 documents.append(Document(page_content=f"{full_header} - {bullet}"))
        
#         # Recurse into subsections
#         if "subsections" in item and item["subsections"]:
#             documents.extend(flatten_hierarchical_data(item["subsections"], parent_header=full_header))
#         print('******************')
#         print(page_content)
    
#     return documents

# def build_vector_store_from_hiearchial_data(data, name):
#     """
#     Build a vector store from hierarchical data.
#     """
#     documents = flatten_hierarchical_data(data)
#     logger.info(f"{TAG}: Total documents indexed in {name}: {len(documents)}")
#     vector_store = FAISS.from_documents(documents, hf_embeddings)
#     return vector_store


def build_vector_store(data, name):
    documents = [Document(page_content=f"{item['header']} - {item['content']}") for item in data]
    logger.info(f"{TAG}: Total documents indexed in {name}: {len(documents)}")
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
    logger.info('------------------------------')
    logger.info(f"{TAG}:Retrieved Documents for Query from handbook '{query}':")
    for i, doc in enumerate(results1, start=1):
        logger.info(f"{TAG}:{i}. {doc.page_content}")
    logger.info('------------------------------')
    logger.info(f"{TAG}:Retrieved Documents for Query from direction '{query}':")
    for i, doc in enumerate(results2, start=1):
        logger.info(f"{TAG}:{i}. {doc.page_content}")
    logger.info('------------------------------')


    # Combine the content of the retrieved documents
    combined_content = " ".join([doc.page_content for doc in results1 + results2])
    return combined_content
