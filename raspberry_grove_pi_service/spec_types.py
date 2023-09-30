from typing import ParamSpec, TypeVar

SensorParam = ParamSpec("SensorParam")
SensorResult = TypeVar("SensorResult", dict, list, bool, None)
