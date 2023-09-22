import abc
from typing import Any, Type, Unpack

from pydantic import BaseModel

from . import analog_sensors, base, consts, digital_sensors, schemas


class AbstractSensorsHandler(abc.ABC):
    def __init__(self, pin_data: dict[consts.Sensor, int]) -> None:
        self._sensors: dict[str, base.AbstractSensor] = {
            _type.name: handler_cls(pin)
            for _type, handler_cls in self._sensors_cls.items()
            if (pin := pin_data.get(_type))
        }

    @abc.abstractmethod
    def execute(self, **kwargs: Unpack[dict[str, Any]]) -> Any:
        ...

    @property
    @abc.abstractmethod
    def _sensors_cls(self) -> dict[consts.Sensor, Type[base.AbstractSensor]]:
        ...

    @property
    @abc.abstractmethod
    def _schema_cls(self) -> Type[BaseModel]:
        ...


class BaseDataCollector(AbstractSensorsHandler):
    _schema_cls = schemas.SensorData
    _sensors_cls = {
        consts.Sensor.temperature: digital_sensors.TemperatureSensor,
        consts.Sensor.humidity: digital_sensors.HumiditySensor,
        consts.Sensor.sound: analog_sensors.SoundSensor,
        consts.Sensor.light: analog_sensors.LightSensor,
    }

    def execute(self, **kwargs: Unpack[dict[str, Any]]) -> _schema_cls:
        return self._schema_cls(**{_type: handler.get_data() for _type, handler in self._sensors.items()})


class BaseRunner(AbstractSensorsHandler):
    _schema_cls = schemas.RunnerData
    _sensors_cls = {
        consts.Sensor.led: digital_sensors.LEDSocket,
    }

    def execute(self, msg: schemas.RunnerData) -> Any:
        ...
