import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
import asyncio

from main import app

@pytest.fixture(scope="session")
def test_user():
    return {
        "username": "trial",
        "password": "trial",
    }

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac