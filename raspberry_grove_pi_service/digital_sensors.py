from grovepi import dht, digitalWrite, pinMode

from . import spec_types, utils


class BaseDigitalSensor:
    def __init__(self, _port: int) -> None:
        self._port: int = _port
        pinMode(_port, "OUTPUT")

    @utils.sensor_error_handler
    def on(self) -> spec_types.SensorResult:
        digitalWrite(self._port, 1)
        return True

    @utils.sensor_error_handler
    def off(self) -> spec_types.SensorResult:
        digitalWrite(self._port, 0)
        return False

    @utils.sensor_error_handler
    def get_data(self) -> spec_types.SensorResult:
        return False


class LEDSocket(BaseDigitalSensor):
    ...


class Buzzer(BaseDigitalSensor):
    ...


class TempHumSensor(BaseDigitalSensor):
    @utils.sensor_error_handler
    def get_data(self) -> list[spec_types.Temperature, spec_types.Humidity]:
        return dht(self._port, 0)

    def on(self) -> spec_types.SensorResult:
        return False

    def off(self) -> spec_types.SensorResult:
        return False
