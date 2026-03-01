import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import trafilatura
import time
import json
from tqdm import tqdm


class DocsCrawler:
    def __init__(self, base_url, allowed_domain, max_pages=500):
        self.base_url = base_url
        self.allowed_domain = allowed_domain
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = [base_url]
        self.documents = []

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return (
            parsed.netloc.endswith(self.allowed_domain)
            and url not in self.visited
            and not any(
                url.lower().endswith(ext)
                for ext in [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".svg",
                    ".css",
                    ".js",
                    ".pdf",
                    ".zip",
                ]
            )
        )

    def extract_text(self, html):
        return trafilatura.extract(html)

    def crawl(self):
        pbar = tqdm(total=self.max_pages)

        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)

            if url in self.visited:
                continue

            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code != 200:
                    continue

                html = resp.text
                text = self.extract_text(html)

                if text and len(text) > 200:
                    self.documents.append(
                        {
                            "url": url,
                            "source": self.allowed_domain,
                            "content": text,
                        }
                    )

                self.visited.add(url)
                pbar.update(1)

                # discover new links
                soup = BeautifulSoup(html, "html.parser")
                for link in soup.find_all("a", href=True):
                    new_url = urljoin(url, link["href"])
                    if self.is_valid_url(new_url):
                        self.to_visit.append(new_url)

                time.sleep(0.5)  # politeness

            except Exception:
                continue

        pbar.close()
        return self.documents


def run_crawl():
    targets = [
        ("https://fastapi.tiangolo.com/", "tiangolo.com"),
        ("https://kubernetes.io/docs/home/", "kubernetes.io"),
        ("https://python.langchain.com/docs/", "langchain.com"),
    ]

    all_docs = []

    for base_url, domain in targets:
        print(f"\n🚀 Crawling {domain}")
        crawler = DocsCrawler(base_url, domain, max_pages=300)
        docs = crawler.crawl()
        all_docs.extend(docs)

    # save
    with open("data/raw_docs.json", "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Collected {len(all_docs)} documents")


if __name__ == "__main__":
    run_crawl()