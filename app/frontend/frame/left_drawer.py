from typing import Callable, Optional

from nicegui import ui


class QuasarDrawer(ui.element, component='./left_drawer.vue'):
    def __init__(self, *, menu_data, on_drawer_toggle: Optional[Callable] = None,
                 on_mini_toggle: Optional[Callable] = None,
                 on_menu_click: Optional[Callable]) -> None:
        super().__init__()
        self.on('drawer-toggle', on_drawer_toggle)
        self.on('mini-toggle', on_mini_toggle)
        self.on('menu-click', on_menu_click)
        self._props['menuData'] = menu_data
        self.client.layout._props['view'] = 'hHh LpR lFf'  # value: https://quasar.dev/layout-builder
        page_container_index = self.client.layout.default_slot.children.index(self.client.page_container)
        self.move(target_index=page_container_index)

    def toggle_drawer(self) -> None:
        self.run_method('toggleDrawer')

    def toggle_mini(self) -> None:
        self.run_method('toggleMini')

    def test_arg(self) -> None:
        self.run_method('testArg', 'test')
