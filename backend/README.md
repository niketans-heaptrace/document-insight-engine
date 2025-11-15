# Backend Service

FastAPI application orchestrating ingestion, processing, and retrieval for uploaded documents. It exposes synchronous APIs for upload/status queries while delegating heavy lifting to Celery workers backed by Redis and a vector store (ChromaDB by default).

## Key Technologies

- FastAPI for HTTP APIs
- Celery + Redis for background processing
- OCR (Tesseract), PDF/Word parsing libraries
- Embeddings + ChromaDB for RAG

## Run Locally

```bash
# create virtual env / install dependencies using uv or pip
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# start FastAPI dev server
uvicorn app.main:app --reload

# run Celery worker (in another terminal)
celery -A app.workers.celery_app.celery_app worker --loglevel=INFO
```

Environment variables live in `.env` (copy from `.env.example`).


