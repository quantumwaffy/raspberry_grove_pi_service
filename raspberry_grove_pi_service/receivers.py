import time

import websockets

from config import CONFIG
from logger import logger

from . import consts, interactors, ws_connectors


class AbstractDataReceiver(interactors.AbstractInteractor):
    _ws_url = CONFIG.APP.SERVER_URL_TO_RECEIVE
    _restart_interval = CONFIG.APP.RESTART_INTERVAL_TO_RECEIVE

    def __init__(self, ws_connected_pin: int, sensor_pins: dict[consts.Sensor, int]) -> None:
        super().__init__(ws_connected_pin, sensor_pins)
        time.sleep(1)

    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        msg: str = await ws.recv()
        logger.info(msg)


class BaseLEDConnectorDataReceiver(AbstractDataReceiver):
    _ws_connector_cls = ws_connectors.LEDWSConnector
