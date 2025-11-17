from __future__ import annotations

from typing import List, Sequence

from loguru import logger
from openai import OpenAI

from app.core.config import get_settings


class LLMClient:
    """Thin wrapper around the OpenAI Responses API with sensible defaults."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.llm_api_key,
            base_url=self.settings.llm_base_url,
        )
        self.model = self.settings.llm_model

    def _complete(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        try:
            response = self.client.responses.create(
                model=self.model,
                max_output_tokens=max_tokens,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            text_chunks: list[str] = []
            for output in response.output:
                for content in getattr(output, "content", []):
                    if getattr(content, "type", None) == "text":
                        text_chunks.append(content.text)
            return " ".join(text_chunks).strip()
        except Exception as exc:  # pragma: no cover - network failure
            logger.exception("LLM request failed: {}", exc)
            raise

    def summarize(self, text: str) -> str:
        prompt = (
            "Summarize the following document in 4-6 concise sentences. "
            "Focus on the core themes and key facts."
        )
        return self._complete(prompt, text[:6000], max_tokens=350)

    def key_points(self, text: str, max_points: int = 5) -> list[str]:
        prompt = (
            f"List the {max_points} most important bullet points from the document. "
            "Return them as a plain list separated by newline characters."
        )
        output = self._complete(prompt, text[:6000], max_tokens=300)
        points = [line.strip("-• ").strip() for line in output.splitlines() if line.strip()]
        return [p for p in points if p][:max_points]

    def classify_sentiment(self, text: str) -> str:
        prompt = (
            "Classify the overall sentiment of this document as Positive, Neutral, or Negative. "
            "Respond with a single word."
        )
        sentiment = self._complete(prompt, text[:4000], max_tokens=5)
        return sentiment.strip().lower()

    def classify_category(self, text: str) -> str:
        prompt = (
            "Classify this document into a high-level category "
            "(e.g., Finance, Legal, Marketing, Technical, HR, Medical, Other). "
            "Respond with just the category."
        )
        category = self._complete(prompt, text[:4000], max_tokens=10)
        return category.strip()

    def answer_question(self, question: str, context: str) -> str:
        prompt = (
            "You are an assistant answering questions based strictly on the provided context. "
            "If the answer is not in the context, respond with \"I don't know\".\n\n"
            f"Context:\n{context}"
        )
        return self._complete(prompt, question, max_tokens=400)


llm_client = LLMClient()

__all__ = ["LLMClient", "llm_client"]

