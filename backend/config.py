import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))
    allowed_origins: tuple[str, ...] = tuple(
        os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    )
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_enabled: bool = os.getenv("ENABLE_GEMINI", "true").lower() == "true"
    vectorizer_path: str = os.getenv("VECTORIZER_PATH", "backend/models/vectorizer.pkl")
    jd_store_path: str = os.getenv("JD_VECTOR_STORE_PATH", "backend/models/jd_vector_store.pkl")


settings = Settings()
