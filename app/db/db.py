from sqlalchemy.orm import session

from app.db import ENGINE, DB_SESSION
from app.db.model import *
from app.utils.password import generate_salt, hash_password


def init_db() -> None:
    # Note: Base需要在Model中导入,记录了Model的元数据才能创建表
    Base.metadata.create_all(ENGINE)
    print("create db tables")
    init_user_pass()


def init_user_pass():
    session = next(get_db())

    def handle_error(e):
        session.rollback()
        session.flush()
        print('错误信息:' + str(e))

    try:
        is_empty = session.query(User).count()
        if is_empty != 0:
            return
    except Exception as e:
        handle_error(e)
    password = "admin"
    salt = generate_salt()
    default_password = hash_password(password, salt)
    user = User(username='admin', password=default_password, name='管理员', salt=salt)
    try:
        session.add(user)
        session.commit()
        print("成功初始化账号")
    except Exception as e:
        handle_error(e)


async def close_db() -> None:
    try:
        DB_SESSION.close_all()
    except:
        import traceback
        traceback.print_exc()


def get_db() -> session:
    db = DB_SESSION()
    try:
        yield db
    finally:
        db.close()
