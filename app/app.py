from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app import frontend
from app.conf.config import Config
from app.db.db import init_db
from app.db.model import User
from app.db.users import current_active_user, init_user
from app.utils.logger import get_logger

config = Config()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    logger.info("init system")
    await init_db()
    if config.common.create_initial_admin_user:
        await init_user()
    yield


app = FastAPI(lifespan=lifespan)


# app.include_router(
#     fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )
# @app.get('/')
# def read_root():
#     return {'Hello': 'World'}


@app.get('/hello')
def read_root():
    return {'Hello': 'World'}


frontend.init(app)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


# @app.exception_handler(404)
# async def not_found_exception_handler(request: Request, exc: HTTPException):
#     logger.info(f"404: {request.url}")
#     return RedirectResponse('/hello')


from fastapi.routing import APIRoute


def get_routes(app: FastAPI):
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                "path": route.path,
                "methods": route.methods,
                "params": route.dependencies
            })
    return routes


routes = get_routes(app)
for route in routes:
    print(route)
