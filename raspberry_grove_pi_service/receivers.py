import json

import websockets

from config import CONFIG
from logger import logger

from . import data_handlers, interactors, schemas, ws_connectors


class AbstractDataReceiver(interactors.AbstractInteractor):
    _ws_url = CONFIG.APP.SERVER_URL_TO_RECEIVE
    _restart_interval = CONFIG.APP.RESTART_INTERVAL_TO_RECEIVE
    _data_handler_cls = data_handlers.BaseRunner

    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        msg: str = await ws.recv()
        msg_data: schemas.RunnerData = schemas.RunnerData(**json.loads(msg))
        logger.info(msg_data)


class BaseLEDConnectorDataReceiver(AbstractDataReceiver):
    _ws_connector_cls = ws_connectors.LEDWSConnector
