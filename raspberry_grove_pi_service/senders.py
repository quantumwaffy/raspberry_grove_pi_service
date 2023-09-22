import asyncio

import websockets

from config import CONFIG

from . import data_handlers, interactors, schemas, ws_connectors


class AbstractDataSender(interactors.AbstractInteractor):
    _ws_url = CONFIG.APP.SERVER_URL_TO_SEND
    _restart_interval = CONFIG.APP.RESTART_INTERVAL_TO_SEND
    _data_handler_cls = data_handlers.BaseDataCollector

    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        sensors_data: schemas.SensorData = self._data_handler.execute()
        await ws.send(sensors_data.model_dump_json())
        await asyncio.sleep(CONFIG.APP.SEND_INTERVAL)


class BaseLEDConnectorDataSender(AbstractDataSender):
    _ws_connector_cls = ws_connectors.LEDWSConnector
