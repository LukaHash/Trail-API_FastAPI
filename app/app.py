from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.tg import send_tg_notifications
from app.models import create_db_and_tables, get_async_session, User, Route
from app.schemas import RouteCreate, UserCreate
from  sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select



async def lifespan(app: FastAPI):
    await create_db_and_tables()
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=report_tg,
        trigger="interval",
        seconds=10,
        replace_existing=True,
        max_instances=1
    )


    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


@app.post("/routes")
async def get_route_data(route: RouteCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        new_route = Route(
            title= route.title,
            distance_km = route.distance_km,
            time_minutes= route.time_minutes,
            route_type= route.route_type,
            user_id= route.user_id
        )
        session.add(new_route)
        await session.commit()
        await session.refresh(new_route)
        return new_route
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


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
        await send_tg_notifications(f"new user was added to db: {new_user.username}\n level:{new_user.level}")
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/stats")
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"can't find any user with id: {user_id}")

    total_distance = 0.0
    total_time = 0.0
    count = 0
    result = await session.execute(select(Route).where(Route.user_id == user_id))
    routes = result.scalars().all()


    for route in routes:
        total_distance += route.distance_km
        total_time += route.time_minutes
        count += 1
    summary = {
        "total_distance": total_distance,
        "total_time": total_time,
        "routes completed": count
    }
    if summary["routes completed"] == 0:
        raise HTTPException(status_code=404, detail=f"can't find any routes for user with id: {user_id}")
    return summary

async def report_tg():
    await send_tg_notifications("Бот работает, все в норме")
    return "Func ends correctly"
