from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions
from nicegui import ui, app
from starlette.responses import RedirectResponse

from app import USER_KEY, USER_AUTHENTICATED, USER_MODEL, USER_NAME
from app.db.model import User
from app.frontend.message import message
from app.frontend.module_base import BaseClass
from app.utils.logger import get_logger

logger = get_logger(__name__)


class UserInfoPage(BaseClass):
    def __init__(self) -> None:
        super().__init__()
        print("UserInfoPage instantiated")

        @BaseClass.router.page(path='/user/info', main_page=super().main_page, label='userInfo')
        async def page_user_info():

            async def verify_password(dialog, error_label, origin, new, new2) -> User | None:
                if origin.value == "" or new.value == "" or new2.value == "":
                    error_label.set_text('请输入完整信息!')
                    return None
                if origin.value == new.value:
                    error_label.set_text('原密码不能与新密码相同!')
                    return None
                if new2.value != new.value:
                    error_label.set_text('新密码不相同!')
                    return None
                username = app.storage.user.get(USER_KEY)
                credentials = OAuth2PasswordRequestForm(username=username, password=origin.value)
                async with self.get_db_user_manager_async() as user_manager:
                    try:
                        user = await user_manager.authenticate(credentials)
                    except Exception as e:
                        logger.error(e)
                        ui.notify("系统错误", type='negative')
                if user is None:
                    error_label.set_text('原密码错误!')
                    return None
                if not user.is_active:
                    error_label.set_text('该用户已被禁用!')
                    ui.notify("该用户已被禁用!", type='negative')
                    return None
                return user

            async def submit_change_password(dialog, error_label, origin, new, new2) -> bool:
                user = await verify_password(dialog, error_label, origin, new, new2)
                if user is None:
                    dialog.submit(False)
                    return False
                # 验证成功,修改密码
                try:
                    async with self.get_db_user_manager_async() as user_manager:
                        async with self.get_db_user_db_async() as user_db:
                            updated_user = await user_db.update(user,
                                                                {"hashed_password": user_manager.password_helper.hash(
                                                                    new.value)})
                            dialog.submit(True)
                            return True
                except Exception as e:
                    logger.error(e)
                    ui.notify("系统错误!", type='negative')
                    dialog.submit(False)
                    return False

            async def change_password():
                with ui.dialog() as dialog, ui.card():
                    ui.label('修改密码')
                    error = ui.label('').classes(replace='text-negative')
                    with ui.grid(columns=2):
                        ui.label('原密码')
                        origin_password = ui.input(password=True).props('clearable')
                        ui.label('新密码')
                        new_password = ui.input(password=True).props('clearable')
                        ui.label('确认新密码')
                        new_password2 = ui.input(password=True).props('clearable')
                    with ui.row():
                        ui.button('保存',
                                  on_click=lambda: submit_change_password(dialog, error, origin_password, new_password,
                                                                          new_password2))
                        ui.button('取消', on_click=lambda: dialog.submit(None))
                result = await dialog
                if result is not None:
                    # 修改密码后需要登出,重新登录,跳转到登录页面
                    if result:
                        ui.notify('密码修改成功，请刷新页面重新登录!', type='positive')
                        app.storage.user.update({USER_KEY: "", USER_AUTHENTICATED: False})
                        # RedirectResponse('/') 重定向不起作用,需要手动刷新页面
                    return

            async def change_info(username, email):
                if username == "" or email == "":
                    ui.notify('请输入完整信息!')
                    return
                change_info_dict = {}
                if username != app.storage.user.get(USER_MODEL)['username']:
                    change_info_dict['username'] = username
                if email != app.storage.user.get(USER_MODEL)['email']:
                    try:
                        async with self.get_db_user_manager_async() as user_manager:
                            await user_manager.get_by_email(email)
                            ui.notify('该邮箱已被使用!', type='warning')
                            return
                    except exceptions.UserNotExists:
                        change_info_dict['email'] = email
                try:
                    async with self.get_db_user_db_async() as user_db:
                        async with self.get_db_user_manager_async() as user_manager:
                            try:
                                user = await user_manager.get_by_email(app.storage.user.get(USER_MODEL)['email'])
                            except exceptions.UserNotExists:
                                ui.notify('当前用户不存在，请刷新页面重试!')
                                return
                        updated_user = await user_db.update(user, change_info_dict)
                        app.storage.user.update(
                            {USER_MODEL: updated_user.to_dict(), USER_KEY: email, USER_NAME: username})
                        ui.notify('修改成功!', type='positive', position='top')
                except Exception as e:
                    logger.error(e)
                    ui.notify("系统错误!", type='negative')

            message('userInfo')
            if app.storage.user is None:
                ui.notify('请先登录!', type='negative')
                return RedirectResponse('/')
            with ui.card():
                with ui.grid(columns=2):
                    ui.label('Name:')
                    username = ui.input('username', value=app.storage.user.get(USER_MODEL)['username'])

                    ui.label('Email')
                    email = ui.input('email', value=app.storage.user.get(USER_MODEL)['email'])
                with ui.row():
                    ui.button('修改密码', on_click=lambda: change_password())
                    ui.button('保存', on_click=lambda: change_info(username.value, email.value))
