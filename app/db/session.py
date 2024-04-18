from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.settings import settings


def get_async_session_maker(
    url: str = settings.DB_SECRET_URL,
    expire_on_commit: bool = False,
) -> sessionmaker:
    engine = create_async_engine(url=url)

    async_session_maker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=expire_on_commit,
    )

    return async_session_maker
