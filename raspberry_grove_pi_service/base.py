import abc

from . import spec_types


class AbstractSensor(abc.ABC):
    def __init__(self, port: int) -> None:
        self._port: int = port

    @abc.abstractmethod
    def get_data(self) -> spec_types.SensorResult:
        ...

    @abc.abstractmethod
    def on(self) -> bool:
        ...

    @abc.abstractmethod
    def off(self) -> bool:
        ...
