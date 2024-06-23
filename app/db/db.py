from typing import AsyncGenerator

import sqlalchemy
from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy.orm import session

from app.conf.config import Config
from app.db import ENGINE, DB_SESSION, DATABASE_URL
from app.db.model import *
from app.utils.logger import get_logger, setup_logger

config = Config()
setup_logger()
logger = get_logger(__name__)
metadata = sqlalchemy.MetaData()
alembic_cfg = AlembicConfig("alembic.ini")
alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_upgrade(conn, cfg):
    cfg.attributes["connection"] = conn
    command.upgrade(cfg, "head")
    conn.commit()


def run_stamp(conn, cfg, revision):
    cfg.attributes["connection"] = conn
    command.stamp(cfg, revision)
    conn.commit()


def run_ensure_version(conn, cfg):
    cfg.attributes["connection"] = conn
    command.ensure_version(cfg)
    conn.commit()


async def init_db() -> None:
    # 如果数据库不存在则创建数据库（数据表）；若有更新，则执行迁移
    # https://alembic.sqlalchemy.org/en/latest/autogenerate.html
    async with ENGINE.connect() as conn:
        # 判断数据库是否存在
        def user_inspector(conn):
            inspector = sqlalchemy.inspect(conn)
            return inspector.has_table("user")

        result = await conn.run_sync(user_inspector)

        if not result:
            logger.info("database not exists, creating database...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("database created!")
            await conn.run_sync(run_stamp, alembic_cfg, "head")
            logger.info(f"stamped database to head")
            return

        is_alembic_empty = await check_alembic_version_empty(conn)
        if is_alembic_empty:
            await conn.run_sync(run_stamp, alembic_cfg, "799396eac938")
            logger.warning(
                f"Alembic version table is empty, stamped database to baseline(799396eac938)!\n"
                "        Note: This is necessary to update from old version. If you see this message, ensure that you have "
                "already set run_migration to true in config file,\n"
                "              or run `alembic upgrade head` manually."
            )

        if config.data.run_migration:
            try:
                logger.info("try to migrate database...")
                await conn.run_sync(run_upgrade, alembic_cfg)
            except Exception as e:
                logger.warning("Database migration might fail, please check the database manually!")
                logger.warning(f"detail: {str(e)}")

        logger.info("Database initialized.")


async def check_alembic_version_empty(conn: AsyncConnection):
    try:
        result = (await conn.execute(text("SELECT version_num FROM alembic_version"))).fetchall()
        return len(result) == 0
    except Exception as e:
        logger.warning(f"check alembic version failed: {str(e)}")
        raise e


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
