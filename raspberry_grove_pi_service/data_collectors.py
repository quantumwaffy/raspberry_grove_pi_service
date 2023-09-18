from typing import Type

from . import analog_sensors, base, consts, digital_sensors, schemas


class BaseDataCollector:
    _schema_cls: Type[schemas.SensorData] = schemas.SensorData
    _sensors_cls: dict[consts.Sensor, Type[base.AbstractSensor]] = {
        consts.Sensor.temperature: digital_sensors.TemperatureSensor,
        consts.Sensor.humidity: digital_sensors.HumiditySensor,
        consts.Sensor.sound: analog_sensors.SoundSensor,
        consts.Sensor.light: analog_sensors.LightSensor,
    }

    def __init__(self, pin_data: dict[consts.Sensor, int]) -> None:
        self._sensors: dict[str, base.AbstractSensor] = {
            _type.name: handler_cls(pin)
            for _type, handler_cls in self._sensors_cls.items()
            if (pin := pin_data.get(_type))
        }

    @property
    def data(self) -> _schema_cls:
        return self._schema_cls(**{_type: handler.get_data() for _type, handler in self._sensors.items()})
