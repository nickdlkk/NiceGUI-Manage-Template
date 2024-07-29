from nicegui import ui

from app.frontend.message import message
from app.frontend.module_base import BaseClass


class ModuleB(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        print("ModuleB instantiated")

        @BaseClass.router.page(path='/b', main_page=super().main_page, title='Page A')
        def page_b():
            # with BaseClass.frame(self, '- Page B -'):
            message('Page B')
            ui.label('This page is defined in a class.')
