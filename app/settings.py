from datetime import datetime, timedelta, timezone
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, Field, SecretStr

load_dotenv()


class Settings(BaseSettings):
    # API
    HOST: str = "127.0.0.1"
    PORT: int = 1500
    API_PREFIX: str = "/api/v1"
    PATH_OF_PYPROJECT: str = "pyproject.toml"

    # Unicorn
    RELOAD: bool = False

    # DB
    POSTGRES_DB: str
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_TIME_ZONE_OFFSET_HOURS: int = Field(default=0, ge=-12, le=14)
    DB_TIME_ZONE_NAME: str = "UTC"
    PATH_OF_ALEMBIC_INI: str = "alembic.ini"

    # DB schemas
    DB_ALEMBIC_SCHEMA: str = "alembic"
    DB_BOOKING_SCHEMA: str = "booking"

    # Redis
    CACHING: bool = False
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    CACHE_RETENTION_TIME_SECONDS: int = Field(default=60, ge=1)
    WARM_UP_CACHE: bool = False

    # Tests
    MODE: Literal["dev", "test", "stage", "prod"] = "prod"
    COMPOSE_FILE: str = "./docker/docker-compose.test.yaml"
    PATH_OF_TEST_DUMP: str = "tests/db_dumps/dump_of_lookup_tables.sql"
    CURRENT_DATE_AND_TIME: str = "2024-08-01 12:00:00"

    # Authorization
    SECRET_KEY: SecretStr
    ALGORITHM: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1)
    ACCESS_TOKEN_COOKIE: str = "hotel_rental_access_token"

    # Business logic
    CHECK_IN_TIME: int = Field(default=14, ge=0, le=21)
    CHECK_OUT_TIME: int = Field(default=12, ge=2, le=23)
    MIN_RENTAL_INTERVAL_HOURS: int = Field(default=22, ge=22)
    BOOKING_CANCELLATION_AVAILABILITY_HOURS: int = Field(default=72, ge=0)
    NOTIFICATION_ABOUT_SOON_BOOKING_HOURS: int = Field(default=24, ge=24)

    # Media
    PATH_OF_MEDIA: str = "media"
    PATH_OF_BOOKING_IMAGES: str = f"{PATH_OF_MEDIA}/images/bookings"

    # Email
    SENDING_EMAIL: bool = False
    MAIL_SMTP_SERVER: str
    MAIL_SMTP_PORT: int
    MAIL_ADDRESS: EmailStr
    MAIL_PASSWORD: SecretStr

    @property
    def DB_URL(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DB_SECRET_URL(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DB_URL(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DB_SECRET_URL(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def NEED_TO_WARM_UP_CACHE(self):
        return self.CACHING and self.WARM_UP_CACHE

    @property
    def WARM_UP_CACHE_SECONDS(self):
        return self.CACHE_RETENTION_TIME_SECONDS + 1

    @property
    def DB_TIME_ZONE(self):
        return timezone(
            offset=timedelta(hours=self.DB_TIME_ZONE_OFFSET_HOURS),
            name=self.DB_TIME_ZONE_NAME,
        )

    @property
    def CURRENT_DT(self):
        return (
            self.MODE == "test"
            and datetime.strptime(self.CURRENT_DATE_AND_TIME, "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.DB_TIME_ZONE)
            or datetime.now(tz=self.DB_TIME_ZONE)
        )

    @property
    def NEED_TO_SENDING_EMAIL(self):
        return self.CACHING and self.SENDING_EMAIL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
