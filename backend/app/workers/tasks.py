from pathlib import Path

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.models.document import Document, DocumentStatus
from app.services.document_processor import DocumentProcessor
from app.workers.celery_app import celery_app

settings = get_settings()
processor = DocumentProcessor()

# Create async engine for database operations in Celery task
engine = create_async_engine(settings.database_url, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@celery_app.task(name="app.workers.tasks.process_document")
def process_document(document_id: int, file_path: str) -> dict:
    import asyncio
    
    async def _process():
        async with async_session() as session:
            try:
                # Get document
                result = await session.execute(select(Document).where(Document.id == document_id))
                document = result.scalar_one_or_none()
                
                if not document:
                    logger.error("Document {} not found", document_id)
                    return {"error": "Document not found"}
                
                logger.info("Starting processing for document {}", document_id)
                document.status = DocumentStatus.PROCESSING
                await session.commit()
                
                # Process document end-to-end
                path = Path(file_path)
                result = processor.process(document_id, path)
                summary = result["summary"]
                key_points = result["key_points"]
                sentiment = result["sentiment"]
                category = result["category"]
                tables = result["tables"]
                keywords = key_points[:8]
                
                # Build insights object
                insights = {
                    "summary": summary,
                    "key_points": key_points,
                    "sentiment": sentiment,
                    "category": category,
                    "keywords": keywords,
                    "tables": tables,
                }
                
                # Update document
                document.summary = summary
                document.key_points = key_points
                document.sentiment = sentiment
                document.category = category
                document.insights = insights
                document.status = DocumentStatus.COMPLETED
                
                await session.commit()
                await session.refresh(document)
                
                logger.info("Finished processing document {}", document_id)
                return {
                    "document_id": document_id,
                    "status": "completed",
                    "summary": summary,
                    "key_points": key_points,
                    "sentiment": sentiment,
                    "category": category,
                }
            except Exception as e:
                logger.error("Error processing document {}: {}", document_id, e)
                # Update document status to failed
                try:
                    result = await session.execute(select(Document).where(Document.id == document_id))
                    document = result.scalar_one_or_none()
                    if document:
                        document.status = DocumentStatus.FAILED
                        await session.commit()
                except Exception as commit_error:
                    logger.error("Error updating document status: {}", commit_error)
                raise
    
    # Run async function
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If loop is already running, create a new task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, _process())
            return future.result()
    else:
        return asyncio.run(_process())


