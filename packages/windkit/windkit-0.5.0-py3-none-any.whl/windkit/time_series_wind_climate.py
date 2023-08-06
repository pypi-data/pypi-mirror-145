# (c) 2022 DTU Wind Energy
"""Time series wind climate module

A time series wind climate is defined by dataset with a time series
``wind speed`` and ``wind direction``.

A valid time series wind climate therefore has a dimension ``time``.
Also it must have one of the valid :ref:`geospatial_structures`. This module contains
functions that operate on time series wind climates.
This includes the ability to create time series datasets from files and from
existing data.
"""

from functools import wraps
import pandas as pd
from datetime import datetime
from .spatial._crs import add_crs
import xarray as xr
from .metadata import _TS_ATTRS, update_var_attrs
import warnings
import re
from ._validate import create_validator

WS = "wind_speed"
WD = "wind_direction"
DIM_TIME = "time"
DATA_VAR_DICT_TS = {WS: [DIM_TIME], WD: [DIM_TIME]}
REQ_DIMS_TS = [DIM_TIME]
REQ_COORDS_TS = ["south_north", "west_east", "height", "crs"]


ts_validate, ts_validate_wrapper = create_validator(
    DATA_VAR_DICT_TS, REQ_DIMS_TS, REQ_COORDS_TS
)


def read_ts_windpro_txt(fpath):
    """Parses windpro format txt file into a dataset.



    Parameters
    ----------
    fpath : [str]
        [file path to be parsed]

    Returns
    -------
    xarray.Dataset

    """

    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # parse parameters from windpro header;
    lng, lat = 0.0, 0.0
    data_start_line = -1
    disp_height = -1
    with open(fpath, "r") as file:
        for i, line in enumerate(file):
            # parse coordinates
            if "Geographical Coordinates" in line:
                parts = line.split()
                for j, p in enumerate(parts):
                    if _is_float(p) and parts[j - 1] == "Longitude:":
                        lng = float(p)
                    if _is_float(p) and parts[j - 1] == "Latitude:":
                        lat = float(p)
            # parse height
            if "Displacement height" in line:
                parts = line.split()
                for p in parts:
                    if _is_float(p):
                        disp_height = float(p)
            # reached header
            if "TimeStamp" in line:
                data_start_line = i
                break

    if disp_height > 0:
        warnings.warn(
            "Displacement height cannot be used in WindKit. Set it up via the map instead."
        )
    if lng == 0.0 and lat == 0.0:
        raise Exception("Couldn't parse coordinates")

    ts = pd.read_csv(
        fpath,
        delimiter="\t{2}|\t",
        parse_dates=["TimeStamp"],
        skiprows=range(data_start_line),
        engine="python",
    )

    # parse height from the wind speed/direction column
    for col in ts.columns:
        if "Mean wind speed" in col:
            height = float(re.findall(r"[0-9]+.[0-9]+m", col)[0].replace("m", ""))
            ts = ts.rename({col: "ws"}, axis="columns")
        if "Wind direction" in col:
            ts = ts.rename({col: "wd"}, axis="columns")

    ts = ts[~ts.ws.str.contains("-")]
    ts = ts[ts["ws"].notna()]
    ts = ts[ts["wd"].notna()]
    ts["ws"] = ts["ws"].astype(float)
    ts["wd"] = ts["wd"].astype(float)

    ts_ds = xr.Dataset(
        {"wind_speed": (["time"], ts["ws"]), "wind_direction": (["time"], ts["wd"]),},
        coords={
            "time": ("time", ts["TimeStamp"]),
            "south_north": lat,
            "west_east": lng,
            "height": height,
            "crs": 0,
        },
    )

    add_crs(ts_ds, 4326)
    update_var_attrs(ts_ds, {**_TS_ATTRS})
    # validate the dataset before returning
    ts_validate(ts_ds)
    return ts_ds
