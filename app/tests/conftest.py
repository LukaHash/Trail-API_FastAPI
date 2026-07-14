import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, delete
from app.models import create_db_and_tables, get_async_session, User, Route
from app.schemas import RouteCreate, UserCreate
from  sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from  random import randint
from app.app import app
import asyncio
from unittest.mock import AsyncMock, patch

#Мок - подменяем send_tg_notifications на заглушку
# чтобы не дай бог она делала реальные HTTP запросы во время тестов
@pytest_asyncio.fixture(scope="session",autouse=True)
async def mock_tg():
    with patch("app.app.send_tg_notifications", new_callable=AsyncMock) as mock:
        yield mock

@pytest_asyncio.fixture(scope="session")
async def prepare_db():
    await create_db_and_tables()
    yield

@pytest_asyncio.fixture(scope="session") #scope -- Область применения короч не будет создаваться каждый раз заново, а будет 1 на всю session
async def client(prepare_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        yield client





@pytest.fixture
def user_payload():
    data = {
        "username": "alice",
        "email": f"alice{randint(1,50000)}@gmail.com",
        "level": "beginner"
    }
    yield data



