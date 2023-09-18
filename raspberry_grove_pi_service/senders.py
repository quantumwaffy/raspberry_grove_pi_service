import abc
import asyncio
from typing import Type

import websockets

from config import CONFIG
from logger import logger

from . import base, consts, data_collectors, digital_sensors, schemas


class AbstractSender(abc.ABC):
    _data_collector_cls: Type[data_collectors.BaseDataCollector] = data_collectors.BaseDataCollector

    def __init__(self, ws_connected_pin: int, sensor_pins: dict[consts.Sensor, int]) -> None:
        self._ws_indicator: base.AbstractSensor = self._ws_indicator_cls(ws_connected_pin)
        self._data_collector: data_collectors.BaseDataCollector = data_collectors.BaseDataCollector(sensor_pins)

    @abc.abstractmethod
    async def run(self) -> None:
        ...

    @abc.abstractmethod
    def _ws_check(self, is_connected: bool) -> None:
        ...

    @property
    @abc.abstractmethod
    def _ws_indicator_cls(self) -> Type[base.AbstractSensor]:
        ...


class BaseDataSender(AbstractSender):
    _ws_indicator_cls = digital_sensors.LEDSocket

    async def run(self) -> None:
        while True:
            try:
                async with websockets.connect(CONFIG.APP.SERVER_URL) as ws:
                    self._ws_check(True)
                    while True:
                        sensors_data: schemas.SensorData = self._data_collector.data
                        await ws.send(sensors_data.model_dump_json())
                        await asyncio.sleep(CONFIG.APP.SEND_INTERVAL)
            except Exception as e:
                self._ws_check(False)
                logger.error(e)
                await asyncio.sleep(CONFIG.APP.RESTART_INTERVAL)

    def _ws_check(self, is_connected: bool) -> None:
        self._ws_indicator.on() if is_connected else self._ws_indicator.off()
