from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import CONFIG, DATA_PATH

Base = declarative_base()
DATABASE_URL = CONFIG('DATABASE_URL', default='sqlite+aiosqlite:///' + DATA_PATH + 'app.db')
print("db url:" + DATABASE_URL)
ENGINE = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DB_SESSION = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)
