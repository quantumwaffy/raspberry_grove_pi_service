from grovepi import dht, digitalWrite, pinMode

from . import base, spec_types, utils


class BaseDigitalSensor(base.AbstractSensor):
    def __init__(self, _port: int) -> None:
        super().__init__(_port)
        pinMode(_port, "OUTPUT")

    @utils.sensor_error_handler
    def on(self) -> bool:
        digitalWrite(self._port, 1)
        return True

    @utils.sensor_error_handler
    def off(self) -> bool:
        digitalWrite(self._port, 0)
        return False

    @utils.sensor_error_handler
    def get_data(self) -> spec_types.SensorResult:
        return False


class LEDSocket(BaseDigitalSensor):
    ...


class Buzzer(BaseDigitalSensor):
    ...


class _TemperatureHumiditySensor(BaseDigitalSensor):
    def __init__(self, _port: int) -> None:
        super(BaseDigitalSensor, self).__init__(_port)

    @staticmethod
    def _get_value(value: float | str) -> float | None:
        return value if value != "nan" else None

    def on(self) -> None:
        ...

    def off(self) -> None:
        ...


class TemperatureSensor(_TemperatureHumiditySensor):
    @utils.sensor_error_handler
    def get_data(self) -> float | None:
        return self._get_value(dht(self._port, 0)[0])


class HumiditySensor(_TemperatureHumiditySensor):
    @utils.sensor_error_handler
    def get_data(self) -> float | None:
        return self._get_value(dht(self._port, 0)[1])
