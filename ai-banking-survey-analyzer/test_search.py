from app.services.embedding_service import EmbeddingService
from app.services.opensearch_service import OpenSearchService

embedding_service = EmbeddingService()
opensearch_service = OpenSearchService()

query_text = "bank fees are expensive"

embedding = embedding_service.get_embedding(query_text)

results = opensearch_service.search_similar(embedding)

for hit in results["hits"]["hits"]:
    print(hit["_source"]["text"])