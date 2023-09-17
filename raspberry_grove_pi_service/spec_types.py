from typing import ParamSpec, TypeVar

SensorParam = ParamSpec("SensorParam")
SensorResult = TypeVar("SensorResult", dict, list, bool)
Temperature = TypeVar("Temperature", bound=int)
Humidity = TypeVar("Humidity", bound=int)
