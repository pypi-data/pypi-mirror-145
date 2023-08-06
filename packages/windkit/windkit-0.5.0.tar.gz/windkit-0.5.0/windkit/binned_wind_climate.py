# (c) 2022 DTU Wind Energy
"""Binned wind climate module

When measuring the wind speed and wind direction over a time period, one can
create a histogram by counting the frequency of occurence for each
wind speed and direction bin.

Because there can be large differences in the wind climate when the wind is
coming from different wind directions, a binned wind distribution is usually
specified per wind direction sector.

A valid Weibull wind climate therefore has a dimension ``sector`` and the variables
``wsbin`` and ``wdfreq``. Also it must have a valid spatial structure. This module contains
functions that operate on and create binned wind climates.
This includes the ability to create bwc datasets both from files and from
existing data, the ability to calculate common parameters from the bwc object,
and the ability to write them to the legacy *.tab* format.
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    from:
#        - text file: open_tabfile()
#        - xml file: read_xmlfile()
#        - from time series of wind speeds and directions: from_ts()
#        - synthetic data: from_synthetic()
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from functools import wraps
import logging
from pathlib import Path

from lxml import etree
import numpy as np
import xarray as xr

from .metadata import _BWC_ATTRS, update_var_attrs, update_history
from .sector import (
    create_sector_coords,
    create_ws_bin_coords,
    create_ws_bin_coords_from_values,
)
from .spatial import (
    create_dataset,
    crs_are_equal,
    is_point,
    to_point,
    spatial_stack,
    spatial_unstack,
)
from .wind import wd_to_sector
from .time_series_wind_climate import ts_validate_wrapper

from ._validate import create_validator


DATA_VAR_DICT_BWC = {"wsfreq": ["wsbin", "sector"], "wdfreq": ["sector"]}

REQ_DIMS_BWC = ["wsbin", "sector"]

REQ_COORDS_BWC = [
    "south_north",
    "west_east",
    "height",
    "sector",
    "crs",
]

bwc_validate, bwc_validate_wrapper = create_validator(
    DATA_VAR_DICT_BWC, REQ_DIMS_BWC, REQ_COORDS_BWC
)

logger = logging.getLogger(__name__)

__all__ = [
    "read_bwc",
    "bwc_from_timeseries",
    "bwc_from_weibull",
    "bwc_to_tabfile",
    "bwc_validate",
    "bwc_validate_wrapper",
    "bwc_kinetic_energy",
    "bwc_mean_windspeed",
    "bwc_mean_windspeed3",
    "bwc_power_density",
    "bwc_ws_moment",
    "combine_bwcs",
    "create_time_attributes",
    "count_to_ws_freq_by_sector",
]

WS = "wind_speed"
WD = "wind_direction"
VAR_WS_FREQ = "ws_freq"
VAR_WD_FREQ = "wdfreq"
VAR_WS_FREQ_BY_SECTOR = "wsfreq"
DIM_TIME = "time"
DIM_WS = "wsbin"
DIM_WD = "sector"
WV_COUNT = "wv_count"


def wv_count_wrapper(func):
    """
    Decorator to handle wind vector count format.

    Handles the case where the parameter is an xarray.DataArray with a wv_count
    format or a xarray.Dataset with a 'wv_count' data variable, i.e. has wind
    counts by bin and sector. If so, returns a binned wind climate xarray.Dataset.
    If it is not the case, it does nothing.
    """

    @wraps(func)
    def wv_count_to_bwc(*args, **kwargs):
        obj = args[0]
        try:
            # handles the case of a xarray.Dataset
            obj = obj["wv_count"]
        except KeyError:
            pass
        if isinstance(obj, xr.DataArray) and obj.name == "wv_count":
            bwc = count_to_ws_freq_by_sector(obj)
            result = func(bwc, *args[1:], **kwargs)
        else:
            result = func(*args, **kwargs)
        return result

    return wv_count_to_bwc


def _freqs_to_dataset(
    wsfreq, wdfreq, wsbins, south_north, west_east, height, crs, **kwargs,
):  # pragma: no cover covered_in_public_method
    """
    Makes data variables, coordinates, and attributes ready for
    xarray.Dataset construction from a histogram of wind speeds and directions

    Parameters
    ----------
    wsfreq: np.array([nwsbin, nsec]): float64
        Wind speed frequency by wind speed and sector

    wdfreq: np.array([nsec]): float64
        Wind direction frequency by sector

    wsbins: np.array([nwsbin + 1]): float64
        Edges of wind speed bins

    south_north: float64
        Coordinate value in y-direction

    west_east: float64
        Coordinate value in x-direction

    height: float64
        Height above ground

    crs : int, dict, str or pyproj.crs.CRS
            Value to initialize `pyproj.crs.CRS`

    kwargs : dict
        Other kwargs are added as attributes to the dataset

    Returns
    -------
    xarray.Dataset
    """

    wsbins = np.asfarray(wsbins)

    _, nsec = wsfreq.shape

    wscenters = create_ws_bin_coords_from_values(wsbins)
    wdcenters = create_sector_coords(nsec)

    na = np.newaxis

    wdfreq /= np.sum(wdfreq)
    with np.errstate(all="ignore"):
        wsfreq = wsfreq / np.sum(wsfreq, axis=0)[na, :]
    if np.isnan(wsfreq).any():
        logging.debug(
            "There are sectors with no wind observations (nan), which will be set to 0.0."
        )
        wsfreq = np.nan_to_num(wsfreq)

    # Build dataset
    ds = create_dataset(west_east, south_north, height, crs).drop_vars("output")
    ds["wdfreq"] = (("sector", "point"), wdfreq[:, na])
    ds["wsfreq"] = (("wsbin", "sector", "point"), wsfreq[:, :, na])

    ds = ds.assign_coords({**wscenters.coords, **wdcenters.coords,})

    ds = ds.assign_attrs(kwargs)

    ds = update_var_attrs(ds, _BWC_ATTRS)
    return update_history(ds)


def read_bwc(file, crs=None):
    """Creates binned wind climate xarray.Dataset from file.

    Parameters
    ----------
    file : str or Path
        Path to a file that can be opened as a bwc. This includes .tab, .owc,
        .omwc, and .nc files that were created as bwc files. The script will
        use the file extension to determine the file type and then parse it
        into a bwc DataSet object.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum) for .tab, .owc and .omwc files,
        and the embedded CRS for .nc files.

    Returns
    -------
    ds : xarray.Dataset
        binned wind climate dataset that is formatted to match the bwc description.

    Raises
    ------
    ValueError
        If crs does not match dataset crs.
    ValueError
        If type of bwc is undetectable.
    """
    file_or_obj = Path(file)
    ext = file_or_obj.suffix

    if ext == ".tab":
        if crs is None:
            crs = 4326
        return update_history(_open_tabfile(file_or_obj, crs))
    if ext in [".owc", ".omwc"]:
        if crs is None:
            crs = 4326
        return update_history(_open_owcfile(str(file_or_obj), crs))
    if ext in [".nc"]:
        ds = xr.load_dataset(file_or_obj)
        if crs is not None and crs_are_equal(ds, crs):
            raise ValueError("Requested crs does not match dataset crs.")
        ds = update_var_attrs(ds, _BWC_ATTRS)
        return update_history(ds)
    raise ValueError(f"Unable to detect type of bwc file {file} with extension {ext}")


def combine_bwcs(bwc_list):
    """Combines a list of bwc's into one binned wind climate.

    .. note:: This always an object with a point structure

    Parameters
    ----------
    bwc_list: list
        List of binned wind climate xarray.Dataset.

    Returns
    -------
    bwcs: xarray.Dataset
        xarray Dataset with merged binned wind climates.
    """
    max_bins = max([bwc.dims["wsbin"] for bwc in bwc_list])
    filled_bwcs = []
    for bwc in bwc_list:
        if not is_point(bwc):
            bwc = to_point(bwc)
        filled_bwcs.append(_fill_wsbin(bwc, max_bins + 1))

    bwcs = xr.concat(filled_bwcs, "point")
    return update_history(bwcs)


def _open_tabfile(tab_file, crs=4326):  # pragma: no cover covered_in_public_method
    """Creates bwc object from a "tab" ascii file

    Parameters
    ----------
    tab_file: str
        Path to file tab file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum)

    Returns
    -------
    xr.DataSet
        xarray DataSet that is formatted to match the bwc description

    Raises
    ------
    ValueError
        If .tab file does not have appropriate string formatting
    """

    def _read_floats(fobj):
        return map(float, fobj.readline().split())

    def _load_tabfile(tab_file, encode="utf_8"):
        with open(tab_file, "r", newline="\r\n", encoding=encode) as fobj:
            header = fobj.readline().strip()
            south_north, west_east, height = _read_floats(fobj)
            tuple_header = tuple(_read_floats(fobj))
            if len(tuple_header) == 4:
                nsec, _, _, tabfile_type = tuple_header
                if tabfile_type != 0:
                    ValueError(
                        "Tabfiles of type {0} are not supported".format(tabfile_type)
                    )
            else:
                nsec, _, _ = tuple_header
            nsec = int(nsec)

            wd_freq = np.array(list(_read_floats(fobj)))
            wsdata = np.genfromtxt(fobj)

        kwargs = {
            "south_north": south_north,
            "west_east": west_east,
            "height": height,
            "wasp_header": header,
            "crs": crs,
        }

        return kwargs, wd_freq, wsdata

    try:
        kwargs, wd_freq, wsdata = _load_tabfile(tab_file, "ascii")
    except (UnicodeDecodeError, UnicodeError):
        try:
            kwargs, wd_freq, wsdata = _load_tabfile(tab_file, "utf_8")
        except (UnicodeDecodeError, UnicodeError):
            try:
                kwargs, wd_freq, wsdata = _load_tabfile(tab_file, "utf_16")
            except (UnicodeDecodeError, UnicodeError):
                try:
                    kwargs, wd_freq, wsdata = _load_tabfile(tab_file, "cp1256")
                except (UnicodeDecodeError, UnicodeError):
                    raise ValueError(
                        "Unknown encoding for .tab file, please save as ASCII or UTF-8"
                    )

    ws_freq = wsdata[:, 1:]
    ws_bins = np.append(0, wsdata[:, 0])

    return _freqs_to_dataset(ws_freq, wd_freq, ws_bins, **kwargs)


def _parse_owc(owc, crs=4326):
    """
    Parses an OWC file into a bwc object

    Parameters
    ----------
    owc : xml tree
        An XML element loaded by lxml
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum)

    Returns
    -------
    xr.DataSet
        xarray DataSet that is formatted to match the bwc description
    """
    # Get main dimensions
    num_sec = int(owc.attrib["CountOfSectors"])
    num_wsbins = int(
        owc.xpath("ObservedWind[1]/SpeedFrequencyDistribution" + "/@NumberOfBins")[0]
    )

    # Create arrays
    ws_freq = np.zeros((num_wsbins, num_sec))
    wd_freq = np.zeros(num_sec)
    cen_angle = np.zeros(num_sec)
    ws_bins = np.zeros(num_wsbins)

    # Get site information
    site_info = owc.xpath("RveaAnemometerSiteDetails")[0].attrib
    lat = float(site_info["LatitudeDegrees"])
    lon = float(site_info["LongitudeDegrees"])
    height = float(site_info["HeightAGL"])
    header = site_info["Description"]

    # Get wind speed histogram
    for obsWind in owc.xpath("ObservedWind"):
        # Get sector information
        sec = int(obsWind.attrib["Index"]) - 1
        cen_angle[sec] = float(obsWind.attrib["SectorWidthDegrees"])
        wd_freq[sec] = float(obsWind.attrib["SectorFrequency"])

        # Get wind speed histogram
        for wsBin, ws in enumerate(obsWind.getchildren()[0]):
            ws_bins[wsBin] = float(ws.attrib["UpperSpeedBound"])
            ws_freq[wsBin, sec] = float(ws.attrib["Frequency"])

    # Extract 1st column which is wind speeds and
    # add a 0.0 value to the first position
    ws_bins = np.insert(ws_bins, 0, 0.0)

    kwargs = {
        "south_north": lat,
        "west_east": lon,
        "height": height,
        "wasp_header": header,
        "crs": crs,
    }

    return _freqs_to_dataset(ws_freq, wd_freq, ws_bins, **kwargs)


def _open_owcfile(xml_file, crs=4326):
    """Creates bwc object from a .owc xml file

    Parameters
    ----------
    n: xml_file
        Path to xml file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum)

    Returns
    -------
    bwc
    """
    tree = etree.parse(str(xml_file))
    root = tree.getroot()
    return _parse_owc(root, crs)


def count_to_wd_freq(wind_hist):
    """Convert wind vector count histogram to wind sector-wise relative frequency.

    Parameters
    ----------
    wind_hist : xarray.DataArray
        A valid pywasp wind-vector-count histogram DataArray


    Returns
    -------
    relfreq : xarray.DataArray
        Data array with sectorwise relative frequencies.
    """
    relfreq = wind_hist.sum(dim=[DIM_WS]) / wind_hist.sum(dim=[DIM_WS] + [DIM_WD])
    relfreq.name = VAR_WD_FREQ
    return update_var_attrs(relfreq, _BWC_ATTRS)


def count_to_ws_freq(wind_hist):
    """Convert wind vector count histogram to wind sector-wise relative frequency.

    Parameters
    ----------
    wind_hist : xarray.DataArray
        A valid pywasp wind-vector-count histogram DataArray


    Returns
    -------
    relfreq : xarray.DataArray
        Data array with sectorwise relative frequencies.
    """
    relfreq = wind_hist.sum(dim=[DIM_WD]) / wind_hist.sum(dim=[DIM_WS] + [DIM_WD])
    relfreq.name = VAR_WS_FREQ
    return update_var_attrs(relfreq, _BWC_ATTRS)


def count_to_ws_freq_by_sector(wind_hist):
    """Convert wind vector count histogram to wind sector-wise relative frequency.

    Parameters
    ----------
    wind_hist : xarray.DataArray
        A valid pywasp wind-vector-count histogram DataArray


    Returns
    -------
    relfreq : xarray.Dataset
        Dataset with wind speed frequencies
        normalized in each sector and the rel.
        frequency of occurance of wind direction.
    """
    ds = xr.Dataset()
    ds[VAR_WS_FREQ_BY_SECTOR] = wind_hist / wind_hist.sum(dim=DIM_WS)
    ds[VAR_WD_FREQ] = count_to_wd_freq(wind_hist)
    ds.attrs.update(wind_hist.attrs)
    # replace nan with 0
    ds = ds.fillna(0)
    ds = update_var_attrs(ds, _BWC_ATTRS)
    return update_history(ds)


@ts_validate_wrapper
def bwc_from_timeseries(
    ts, ws_bin_width=1.0, nwsbin=30, nsec=12, normalize=True, **kwargs
):
    """Creates object from a timeseries.

    Parameters
    ----------
    ts : xarray.Dataset
        Xarray dataset with variables 'wind_speed'
        and 'wind_direction' and with a coordinate and
        dimension 'time'.
    ws_bin_width: float
        Width of the wind speed bins, defaults to 1.0.
    nwsbin : int
        Number of wind speed bins, defaults to 30.
    nsec : int
        Number of sectors, defaults to 12.
    normalize : bool
        If set to True, convert wind vector count histogram to
        wind sector-wise relative frequency. Defaults to True
    kwargs: dict
        Additional argument 'wasp_header'

    Returns
    -------
    bwc : xarray.Dataset
        Binned wind climate from the timeseries.
    """

    def point_histogram2d(ws, wd, bins):
        hist, _, _ = np.histogram2d(ws, wd, bins=bins)
        hist_no_nan = np.nan_to_num(hist)

        return hist_no_nan

    # stack windkit dataset to point
    ds = spatial_stack(ts.squeeze(), copy=False).transpose(..., "time", "point")

    ds_attrs = {
        "wasp_header": kwargs.get("wasp_header", ""),
        **create_time_attributes(ds),
    }
    # ignore times when any of the time series is not available
    ds = ds.dropna(dim=DIM_TIME)
    if ds.dims["time"] < 1:
        raise ValueError("Need at least 1 sample to create a histogram")

    ws_bins = create_ws_bin_coords(bin_width=ws_bin_width, nws=nwsbin)
    wd_bins = create_sector_coords(nsec=nsec)
    ws_bin_edges = np.append(0.0, ws_bins["wsceil"].values)

    # convert wdir to sectors
    # wd, wd_sec = dir_to_sec(ds[WD], nsec)
    wd, wd_sec = wd_to_sector(ds[WD], nsec, return_centers=True)
    ds["wd_bins"] = (ds[WD].dims, wd.data)
    bins = (ws_bin_edges, np.arange(nsec + 1))

    hist = xr.apply_ufunc(
        point_histogram2d,
        ds["wind_speed"],
        ds["wd_bins"],
        dask="allowed",
        vectorize=True,
        input_core_dims=[["time"], ["time"]],
        output_core_dims=[["wsbin", "sector"]],
        kwargs={"bins": bins},
        keep_attrs=True,
    )
    # the _pwio_was_stacked_point attribute is lost with apply_ufunc
    hist.attrs.update(ds.attrs)
    hist.name = WV_COUNT
    hist = hist.assign_coords({**ws_bins.coords, **wd_bins.coords})

    if normalize:
        hist = count_to_ws_freq_by_sector(hist)
    else:
        hist = update_var_attrs(hist.to_dataset(), _BWC_ATTRS)

    hist = hist.assign_attrs(ds_attrs)
    hist = spatial_unstack(hist)

    return update_var_attrs(spatial_unstack(hist), _BWC_ATTRS)


@ts_validate_wrapper
def create_time_attributes(ds: xr.Dataset, hist=None):
    """Create time attributes for binned wind climate.

    We attached the time attributes to a new or existing
    binned wind climate. If it has existing attributes, these
    will be used as well when calculating the meta data.

    Parameters
    ----------
    ds : xarray.Dataset
        Xarray dataset with variables 'wind_speed'
        and 'wind_direction' and with a coordinate and
        dimension 'time'.
    hist : xarray.Dataset, optional
        A valid pywasp histogram dataset with, defaults to None

    Returns
    -------
    dic_result: dict
        Dictionary with 'start_time', 'end_time', 'interval',
        'count', 'count_missing', 'recovering_percentage'
    """
    # find the first and last time in the time series we process
    first_time = ds["time"].min().values
    last_time = ds["time"].max().values
    number_of_samples = int(ds.dropna(dim="time").sizes["time"])
    # find most frequent interval in minutes
    # currently when you provide an existing histogram
    # as input it will just overwrite the sampling interval
    # and recovery percentage. Since we only process model
    # data this way, it is probably OK for now.
    intervals, counts = np.unique(
        np.diff(ds["time"]) / np.timedelta64(1, "m"), return_counts=True
    )
    interval = intervals[counts.argmax()]
    series_start_to_end = np.arange(
        first_time, last_time, np.timedelta64(int(interval), "m")
    )
    # arange does not include the last step but we want
    # this for the max samples
    max_possible_samples = int(series_start_to_end.size + 1)

    # check for existing first and last time in input
    # it is assumed that this histogram has also been created
    # with this function and the attributes should be present
    try:
        first_time = np.min([first_time, np.datetime64(hist.attrs["start_time"])])
        last_time = np.max([last_time, np.datetime64(hist.attrs["end_time"])])
        max_possible_samples = max_possible_samples + hist.attrs["count_expected"]
        number_of_samples = number_of_samples + hist.attrs["count"]
    except (KeyError, AttributeError) as e:
        logging.info("No attributes present yet, adding new ones.")

    dic_result = {
        "start_time": first_time.astype(str),
        "end_time": last_time.astype(str),
        "interval": f"{interval} minutes",
        "count_expected": max_possible_samples,
        "count": number_of_samples,
        "count_missing": max_possible_samples - number_of_samples,
        "recovery_percentage": 100 * number_of_samples / max_possible_samples,
    }

    return dic_result


def _bwc_from_synthetic():  # pragma: no cover unnecessary method
    """Makes bwc object from synthetic data

    Returns
    -------
    xarray
        binned wind climate xarray dataset
    """

    def _synthetic():
        np.random.seed(256)
        ws = 10 * np.random.weibull(2.0, 10000)
        wd = 360 * np.random.rand(10000)
        ws[[1, 3, 4]] = np.nan
        wd[[59, 100, 150]] = np.nan
        return ws, wd

    ws, wd = _synthetic()
    times = np.arange(
        np.datetime64("2009-12-31 23:00"),
        np.datetime64("2009-12-31 23:00") + np.timedelta64(10 * ws.size, "m"),
        np.timedelta64(10, "m"),
    )
    ds = create_dataset(12.0, 56.0, 50, 4326).drop_vars("output")
    ds["wind_direction"] = (("point", "time"), [wd])
    ds["wind_speed"] = (("point", "time"), [ws])
    ds = ds.assign_coords({"time": times})
    return bwc_from_timeseries(ds, nwsbin=30, nsec=12, header="synthetic data")


def bwc_from_weibull(A, k, wd_freq, ws_bins, crs=4326, **kwargs):
    """Creates object from directional A's and k's.

    Parameters
    ----------
    A : numpy.ndarray or array_like
        1D array with Weibull A by sector.
    k : numpy.ndarray or array_like
        1D array with Weibull k by sector.
    wd_freq : numpy.ndarray or array_like
        1D array with wind direction frequency by sector.
    ws_bins : numpy.ndarray or array_like
        1D array with edges of the wind speed bins (# of wind speeds + 0.0 as the lower bound)
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum).
    **kwargs : dict
        Additional arguments header, height, south_north, west_east.

    Returns
    -------
    bwc : xarray.Dataset
        binned wind climate from a Weibull distribution.
    """

    def _weibull_acprob(u, k, A):
        """
        Weibull Cumulative distribution function for a
        given wind speed (u) and A,k parameter

        Parameters
        ----------
        u: float
            Wind speed

        A, k: float
            Weibull parameters

        Returns
        -------
        f: float
            Weibull Cumulative distribution
        """

        with np.errstate(all="raise"):
            try:
                F = 1 - np.exp(-((u / A) ** k))
            except (ZeroDivisionError, FloatingPointError):
                F = 1
        return F

    def _weibull_binfreq(ws_bins, k, A):
        """
        Weibull density for given wind speed bins for a
        given wind speed (u) and A,k parameter

        Parameters
        ----------
        ws_bins: np.array: float64
            Wind speed bin edges

        A, k: float
            Weibull parameters

        Returns
        -------
        f: float
                Weibull density
        """
        nws = len(ws_bins) - 1
        f = np.zeros([nws])

        for iws in range(nws):

            u0 = ws_bins[iws]
            u1 = ws_bins[iws + 1]

            accp0 = _weibull_acprob(u0, k, A)
            accp1 = _weibull_acprob(u1, k, A)

            f[iws] = accp1 - accp0

        # Make sure it sums to 1.0
        with np.errstate(all="raise"):
            try:
                f = f / np.sum(f)
            except (ZeroDivisionError, FloatingPointError):
                f = 0
        return f

    kwargs["wasp_header"] = kwargs.get("wasp_header", "") + " from Weibull"

    nsec = len(wd_freq)
    nwsbin = len(ws_bins) - 1
    ws_freq = np.zeros([nwsbin, nsec])

    for isec in range(nsec):
        ws_freq[:, isec] = _weibull_binfreq(ws_bins, k[isec], A[isec])
    kwargs["crs"] = crs

    ds = _freqs_to_dataset(ws_freq, wd_freq, ws_bins, **kwargs)

    return update_history(ds)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#    Binned wind climate functions for working with bwc datasets
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def _tab_string(bwc):  # pragma: no cover covered_in_public_method
    """Returns string representation of bwc dataset

    Parameters
    ----------
    bwc: xr.Dataset
        Binned wind climate xr.Dataset object

    Returns
    -------
    string: str
        String representation of bwc dataset
    """

    def _to_string(node):

        nwsbin = node.dims["wsbin"]
        nsec = node.dims["sector"]

        le = "\n"
        string = node.attrs["wasp_header"] + le

        string += (
            "\t".join(
                map(
                    str,
                    [
                        node["south_north"].values,
                        node["west_east"].values,
                        node["height"].values,
                    ],
                )
            )
            + le
        )

        string += "\t".join(map(str, [nsec, 1.0, 0.0])) + le

        string += "    \t" + "\t".join("%6.2f" % f for f in node.wdfreq * 100.0) + le

        wsfreq = np.round(node.wsfreq.values * 1000.0, 3)

        for iws in range(nwsbin):
            string += "%4.1f" % node.wsceil.values[iws] + "\t"
            string += "\t".join("%6.2f" % f for f in wsfreq[iws, :])
            if iws < nwsbin - 1:
                string += le

        return string

    # If dataset has no extra dimensions (larger than  size=1):
    # Return the single tab string.
    if bwc.squeeze().wsfreq.ndim == 2:
        return _to_string(bwc.squeeze())

    # If dataset has extra dimensions (of size > 1):
    # Stack extra dimensions, loop over them, and append string to list
    # finally: return list
    dims_extra = [d for d in bwc.wsfreq.dims if d not in ["wsbin", "sector"]]
    stacked = bwc.stack(point=dims_extra)

    string = []
    for ipt in range(stacked.dims["point"]):
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        string.append(_to_string(node))

    return string


@wv_count_wrapper
@bwc_validate_wrapper
def bwc_to_tabfile(bwc, path=None):
    """Write bwc to tab-style ascii file.

    Parameters
    ----------
    bwc: xr.Dataset
        Binned wind climate xr.Dataset object.

    path: str
        dir or file path to write the file. Default value set
        to the current working directory.

    """

    def _write(node, fpath):
        with open(fpath, "w", newline="\r\n") as fobj:
            fobj.write(_tab_string(node))

    if path is None:
        path = Path.cwd()

    # If dataset has no extra dimensions (larger than  size=1):
    # write file and return early.
    if bwc.squeeze().wsfreq.ndim == 2:
        if Path(path).is_dir():
            fpath = Path(path) / "bwc.tab"
        else:
            fpath = path
        _write(bwc.squeeze(), fpath)
        return

    # If dataset has extra dimensions (of size > 1):
    # Stack extra dimensions, loop over them, and write to tab files
    # Using file_name that contains coordinate information.
    dims_extra = [d for d in bwc.wsfreq.dims if d not in ["wsbin", "sector"]]
    stacked = bwc.stack(point=dims_extra)

    # Create file_name format string
    if Path(path).is_dir():
        file_name_fmt = (
            "_".join(["bwc"] + [f"{d}" + "{" + f"{d}" + "}" for d in dims_extra])
            + ".tab"
        )

    # Loop and write to tab files
    for ipt in range(stacked.dims["point"]):
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        kw = {d: node[d].values for d in dims_extra}
        fpath = path / file_name_fmt.format(**kw)
        _write(node, fpath)

    return


@wv_count_wrapper
@bwc_validate_wrapper
def bwc_ws_moment(bwc, n=1.0, bysector=False):
    """Calculate the n^th moment of the wind speed from a bwc

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xr.Dataset object

    n : float
        Moment to compute, defaults to 1.0.

    bysector: bool
        Whether to return the sectorwise wind speed moment or the
        all-sector mean moment. Defaults to False.

    Returns
    -------
    ws_moment: xarray.DataArray
        Array of wind speed moments.
    """
    if bysector:
        return (bwc.wsfreq * bwc.wsbin ** n).sum(dim=["wsbin"])
    return (bwc.wdfreq * bwc.wsfreq * bwc.wsbin ** n).sum(dim=["wsbin", "sector"])


@wv_count_wrapper
@bwc_validate_wrapper
def bwc_kinetic_energy(bwc, air_density=1.225, bysector=False):
    """Compute kinetic energy of the bwc.

    Parameters
    ----------
    bwc : xarray.Dataset
        Binned wind climate dataset.
    air_dens: float
        Air density, default set to 1.225 kg.m^-3.

    bysector: bool
        Whether to return the sectorwise or all-sector mean wind speed moment.
        Default set to `False`, i.e. return all-sector mean moment.

    Returns
    -------
    ws_monent: xarray.DataArray
        Array of wind kinetic energy.
    """
    ke_cen = 0.5 * air_density * bwc.wsbin ** 3.0
    if bysector:
        return (bwc.wsfreq * ke_cen).sum(dim=["wsbin"])
    return (bwc.wdfreq * ke_cen * bwc.wsfreq).sum(dim=["wsbin", "sector"])


@bwc_validate_wrapper
def _fill_wsbin(bwc, nwsbin):  # pragma: no cover covered_in_public_method
    """Expands a binned wind climate to nwsbin number of bins
    This is a useful feature when you want to combine several
    binnen wind climates in one dataset, because that requires that they
    have the same dimensions.

    Parameters
    ----------
    bwc: :any:`windkit.bwc`
        Binned wind climate

    nwsbin: int
        Number of wind speeds bins

    Returns
    -------
    filled_bwc: :any:`windkit.bwc`
        Binned wind climate with nwsbin number of bins
    """
    owsbin = bwc.dims["wsbin"]
    dws = np.diff(bwc.wsbin[-2:])
    newbins = np.zeros(nwsbin)
    newbins[0:owsbin] = bwc.wsbin.values
    newbins[owsbin:nwsbin] = newbins[owsbin - 1] + dws * np.arange(
        1, nwsbin - owsbin + 1
    )
    wscenters = 0.5 * (newbins[:-1] + newbins[1:])
    filled_bwc = bwc.interp(wsbin=newbins[:-1], kwargs={"fill_value": 0.0})
    filled_bwc["wsceil"] = (("wsbin"), wscenters)

    return filled_bwc


def bwc_mean_windspeed(bwc, bysector=False):
    """Calculate the mean wind speed.

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xr.Dataset object.

    bysector: bool
        Return sectorwise mean wind speed if True. Defaults to False.

    Returns
    -------
    bwc : xarray.DataArray
        Mean wind speed of the bwc.
    """
    ds = bwc_ws_moment(bwc, 1.0, bysector)
    return update_history(ds)


def bwc_mean_windspeed3(bwc, bysector=False):
    """Calculates mean third moment of the wind speed.

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xarray.Dataset object.
    bysector: bool
        Return sectorwise mean wind speed if True. Defaults to False.

    Returns
    -------
    bwc : xarray.DataArray
        Mean wind speed of the third-moment of the bwc.
    """
    ds = bwc_ws_moment(bwc, 3.0, bysector)
    return update_history(ds)


def bwc_power_density(bwc, bysector=False, air_density=1.225):
    """Calculate the power density

    Calculates the power density using a standard atmosphere air density of 1.225 kg m-3

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xr.Dataset object.
    bysector: bool
        Return sectorwise mean wind speed if True. Defaults to False.
    air_dens : float
        Air density. Default set to 1.225 kg.m^-3.

    Returns
    -------
    bwc : xarray.DataArray
        Power density of the bwc.
    """
    return 1 / 2 * air_density * bwc_mean_windspeed3(bwc, bysector)
