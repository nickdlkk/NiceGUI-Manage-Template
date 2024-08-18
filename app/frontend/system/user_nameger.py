from nicegui import ui
from sqlalchemy import select

from app.db.db import DBSessionManager
from app.db.model import User
from app.frontend.module_base import BaseClass
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UserManagerPage(BaseClass):
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
        {'name': 'name', 'label': 'UserName', 'field': 'username', 'required': True},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
    ]

    def __init__(self) -> None:
        super().__init__()
        print("UserManagerPage instantiated")

        @BaseClass.router.page(path='/user', main_page=super().main_page, label='user')
        async def page_user_manager():
            users = []
            # 获取所有user
            async with DBSessionManager() as session:
                result = await session.execute(select(User))
                # 获取所有实体
                _users = result.scalars().all()
                if len(_users) > 0:
                    users = [_user.to_dict() for _user in _users]
                logger.info(_users)

            with ui.table(title='用户列表', columns=self.columns, rows=users, selection='multiple',
                          pagination=3, on_pagination_change=lambda e: ui.notify(e.value),
                          ) as table:
                with table.add_slot('top-right'):
                    with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot(
                            'append'):
                        ui.icon('search')
