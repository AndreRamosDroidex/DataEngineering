from opensearchpy import OpenSearch


class OpenSearchService:

    def __init__(self):
        self.client = OpenSearch(
            hosts=[{
                "host": "search-banking-survey-rag-rugyqe2cbavd5zwdgziyttjosu.us-east-2.es.amazonaws.com",
                "port": 443
            }],
            http_auth=("admin", "3android3.Admin$"),
            use_ssl=True,
            verify_certs=False
        )

    def index_document(self, text, embedding):
        doc = {
            "text": text,
            "embedding": embedding
        }

        return self.client.index(
            index="survey-index",
            body=doc
        )

    def search_similar(self, embedding, k=3):
        query = {
            "size": k,
            "_source": ["text"],
            "query": {
                "knn": {
                    "embedding": {
                        "vector": embedding,
                        "k": k
                    }
                }
            }
        }

        response = self.client.search(
            index="survey-index",
            body=query
        )

        return response