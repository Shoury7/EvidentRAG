from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

COLLECTION_NAME = "evidentrag"

class LangChainRetriever:
    def __init__(self):
        
        embeddings = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.db = QdrantVectorStore(
            client=QdrantClient(url="http://localhost:6333"),
            collection_name=COLLECTION_NAME,
            embedding=embeddings
        )
    
    def retrieve(self,query,k=5):

        docs = self.db.similarity_search(query,k=k)
        return docs
    