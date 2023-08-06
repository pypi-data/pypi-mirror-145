from wind_validation.stats import Stats
import numpy as np
import xarray as xr
from wind_validation.constants import *
from windkit.binned_wind_climate import (
    bwc_mean_windspeed,
    bwc_ws_moment,
    bwc_power_density,
)


def bwc_air_density(bwc):
    return bwc[VAR_AIR_DENS]


def bwc_power_density(bwc, bysector=False):
    """Calculate the power density

    Calculates the power density using a standard atmosphere air density of 1.225 kg m-3

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xr.Dataset object

    bysector: bool
        Return sectorwise mean wind speed if True
    """
    return 1 / 2 * bwc[VAR_AIR_DENS] * bwc_ws_moment(bwc, 3.0, bysector)


class HistogramStats(Stats):
    """Stores specific histogram stats function mappings"""

    FUNC_MAPPER = {
        (VAR_WIND_SPEED, "mean"): bwc_mean_windspeed,
        (VAR_POWER_DENS, "mean"): bwc_power_density,
        (VAR_AIR_DENS, "mean"): bwc_air_density,
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
