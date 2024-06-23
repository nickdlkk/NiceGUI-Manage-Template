from typing import Literal

from pydantic import BaseModel, field_validator, Field

from app.conf.base_config import BaseConfig
from app.utils.common import SingletonMeta

_TYPE_CHECKING = False


class CommonSetting(BaseModel):
    print_sql: bool = False
    print_traceback: bool = True
    create_initial_admin_user: bool = True
    initial_admin_user_username: str = 'admin'
    initial_admin_user_password: str = 'password'

    @field_validator("initial_admin_user_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password too short")
        return v


class DataSetting(BaseModel):
    data_dir: str = './data'
    database_url: str = 'sqlite+aiosqlite:///data/app.db'
    run_migration: bool = True
    max_file_upload_size: int = Field(100 * 1024 * 1024, ge=0)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v.startswith('sqlite+aiosqlite:///'):
            raise ValueError("Only support sqlite: 'sqlite+aiosqlite:///'")
        return v

class HttpSetting(BaseModel):
    host: str = '127.0.0.1'
    port: int = Field(8000, ge=1, le=65535)
    cors_allow_origins: list[str] = ['http://localhost:8000', 'http://localhost:5173', 'http://127.0.0.1:8000',
                                     'http://127.0.0.1:5173']


class LogSetting(BaseModel):
    console_log_level: Literal['INFO', 'DEBUG', 'WARNING'] = 'INFO'


class ConfigModel(BaseModel):
    log: LogSetting = LogSetting()
    common: CommonSetting = CommonSetting()
    data: DataSetting = DataSetting()
    http: HttpSetting = HttpSetting()


class Config(BaseConfig[ConfigModel], metaclass=SingletonMeta):
    if _TYPE_CHECKING:
        log: LogSetting = LogSetting()
        common: CommonSetting = CommonSetting()
        data: DataSetting = DataSetting()
        http: HttpSetting = HttpSetting()

    def __init__(self, load_config: bool = True):
        super().__init__(ConfigModel, "config.yaml", load_config=load_config)
