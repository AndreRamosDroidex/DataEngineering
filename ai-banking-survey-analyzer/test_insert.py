from app.services.embedding_service import EmbeddingService
from app.services.opensearch_service import OpenSearchService

embedding_service = EmbeddingService()
opensearch_service = OpenSearchService()

text = "The bank charges too many fees"

embedding = embedding_service.get_embedding(text)

response = opensearch_service.index_document(text, embedding)

print(response)