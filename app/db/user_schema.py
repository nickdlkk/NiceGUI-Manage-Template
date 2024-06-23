import uuid

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    email: EmailStr
    role: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    role: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
    role: str
