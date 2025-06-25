from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # App configuration
    APP_NAME: str = "pgpyfatovutwls"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgres://pgpyfatovutwls_user:aquila-vita-casa@localhost:5432/pgpyfatovutwls_db"
    
    # Security
    SECRET_KEY: str = "porta-terra-cielo-ponte-mare-stella-sole-luna"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "paodal@gmail.com"
    SMTP_PASSWORD: Optional[str] = None
    
    # Lemon Squeezy
    LEMON_SQUEEZY_API_KEY: Optional[str] = None
    LEMON_SQUEEZY_WEBHOOK_SECRET: Optional[str] = None
    LEMON_SQUEEZY_STORE_ID: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # Super admin
    SUPER_ADMIN_EMAIL: str = "paodal@gmail.com"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Tortoise ORM configuration
TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC"
}