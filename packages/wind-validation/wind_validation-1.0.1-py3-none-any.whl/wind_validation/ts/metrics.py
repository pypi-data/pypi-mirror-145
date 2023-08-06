import numpy as np
import xarray as xr
import xskillscore as xs
import functools
from ..constants import *

from windkit.wind import wind_direction_difference
from wind_validation.metrics import Metrics


def pearson_r(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.pearson_r`"""
    return xs.pearson_r(*args, **kwargs)


def spearman_r(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.spearman_r`"""
    return xs.spearman_r(*args, **kwargs)


def pearson_r_p_value(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.pearson_r_p_value`"""
    return xs.pearson_r_p_value(*args, **kwargs)


def pearson_r_eff_p_value(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.pearson_r_eff_p_value`"""
    return xs.pearson_r_eff_p_value(*args, **kwargs)


def spearman_r_p_value(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.spearman_r_p_value`"""
    return xs.spearman_r_p_value(*args, **kwargs)


def spearman_r_eff_p_value(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.spearman_r_eff_p_value`"""
    return xs.spearman_r_eff_p_value(*args, **kwargs)


def effective_sample_size(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.effective_sample_size`"""
    return xs.effective_sample_size(*args, **kwargs)


def r2(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.r2`"""
    return xs.r2(*args, **kwargs)


def rmse(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.rmse`"""
    return xs.rmse(*args, **kwargs)


def mse(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.mse`"""
    return xs.mse(*args, **kwargs)


def median_absolute_error(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.median_absolute_error`"""
    return xs.median_absolute_error(*args, **kwargs)


def smape(*args, **kwargs):
    """Wrapper for :py:func:`xskillscore.smape`"""
    return xs.smape(*args, **kwargs)


def me(obs, mod, dim=None, percent=False, abs=False):
    """Mean Error."""
    if dim is None:
        dim = DIM_TIME

    def _me(obs, mod, percent, abs):
        if percent:
            if abs:
                return 100 * np.abs(np.nanmean(mod - obs)) / np.nanmean(obs)
            else:
                return 100 * np.nanmean(mod - obs) / np.nanmean(obs)
        else:
            if abs:
                return np.abs(np.nanmean(mod - obs))
            else:
                return np.nanmean(mod - obs)

    return xr.apply_ufunc(
        _me,
        obs,
        mod,
        input_core_dims=[[dim], [dim]],
        vectorize=True,
        kwargs={"percent": percent, "abs": abs},
    )


def cme(obs, mod, dim=None):
    """Circular Mean Error."""

    if dim is None:
        dim = DIM_TIME

    diff = wind_direction_difference(obs, mod)

    return diff.mean(dim=dim)


def cmae(obs, mod, dim=None):
    """:py:func:`xskillscore.pearson_r_eff_p_value`"""

    if dim is None:
        dim = DIM_TIME

    diff = wind_direction_difference(obs, mod)

    return np.abs(diff).mean(dim=dim)


def crmse(obs, mod, dim=None):
    """Circular Root Mean Squared Error."""

    if dim is None:
        dim = DIM_TIME

    diff = wind_direction_difference(obs, mod)

    return np.sqrt((diff**2).mean(dim=dim))


def circular_median_absolute_error(obs, mod, dim=None):
    """Circular Median Absolute Error."""

    if dim is None:
        dim = DIM_TIME

    diff = wind_direction_difference(obs, mod)

    return np.abs(diff).median(dim=dim)


class TimeSeriesMetrics(Metrics):
    """Stores specific timeseries metrics function mappings

    There is two suits of metrics available, `basic` and `all`.
    The list of metrics calculated for these are listed below.
    One can also pick any of the tuples below to calculate only
    that metric.


    "basic":

    * ("wind_speed", "pearson_r")
    * ("wind_speed", "spearman_r")
    * ("wind_speed", "r2")
    * ("wind_speed", "me")
    * ("wind_speed", "mpe")
    * ("wind_speed", "rmse")
    * ("wind_speed", "mae")
    * ("wind_speed", "mape")
    * ("wind_direction", "cme")
    * ("wind_direction", "cmae")
    * ("power_density", "me")
    * ("power_density", "mpe")
    * ("power_density", "mae")
    * ("power_density", "mape")
    * ("air_density", "mpe")


    "all", all of the "basic" metrics but also including:

    * ("wind_speed", "pearson_r_p_value")
    * ("wind_speed", "pearson_r_eff_p_value")
    * ("wind_speed", "spearman_r_p_value")
    * ("wind_speed", "spearman_r_eff_p_value")
    * ("wind_speed", "effective_sample_size")
    * ("wind_speed", "mse")
    * ("wind_speed", "median_absolute_error")
    * ("wind_speed", "smape")
    * ("wind_direction", "crmse")
    * ("wind_direction", "circular_median_absolute_error")

    """

    SUITE_MAPPER = {
        "none": [],
        "basic": [
            (VAR_WIND_SPEED, "pearson_r"),
            (VAR_WIND_SPEED, "spearman_r"),
            (VAR_WIND_SPEED, "r2"),
            (VAR_WIND_SPEED, "me"),
            (VAR_WIND_SPEED, "mpe"),
            (VAR_WIND_SPEED, "rmse"),
            (VAR_WIND_SPEED, "mae"),
            (VAR_WIND_SPEED, "mape"),
            (VAR_WIND_DIRECTION, "cme"),
            (VAR_WIND_DIRECTION, "cmae"),
            (VAR_POWER_DENS, "me"),
            (VAR_POWER_DENS, "mpe"),
            (VAR_POWER_DENS, "mae"),
            (VAR_POWER_DENS, "mape"),
            (VAR_AIR_DENS, "mpe"),
        ],
        "all": [
            (VAR_WIND_SPEED, "pearson_r"),
            (VAR_WIND_SPEED, "pearson_r_p_value"),
            (VAR_WIND_SPEED, "pearson_r_eff_p_value"),
            (VAR_WIND_SPEED, "spearman_r_p_value"),
            (VAR_WIND_SPEED, "spearman_r_eff_p_value"),
            (VAR_WIND_SPEED, "spearman_r"),
            (VAR_WIND_SPEED, "effective_sample_size"),
            (VAR_WIND_SPEED, "r2"),
            (VAR_WIND_SPEED, "me"),
            (VAR_WIND_SPEED, "mpe"),
            (VAR_WIND_SPEED, "rmse"),
            (VAR_WIND_SPEED, "mse"),
            (VAR_WIND_SPEED, "mae"),
            (VAR_WIND_SPEED, "median_absolute_error"),
            (VAR_WIND_SPEED, "smape"),
            (VAR_WIND_SPEED, "mape"),
            (VAR_POWER_DENS, "me"),
            (VAR_POWER_DENS, "mpe"),
            (VAR_POWER_DENS, "mae"),
            (VAR_POWER_DENS, "mape"),
            (VAR_AIR_DENS, "mpe"),
            (VAR_WIND_DIRECTION, "cme"),
            (VAR_WIND_DIRECTION, "cmae"),
            (VAR_WIND_DIRECTION, "crmse"),
            (VAR_WIND_DIRECTION, "circular_median_absolute_error"),
        ],
    }

    FUNC_MAPPER = {
        "mpe": functools.partial(me, percent=True),
        "pearson_r": functools.partial(pearson_r, skipna=True),
        "spearman_r": functools.partial(spearman_r, skipna=True),
        "pearson_r_p_value": functools.partial(pearson_r_p_value, skipna=True),
        "pearson_r_eff_p_value": functools.partial(pearson_r_eff_p_value, skipna=True),
        "spearman_r_p_value": functools.partial(spearman_r_p_value, skipna=True),
        "spearman_r_eff_p_value": functools.partial(
            spearman_r_eff_p_value, skipna=True
        ),
        "effective_sample_size": functools.partial(effective_sample_size, skipna=True),
        "r2": functools.partial(r2, skipna=True),
        "me": me,
        "rmse": functools.partial(rmse, skipna=True),
        "mse": functools.partial(mse, skipna=True),
        "mae": functools.partial(me, abs=True),
        "median_absolute_error": functools.partial(median_absolute_error, skipna=True),
        "smape": functools.partial(smape, skipna=True),
        "mape": functools.partial(me, percent=True, abs=True),
        "cme": cme,
        "cmae": cmae,
        "crmse": crmse,
        "circular_median_absolute_error": circular_median_absolute_error,
    }

    @classmethod
    def _get_suite_mapper(cls) -> dict:
        return cls.SUITE_MAPPER

    @classmethod
    def _get_func_mapper(cls) -> dict:
        return cls.FUNC_MAPPER
