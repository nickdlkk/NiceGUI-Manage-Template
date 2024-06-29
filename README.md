# NiceGUI Manage Template

NiceGUI的管理系统模板

- 数据库:SQLite
- 数据库ORM:SQLAlchemy
- 后端:FastAPI

# Run

main.py -> app -> app.create_app() -> init_db -> init_frontend -> init_backend

setting => .env

default username: admin password: passw0rd

# requirements

依赖

- [NiceGUI](https://github.com/zauberzeug/nicegui/)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [FastAPIUsers](https://github.com/fastapi-users/fastapi-users) `pip install 'fastapi-users[sqlalchemy]'`
- [aiosqlite](https://github.com/omnilib/aiosqlite) Sqlite for AsyncIO `pip install aiosqlite`
- [alembic](https://github.com/sqlalchemy/alembic)

# Ref

参考了以下项目

- https://github.com/thekingofhero2/nicegui_login_template
- https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi
- https://github.com/ffillouxdev/NiceGui_project-portfolio
- https://github.com/chatpire/chatgpt-web-share
- https://gist.github.com/ProbablyBrian/5a47e6ee2242eb0edb572d07b54dcd73
- https://github.com/fastapi-users/fastapi-users/discussions/1361

# usage

## [alembic usage](https://alembic.sqlalchemy.org/en/latest/#)

TODO

# TODO
- [ ] 添加[sidebar](https://github.com/zauberzeug/nicegui/tree/main/examples/menu_and_tabs)
- [ ] 更改密码
- [ ] 注册用户
- [ ] 用户管理页面
- [ ] FastAPI Token认证接口
- [ ] 简单表格增删改查示例
- [ ] 简单图表示例
- [ ] 完善使用示例
- [ ] DockerFile

# Authorization


## NiceGUI

NiceGUI的鉴权方式使用NiceGUI自身的存储app.storage.user

登录成功后,在app.storage.user中存储用户信息

需要鉴权的页面使用:
```python
from app.db.users import current_authenticated_user_nicegui
@ui.page('/')
def show(request: Request, user: User = Depends(current_authenticated_user_nicegui)):
    pass
```

## FastAPI
FastAPI的接口使用FastAPIUsers

```python
from app.db.users import current_active_user
@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
```

其鉴权方式为:
```python
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

TODO token auth