import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

from ingestion.embedder import embed_texts

COLLECTION_NAME = "evidentrag"


def init_qdrant():
    client = QdrantClient(url="http://localhost:6333")

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

    return client


def ingest_chunks(chunks_path: str):
    client = init_qdrant()

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    points = []

    for chunk, vector in tqdm(
        zip(chunks, embeddings),
        total=len(chunks),
        desc="Uploading to Qdrant",
    ):
        payload = {
            "doc_id": chunk["doc_id"],
            "url": chunk["url"],
            "title": chunk["title"],
            "text": chunk["text"],
            "chunk_index": chunk["chunk_index"],
        }

        points.append(
            PointStruct(
                id=chunk["chunk_id"],
                vector=vector.tolist(),
                payload=payload,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print("✅ Ingestion complete")