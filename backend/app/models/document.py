import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DocumentStatus(str, enum.Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(128))
    size_bytes: Mapped[int]
    storage_path: Mapped[str] = mapped_column(String(512))
    document_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), default=DocumentStatus.RECEIVED)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    summary: Mapped[Optional[str]]
    key_points: Mapped[Optional[list[str]]] = mapped_column(JSON)
    sentiment: Mapped[Optional[str]]
    category: Mapped[Optional[str]]
    insights: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)