from typing import Literal

from pydantic import BaseModel

from app.conf.base_config import BaseConfig
from app.utils.common import SingletonMeta

_TYPE_CHECKING = False


class LogSetting(BaseModel):
    console_log_level: Literal['INFO', 'DEBUG', 'WARNING'] = 'INFO'


class ConfigModel(BaseModel):
    log: LogSetting = LogSetting()


class Config(BaseConfig[ConfigModel], metaclass=SingletonMeta):
    if _TYPE_CHECKING:
        log: LogSetting = LogSetting()

    def __init__(self, load_config: bool = True):
        super().__init__(ConfigModel, "config.yaml", load_config=load_config)
