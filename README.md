# Generative Document Intelligence Platform

Scaffolding for a multi-stage system that ingests arbitrary documents, processes them asynchronously, and surfaces GenAI-powered insights and conversational Q&A via a web UI.

## Architecture

- `backend/`: FastAPI service exposing upload + retrieval endpoints. Celery + Redis workers orchestrate OCR, text extraction, embeddings, summaries, and other signals stored in SQL + vector DB.
- `frontend/`: React (Vite) single-page app for uploading files, tracking status, and chatting with processed documents.
- `docs/`: design notes, diagrams, and playbooks (start with `docs/architecture.md`).

## Getting Started

1. **Backend**
   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e .
   uvicorn app.main:app --reload
   ```
   In another terminal:
   ```bash
   cd backend
   celery -A app.workers.celery_app worker --loglevel=INFO
   ```
   Or use the convenience script:
   ```bash
   python celery_worker.py
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Copy `backend/.env.example` to `.env` and set secrets.

