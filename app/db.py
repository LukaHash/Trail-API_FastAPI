from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/traildb"


engine = create_async_engine(DATABASE_URL,echo=True)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)


class Base(DeclarativeBase):
    pass



