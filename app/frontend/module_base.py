from contextlib import contextmanager

from nicegui import ui

from app.frontend.router import Router
from app.utils.logger import get_logger

logger = get_logger(__name__)

class BaseClass:
    current_tab: str

    router = Router()

    def __init__(self):
        self.current_tab = ''

    def show_route(self):
        self.router.open(self.current_tab)

    def main_page(self):
        ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
        with ui.left_drawer().classes('bg-blue-100') as left_drawer:
            ui.label('Side menu')

        with ui.header().classes(replace='row items-center') as header:
            with ui.tabs().on('update:model-value', self.show_route).bind_value(self, 'current_tab'):
                logger.info("ALL Router:" + str(self.router.routes))
                for i in self.router.routes:
                    ui.tab(i, label=i).classes('w-32')
        # this places the content which should be displayed
        self.router.frame().classes('w-full p-4 bg-gray-100')
    @DeprecationWarning
    @contextmanager
    def frame(self, navigation_title: str):
        """Custom page frame to share the same styling and behavior across all pages"""
        ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
        with ui.left_drawer().classes('bg-blue-100') as left_drawer:
            ui.label('Side menu')

        with ui.header():
            with ui.tabs().on('update:model-value', self.show_route).bind_value(self, 'current_tab'):
                ui.tab('/a', label='A').classes('w-32')
                ui.tab('/b', label='B').classes('w-32')
                ui.tab('/c', label='C').classes('w-32')
            # menu(left_drawer)
        self.router.frame().classes('w-full p-4 bg-gray-100')
        with ui.column().classes('absolute-center items-center'):
            yield
