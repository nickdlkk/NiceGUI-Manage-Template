from nicegui import ui

from app.frontend.message import message
from app.frontend.module_base import BaseClass


class UserInfoPage(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        print("UserInfoPage instantiated")

        @BaseClass.router.page(path='/user/info', main_page=super().main_page, label='userInfo')
        def page_user_info():
            # TODO
            message('userInfo')
            ui.label('user info page')
