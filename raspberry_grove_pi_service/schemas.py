from pydantic import BaseModel


class SensorData(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    sound: int | None = None
    light: int | None = None
