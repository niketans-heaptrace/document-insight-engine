from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, Field, RedisDsn
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    project_name: str = Field("DocInsights", alias="PROJECT_NAME")
    api_v1_prefix: str = Field("/api/v1", alias="API_V1_PREFIX")
    environment: str = Field("development", alias="ENVIRONMENT")
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        alias="BACKEND_CORS_ORIGINS",
    )

    redis_url: RedisDsn = Field("redis://localhost:6379/0", alias="REDIS_URL")
    celery_broker_url: str = Field("redis://localhost:6379/1", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field("redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND")

    vector_db_path: Path = Field(Path("./storage/chroma"), alias="VECTOR_DB_PATH")
    database_url: str = Field("sqlite+aiosqlite:///./storage/app.db", alias="DATABASE_URL")

    embedding_model: str = Field("all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    llm_model: str = Field("gpt-4o-mini", alias="LLM_MODEL")
    llm_api_key: str = Field("changeme", alias="LLM_API_KEY")
    llm_base_url: str | None = Field(default=None, alias="LLM_BASE_URL")

    chroma_collection: str = Field("documents", alias="CHROMA_COLLECTION")

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "allow",
    }


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.vector_db_path.mkdir(parents=True, exist_ok=True)
    return settings


