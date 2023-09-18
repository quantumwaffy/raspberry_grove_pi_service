from pydantic import BaseModel


class SensorData(BaseModel):
    temperature: int | None = None
    humidity: int | None = None
    sound: int | None = None
    light: int | None = None
