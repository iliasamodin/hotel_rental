from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

load_dotenv()


class Settings(BaseSettings):
    # API
    HOST: str = "127.0.0.1"
    PORT: int = 1500
    API_PREFIX: str = "/api/v1"

    # Unicorn
    RELOAD: bool = False

    # DB
    POSTGRES_DB: str
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int

    # DB schemas
    DB_ALEMBIC_SCHEMA: str = "alembic"
    DB_BOOKING_SCHEMA: str = "booking"

    MODE: str

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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
