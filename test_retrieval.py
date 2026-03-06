from retrieval.vector_search import VectorRetriever

retriever = VectorRetriever()

results = retriever.search(
    "How to install kubeadm and kubelet on Ubuntu using apt?",
    top_k=3,
)

for r in results:
    print(r["score"], r["title"])