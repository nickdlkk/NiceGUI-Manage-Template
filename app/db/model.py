from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True, comment="用户名")
    role: str = Column(String, default='user')

    def to_dict(self):
        return {"username": self.username, "role": self.role, "email": self.email}
