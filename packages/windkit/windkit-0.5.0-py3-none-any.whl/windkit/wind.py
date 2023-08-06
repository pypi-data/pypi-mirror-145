# (c) 2022 DTU Wind Energy
"""
Utility functions for working with wind data
"""
import numpy as np
import xarray as xr


def wind_speed(u, v):
    """
    Calculate wind speed from wind vectors.

    Parameters
    ----------
    u, v : numpy.ndarray, xarray.DataArray
        U and V wind vectors.

    Returns
    -------
    ws : numpy.ndarray, xarray.DataArray
        Wind speed.

    """
    return np.sqrt(u * u + v * v)


def wind_direction(u, v):
    """
    Calculate wind directions from wind vectors.

    Parameters
    ----------
    u, v : np.ndarray, xr.DataArray
        U and V wind vectors.

    Returns
    -------
    wd : np.ndarray, xr.DataArray
        Wind direction

    """
    return 180.0 + np.arctan2(u, v) * 180.0 / np.pi


def wind_speed_and_direction(u, v):
    """
    Calculate wind speed and wind direction from wind vectors.

    Parameters
    ----------
    u, v : numpy.ndarray, xarray.DataArray
        U and V wind vectors.

    Returns
    -------
    speed : numpy.ndarray, xarray.DataArray
        Wind speed.
    direction : numpy.ndarray, xarray.DataArray
        Wind direction.

    """
    return wind_speed(u, v), wind_direction(u, v)


def wind_vectors(ws, wd):
    """
    Calculate wind vectors u,v from the speed and direction.

    Parameters
    ----------
    speed : numpy.ndarray, xarray.DataArray
        Wind speed
    direction : numpy.ndarray, xarray.DataArray
        Wind direction

    Returns
    -------
    u, v : numpy.ndarray, xarray.DataArray
        Wind vectors u and v

    """
    return (
        -np.abs(ws) * np.sin(np.pi / 180.0 * wd),
        -np.abs(ws) * np.cos(np.pi / 180.0 * wd),
    )


def wind_direction_difference(wd_obs, wd_mod):
    """
    Calculate the circular (minimum) distance between
    two directions (observed and modelled).

    Parameters
    ----------
    wd_obs : xarray.DataArray
        observed direction arrays.
    wd_mod: xarray.DataArray
        modelled direction arrays.

    Returns
    -------
    xarray.DataArray: circular (minimum) differences.

    Examples
    --------
    >>> wd_obs = xr.DataArray([15.0, 345.0, 355.0], dims=('time',))
    >>> wd_mod = xr.DataArray([345.0, 300.0, 5.0], dims=('time',))
    >>> wind_direction_difference(wd_obs, wd_mod)
    <xarray.DataArray (time: 3)>
    array([-30., -45.,  10.])
    Dimensions without coordinates: time

    """
    wd_diff = wd_mod - wd_obs
    wd_diff = wd_diff.where(wd_diff < 180.0, wd_diff - 360.0)
    wd_diff = wd_diff.where(wd_diff > -180.0, wd_diff + 360.0)
    return wd_diff


def wd_to_sector(wd, bins=12, return_centers=False):
    """
    Convert wind directions to 0-based sector indices.

    Parameters
    ----------
    wd : xarray.DataArray
        Wind directions.
    bins : int, optional
        Number of bins / sectors. Defaults to 12.
    return_centers : bool, optional
        If True, return the bin centers in addition to the
        sector indices. Defaults to False.

    Returns
    -------
    xarray.DataArray:
        wind speed sectors.
    xarray.DataArray, optional:
        bin centers.

    Examples
    --------
    >>> wd = xr.DataArray([355.0, 14.0, 25.0, 270.0,], dims=('time',))
    >>> wd_to_sector(wd, bins=12)
    <xarray.DataArray (time: 4)>
    array([0., 0., 1., 9.])
    Dimensions without coordinates: time

    """

    def _wd_to_sector(wd, bins=12):
        width = 360.0 / bins
        edges = np.linspace(0.0, 360.0, bins + 1)
        edges[0] = -0.1
        edges[-1] = 360.1
        sector = np.digitize(np.mod(wd + width / 2.0, 360.0), edges) - 1
        sector = sector.astype(np.float64)
        sector[sector >= bins] = np.nan
        return sector

    sectors = xr.apply_ufunc(_wd_to_sector, wd, kwargs={"bins": bins})

    if return_centers:
        return sectors, sectors * 360.0 / bins
    else:
        return sectors
