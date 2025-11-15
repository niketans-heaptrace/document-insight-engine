#!/usr/bin/env python
"""Convenience script to run Celery worker."""
from app.workers.celery_app import celery_app

if __name__ == "__main__":
    celery_app.worker_main()


