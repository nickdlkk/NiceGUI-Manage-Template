from typing import Optional

from fastapi import FastAPI, Depends, APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from nicegui import ui, app, Client

from app import USER_KEY, USER_AUTHENTICATED
from app.db.db import close_db
from app.db.model import User
from app.db.users import get_user_manager, current_authenticated_user_nicegui
from app.frontend import derived_class_registry
from app.frontend.frame.left_drawer import QuasarDrawer
from app.frontend.router import Router
from app.utils.logger import get_logger
from app.utils.menu_node import MenuNode

unrestricted_page_routes = {'/login', '/register'}
router = APIRouter()

logger = get_logger(__name__)


def init(fastapi_app: FastAPI) -> None:
    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)

    @ui.page('/')
    def show(request: Request, user: User = Depends(current_authenticated_user_nicegui)):
        with ui.header().classes(replace='row items-center') as header:
            ui.button(on_click=lambda: drawer.toggle_mini(), icon='menu').props('flat color=white')

        #     ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        #     with ui.tabs() as tabs:
        #         ui.tab('A')
        #         ui.tab('B')
        #         ui.tab('C')
        def on_drawer_toggle(e):
            ui.notify(f'Drawer {"opened" if e.args else "closed"}')

        def on_mini_toggle(e):
            ui.notify(f'Mini mode {"activated" if e.args else "deactivated"}')

        def on_menu_click(e):
            ui.notify(f'click {e.args}')

        with ui.footer(value=False) as footer:
            ui.label('Footer')

        # with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        #     ui.label('Side menu')
        test_data = [
            {
                "icon": 'perm_identity',
                "label": 'Account settings',
                "caption": 'John Doe',
                "children": [
                    {"icon": 'inbox', "title": 'Inbox'},
                    {"icon": 'send', "title": 'Outbox'},
                    {"icon": 'delete', "title": 'Trash'},
                    {"icon": 'settings', "title": 'Settings'},
                    {"icon": 'help', "title": 'Help'}
                ]
            },
            {
                "icon": 'signal_wifi_off',
                "label": 'Wifi settings',
                "children": []
            }
        ]

        drawer = QuasarDrawer(menu_data=test_data, on_drawer_toggle=on_drawer_toggle, on_mini_toggle=on_mini_toggle,
                              on_menu_click=on_menu_click)

        with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
            ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

        # with ui.tab_panels(tabs, value='A').classes('w-full'):
        #     with ui.tab_panel('A'):
        #         ui.label('Content of A')
        #         ui.label('Hello, FastAPI!')
        #         print(f'main_page Auth: {request.headers.get("Authorization")}')
        #         print(f'main_page auth: {request.headers.get("authorization")}')
        #         print(f'main_page user: {user}')
        #         # NOTE dark mode will be persistent for each user across tabs and server restarts
        #         ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        #         ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')
        #     with ui.tab_panel('B'):
        #         ui.label('Content of B')
        #         ui.button('GoTo C', on_click=lambda: tabs.set_value('C'))
        #     with ui.tab_panel('C'):
        #         ui.label('Content of C')

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
                app.storage.user.update({USER_KEY: username.value, USER_AUTHENTICATED: True})
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

    def print_routers():
        router = Router()
        logger.info("ALL Router:" + str(router.routes))
        root_menus = MenuNode.build_menu(router.menus)
        menu_dict = MenuNode.menus_to_dict(root_menus)
        logger.info("menu_dict:{}".format(menu_dict))

    app.on_startup(print_routers)
    app.on_shutdown(close_db)
    # app.add_middleware(AuthMiddleware)
    logger.info(derived_class_registry)
    ui.run_with(
        fastapi_app,
        mount_path='/',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='SECRET',
        title='NiceGUI Template'
    )
