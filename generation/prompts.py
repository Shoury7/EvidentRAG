from langchain.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate(
    input_variables=["context","question"],
    template="""
    You are an expert Kubernetes assistant.
    Answer the user's question ONLY using the provided context.

    If the answer cannot be found in the context, say:
    "I don't have enough information"

    Context :
    {context}

    Question :
    {question}

    Answer:
"""
)
 