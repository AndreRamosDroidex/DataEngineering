from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch

from app.config import (
    OPENSEARCH_URL,
    OPENSEARCH_USER,
    OPENSEARCH_PASSWORD,
    INDEX_NAME
)

texts = [
    "The bank fees are too high",
    "Customer service is slow but friendly",
    "The app is easy to use",
]

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = OpenSearchVectorSearch(
    opensearch_url=OPENSEARCH_URL,
    index_name=INDEX_NAME,
    embedding_function=embeddings,
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
)

vectorstore.add_texts(texts)

print("Data inserted with LangChain")