from pydantic import BaseModel



class RouteCreate(BaseModel):
    title: str
    distance_km: float
    time_minutes: int
    route_type: str
    user_id: int

class UserCreate(BaseModel):
    username: str
    email: str
    level: str



