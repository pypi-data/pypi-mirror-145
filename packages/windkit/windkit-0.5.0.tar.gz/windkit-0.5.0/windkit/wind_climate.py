# (c) 2022 DTU Wind Energy
"""
Wind climate functions.
"""
from .weibull_wind_climate import wwc_validate, wwc_mean_windspeed, wwc_power_density
from .binned_wind_climate import bwc_validate, bwc_ws_moment, bwc_power_density
from .metadata import _MET_ATTRS, update_var_attrs
from ._errors import WindClimateValidationError


def _is_bwc(wco):
    """Check if a wind climate is binned?

    Returns true if bwc and false if wwc

    Parameters
    ----------
    wco: xarray.Dataset
        Weibull Wind Climate or Binned Wind Climate Object

    Returns
    -------
    Bool
        Returns true if bwc and false if wwc
    """
    try:
        bwc_validate(wco)
        return True
    except WindClimateValidationError:
        try:
            wwc_validate(wco)
            return False
        except ValueError:
            raise ValueError("Function only works with bwc or wwc datasets.")


def mean_windspeed(wco, bysector=False, emergent=True):
    """Calculate the mean wind speed from a wind climate.

    Parameters
    ----------
    wco: xarray.Dataset
        Weibull Wind Climate or Binned Wind Climate Object.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.

    Returns
    -------
    xarray.DataArray
        DataArray with the wind speed.
    """
    # TODO: add mean wind speed of time series object
    if bysector and emergent:
        raise ValueError(
            "Emergent wind speed can only be calculated for sectorwise wind speed."
        )
    if _is_bwc(wco):
        ws = bwc_ws_moment(wco, 1.0, bysector)
    elif emergent:
        ws = wwc_mean_windspeed(wco, bysector, emergent=True)
        ws.name = "wspd"
        return update_var_attrs(ws, _MET_ATTRS)
    else:
        ws = wwc_mean_windspeed(wco, bysector, emergent=False)

    if bysector:
        ws.name = "wspd_sector"
    else:
        ws.name = "wspd_combined"

    return update_var_attrs(ws, _MET_ATTRS)


def power_density(wco, bysector=False, emergent=True, air_density=1.225):
    """Calculate the power density of a bwc or wwc

    Parameters
    ----------
    wco: xarray.Dataset
        Weibull Wind Climate or Binned Wind Climate Object.
    bysector: bool
        Return results by sector or as an all-sector value. Defaults to False.
    emergent: bool
        Calculate the all-sector mean using the emergent (True) or the combined Weibull
        distribution (False). Defaults to True.
    air_dens: xarray.DataArray or float
        xarray.DataArray with air density with the same dimensions
        as wco, by default use US standard atmosphere air density
        of 1.225 kg/m^3

    Returns
    -------
    xarray.DataArray
        DataArray with the power density.
    """
    if bysector and emergent:
        raise ValueError(
            "Emergent power density can only be calculated for sectorwise wind speed."
        )

    # calculate power density
    if _is_bwc(wco):
        pd = bwc_power_density(wco, bysector, air_density)
    elif emergent:
        pd = wwc_power_density(wco, air_density, bysector=False, emergent=True)
        pd.name = "power_density"
        return update_var_attrs(pd, _MET_ATTRS)
    else:
        pd = wwc_power_density(wco, air_density, bysector, emergent=False)

    if bysector:
        pd.name = "power_density_sector"
    else:
        pd.name = "power_density_combined"

    return update_var_attrs(pd, _MET_ATTRS)
