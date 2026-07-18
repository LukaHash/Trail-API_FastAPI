from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


db_user = os.getenv("DB_USER","myuser")
db_password = os.getenv("DB_PASS","mypassword")
db_host = os.getenv("DB_HOST","localhost")
db_port = os.getenv("DB_PORT","5432")
db_name = os.getenv("DB_NAME","traildb")


DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_async_engine(DATABASE_URL,echo=True)
async_session_maker = async_sessionmaker(engine,expire_on_commit=False)


class Base(DeclarativeBase):
    pass
