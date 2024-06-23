from sqlalchemy import Column, Integer, String

from app.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, comment="主键ID")
    username = Column(String(40), unique=False)
    password = Column(String(64), unique=False)
    salt = Column(String(40), unique=False)
    name = Column(String(40), unique=False)
