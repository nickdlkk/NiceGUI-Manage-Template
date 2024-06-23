from typing import AsyncGenerator

import sqlalchemy
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from app.db import ENGINE, DB_SESSION
from app.db.model import *
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def init_db() -> None:
    logger.info("Initializing database")
    await ENGINE.connect()
    Base.metadata.create_all(ENGINE)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with DB_SESSION() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def close_db() -> None:
    try:
        DB_SESSION.close_all()
    except:
        import traceback
        traceback.print_exc()


def get_db() -> session:
    db = DB_SESSION()
    try:
        yield db
    finally:
        db.close()
