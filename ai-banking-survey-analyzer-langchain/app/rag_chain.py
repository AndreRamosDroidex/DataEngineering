from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain.chains import RetrievalQA

from app.config import (
    OPENSEARCH_URL,
    OPENSEARCH_USER,
    OPENSEARCH_PASSWORD,
    INDEX_NAME
)

# 🔹 embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 🔹 vector store (OpenSearch)
vectorstore = OpenSearchVectorSearch(
    opensearch_url=OPENSEARCH_URL,
    index_name=INDEX_NAME,
    embedding_function=embeddings,
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
)

# 🔹 retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# 🔹 LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# 🔹 RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

def ask_question(question: str):
    response = rag_chain.invoke({
        "query": question
    })
    return response