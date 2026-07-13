import pytest
from sqlalchemy import select, delete
from app.models import create_db_and_tables, get_async_session, User, Route
from app.schemas import RouteCreate, UserCreate
from  sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends




@pytest.fixture
async def user_payload(session: AsyncSession = Depends(get_async_session)):
    data = {
        "username": "alice",
        "email": "alice@gmaill",
        "level": "beginner"
    }
    # yield data
    # result = await session.execute(delete(User).where(User.email == data["email"]))



