from retrieval.langchain_retriever import LangChainRetriever

retriever = LangChainRetriever()

results = retriever.retrieve(
    "How to install kubeadm?",
    k=3
)

for r in results:
    print(r.metadata["url"])
    print(r.page_content[:300])
    print("-"*50)