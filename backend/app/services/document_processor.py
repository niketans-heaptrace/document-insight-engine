from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document as DocxDocument
from loguru import logger
from pdfminer.high_level import extract_text as extract_pdf_text
from PIL import Image
import pytesseract

from app.services.embeddings import embedding_service
from app.services.llm_client import llm_client
from app.services.vector_store import vector_store


class DocumentProcessor:
    def extract_text(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".pdf":
                return extract_pdf_text(file_path)
            if suffix in {".docx", ".doc"}:
                doc = DocxDocument(file_path)
                return "\n".join(paragraph.text for paragraph in doc.paragraphs)
            if suffix in {".png", ".jpg", ".jpeg"}:
                image = Image.open(file_path)
                return pytesseract.image_to_string(image)
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            logger.exception("Failed to extract text from {}: {}", file_path, exc)
            return file_path.read_text(encoding="utf-8", errors="ignore")

    def extract_tables(self, text: str) -> list[dict[str, Any]]:
        tables: list[list[list[str]]] = []
        current: list[list[str]] = []

        for line in text.splitlines():
            if "|" in line:
                row = [cell.strip() for cell in line.split("|") if cell.strip()]
                if row:
                    current.append(row)
            elif current:
                if len(current) >= 2:
                    tables.append(current)
                current = []

        if current and len(current) >= 2:
            tables.append(current)

        structured = []
        for raw_table in tables:
            headers = raw_table[0]
            rows = raw_table[1:]
            structured.append({"headers": headers, "rows": rows})
        return structured

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        chunks: list[str] = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks or [text]

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        return embedding_service.embed(chunks)

    def summarize(self, text: str) -> str:
        return llm_client.summarize(text)

    def extract_key_points(self, text: str) -> list[str]:
        return llm_client.key_points(text)

    def detect_sentiment(self, text: str) -> str:
        return llm_client.classify_sentiment(text)

    def classify_document(self, text: str) -> str:
        return llm_client.classify_category(text)

    def process(self, document_id: int, file_path: Path) -> dict[str, Any]:
        text = self.extract_text(file_path)
        chunks = self.chunk_text(text)
        embeddings = self.embed_chunks(chunks)
        vector_store.upsert_document_chunks(document_id, chunks, embeddings)

        summary = self.summarize(text)
        key_points = self.extract_key_points(text)
        sentiment = self.detect_sentiment(text)
        category = self.classify_document(text)
        tables = self.extract_tables(text)

        return {
            "text": text,
            "chunks": chunks,
            "summary": summary,
            "key_points": key_points,
            "sentiment": sentiment,
            "category": category,
            "tables": tables,
        }


