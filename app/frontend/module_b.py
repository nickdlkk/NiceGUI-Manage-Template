from nicegui import ui

from app.frontend import theme
from app.frontend.message import message
from app.frontend.module_base import BaseClass


class ModuleB(BaseClass):
    def __init__(self) -> None:
        print("ModuleB instantiated")

        @ui.page('/b')
        def page_b():
            with theme.frame('- Page B -'):
                message('Page B')
                ui.label('This page is defined in a class.')
