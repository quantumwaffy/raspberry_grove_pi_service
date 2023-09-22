import json

import websockets

from config import CONFIG

from . import data_handlers, interactors, schemas, ws_connectors


class AbstractDataReceiver(interactors.AbstractInteractor):
    _ws_url = CONFIG.APP.SERVER_URL_TO_RECEIVE
    _restart_interval = CONFIG.APP.RESTART_INTERVAL_TO_RECEIVE
    _data_handler_cls = data_handlers.BaseRunner

    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        msg_text: str = await ws.recv()
        msg: schemas.RunnerData = schemas.RunnerData(**json.loads(msg_text))
        self._data_handler.execute(msg=msg)
        print(msg)


class BaseLEDConnectorDataReceiver(AbstractDataReceiver):
    _ws_connector_cls = ws_connectors.LEDWSConnector
