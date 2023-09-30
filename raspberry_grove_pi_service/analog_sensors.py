from grovepi import analogRead

from . import base, spec_types, utils


class BaseAnalogSensor(base.AbstractSensor):
    @utils.sensor_error_handler
    def get_data(self) -> spec_types.SensorResult:
        return analogRead(self._port)

    def on(self) -> None:
        ...

    def off(self) -> None:
        ...


class LightSensor(BaseAnalogSensor):
    ...


class SoundSensor(BaseAnalogSensor):
    ...
