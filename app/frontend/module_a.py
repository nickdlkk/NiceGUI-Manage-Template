from nicegui import ui

from app.frontend import theme
from app.frontend.message import message
from app.frontend.module_base import BaseClass


class ModuleA(BaseClass):
    def __init__(self):
        print("ModuleA instantiated")

        @ui.page('/a')
        def page_b():
            with theme.frame('- Page A -'):
                message('Page A')
                ui.label('This page is defined in a class.')
