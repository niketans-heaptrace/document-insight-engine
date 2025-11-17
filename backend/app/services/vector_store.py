from __future__ import annotations

from typing import Sequence

import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection

from app.core.config import get_settings

class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.client: ClientAPI = chromadb.PersistentClient(path=str(settings.vector_db_path))
        self.collection: Collection = self.client.get_or_create_collection(settings.chroma_collection)

    def upsert_document_chunks(
        self,
        document_id: int,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        ids = [f"{document_id}:{idx}" for idx in range(len(chunks))]
        metadatas = [{"document_id": str(document_id), "chunk_index": idx} for idx in range(len(chunks))]
        self.collection.upsert(
            ids=ids,
            embeddings=list(embeddings),
            documents=list(chunks),
            metadatas=metadatas,
        )

    def query_document(
        self,
        document_id: int,
        query_embedding: Sequence[float],
        top_k: int = 4,
    ) -> dict:
        return self.collection.query(
            query_embeddings=[list(query_embedding)],
            n_results=top_k,
            where={"document_id": str(document_id)},
        )


vector_store = VectorStore()

__all__ = ["VectorStore", "vector_store"]


