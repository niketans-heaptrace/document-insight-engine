# Architecture Overview

```text
┌──────────┐    Upload        ┌────────────┐          ┌──────────────┐
│  React   │ ───────────────► │  FastAPI   │ ───────► │ Celery Queue │
└──────────┘                  │  Backend   │ ◄──────┐ └──────────────┘
   ▲   │   Poll/Stream        └────────────┘        │  Redis broker
   │   │                                            │
   │   └──────── Insights & Chat ◄──────────────────┘
   │                      │                           Worker pulls task
   │                      ▼
   │             ┌──────────────────────┐
   │             │ Processing Workers   │
   │             │ - OCR / Parsing      │
   │             │ - Chunk + Embedding  │
   │             │ - LLM Summaries/RAG  │
   │             └──────────────────────┘
   │                      │
   │                      ▼
   │             ┌──────────────────────┐
   │             │ Storage Layer        │
   │             │ - SQL DB (metadata)  │
   │             │ - Chroma (vectors)   │
   │             └──────────────────────┘
   ▼
End users consume dashboards, status, and chat answers once processing completes.
```


