from pydantic.v1 import BaseSettings

from core import mixins as core_mixins


class AppConfig(core_mixins.EnvSettingsMixin):
    SERVER_URL: str = ""
    SEND_INTERVAL: float = 3
    RESTART_INTERVAL: float = 60
    LOG_PATH: str = "/var/log/raspberry_grove_pi_service.log"


class Config(BaseSettings):
    APP: AppConfig = AppConfig()


CONFIG: Config = Config()
