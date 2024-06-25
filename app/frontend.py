from typing import Optional

from fastapi import FastAPI, Depends, APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from nicegui import ui, app, Client
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.db import close_db
from app.db.model import User
from app.db.users import get_user_manager, current_active_user
from app.utils.logger import get_logger

unrestricted_page_routes = {'/login', '/register'}
router = APIRouter()

logger = get_logger(__name__)


def init(fastapi_app: FastAPI) -> None:
    class AuthMiddleware(BaseHTTPMiddleware):
        """This middleware restricts access to all NiceGUI pages.

        It redirects the user to the login page if they are not authenticated.
        """

        async def dispatch(self, request: Request, call_next):
            if not app.storage.user.get('authenticated', False):
                if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                    app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                    return RedirectResponse('/login')
            return await call_next(request)

    @ui.page('/')
    def show(request: Request, user: User = Depends(current_active_user)):
        ui.label('Hello, FastAPI!')
        print(f'main_page Auth: {request.headers.get("Authorization")}')
        print(f'main_page auth: {request.headers.get("authorization")}')
        print(f'main_page user: {user}')
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    @ui.page('/login')
    async def login(
            user_manager: BaseUserManager = Depends(get_user_manager)
    ) -> Optional[RedirectResponse]:
        async def try_login() -> None:
            credentials = OAuth2PasswordRequestForm(username=username.value, password=password.value)
            user = await user_manager.authenticate(credentials)
            if user is None or not user.is_active:
                logger.info(f'Authentication failed for user {username.value}')
                ui.notify('Wrong username or password', color='negative')
            else:
                app.storage.user.update({'username': username.value, 'authenticated': True})
                logger.info(f'User {username.value} authenticated')
                ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go

        if app.storage.user.get('authenticated', False):
            return RedirectResponse('/')
        with ui.card().classes('absolute-center'):
            username = ui.input('Username').on('keydown.enter', try_login)
            password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter',
                                                                                           try_login)
            ui.button('Log in', on_click=try_login)
        return None

    # app.on_startup(init_db)
    app.on_shutdown(close_db)
    app.add_middleware(AuthMiddleware)

    ui.run_with(
        fastapi_app,
        mount_path='/',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',
        # NOTE setting a secret is optional but allows for persistent storage per user
    )
