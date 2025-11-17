from __future__ import annotations

from functools import lru_cache
from typing import Iterable

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache
def _load_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


class EmbeddingService:
    def __init__(self) -> None:
        settings = get_settings()
        self.model = _load_model(settings.embedding_model)

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        vectors = self.model.encode(
            list(texts),
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return [vector.tolist() for vector in vectors]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


embedding_service = EmbeddingService()

__all__ = ["EmbeddingService", "embedding_service"]

