from grovepi import analogRead

from . import spec_types, utils


class BaseAnalogSensor:
    def __init__(self, port: int) -> None:
        self._port: int = port

    @utils.sensor_error_handler
    def get_data(self) -> spec_types.SensorResult:
        return analogRead(self._port)


class LightSensor(BaseAnalogSensor):
    ...


class SoundSensor(BaseAnalogSensor):
    ...
