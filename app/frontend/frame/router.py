from typing import Callable, Dict, Union

from nicegui import background_tasks, helpers, ui
from nicegui.page import page

from app.utils.logger import get_logger
from app.utils.menu_node import MenuNode

logger = get_logger(__name__)


class RouterFrame(ui.element, component='router_frame.js'):
    pass


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class PageDict:
    title: str
    sub_title: str
    path: str
    page_func: Callable

    def __init__(self, title: str = None, sub_title: str = None) -> None:
        self.title = title
        self.sub_title = sub_title
        self.path = ''


@singleton
class Router:
    """
    该类为单例,管理由@router.page装饰的函数的路由
    """
    current_tab: str

    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}
        self.menus = []  # menuNode添加到这个列表里
        self.virtual_menus_root_node = None  # 方便用于查找
        self.content: ui.element = None
        self.current_tab = ''

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func

        return decorator

    def show_route(self):
        self.open(self.current_tab)

    def page(self, *page_args, **page_kwargs):
        def decorator(func):
            main_page = None
            label = None
            # 主页函数由注解加入
            if 'main_page' in page_kwargs:
                main_page = page_kwargs.pop("main_page")
            if 'label' in page_kwargs:
                label = page_kwargs.pop("label")

            decorated_func = page(*page_args, **page_kwargs)

            # 向page传递的func改为统一的一个主页,添加到routes里的是装饰器修饰的func
            if main_page is not None:
                decorated_func = decorated_func(main_page)
                logger.info(f'Added {func.__name__} to routes with main_page: {main_page}')

            logger.info(f'Calling {func.__name__} with outer message')
            path = page_kwargs.get('path')
            if path is not None:
                self.routes[path] = func
                logger.info(f'Added {func.__name__} to routes with path: {path}')
                menu = MenuNode(label, path)
                if 'title' in page_kwargs:
                    menu.title = page_kwargs.pop("title")
                if 'caption' in page_kwargs:
                    menu.caption = page_kwargs.pop("caption")
                if 'icon' in page_kwargs:
                    menu.icon = page_kwargs.pop("icon")
                self.menus.append(menu)

            # @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info(f'Calling {func.__name__} with outer message')
                result = decorated_func(*args, **kwargs)
                logger.info(f'Called {func.__name__} with outer message')
                return result

            logger.info(f'Returning {func.__name__} with outer message')
            return wrapper

        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            with self.content:
                ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''')
                result = builder()
                if helpers.is_coroutine_function(builder):
                    try:
                        await result
                    except Exception as e:
                        logger.exception(e)
                        ui.notify("渲染错误")

        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = RouterFrame().on('open', lambda e: self.open(e.args))
        return self.content
