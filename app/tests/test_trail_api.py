from fastapi.testclient import TestClient
from app.app import app
import pytest
from httpx import AsyncClient, ASGITransport


# импорты для стирания из бд
from fastapi import Depends
from app.models import User, get_async_session
from  sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# TODO: Сделать тестовую БД которая в точности повторяет основную

@pytest.mark.asyncio
async def test_user(client,user_payload):
        response = await client.post("/users",json=user_payload)
        assert response.status_code == 200
        async for session in get_async_session():
            res = await session.execute(select(User).where(User.email == user_payload["email"]))
            test_us = res.scalar_one_or_none() # возвращает только 1 предмет из объекта бд если их много просто делает Raises MultipleResultsFound
            if test_us:
                await session.delete(test_us)
                await session.commit() # Сохраняет действия в бд НЕ ЗАБЫТЬ
                return None
            break



@pytest.mark.asyncio
@pytest.mark.parametrize("title,distance_km,time_minutes,route_type,user_id",[
            (12,12,12,12,12),
            ("night_run","twelve","twelve","","1"),
            ("S","SS",-1,"ema","shish"),
            ("capone",12,56,"bicycle","capone"),
            ("Z","Z","Z","Z","Z"),

                         ])
async def test_bad_data(client,title,distance_km,time_minutes,route_type,user_id):
        res = await client.post("/routes",json={
            "title":title,
            "distance_km":distance_km,
            "time_minutes":time_minutes,
            "route_type":route_type,
            "user_id":user_id})
        assert res.status_code == 422

@pytest.mark.asyncio
async def test_unreal_userid(client):
        res = await client.get("/users/999/stats")
        assert res.status_code == 404
        assert res.json()["detail"] == "can't find any user with id: 999"
