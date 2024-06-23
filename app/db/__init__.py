from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from settings import CONFIG, DATA_PATH

Base = declarative_base()
DATABASE_URL = CONFIG('DATABASE_URL', default='sqlite+aiosqlite:///' + DATA_PATH + 'app.db')
print("db url:" + DATABASE_URL)
ENGINE = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DB_SESSION = async_sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
print("init db done")
