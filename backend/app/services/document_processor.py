from pathlib import Path

from loguru import logger

from app.core.config import get_settings


class DocumentProcessor:
    def __init__(self) -> None:
        self.settings = get_settings()

    def run_ocr_if_needed(self, file_path: Path) -> str:
        logger.info("Pretending to OCR file {}", file_path)
        return file_path.read_text() if file_path.suffix == ".txt" else "Extracted text placeholder"

    def chunk_text(self, text: str) -> list[str]:
        return [text[i : i + 1000] for i in range(0, len(text), 1000)] or [text]

    def create_embeddings(self, chunks: list[str]) -> list[list[float]]:
        logger.info("Generating embeddings with model {}", self.settings.embedding_model)
        return [[float(idx)] for idx, _chunk in enumerate(chunks)]

    def summarize(self, text: str) -> str:
        return text[:500] + "..."

    def extract_key_points(self, text: str) -> list[str]:
        return [text[:120]]

    def detect_sentiment(self, text: str) -> str:
        return "neutral"

    def classify_document(self, text: str) -> str:
        return "general"


