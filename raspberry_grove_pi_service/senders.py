import abc
import asyncio
import time
from typing import Type

import websockets

from config import CONFIG

from . import consts, data_collectors, interactors, schemas, ws_connectors


class AbstractDataSender(interactors.AbstractInteractor):
    _ws_url = CONFIG.APP.SERVER_URL_TO_SEND
    _restart_interval = CONFIG.APP.RESTART_INTERVAL_TO_SEND

    def __init__(self, ws_connected_pin: int, sensor_pins: dict[consts.Sensor, int]) -> None:
        super().__init__(ws_connected_pin, sensor_pins)
        self._data_collector: data_collectors.BaseDataCollector = self._data_collector_cls(sensor_pins)
        time.sleep(1)

    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        sensors_data: schemas.SensorData = self._data_collector.data
        await ws.send(sensors_data.model_dump_json())
        await asyncio.sleep(CONFIG.APP.SEND_INTERVAL)

    @property
    @abc.abstractmethod
    def _data_collector_cls(self) -> Type[data_collectors.BaseDataCollector]:
        ...


class BaseLEDConnectorDataSender(AbstractDataSender):
    _data_collector_cls: Type[data_collectors.BaseDataCollector] = data_collectors.BaseDataCollector
    _ws_connector_cls = ws_connectors.LEDWSConnector
