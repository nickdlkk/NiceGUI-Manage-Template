from nicegui import ui

from app.frontend.message import message
from app.frontend.module_base import BaseClass


class ModuleC(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        print("ModuleC instantiated")

        @BaseClass.router.page(path='/c', main_page=super().main_page, label='C')
        def page_c():
            # with BaseClass.frame(self, '- Page C -'):
            message('Page C')
            ui.label('This page is defined in a class.')
