from nicegui import ui


def menu(left_drawer=None) -> None:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    ui.label('Modularization Example').classes('font-bold')
    with ui.tabs() as tabs:
        ui.tab('Home').on()
    ui.space()
    ui.link('Home', '/').classes(replace='text-white')
    ui.space()
    ui.link('A', '/a').classes(replace='text-white')
    ui.space()
    ui.link('B', '/b').classes(replace='text-white')
    ui.space()
    ui.link('C', '/c').classes(replace='text-white')
