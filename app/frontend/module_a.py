from nicegui import ui, APIRouter, app

from app.frontend import theme
from app.frontend.message import message
from app.frontend.module_base import BaseClass


class ModuleA(BaseClass):
    def __init__(self):
        super().__init__()
        print("ModuleA instantiated")
        # 统一的前缀
        router = APIRouter(prefix='/example')

        @router.page('/a')
        def page_b():
            with super().frame('- Page A -'):
                message('Page A')
                ui.label('This page is defined in a class.')

        # 需要手动引入
        app.include_router(router)
