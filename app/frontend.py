from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui, app, Client
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.db import close_db

unrestricted_page_routes = {'/login', '/register'}


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
    def show():
        ui.label('Hello, FastAPI!')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    # app.on_startup(init_db)
    app.on_shutdown(close_db)
    app.add_middleware(AuthMiddleware)

    ui.run_with(
        fastapi_app,
        mount_path='/app',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',
        # NOTE setting a secret is optional but allows for persistent storage per user
    )
