from datetime import datetime, timedelta, timezone
from fastapi import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

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
    DB_TIME_ZONE_OFFSET_HOURS: int = 0
    DB_TIME_ZONE_NAME: str = "UTC"
    PATH_OF_ALEMBIC_INI: str = "alembic.ini"

    # DB schemas
    DB_ALEMBIC_SCHEMA: str = "alembic"
    DB_BOOKING_SCHEMA: str = "booking"

    # Tests
    MODE: Literal["dev", "test", "stage", "prod"] = "prod"
    COMPOSE_FILE: str = "./docker/docker-compose.test.yaml"
    PATH_OF_TEST_DUMP: str = "tests/db_dumps/dump_of_lookup_tables.sql"
    CURRENT_DATE_AND_TIME: str = "2024-08-01 12:00:00"

    # Authorization
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_COOKIE: str = "hotel_rental_access_token"

    # Business logic
    CHECK_IN_TIME: int = 14
    CHECK_OUT_TIME: int = 12
    MIN_RENTAL_INTERVAL_HOURS: int = 22
    BOOKING_CANCELLATION_AVAILABILITY_HOURS: int = 72

    # Media
    PATH_OF_MEDIA: str = "media"
    PATH_OF_BOOKING_IMAGES: str = f"{PATH_OF_MEDIA}/images/bookings"

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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
