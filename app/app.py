from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.models import create_db_and_tables, get_async_session, User
from app.schemas import RouteCreate, UserCreate
from  sqlalchemy.ext.asyncio import AsyncSession

async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/routes")
def get_route_data(route: RouteCreate):
    new_route = {
        "title": route.title,
        "distance_km": route.distance_km,
        "time_minutes": route.time_minutes,
        "route_type": route.route_type

    }
    return new_route



@app.post("/users")
async def user_create(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            level=user.level

        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))










