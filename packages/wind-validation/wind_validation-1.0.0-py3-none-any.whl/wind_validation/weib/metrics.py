from wind_validation.metrics import Metrics
import numpy as np
import functools
from ..constants import *
from ..metrics import error, squared_error


class WeibMetrics(Metrics):
    """Stores specific Webull metrics function mappings

    There is two suits of metrics available, `basic` and `all`.
    The list of metrics calculated for these are listed below.
    One can also pick any of the tuples below to calculate only
    that metric.

    "basic": [
        (("wind_speed", "mean"), "mpe"),
        (("power_density", "mean"), "mpe"),
        (("wind_speed", "mean"), "mae"),
        (("power_density", "mean"), "mae"),
        (("wind_speed", "mean"), "me"),
        (("power_density", "mean"), "me"),
        (("wind_speed", "mean"), "mape"),
        (("power_density", "mean"), "mape"),
        (("air_density", "mean"), "mpe"),
    ]

    "all": [
        (("wind_speed", "mean"), "mape"),
        (("power_density", "mean"), "mape"),
        (("wind_speed", "mean"), "mpe"),
        (("power_density", "mean"), "mpe"),
        (("wind_speed", "mean"), "mae"),
        (("power_density", "mean"), "mae"),
        (("wind_speed", "mean"), "me"),
        (("power_density", "mean"), "me"),
        (("wind_speed", "mean"), "sqep"),
        (("power_density", "mean"), "sqep"),
        (("wind_speed", "mean"), "sqe"),
        (("power_density", "mean"), "sqe"),
        (("air_density", "mean"), "mpe"),
    ]

    """

    SUITE_MAPPER = {
        "none": [],
        "basic": [
            ((VAR_WIND_SPEED, "mean"), "mpe"),
            ((VAR_POWER_DENS, "mean"), "mpe"),
            ((VAR_WIND_SPEED, "mean"), "mae"),
            ((VAR_POWER_DENS, "mean"), "mae"),
            ((VAR_WIND_SPEED, "mean"), "me"),
            ((VAR_POWER_DENS, "mean"), "me"),
            ((VAR_WIND_SPEED, "mean"), "mape"),
            ((VAR_POWER_DENS, "mean"), "mape"),
            ((VAR_AIR_DENS, "mean"), "mpe"),
        ],
        "all": [
            ((VAR_WIND_SPEED, "mean"), "mape"),
            ((VAR_POWER_DENS, "mean"), "mape"),
            ((VAR_WIND_SPEED, "mean"), "mpe"),
            ((VAR_POWER_DENS, "mean"), "mpe"),
            ((VAR_WIND_SPEED, "mean"), "mae"),
            ((VAR_POWER_DENS, "mean"), "mae"),
            ((VAR_WIND_SPEED, "mean"), "me"),
            ((VAR_POWER_DENS, "mean"), "me"),
            ((VAR_WIND_SPEED, "mean"), "sqep"),
            ((VAR_POWER_DENS, "mean"), "sqep"),
            ((VAR_WIND_SPEED, "mean"), "sqe"),
            ((VAR_POWER_DENS, "mean"), "sqe"),
            ((VAR_AIR_DENS, "mean"), "mpe"),
        ],
    }

    FUNC_MAPPER = {
        "me": functools.partial(error, percent=False, abs=False),
        "mae": functools.partial(error, percent=False, abs=True),
        "mape": functools.partial(error, percent=True, abs=True),
        "mpe": functools.partial(error, percent=True, abs=False),
        "sqe": functools.partial(squared_error, percent=False),
        "sqep": functools.partial(squared_error, percent=True),
    }

    @classmethod
    def _get_suite_mapper(self) -> dict:
        return self.SUITE_MAPPER

    @classmethod
    def _get_func_mapper(self) -> dict:
        return self.FUNC_MAPPER
