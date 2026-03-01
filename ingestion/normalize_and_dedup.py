import json
import hashlib
from urllib.parse import urldefrag
from datetime import datetime
from tqdm import tqdm


# ============================================================
# Helpers
# ============================================================

def normalize_url(url: str) -> str:
    """
    Remove anchor fragments and trailing slash normalization.
    Example:
    /overview#create-agent → /overview
    """
    clean_url, _ = urldefrag(url)
    return clean_url.rstrip("/")


def content_hash(text: str) -> str:
    """Stable hash for deduplication"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def make_doc_id(url: str) -> str:
    """Deterministic short doc id from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def extract_title(content: str) -> str:
    """
    Simple but effective title extraction.
    Uses first non-empty line.
    """
    for line in content.split("\n"):
        line = line.strip()
        if line:
            return line[:200]
    return "untitled"


# ============================================================
# Load raw docs
# ============================================================

def load_raw_docs(path="data/raw_docs.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Main cleaning pipeline
# ============================================================

def clean_documents(raw_docs):
    seen_hashes = set()
    cleaned_docs = []

    crawl_time = datetime.utcnow().isoformat()

    for doc in tqdm(raw_docs, desc="Cleaning docs"):

        content = doc.get("content", "").strip()
        if not content:
            continue

        # -------------------------
        # 1. URL normalization
        # -------------------------
        normalized_url = normalize_url(doc["url"])

        # -------------------------
        # 2. Content deduplication
        # -------------------------
        h = content_hash(content)

        if h in seen_hashes:
            continue  # duplicate content — skip

        seen_hashes.add(h)

        # -------------------------
        # 3. Metadata enrichment
        # -------------------------
        enriched_doc = {
            "doc_id": make_doc_id(normalized_url),
            "url": normalized_url,
            "source": doc.get("source", "unknown"),
            "title": extract_title(content),
            "content": content,
            "crawl_timestamp": crawl_time,
        }

        cleaned_docs.append(enriched_doc)

    print(f"\n✅ Raw docs: {len(raw_docs)}")
    print(f"✅ After dedup: {len(cleaned_docs)}")

    return cleaned_docs


# ============================================================
# Save output
# ============================================================

def save_clean_docs(clean_docs, path="data/clean_docs.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean_docs, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved → {path}")


# ============================================================
# Entry point
# ============================================================

def main():
    print("🚀 Loading raw docs...")
    raw_docs = load_raw_docs()

    print("🧹 Normalizing + deduplicating...")
    clean_docs = clean_documents(raw_docs)

    save_clean_docs(clean_docs)

    print("\n🎉 Cleaning pipeline complete!")


if __name__ == "__main__":
    main()