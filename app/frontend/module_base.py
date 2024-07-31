from contextlib import contextmanager

from nicegui import ui

from app.frontend.frame.left_drawer import QuasarDrawer
from app.frontend.router import Router
from app.utils.logger import get_logger
from app.utils.menu_node import MenuNode

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
        with ui.header().classes(replace='row items-center') as header:
            ui.button(on_click=lambda: drawer.toggle_mini(), icon='menu').props('flat color=white')
        # this places the content which should be displayed
        self.router.frame().classes('w-full p-4 bg-gray-100')

        root_menus = MenuNode.build_menu(self.router.menus)
        self.router.virtual_menus_root_node = MenuNode.create_virtual_root_node(root_menus)
        menu_dict = MenuNode.menus_to_dict(root_menus)

        def on_drawer_toggle(e):
            ui.notify(f'Drawer {"opened" if e.args else "closed"}')

        def on_mini_toggle(e):
            ui.notify(f'Mini mode {"activated" if e.args else "deactivated"}')

        def on_menu_click(e):
            # 传过来的是label
            node = self.router.virtual_menus_root_node.find_by_label(e.args)
            if node is None:
                ui.notify(f'{e.args} 菜单不存在')
                return
            ui.notify(f'click {e.args}')
            self.router.open(node.path)

        with ui.footer(value=False) as footer:
            ui.label('Footer')

        drawer = QuasarDrawer(menu_data=menu_dict, on_drawer_toggle=on_drawer_toggle, on_mini_toggle=on_mini_toggle,
                              on_menu_click=on_menu_click)

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
