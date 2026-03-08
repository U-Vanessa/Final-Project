import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Always load backend/.env regardless of current working directory.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=BACKEND_ROOT / ".env")


def _parse_csv(value: str) -> list[str]:
	return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production")
	jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
	access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
	database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
	cors_origins: list[str] = field(
		default_factory=lambda: _parse_csv(
			os.getenv(
				"CORS_ORIGINS",
				"http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
			)
		)
	)
	openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
	openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
