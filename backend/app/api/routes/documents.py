from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentRead
from app.workers.tasks import process_document

router = APIRouter(prefix="/documents", tags=["documents"])


class QuestionRequest(BaseModel):
    question: str


class CompareRequest(BaseModel):
    document_ids: list[int]


@router.post("/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: Annotated[UploadFile, File(..., description="Binary document")],
    db: AsyncSession = Depends(get_db),
) -> DocumentRead:
    file_bytes = await file.read()
    storage_dir = Path("storage/uploads")
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_path = storage_dir / file.filename
    storage_path.write_bytes(file_bytes)

    document = Document(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(file_bytes),
        storage_path=str(storage_path),
        document_metadata={"original_name": file.filename},
        status=DocumentStatus.PROCESSING,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    process_document.delay(document.id, str(storage_path))
    return DocumentRead.from_orm(document)


@router.get("/", response_model=list[DocumentRead])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[DocumentRead]:
    result = await db.execute(select(Document).offset(skip).limit(limit).order_by(Document.created_at.desc()))
    documents = result.scalars().all()
    return [DocumentRead.from_orm(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(document_id: int, db: AsyncSession = Depends(get_db)) -> DocumentRead:
    document = await db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return DocumentRead.from_orm(document)


@router.post("/{document_id}/ask")
async def ask_question(
    document_id: int,
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    document = await db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    if document.status != DocumentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document processing is not complete yet"
        )
    
    # TODO: Implement RAG-based Q&A using embeddings
    # For now, return a placeholder answer
    answer = f"This is a placeholder answer for the question: '{request.question}'. The document '{document.filename}' has been processed, but Q&A functionality needs to be implemented with RAG."
    
    return {"answer": answer, "document_id": document_id}


@router.post("/compare")
async def compare_documents(
    request: CompareRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    if len(request.document_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 2 documents are required for comparison"
        )
    
    documents = []
    for doc_id in request.document_ids:
        doc = await db.get(Document, doc_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {doc_id} not found"
            )
        if doc.status != DocumentStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document {doc_id} processing is not complete yet"
            )
        documents.append(doc)
    
    # TODO: Implement document comparison logic
    # For now, return a placeholder comparison
    comparison = {
        "documents": [{"id": doc.id, "filename": doc.filename} for doc in documents],
        "similarities": "Placeholder: Documents are being compared...",
        "differences": "Placeholder: Differences will be highlighted here...",
    }
    
    return comparison


