import warnings
import xarray as xr
import numpy as np
from typing import Union

from wind_validation.ts.stats import TimeSeriesStats
from wind_validation.hist.stats import HistogramStats
from wind_validation.weib.stats import WeibStats
from wind_validation.ts.metrics import TimeSeriesMetrics
from wind_validation.hist.metrics import HistogramMetrics
from wind_validation.weib.metrics import WeibMetrics
from wind_validation.constants import (
    DIM_TIME,
    VAR_POWER_DENS,
    VAR_WIND_SPEED,
    VAR_AIR_DENS,
    VAR_WD_FREQ,
    VAR_WV_COUNT,
)

from windkit.time_series_wind_climate import ts_validate
from windkit.binned_wind_climate import bwc_validate, count_to_ws_freq_by_sector


def wwc_validate(wwc):
    """This one is required because windkit has only decorator
    for validating the wwc and here a simple function is needed
    that you can call on observations and model datasets. The checks
    are just copied from the decorator function in windkit:

    from windkit.weibull_wind_climate import wwc_validate

    Parameters
    ----------
    wwc : [type]
        [description]

    Raises
    ------
    ValueError
        [description]
    ValueError
        [description]
    """

    if not all(v in wwc.data_vars for v in ["A", "k", "wdfreq"]):
        raise ValueError("wwc dataset should contain A, k and wdfreq!")
    if "sector" not in wwc["wdfreq"].dims:
        raise ValueError("Expected sector in wdfreq dims!")


def bwc_validate_mod(bwc: xr.Dataset):
    """Convert binned wind climate format from wind vector count
    to ws freq by sector before validation and validates afterwards

    Parameters
    ----------
    bwc : [xr.Dataset]
        [bwc xarray dataset to validate]
    """
    if "wsfreq" in bwc.data_vars:
        return

    bwc = count_to_ws_freq_by_sector(bwc["wv_count"])

    bwc_validate(bwc)


"""all stats & metrics obj are created beforehand
in this way we can select whichever fits the need
depending on the type of data during the validation"""
STATS = {
    "ts": TimeSeriesStats(),
    "hist": HistogramStats(),
    "weib": WeibStats(),
}
METRICS = {
    "ts": TimeSeriesMetrics(),
    "hist": HistogramMetrics(),
    "weib": WeibMetrics(),
}


def validate(
    obs: xr.Dataset,
    mod: xr.Dataset,
    dtype: str = None,
    stats: str = "basic",
    metrics: str = "basic",
    **kwargs,
) -> xr.Dataset:
    """Function to validate modelled wind data against observations.

    The validation calculates "stats" and "metrics" and outputs them as the results.

    Stats are calculated on the modelled and observed data seperately. An example is the
    mean of the wind speed or the variance of the wind direction.

    Metrics are measures that are calculated between the observed and modelled wind data.
    This can be for example the pearson correlation coefficient, the mean absolute error,
    and the mean wind direction error.

    The data variables in the output xr.dataset are named with the convention
    `obs_VARIABLE_STATISTIC` for observations and `mod_VARIABLE_STATISTIC` for modelled
    data. The metrics are labelled as `VARIABLE_METRIC`.

    Parameters
    ----------

    obs, mod: xarray.Dataset
        Observed and modelled data to validate.

    dtype : str, optional
        Explicitely state the data format. Possible options: ts, hist, weib. By default None.

    stats: str or list, optional

        Stats to be calculated.

        str: if a string is used, it should the name of a suite of stats.
            the available suites and their included stats are:

            "basic":
                - wind speed mean
                - wind speed standard deviation
                - wind direction circular mean
                - wind direction circular standard deviation
                - etc.

            "all":
                - every available stat (see documentation for stats)

        If a list is used, it must contain tuples in a form of: ('variable', 'stat').
        For example: [('wind_speed', 'mean'), ('power_density', 'mean'), ...]. All
        available option can be found under the respective format folder in the stats.py file.

    metrics: str or list, optional

        Metrics to be calculated.

        metrics suites are:

            "basic":
                - wind speed pearson correlation coefficient
                - wind speed spearman correlation coefficient
                - wind speed coefficient of determination
                - wind speed mean error
                - wind speed root-mean-square error
                - wind speed mean-absolute error
                - wind speed mean-absolute-percentage error
                - wind direction circular mean error
                - wind direction circular mean-absolute error

            "all":
                - every available metric (see documentation for metrics)

        If a list is used, it must contain tuples in a form of: (('variable','stat'), 'metric').
        For example: [(('wind_speed', 'mean'), 'me'), (('power_density', 'mean'), 'mpe')]. All
        available option can be found under the respective format folder in the metrics.py file.

    dim: str, optional
        Dimension to calculate timeseries stats and metrics along. By default dim is "time".
        It's important to note that this is only applicable to timeseries data.

    by: numpy.array or xarray.DataArray, optional
        Optional grouper-array to calculate stats and metrics in
        groups based on the unique values in the array.

    Returns
    -------
    xarray.Dataset
        Validation results of stats and metrics.

    Raises
    ------
    ValueError
        Raises this in case the automatic inference of data format from "hist", "ts", "weib"
        is unsuccessful, a user should provide it manually in this case.

    Examples
    --------
    >>> results = validate(obs, mod, stats='all', metrics='all')

    """
    dtype = _infer_data_type(obs, mod) if dtype is None else dtype

    if dtype not in STATS.keys():
        raise ValueError(
            f"Failed to infer known format for both datasets. "
            f"Known types: {list(STATS.keys())}. "
            f"While provided one is: {str(dtype)}."
        )

    stats = STATS[dtype]._prepare_stats_from_user_input(stats)
    metrics = METRICS[dtype]._prepare_metrics_from_user_input(metrics)

    result = {}
    datasets = [("obs", obs), ("mod", mod)]
    """TODO: This is ugly, but for now it will do the job.
             Time series validation is handled a bit differentely."""
    if dtype == "ts":
        kwargs["dim"] = DIM_TIME
        for name, dataset in datasets:
            # add power density variable, this can always be calculated based on the
            # wind speed. The air density is optionally used if available.
            dataset = _add_power_density(dataset, dtype)
            for var, stat, func in stats:
                label = f"{name}_{var}_{stat}"
                da = dataset[var].copy()
                da.name = label
                result[label] = _calc(func, da, **kwargs)

        for var, metric, func in metrics:
            label = f"{var}_{metric}"
            da_obs, da_mod = obs[var].copy(), mod[var].copy()
            da_obs.name, da_mod.name = label, label
            result[label] = _calc(func, da_obs, da_mod, **kwargs)
    else:
        for name, dataarr in datasets:
            dataarr = _add_power_density(dataarr, dtype)
            for var, stat, func in stats:
                label = f"{name}_{var}_{stat}"
                da = dataarr.copy()
                da_out = _calc(func, da, **kwargs)
                da_out.name = label
                result[label] = da_out

        for var, metric, func in metrics:
            label = f"{var}_{metric}"
            if isinstance(var, tuple):
                # calculates metric on specific stat
                label = f"{var[0]}_{metric}"
                stat_var = "_".join([*var])
                obs_label = "_".join(["obs", stat_var])
                mod_label = "_".join(["mod", stat_var])
                try:
                    da_obs, da_mod = result[obs_label], result[mod_label]
                except KeyError:
                    warnings.warn(
                        f"The required stat {stat_var} is not present"
                        f" to calculate {'_'.join(var)}_{metric} metric."
                    )
                    continue
            elif isinstance(var, str):
                # calculates metric on raw dataset
                label = f"{var}_{metric}"
                da_obs, da_mod = obs.copy(), mod.copy()
            else:  # pragma: no cover
                raise RuntimeError("Unknown internal type of metric variable")
            da_out = _calc(func, da_obs, da_mod, **kwargs)
            da_out.name = label
            result[label] = da_out

    validation_result = xr.merge(result.values(), compat="override")
    validation_result = validation_result.assign_attrs(mod.attrs)
    validation_result = validation_result.assign_attrs(obs.attrs)
    validation_result = validation_result.assign_attrs(
        {"format": _get_full_name_of_data_format(dtype)}
    )
    return validation_result


def _calc(func, *args, **kwargs):
    if kwargs.get("by", None) is None:
        return func(*args, **kwargs)

    result = []
    by = kwargs.get("by")
    del kwargs["by"]
    for cat in np.unique(by):
        if np.isnan(cat):
            continue
        args_cat = tuple(arg.where(by == cat) for arg in args)
        da_out_cat = func(*args_cat, **kwargs)
        da_out_cat = da_out_cat.expand_dims(**{by.name: [cat]})
        result.append(da_out_cat)
    return xr.merge(result)


def _get_full_name_of_data_format(dtype):
    if dtype == "hist":
        return "histogram"
    if dtype == "ts":
        return "timeseries"
    if dtype == "weib":
        return "weibull"
    return ""  # pragma: no cover


def _infer_data_type(obs: xr.Dataset, mod: xr.Dataset) -> Union[str, None]:
    """Function tries to infer what data format of both observation and model data.

    Parameters
    ----------
    obs : xarray.Dataset
        Observations dataset.
    mod : xarray.Dataset
        Model dataset

    Returns
    -------
    Union[str, None]
        If data format is detected returns the string with the format,
        otherwise just return None.
    """
    # The sequence of validation is meant to be maintained as it is now
    # because weibull is the most mainstream format of the data
    try:
        if "sector" not in obs.dims or "sector" not in mod.dims:
            raise ValueError
        wwc_validate(obs)
        wwc_validate(mod)
        return "weib"
    except ValueError:
        pass

    try:
        if "sector" not in obs.dims or "sector" not in mod.dims:
            raise ValueError
        bwc_validate_mod(obs)
        bwc_validate_mod(mod)
        return "hist"
    except ValueError:
        pass
    except KeyError:
        pass

    try:
        ts_validate(obs)
        ts_validate(mod)
        return "ts"
    except ValueError:
        pass

    return None


def detect_spatial_dims(ds):
    if VAR_WIND_SPEED in ds.data_vars:
        air_density_dims = ds[VAR_WIND_SPEED]
    elif VAR_WD_FREQ in ds.data_vars:
        air_density_dims = ds[VAR_WD_FREQ].isel(sector=0)
    elif VAR_WV_COUNT in ds.data_vars:
        air_density_dims = ds[VAR_WV_COUNT].isel(sector=0, wsbin=0)
    else:
        raise ValueError("Could not detect structure for adding air density!")
    return air_density_dims


def _add_power_density(ds, dtype):
    try:
        _ = ds[VAR_AIR_DENS]
    except KeyError:
        air_density_dims = detect_spatial_dims(ds)
        ds[VAR_AIR_DENS] = xr.full_like(air_density_dims, 1.225)
    if dtype == "ts":
        ds[VAR_POWER_DENS] = 0.5 * ds[VAR_AIR_DENS] * ds[VAR_WIND_SPEED] ** 3
    return ds
