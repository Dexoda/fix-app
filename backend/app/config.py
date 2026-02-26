from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://fixapp:fixapp123@db:5432/fixapp"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    UPLOAD_DIR: str = "/app/uploads"
    MAX_VIDEO_SIZE_MB: int = 50
    FIRST_SUPERADMIN_EMAIL: str = "admin@fixapp.local"
    FIRST_SUPERADMIN_PASSWORD: str = "admin123"
    FIRST_SUPERADMIN_NAME: str = "Super Admin"

    class Config:
        env_file = ".env"

settings = Settings()
