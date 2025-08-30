import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from datetime import timezone, datetime

# Loading variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    # API
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = os.getenv("API_PORT", 8000)
    API_URL: str = os.getenv("API_URL", "http://127.0.0.1:8000")

    # CATAPI
    CAT_API_URL: str = "https://api.thecatapi.com/v1/breeds"

    # DB
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "default_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "default_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "default_dbname")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", 'localhost')

    # DEBUG
    DEBUG: int = os.getenv("DEBUG", 1)

    class Config:
        env_file = ".env"
        extra = "ignore"


class TimeZone:
    IS_ACTIVE: bool = False
    DATETIME_TZ: timezone = timezone.utc

    @classmethod
    def get_tz(cls):
        if cls.IS_ACTIVE:
            return cls.DATETIME_TZ
        return None

    @classmethod
    def handle_tz(cls, tz=None):
        if cls.IS_ACTIVE:
            if not tz:
                tz = cls.DATETIME_TZ
        else:
            tz = None
        return tz

    @classmethod
    def handle_datetime(cls, dt: datetime):
        return dt.replace(tzinfo=cls.get_tz())


settings = Settings()
