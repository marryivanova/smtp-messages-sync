from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from src.utils.custom_logger import get_logger


logger = get_logger(__name__)
logger.propagate = False


class Settings(BaseSettings):
    APP_DEBUG: bool
    APP_HOST: str | int
    APP_PORT: str | int

    APP_ENV: str
    TZ: str
    API_PORT: int

    # db
    DB_HOST: str | int
    DB_PORT: str | int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # RabbitMQ
    RABBITMQ_PORT: int
    RABBITMQ_MANAGEMENT_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    # Maildev
    MAILDEV_WEB_PORT: int
    MAILDEV_SMTP_PORT: int
    MAILDEV_WEB_EXPOSE_PORT: int
    MAILDEV_SMTP_EXPOSE_PORT: int

    # SMTP
    SMTP_SERVER: str
    SMTP_PORT: int
    FROM_EMAIL: str

    @property
    def DB_URL(self) -> str:
        try:
            password = quote_plus(self.DB_PASSWORD)
            return f"postgresql+asyncpg://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        except Exception as e:
            logger.error(f"Error generating DB_URL: {str(e)}")
            raise ValueError("Invalid database configuration") from e

    class Config:
        env_file = [".env", "../.env", "../../.env", "../../../.env"]
        env_file_encoding = "utf-8"


settings = Settings()
