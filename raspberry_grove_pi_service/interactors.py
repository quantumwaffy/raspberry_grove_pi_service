import abc
import asyncio
from typing import Type

import websockets

from logger import logger

from . import consts, ws_connectors


class AbstractInteractor(abc.ABC):
    def __init__(self, ws_connected_pin: int, sensor_pins: dict[consts.Sensor, int]) -> None:
        self._ws_connector: ws_connectors.AbstractWSConnector = self._ws_connector_cls(ws_connected_pin)
        self._sensor_pins: dict[consts.Sensor, int] = sensor_pins

    @property
    @abc.abstractmethod
    def _ws_connector_cls(self) -> Type[ws_connectors.AbstractWSConnector]:
        ...

    @property
    @abc.abstractmethod
    def _ws_url(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def _restart_interval(self) -> float:
        ...

    @abc.abstractmethod
    async def _run(self, ws: websockets.WebSocketClientProtocol) -> None:
        ...

    async def run(self) -> None:
        while True:
            try:
                async with websockets.connect(self._ws_url) as ws:
                    self._ws_check(True)
                    while True:
                        await self._run(ws)
            except Exception as e:
                self._ws_check(False)
                logger.error(e)
                await asyncio.sleep(self._restart_interval)

    def _ws_check(self, is_connected: bool) -> None:
        self._ws_connector.ws_check(is_connected)
