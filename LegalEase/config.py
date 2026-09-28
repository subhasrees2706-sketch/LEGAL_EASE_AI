from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    )


settings = Settings()