# fixtures for pytest

from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.routers.post import comment_table, post_table


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    print("Generating test client")
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    print("Setting up database")
    post_table.clear()
    comment_table.clear()
    yield


@pytest.fixture()
async def async_client(
    client,
) -> AsyncGenerator:  # dependency injection using client() method above.
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=client.base_url
    ) as ac:
        yield ac
