from windkit.spatial import (
    is_point,
    add_crs,
    reproject,
    to_point,
    get_crs,
    to_stacked_point,
)
import xarray as xr
import pandas as pd
import math

# this function is in a new branch from windkit  that has not been merged yet
# can be changed to this once that is done:
# from windkit.spatial import get_nearest_points
def get_nearest_points(ds: xr.Dataset, ds_target: xr.Dataset):
    """Get nearest points from x,y,z point dataset

    Parameters
    ----------
    ds : xarray.Dataset
        Input dataset of which we want to select nearest points
    ds_target : xarray.Dataset
        Target dataset of the points we want to obtain from the input

    Returns
    -------
    xr.Dataset
        ds but with the nearest points provided in ds_target (i.e. ds will have the shape of ds_target)
    """
    if not is_point(ds):
        ds = to_point(ds)

    if not is_point(ds_target):
        ds_target = to_point(ds_target)

    if get_crs(ds).is_geographic or get_crs(ds_target).is_geographic:
        raise ValueError(
            "Can only do nearest neighbour lookup in metric coordinate systems!"
        )
    if get_crs(ds) != get_crs(ds_target):
        raise ValueError("Datasets must have the same coordinate system!")

    # create point MultiIndeces (i.e. list of tuples [(x,y,z),...]) to do nearest neighbour lookups
    xy_pos = pd.MultiIndex.from_arrays(
        [ds.west_east.values, ds.south_north.values, ds.height.values]
    )
    xy_pos_target = pd.MultiIndex.from_arrays(
        [
            ds_target.west_east.values,
            ds_target.south_north.values,
            ds_target.height.values,
        ]
    )

    # calculate euclidian shortest distance using math.hypot of the x,y,z components
    nearest_xy = [
        min(xy_pos, key=lambda p: math.hypot(p[0] - xy[0], p[1] - xy[1], p[2] - xy[2]))
        for xy in xy_pos_target
    ]

    # set index on source dataset and select by the nearest coordinates
    ds = ds.set_index(point=["west_east", "south_north", "height"])
    ds = ds.sel(point=nearest_xy).reset_index("point")

    return ds
