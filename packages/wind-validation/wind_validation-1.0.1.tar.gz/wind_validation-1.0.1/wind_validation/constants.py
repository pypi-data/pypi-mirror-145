# TODO: check unused & remove them
VAR_WIND_SPEED = "wind_speed"
VAR_POWER_DENS = "power_density"
VAR_AIR_DENS = "air_density"
VAR_WIND_DIRECTION = "wind_direction"
VAR_WIND_VECTOR = "wind_vector"
VAR_WEIBULL_DISTRIBUTION = "weibull"
VAR_FREQ = "relative_frequency"
VAR_COUNT = "count"

DIM_WIND_SPEED = "wsbin"
DIM_WIND_DIRECTION = "sector"
DIM_TIME = "time"

VAR_WV_COUNT = f"wv_{VAR_COUNT}"
VAR_WD_FREQ = "wdfreq"
VAR_WS_FREQ_BY_SECTOR = "wsfreq"
GRID = {"grid_mapping": "crs"}

VARS_HIST = {
    VAR_WV_COUNT: {
        "long_name": f"{VAR_COUNT} of {VAR_WIND_VECTOR} per {DIM_WIND_SPEED} and {DIM_WIND_DIRECTION} over {DIM_TIME}",
        "standard_name": f"{VAR_COUNT}_of_{VAR_WIND_VECTOR}_per_{DIM_WIND_SPEED}_and_{DIM_WIND_DIRECTION}_over_{DIM_TIME}",
        "short_name": VAR_WV_COUNT,
        "units": "1",
        "dims": (DIM_WIND_SPEED, DIM_WIND_DIRECTION),
        "cell_method": "time: sum",
        **GRID,
    }
}

VARS_FREQ = {
    VAR_WD_FREQ: {
        "long_name": f"{VAR_FREQ} of {VAR_WIND_VECTOR} per {DIM_WIND_DIRECTION} over {DIM_TIME} and {DIM_WIND_SPEED}",
        "standard_name": f"{VAR_FREQ}_of_{VAR_WIND_VECTOR}_per_{DIM_WIND_DIRECTION}_over_{DIM_TIME}_and_{DIM_WIND_SPEED}",
        "short_name": VAR_WD_FREQ,
        "units": "1",
        "dims": (DIM_WIND_DIRECTION),
        **GRID,
    },
    VAR_WS_FREQ_BY_SECTOR: {
        "long_name": f"{VAR_FREQ} of {VAR_WIND_VECTOR} per {DIM_WIND_SPEED} over {DIM_TIME} conditional on {DIM_WIND_DIRECTION}",
        "standard_name": f"{VAR_FREQ}_of_{VAR_WIND_SPEED}_per_{DIM_WIND_SPEED}_over_{DIM_TIME}_conditional_on_{DIM_WIND_DIRECTION}",
        "short_name": VAR_WS_FREQ_BY_SECTOR,
        "units": "1",
        "dims": (DIM_WIND_SPEED, DIM_WIND_DIRECTION),
        **GRID,
    },
}
