from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from app.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    role: str = Column(String, default='user')
