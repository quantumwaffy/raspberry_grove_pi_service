from pydantic.v1 import BaseSettings

from core import mixins as core_mixins


class AppConfig(core_mixins.EnvSettingsMixin):
    SERVER_URL_TO_SEND: str
    SERVER_URL_TO_RECEIVE: str
    LOG_PATH: str
    SEND_INTERVAL: float = 3
    RESTART_INTERVAL_TO_SEND: float = 60
    RESTART_INTERVAL_TO_RECEIVE: float = 60


class Config(BaseSettings):
    APP: AppConfig = AppConfig()


CONFIG: Config = Config()
