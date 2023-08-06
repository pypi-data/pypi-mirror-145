from wind_validation.metrics import Metrics
import numpy as np
import xarray as xr
from scipy.spatial import distance_matrix
import functools

from windkit.wind import wind_vectors
from ..constants import *
from .stats import bwc_ws_moment
from ..metrics import error


def _bins_distance_matrix(hist, dim=None):
    """Calculate the inter-bin distances appropriate dimension
    by default, the m/s distance in U,V-space is provided
    between each bin. dim="wsbin" gives the bin-distances along
    the wind speed axis and dim="sector" gives the bin-stances
    along the direction axis

    Parameters
    ----------
    hist : xarray.DataArray
        Wind histogram
    dim : str, optional
        dimension to calculate inter-bin distances, by default None,
        which gives the U,V-space distances in meters per second.

    Returns
    -------
    numpy.array
        Matrix of inter-bin distances
    """
    if dim == None:
        wspd, wdir = xr.broadcast(
            hist.coords[DIM_WIND_SPEED], hist.coords[DIM_WIND_DIRECTION]
        )
        u, v = wind_vectors(wspd, wdir)
        pos2d = np.stack([u.values.ravel(), v.values.ravel()], axis=1)
        return distance_matrix(pos2d, pos2d)
    elif dim == DIM_WIND_SPEED:
        pos2d = np.array([(v, 0.0) for v in hist.coords[DIM_WIND_SPEED]])
        return distance_matrix(pos2d, pos2d)
    elif dim == DIM_WIND_DIRECTION:
        pos2d = np.array([(v, 0) for v in hist.coords[DIM_WIND_DIRECTION]])
        mdist = distance_matrix(pos2d, pos2d)
        mdist[mdist > 180.0] -= 360.0
        mdist = np.abs(mdist)
        return mdist


def emd(hist1, hist2, dim=None):
    """Calculates the Earth Movers Distance (EMD) between
    two xarray.DataArrays's containing pywasp wind histogram's

    Parameters
    ----------
    hist1, hist2 : xarray.DataArray
        PyWAsP-formatted Wind Histograms
    dim : str or None, optional
        The dimension to calculate the EMD over,
        options are: "wsbin" and "sector" and None (the default),
        which calculates the 2D EMD in U,V-space
        If "sector" is chosen, the shortest
        circular distance between bins is used.

    Returns
    -------
    xarray.DataArray:
        Earth Movers Distance the histograms
    """
    try:
        import pyemd
    except (ModuleNotFoundError, ImportError):
        raise ModuleNotFoundError(
            "You need to install the 'pyemd' package to calculate the emd. This is most easily done with `conda install pyemd`."
        )

    def _emd(freq1, freq2, dist_matrix):
        return pyemd.emd(
            freq1.astype(np.float64).ravel(),
            freq2.astype(np.float64).ravel(),
            dist_matrix,
        )

    dist_matrix = _bins_distance_matrix(hist1, dim=dim)

    dims_agg_total = (DIM_WIND_SPEED, DIM_WIND_DIRECTION)

    if dim is None:
        dims_emd = (DIM_WIND_SPEED, DIM_WIND_DIRECTION)
        dims_agg_count = None
    elif dim == DIM_WIND_SPEED:
        dims_emd = (DIM_WIND_SPEED,)
        dims_agg_count = (DIM_WIND_DIRECTION,)
    elif dim == DIM_WIND_DIRECTION:
        dims_emd = (DIM_WIND_DIRECTION,)
        dims_agg_count = (DIM_WIND_SPEED,)

    if dims_agg_count is None:
        freq1 = hist1 / hist1.sum(dim=dims_agg_total)
        freq2 = hist2 / hist2.sum(dim=dims_agg_total)
    else:
        freq1 = hist1.sum(dim=dims_agg_count) / hist1.sum(dim=dims_agg_total)
        freq2 = hist2.sum(dim=dims_agg_count) / hist2.sum(dim=dims_agg_total)

    # TODO: this is related to hist/stats.py count_to_ws_freq_by_sector
    if "wsfreq" in freq1.data_vars:
        freq1 = freq1["wsfreq"]
        freq2 = freq2["wsfreq"]
    elif "wv_count" in freq1.data_vars:
        freq1 = freq1["wv_count"]
        freq2 = freq2["wv_count"]

    result = xr.apply_ufunc(
        _emd,
        freq1,
        freq2,
        dist_matrix,
        input_core_dims=[dims_emd, dims_emd, ["_D1", "_D2"]],
        output_core_dims=[[]],
        dask="allowed",
        vectorize=True,
    )
    result.name = "euclidian_emd"
    return result


def euclidian_emd(hist1, hist2):
    """Wrapper for :py:func:`emd`

    Calculates the EMD over the dimension wind speed with keyword argument `dim='wsbin'`.
    """
    return emd(hist1, hist2, dim=DIM_WIND_SPEED)


def emd_2d(hist1, hist2):
    """Wrapper for :py:func:`emd`

    Calculates the EMD over the dimension wind speed with keyword argument `dim=None`.
    """
    return emd(hist1, hist2, dim=None)


def circular_emd(hist1, hist2):
    """Wrapper for :py:func:`emd`

    Calculates the EMD over the dimension wind speed with keyword argument `dim='sector'`
    """
    return emd(hist1, hist2, dim=DIM_WIND_DIRECTION)


class HistogramMetrics(Metrics):
    """Stores specific histogram metrics function mappings"""

    SUITE_MAPPER = {
        "none": [],
        "basic": [
            ((VAR_WIND_SPEED, "mean"), "me"),
            ((VAR_WIND_SPEED, "mean"), "mae"),
            ((VAR_WIND_SPEED, "mean"), "mpe"),
            ((VAR_WIND_SPEED, "mean"), "mape"),
            ((VAR_POWER_DENS, "mean"), "me"),
            ((VAR_POWER_DENS, "mean"), "mae"),
            ((VAR_POWER_DENS, "mean"), "mpe"),
            ((VAR_POWER_DENS, "mean"), "mape"),
            ((VAR_AIR_DENS, "mean"), "mpe"),
        ],
        "all": [
            ((VAR_WIND_SPEED, "mean"), "me"),
            ((VAR_WIND_SPEED, "mean"), "mae"),
            ((VAR_WIND_SPEED, "mean"), "mpe"),
            ((VAR_WIND_SPEED, "mean"), "mape"),
            ((VAR_POWER_DENS, "mean"), "me"),
            ((VAR_POWER_DENS, "mean"), "mae"),
            ((VAR_POWER_DENS, "mean"), "mpe"),
            ((VAR_POWER_DENS, "mean"), "mape"),
            ((VAR_AIR_DENS, "mean"), "mpe"),
            (VAR_WV_COUNT, "emd"),
            (VAR_WV_COUNT, "eemd"),
            (VAR_WV_COUNT, "cemd"),
        ],
    }

    FUNC_MAPPER = {
        "me": functools.partial(error, percent=False, abs=False),
        "mpe": functools.partial(error, percent=True, abs=False),
        "mae": functools.partial(error, percent=False, abs=True),
        "mape": functools.partial(error, percent=True, abs=True),
        "eemd": euclidian_emd,
        "cemd": circular_emd,
        "emd": emd_2d,
    }

    @classmethod
    def _get_suite_mapper(self) -> dict:
        return self.SUITE_MAPPER

    @classmethod
    def _get_func_mapper(self) -> dict:
        return self.FUNC_MAPPER
