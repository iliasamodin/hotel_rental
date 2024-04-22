from fastapi import FastAPI
from httpx import ASGITransport

import pytest

from app.settings import settings


@pytest.fixture(scope="session")
def transport_for_client(app: FastAPI) -> ASGITransport:
    transport = ASGITransport(
        app=app,
        client=(
            settings.HOST,
            settings.PORT,
        ),
    )
    return transport
