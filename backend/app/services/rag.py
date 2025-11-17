from __future__ import annotations

from app.services.embeddings import embedding_service
from app.services.llm_client import llm_client
from app.services.vector_store import vector_store


class RagService:
    def answer(self, document_id: int, question: str, top_k: int = 4) -> dict:
        question_embedding = embedding_service.embed_one(question)
        results = vector_store.query_document(document_id, question_embedding, top_k=top_k)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        if not documents:
            return {
                "answer": "I don't know",
                "sources": [],
            }

        context = "\n\n".join(documents)
        answer = llm_client.answer_question(question, context)

        sources = [
            {
                "chunk": doc,
                "metadata": metadata,
            }
            for doc, metadata in zip(documents, metadatas)
        ]

        return {"answer": answer, "sources": sources}


rag_service = RagService()

__all__ = ["RagService", "rag_service"]


