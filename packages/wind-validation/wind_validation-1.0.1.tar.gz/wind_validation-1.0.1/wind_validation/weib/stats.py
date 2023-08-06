from wind_validation.stats import Stats
import numpy as np
import xarray as xr
from ..constants import *
from windkit.wind_climate import power_density
from windkit.wind_climate import mean_windspeed
from wind_validation.constants import VAR_AIR_DENS


def weib_air_density(wwc):
    return wwc[VAR_AIR_DENS]


def weib_power_density(wwc):
    return power_density(wwc, air_density=wwc[VAR_AIR_DENS])


class WeibStats(Stats):
    """Stores specific timeseries metrics function mappings

    There is two suits of metrics available, `basic` and `all`.
    The list of metrics calculated for these are listed below.
    One can also pick any of the tuples below to calculate only
    that metric.

    "basic": [
        ("wind_speed", "mean"),
        ("power_density", "mean"),
        ("air_density", "mean"),
    ]

    "all": [
        ("wind_speed", "mean"),
        ("power_density", "mean"),
        ("air_density", "mean"),
    ]

    """

    FUNC_MAPPER = {
        (VAR_POWER_DENS, "mean"): weib_power_density,
        (VAR_WIND_SPEED, "mean"): mean_windspeed,
        (VAR_AIR_DENS, "mean"): weib_air_density,
    }

    SUITE_MAPPER = {
        "none": [],
        "basic": [
            (VAR_WIND_SPEED, "mean"),
            (VAR_POWER_DENS, "mean"),
            (VAR_AIR_DENS, "mean"),
        ],
        "all": [
            (VAR_WIND_SPEED, "mean"),
            (VAR_POWER_DENS, "mean"),
            (VAR_AIR_DENS, "mean"),
        ],
    }

    @classmethod
    def _get_suite_mapper(self) -> dict:
        return self.SUITE_MAPPER

    @classmethod
    def _get_func_mapper(self) -> dict:
        return self.FUNC_MAPPER
