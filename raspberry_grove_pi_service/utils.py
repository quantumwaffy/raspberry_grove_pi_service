import functools
import logging
from typing import Callable, Concatenate, Self

from . import spec_types

logger: logging.Logger = logging.getLogger(__name__)


def sensor_error_handler(
    func: Callable[Concatenate[Self, spec_types.SensorParam], spec_types.SensorResult]
) -> Callable[[Self, spec_types.SensorParam], spec_types.SensorResult]:
    @functools.wraps(func)
    def wrapper(
        self: Self, *args: spec_types.SensorParam.args, **kwargs: spec_types.SensorParam.kwargs
    ) -> spec_types.SensorResult:
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error {e}")
            return False

    return wrapper
