import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production")
	jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
	access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
