import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: str


class UserCreate(schemas.BaseUserCreate):
    role: str


class UserUpdate(schemas.BaseUserUpdate):
    role: str
