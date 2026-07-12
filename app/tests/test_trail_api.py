from fastapi.testclient import TestClient
from app.app import app
from app.tests.conftest import user_payload
import pytest
client = TestClient(app)

# def test_user(user_payload):
#     response =client.post("/users",json=user_payload)
#     assert response.status_code == 200


@pytest.mark.parametrize("title,distance_km,time_minutes,route_type,user_id",[
            (12,12,12,12,12),
            ("night_run","twelve","twelve","","1"),
            ("S","SS",-1,"ema","shish"),
            ("capone",12,56,"bicycle","capone"),
            ("Z","Z","Z","Z","Z"),

                         ])
def test_bad_data(title,distance_km,time_minutes,route_type,user_id):
    res = client.post("/routes",json={
        "title":title,
        "distance_km":distance_km,
        "time_minutes":time_minutes,
        "route_type":route_type,
        "user_id":user_id})
    assert res.status_code == 422


def test_unreal_userid():
    res = client.get("/users/999/stats")
    assert res.status_code == 404
    assert res.json()["detail"] == "can't find any user with id: 999"
