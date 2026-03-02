import json
import uuid
from typing import List, Dict
import tiktoken
from tqdm import tqdm

ENCODER = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(ENCODER.encode(text))


def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 120,
) -> List[str]:
    tokens = ENCODER.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = ENCODER.decode(chunk_tokens)
        chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


def create_chunks(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    all_chunks = []

    for doc in tqdm(docs, desc="Chunking docs"):
        text = doc["content"]

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "doc_id": doc["doc_id"],
                    "url": doc["url"],
                    "title": doc.get("title", ""),
                    "text": chunk,
                    "chunk_index": i,
                }
            )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"✅ Created {len(all_chunks)} chunks")


if __name__ == "__main__":
    create_chunks(
    "data/clean_docs.json",
    "data/chunks.json"
)