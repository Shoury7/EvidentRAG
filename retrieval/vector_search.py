from qdrant_client import QdrantClient
from ingestion.embedder import embed_texts

COLLECTION_NAME = "evidentrag"


class VectorRetriever:
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")

    def search(self, query: str, top_k: int = 5):
        query_vec = embed_texts([query])[0]

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vec.tolist(),
            limit=top_k,
        ).points

        return [
            {
                "score": r.score,
                "text": r.payload["text"],
                "url": r.payload["url"],
                "title": r.payload["title"],
            }
            for r in results
        ]