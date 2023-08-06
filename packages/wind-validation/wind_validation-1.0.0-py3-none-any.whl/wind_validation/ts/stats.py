import numpy as np
import xarray as xr

import scipy.stats as sp_stats
from ..constants import *

from wind_validation.stats import Stats


def minimum(da, **kwargs):
    """Minimum."""
    return da.min(**kwargs)


def maximum(da, **kwargs):
    """Maximum."""
    return da.max(**kwargs)


def mean(da, **kwargs):
    """Mean."""
    return da.mean(**kwargs)


def median(da, **kwargs):
    """Median."""
    return da.median(**kwargs)


def std(da, **kwargs):
    """Standard Deviation."""
    return da.std(**kwargs)


def variance(da, **kwargs):
    """Variance."""
    return da.var(**kwargs)


def circmean(da, dim=None, low=0.0, high=360.0, nan_policy="omit", **kwargs):
    """Circular Mean."""

    if dim is None:
        dim = DIM_TIME

    def _circmean(x, **kwargs):
        return sp_stats.circmean(x, **kwargs)

    kwargs = {
        "low": low,
        "high": high,
        "nan_policy": nan_policy,
        **kwargs,
    }

    return xr.apply_ufunc(
        _circmean, da, input_core_dims=[[DIM_TIME]], vectorize=True, kwargs=kwargs
    )


def circstd(da, dim=None, low=0.0, high=360.0, nan_policy="omit", **kwargs):
    """Circular Standard Deviation."""

    if dim is None:
        dim = DIM_TIME

    def _circstd(x, **kwargs):
        return sp_stats.circstd(x, **kwargs)

    kwargs = {
        "low": low,
        "high": high,
        "nan_policy": nan_policy,
        **kwargs,
    }

    return xr.apply_ufunc(
        _circstd, da, input_core_dims=[[DIM_TIME]], vectorize=True, kwargs=kwargs
    )


def circvar(da, dim=None, low=0.0, high=360.0, nan_policy="omit", **kwargs):
    """Circular Variance."""

    if dim is None:
        dim = DIM_TIME

    def _circvar(x, **kwargs):
        return sp_stats.circvar(x, **kwargs)

    kwargs = {
        "low": low,
        "high": high,
        "nan_policy": nan_policy,
        **kwargs,
    }

    return xr.apply_ufunc(
        _circvar, da, input_core_dims=[[DIM_TIME]], vectorize=True, kwargs=kwargs
    )


class TimeSeriesStats(Stats):
    """Stores specific timeseries statistics function mappings

    There is two suits of statistics available, `basic` and `all`.
    The list of statistics calculated for these are listed below.
    One can also pick any of the tuples below to calculate only
    that metric.

    "basic": [
        ("wind_speed", "mean"),
        ("wind_speed", "std"),
        ("wind_direction", "cmean"),
        ("wind_direction", "cstd"),
        ("power_density", "mean"),
        ("air_density", "mean"),
    ]

    "all": [
        ("wind_speed", "min"),
        ("wind_speed", "max"),
        ("wind_speed", "mean"),
        ("wind_speed", "median"),
        ("wind_speed", "std"),
        ("wind_speed", "var"),
        ("wind_direction", "cmean"),
        ("wind_direction", "cstd"),
        ("wind_direction", "cvar"),
        ("power_density", "mean"),
        ("air_density", "mean"),
    ]

    """

    FUNC_MAPPER = {
        "min": minimum,
        "max": maximum,
        "mean": mean,
        "median": median,
        "std": std,
        "var": variance,
        "cmean": circmean,
        "cstd": circstd,
        "cvar": circvar,
    }

    SUITE_MAPPER = {
        "none": [],
        "basic": [
            (VAR_WIND_SPEED, "mean"),
            (VAR_WIND_SPEED, "std"),
            (VAR_WIND_DIRECTION, "cmean"),
            (VAR_WIND_DIRECTION, "cstd"),
            (VAR_POWER_DENS, "mean"),
            (VAR_AIR_DENS, "mean"),
        ],
        "all": [
            (VAR_WIND_SPEED, "min"),
            (VAR_WIND_SPEED, "max"),
            (VAR_WIND_SPEED, "mean"),
            (VAR_WIND_SPEED, "median"),
            (VAR_WIND_SPEED, "std"),
            (VAR_WIND_SPEED, "var"),
            (VAR_WIND_DIRECTION, "cmean"),
            (VAR_WIND_DIRECTION, "cstd"),
            (VAR_WIND_DIRECTION, "cvar"),
            (VAR_POWER_DENS, "mean"),
            (VAR_AIR_DENS, "mean"),
        ],
    }

    def _get_suite_mapper(self) -> dict:
        return self.SUITE_MAPPER

    def _get_func_mapper(self) -> dict:
        return self.FUNC_MAPPER
