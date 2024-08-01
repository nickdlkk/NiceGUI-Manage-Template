from nicegui import ui

from app.frontend.message import message
from app.frontend.module_base import BaseClass


class UserManagerPage(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        print("UserManagerPage instantiated")

        @BaseClass.router.page(path='/user', main_page=super().main_page, label='user')
        def page_user_manager():
            # TODO
            message('Page B')
            ui.label('This page is defined in a class.')
