from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from app.models.document import DocumentStatus


class DocumentCreate(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    storage_path: str
    document_metadata: dict | None = None


class DocumentUpdate(BaseModel):
    status: DocumentStatus | None = None
    summary: Optional[str] = None
    key_points: Optional[list[str]] = None
    sentiment: Optional[str] = None
    category: Optional[str] = None


class DocumentRead(BaseModel):
    id: int
    filename: str
    content_type: str
    size_bytes: int
    storage_path: str
    document_metadata: dict | None = None
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    summary: Optional[str]
    key_points: Optional[list[str]]
    sentiment: Optional[str]
    category: Optional[str]
    insights: Optional[dict] = None

    @property
    def uploaded_at(self):
        return self.created_at

    class Config:
        from_attributes = True
