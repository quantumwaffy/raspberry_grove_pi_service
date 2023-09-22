from pydantic import BaseModel

from . import consts


class SensorData(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    sound: int | None = None
    light: int | None = None


class RunnerData(BaseModel):
    handler: str
    action: consts.TaskAction
