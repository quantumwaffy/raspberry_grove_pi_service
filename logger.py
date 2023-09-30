import logging.config

from config import CONFIG

logging.basicConfig(
    filename=CONFIG.APP.LOG_PATH,
    format="%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s  call_trace="
    "%(pathname)s L%(lineno)-4d",
)
logger: logging.Logger = logging.getLogger(__name__)
