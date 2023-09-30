import abc
import asyncio
from typing import Any, Type, Unpack

from pydantic import BaseModel

from . import analog_sensors, base, consts, digital_sensors, runner_tasks, schemas


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
        consts.Sensor.buzzer: digital_sensors.Buzzer,
    }
    _available_tasks: tuple[Type[runner_tasks.AbstractTask], ...] = (
        runner_tasks.LEDSocketTask,
        runner_tasks.BuzzerTask,
    )
    _run_tasks: dict[str, asyncio.Task] = {}

    def __init__(self, pin_data: dict[consts.Sensor, int]) -> None:
        super().__init__(pin_data)
        self._tasks: dict[str, runner_tasks.AbstractTask] = {
            task.__name__: task(self._sensors) for task in self._available_tasks
        }

    def execute(self, msg: schemas.RunnerData) -> Any:
        task_name: str = msg.task
        action: consts.TaskAction = msg.action

        if not (runner_task := self._tasks.get(task_name)):
            return None

        if (
            (in_process_async_task := self._run_tasks.get(task_name))
            and not in_process_async_task.done()
            and action == action.OFF
        ):
            in_process_async_task.cancel()
            del self._run_tasks[task_name]
        else:
            async_task: asyncio.Task = asyncio.create_task(runner_task.execute(action))
            self._run_tasks[task_name] = async_task
