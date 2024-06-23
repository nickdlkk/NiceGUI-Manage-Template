# import uuid
# from typing import Optional
#
# from fastapi import Request
# from fastapi_users import BaseUserManager, UUIDIDMixin
# from fastapi_users.exceptions import UserAlreadyExists
#
# from app.db import ENGINE
# from app.db.db import get_user_db
# from app.db.model import User
# from app.db.user_schema import UserCreate
# from app.db.users import get_user_manager
#
# SECRET = "secret"
#
#
# class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
#     user_db_model = User
#     reset_password_token_secret = SECRET
#     verification_token_secret = SECRET
#
#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         print(f"User {user.id} has registered.")
#
#     async def on_after_forgot_password(
#             self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"User {user.id} has forgot their password. Reset token: {token}")
#
#     async def on_after_request_verify(
#             self, user: User, token: str, request: Optional[Request] = None
#     ):
#         print(f"Verification requested for user {user.id}. Verification token: {token}")
#
#
# async def init_user() -> None:
#     async with ENGINE.begin() as conn:
#         await init_user_pass()
#
#
# async def init_user_pass():
#     password = "admin"
#     email = "admin@admin.com"
#     role = "admin"
#     try:
#         for user_db in get_user_db():
#             for user_manager in get_user_manager(user_db):
#                 superuser = user_manager.create(
#                     UserCreate(email=email, password=password, is_superuser=True, role=role)
#                 )
#                 print(f"Superuser created {superuser}")
#     except UserAlreadyExists:
#         print(f"Superuser {email} already exist")
