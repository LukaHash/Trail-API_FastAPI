from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.db import *


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(40),unique=True)
    level: Mapped[str] = mapped_column(String(20))

    routes: Mapped[list["Route"]] = relationship(back_populates="user")


class Route(Base):
    __tablename__ = "route"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(200))
    distance_km: Mapped[float]
    time_minutes: Mapped[float]
    route_type: Mapped[str] = mapped_column(Text())

    user: Mapped["User"] = relationship(back_populates="routes")





async def create_db_and_tables():
    async  with engine.begin() as conn:
        await  conn.run_sync(Base.metadata.create_all)




async def get_async_session() -> [AsyncSession, None]:
    async with async_session_maker() as session:
        yield session