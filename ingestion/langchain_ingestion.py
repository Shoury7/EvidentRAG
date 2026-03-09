import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

DATA_PATH = "data/clean_docs.json"
COLLECTION_NAME = "evidentrag"


def load_documents():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    documents = []

    for d in docs:
        documents.append(
            Document(
                page_content=d["content"],
                metadata={
                    "doc_id": d["doc_id"],
                    "url": d["url"],
                    "title": d["title"],
                    "source": d["source"],
                },
            )
        )

    return documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
    )

    chunks = splitter.split_documents(documents)

    return chunks


def ingest_to_qdrant(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    client = QdrantClient(url="http://localhost:6333")

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="http://localhost:6333",
        collection_name=COLLECTION_NAME,
    )


def run_pipeline():

    docs = load_documents()

    print(f"Loaded {len(docs)} docs")

    chunks = chunk_documents(docs)

    print(f"Created {len(chunks)} chunks")

    ingest_to_qdrant(chunks)

    print("Ingestion complete")


if __name__ == "__main__":
    run_pipeline()