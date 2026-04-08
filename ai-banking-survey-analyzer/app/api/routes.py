from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.opensearch_service import OpenSearchService
from app.services.llm_service import LLMService

router = APIRouter()

embedding_service = EmbeddingService()
opensearch_service = OpenSearchService()
llm_service = LLMService()


class SurveyRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze(request: SurveyRequest):
    user_question = request.text

    query_embedding = embedding_service.get_embedding(user_question)

    search_results = opensearch_service.search_similar(query_embedding, k=3)

    context_chunks = []
    for hit in search_results["hits"]["hits"]:
        context_chunks.append(hit["_source"]["text"])

    final_response = llm_service.analyze_with_context(
        user_question=user_question,
        context_chunks=context_chunks
    )

    return {
        "question": user_question,
        "retrieved_context": context_chunks,
        "rag_response": final_response
    }