import abc
from typing import Type

from . import base, digital_sensors


class AbstractWSConnector(abc.ABC):
    def __init__(self, ws_connected_pin: int) -> None:
        self._ws_indicator: base.AbstractSensor = self._ws_indicator_cls(ws_connected_pin)

    @property
    @abc.abstractmethod
    def _ws_indicator_cls(self) -> Type[base.AbstractSensor]:
        ...

    @abc.abstractmethod
    def ws_check(self, is_connected: bool) -> None:
        ...


class LEDWSConnector(AbstractWSConnector):
    _ws_indicator_cls = digital_sensors.LEDSocket

    def ws_check(self, is_connected: bool) -> None:
        self._ws_indicator.on() if is_connected else self._ws_indicator.off()
