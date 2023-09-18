from pydantic.v1 import BaseSettings

from core import mixins as core_mixins


class AppConfig(core_mixins.EnvSettingsMixin):
    SERVER_URL: str
    LOG_PATH: str
    SEND_INTERVAL: float = 3
    RESTART_INTERVAL: float = 60


class Config(BaseSettings):
    APP: AppConfig = AppConfig()


CONFIG: Config = Config()
