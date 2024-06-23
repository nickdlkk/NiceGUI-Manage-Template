import contextlib
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.exceptions import UserAlreadyExists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing_extensions import AsyncGenerator

from app.conf.config import Config
from app.db import ENGINE
from app.db.db import get_user_db
from app.db.model import User
from app.db.user_schema import UserCreate
from app.utils.logger import setup_logger, get_logger

SECRET = "SECRET"

config = Config()

setup_logger()

logger = get_logger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


# async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
#     yield UserManager(user_db)
async_session_maker = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# 使得 get_async_session_context 和 get_user_db_context 可以使用async with语法
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


async def init_user() -> None:
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    superuser = await user_manager.create(
                        UserCreate(
                            username=config.common.initial_admin_user_username,
                            email="admin@admin.com",
                            password=config.common.initial_admin_user_password,
                            is_active=True,
                            is_verified=True,
                            is_superuser=True,
                            role="admin")
                    )
                    logger.debug(f"Superuser created {config.common.initial_admin_user_username} {superuser}")
    except UserAlreadyExists:
        logger.debug(f"admin already exists, skip creating admin user")
    except Exception as e:
        raise e
