import abc

from . import base, consts


class AbstractTask(abc.ABC):
    def __init__(self, sensors: dict[str, base.AbstractSensor]) -> None:
        self._sensors: dict[str, base.AbstractSensor] = sensors

    @abc.abstractmethod
    async def execute(self, action: consts.TaskAction) -> None:
        ...


class AbstractSimpleTask(AbstractTask):
    @property
    def _sensor(self) -> base.AbstractSensor:
        return self._sensors[self._sensor_name]

    @property
    @abc.abstractmethod
    def _sensor_name(self) -> str:
        ...

    async def execute(self, action: consts.TaskAction) -> None:
        self._sensor.on() if action == consts.TaskAction.ON else self._sensor.off()


class LEDSocketTask(AbstractSimpleTask):
    _sensor_name = consts.Sensor.led.name


class BuzzerTask(AbstractSimpleTask):
    _sensor_name = consts.Sensor.buzzer.name
