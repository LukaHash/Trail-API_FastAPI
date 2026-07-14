from fastapi.testclient import TestClient
from app.app import app
import pytest
from httpx import AsyncClient, ASGITransport



@pytest.mark.asyncio
async def test_user(client,user_payload):
        response = await client.post("/users",json=user_payload)
        print(f"\nОТВЕТ: {response.status_code} — {response.json()}")
        assert response.status_code == 200

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
