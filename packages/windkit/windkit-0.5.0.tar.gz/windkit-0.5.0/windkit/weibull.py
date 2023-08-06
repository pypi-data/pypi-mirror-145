# (c) 2022 DTU Wind Energy
"""
Utility functions for Weibull distributions
"""
import math
from scipy.special import gamma
import numpy as np
import xarray as xr

from .metadata import _WEIB_ATTRS, update_var_attrs, update_history


def weibull_fit(bwc, include_met_fields=None, keep_attrs=True):
    """
    Returns sectorwise Weibull parameters using WAsP's fitting algorithm.

    Parameters
    ----------
    bwc: xarray.Dataset
        Binned wind climate xr.Dataset object
    include_met_fields : list of str
        NOTE: not currently implemented
        Calculate the included meteorological variables, see fields argument to
        pywasp.wasp.wc_to_met.add_met_fields for more details. (Default: None, which
        means to not include any meteorological fields)
    keep_attrs: bool
        Should we keep the attributes from the Binned Wind Climate. Defaults to True.

    Returns
    -------
    xarray.Dataset
        Weibull Wind Climate of same spatial extent as the input bwc
    """
    if keep_attrs:
        bwc_attrs = bwc.attrs.copy()

    ws_freq = bwc["wsfreq"] / bwc["wsfreq"].sum(dim="wsbin")
    ws_ceil = bwc.coords["wsceil"].values

    scale, shape = xr.apply_ufunc(
        _weibull_fit,
        ws_freq,
        ws_ceil,
        input_core_dims=[["wsbin"], ["wsbin"]],
        output_core_dims=[[], []],
        vectorize=True,
        dask="allowed",
        keep_attrs=keep_attrs,
    )

    wb = xr.Dataset({"k": shape, "A": scale})
    wb["wdfreq"] = bwc["wdfreq"]
    if keep_attrs:
        wb.attrs.update(bwc_attrs)

    # TODO: Add include met_fields here

    wb = update_var_attrs(wb, _WEIB_ATTRS)

    return update_history(wb)


def _weibull_fit(ws_freq, ws_ceil):
    """
    Fit two-parameter Weibull distribution
    to wind speedhistogram.

    Parameters
    ----------
    ws_freq : ndarray
        1D array of size N containing data with "float" type.
        Frequencies for each histogram bin.
    ws_ceil : ndarray
        1D array of size N containing data with "float" type.
        histogram bin ceilings. Equal-size bins is assumed.

    Returns
    -------
    float, float
        Weibull scale and shape (A, k)
    """
    ws_freq = ws_freq / ws_freq.sum()
    ws_center = ws_ceil - np.median(np.diff(ws_ceil)) / 2
    ws_mean = (ws_freq * ws_center).sum()
    ws3_mean = (ws_freq * ws_center ** 3).sum()
    freq_gt_mean = _freq_gt_mean(ws_freq, ws_ceil, ws_mean)
    scale, shape = _fit03(ws_mean, ws3_mean, freq_gt_mean)
    return scale, shape  # A, k


def _freq_gt_mean(ws_freq, ws_ceil, ws_mean):
    """
    Calculate the fraction of probability mass
    that lie above the mean wind speed
    for a wind-speed histogram

    Parameters
    ----------
    ws_freq : ndarray
        1D array of size N containing data with "float" type.
        Frequencies for each histogram bin.
    ws_ceil : ndarray
        1D array of size N containing data with "float" type.
        histogram bin ceilings. Equal-size bins is assumed.
    ws_mean : float
        Mean wind speed

    Returns
    -------
    float:
        Probability mass above the mean wind speed.
        Fraction between 0 and 1.

    """
    ws_freq_cumsum = np.cumsum(ws_freq)
    return 1.0 - np.interp(ws_mean, ws_ceil, ws_freq_cumsum)


def _calc_fit03_cval(CNST, DEN, C):
    """Calculate value used for WAsP
    moments-bassed fitting algo.

    Parameters
    ----------
    CNST : float
        -log(ws3_mean) - 3*log(ws_mean))
    DEN : float
        log(-log(freq_gt_mean))
    C : float


    Returns
    -------
    float

    """
    cval = CNST + math.lgamma(1.0 + C) - DEN * C
    return cval


def _fit03(ws_mean, ws3_mean, freq_gt_mean):
    """WAsP Weibull fit algorithm using methods
    of moments

    Parameters
    ----------
    ws_mean : float
        First moment of wind speed (Mean wind speed)
    ws3_mean : float
        Third moment of wind speed
    freq_gt_mean : float
        Skewness term: frequency-mass that falls above
        the mean value

    Returns
    -------
    float, float
        Weibull scale and shape (A, k)
    """
    DEN = np.log(-np.log(freq_gt_mean))
    CNST = -(np.log(ws3_mean) - 3.0 * np.log(ws_mean))

    # Factor used to reduce/increase CL, CH, and CC in the effort to
    # approximate value
    FACT = 2.0

    # initial values of constants cl, ch, cc
    CL = 3.0 / 2.0
    CH = 3.0 / 2.0
    CC = 3.0 / 2.0

    one_third = 1.0 / 3.0
    eps = 0.003

    # The goal of step one is to get two constants (C1, C2) that correspond to
    # values on both 'sides' of 0 (i.e. one negative and one positive).
    cval = _calc_fit03_cval(CNST, DEN, CH)

    # ABS
    abs_cval = np.abs(cval)

    # SI, SL, and SH are used to store the sign of value at a given time.
    SI = np.sign(cval)
    SL = np.sign(cval)
    SH = np.sign(cval)

    CMAX = 30
    # The while loop below keeps iterating the constants CL, CH, CC
    # Until two of the constants represent value's that are negative and
    # positive respectively. Then those constants are used in the next
    # procedure.
    while (SI == SL) & (SH == SI):
        CI = CL
        CL = CI / FACT

        cval = _calc_fit03_cval(CNST, DEN, CL)

        if np.abs(cval) < abs_cval:
            abs_cval = np.abs(cval)
            CC = CL

        SL = np.sign(cval)

        if SL != SI:
            C1 = CI
            C2 = CL
            break

        CI = CH
        CH = CH * FACT

        if CH > CMAX:
            CI = CC
            k = 3.0 / CI
            A = (ws3_mean / math.gamma(1.0 + CI)) ** one_third
            return A, k

        cval = _calc_fit03_cval(CNST, DEN, CH)

        if np.abs(cval) < abs_cval:
            abs_cval = np.abs(cval)
            CC = CH

        SH = np.sign(cval)

        if SH != SI:
            C1 = CI
            C2 = CH

    # The procedure below lets the constants C1 and C2 approach each other
    # until the difference between them is small enough. Then the constant
    # that is found is used to derive k and A.
    diff = np.abs(C2 - C1)
    while diff > eps:

        CI = 0.5 * (C1 + C2)
        cval = _calc_fit03_cval(CNST, DEN, CI)

        if np.sign(cval) != SI:
            C2 = CI
        else:
            C1 = CI

        diff = np.abs(C2 - C1)

    k = 3.0 / CI
    A = (ws3_mean / math.gamma(1.0 + CI)) ** one_third

    return A, k


def _solve_k(x, first_moment=1, higher_moment=3):
    """WAsP Weibull fit algorithm using methods
    of moments

    Parameters
    ----------
    x : float
        Precalculated som of logs of moments
    first_moment : int
        First moment of wind speed
    higher_moment : int
        Higher moment of wind speed

    Returns
    -------
    float
        Weibull scale parameter
    """
    # Factor used to reduce/increase CL, CH, and CC in the effort to
    # approximate value
    FACT = 2.0

    # initial values of constants cl, ch, cc
    CL = 2.0
    CH = 2.0
    eps = 0.003

    # The goal of step one is to get two constants (C1, C2) that correspond to
    # values on both 'sides' of 0 (i.e. one negative and one positive).
    cval = _calc_cval(x, CL, higher_moment, first_moment)

    # ABS
    abs_cval = np.abs(cval)

    # SI, SL, and SH are used to store the sign of value at a given time.
    SI = np.sign(cval)
    SL = np.sign(cval)
    SH = np.sign(cval)

    # The while loop below keeps iterating the constants CL, CH, CC
    # Until two of the constants represent value's that are negative and
    # positive respectively. Then those constants are used in the next
    # procedure.
    while (SI == SL) & (SH == SI):
        CI = CL
        CL = CI / FACT
        cval = _calc_cval(x, CL, higher_moment, first_moment)

        if np.abs(cval) < abs_cval:
            abs_cval = np.abs(cval)

        SL = np.sign(cval)

        if SL != SI:
            C1 = CI
            C2 = CL
            break

        CI = CH
        CH = CH * FACT
        cval = _calc_cval(x, CH, higher_moment, first_moment)

        if np.abs(cval) < abs_cval:
            abs_cval = np.abs(cval)

        SH = np.sign(cval)

        if SH != SI:
            C1 = CI
            C2 = CH

    # The procedure below lets the constants C1 and C2 approach each other
    # until the difference between them is small enough. Then the constant
    # that is found is used to derive k and A.
    diff = np.abs(C2 - C1)
    while diff > eps:

        CI = 0.5 * (C1 + C2)
        cval = _calc_cval(x, CI, higher_moment, first_moment)

        if np.sign(cval) != SI:
            C2 = CI
        else:
            C1 = CI

        diff = np.abs(C2 - C1)

    return CI


def _solve_k_vec(sum, first_moment=1, higher_moment=3):
    """Solve k from weibull wind climate

    This is a vectorized version of `_solve_k`

    Parameters
    ----------
    sum : xr.DataArray
        xr.DataArray with sum of the log of moments
    first_moment : int
        First moment that is conserved when solving k
    higher_moment : int
        Higher moment that is conserved when solving k

    Returns
    -------
    ds : xr.DataArray
        Weibull shape parameter
    """
    ds = xr.apply_ufunc(
        _solve_k,
        sum,
        input_core_dims=[[]],
        output_core_dims=[[]],
        kwargs={"first_moment": first_moment, "higher_moment": higher_moment},
        vectorize=True,
        dask="allowed",
        keep_attrs=True,
    )
    return ds


def _calc_cval(x, c, powu, powl):
    """Calculate value used for WAsP
    moments-bassed fitting algo.

    Parameters
    ----------
    CNST : float
        -log(ws3_mean) - 3*log(ws_mean))
    DEN : float
        log(-log(freq_gt_mean))
    C : float

    Returns
    -------
    float
    """
    cval = x - math.lgamma(1.0 + powu / c) / powu + math.lgamma(1.0 + powl / c) / powl
    return cval


def weibull_moment(A, k, n=1):
    """Calculate moment for a weibull distribution.

    Parameters
    ----------
    A : xarray.DataArray
        Weibull scale parameter.
    k : xarray.DataArray
        Weibull shape parameter.
    n : int
        Moment to consider, defautls to 1.


    Returns
    -------
    xarray.DataArray
    """
    return A ** n * gamma(1.0 + n / k)


def get_weibull_probability(
    A: float, k: float, speed_range: np.ndarray, single_speed=False
):
    """Calculate Weibull probability.

    Parameters
    ----------
    A : float
        Scale parameter of the Weibull distribution.

    k :  float
        Shape parameter of the Weibull distribution.

    speed_range :  numpy.ndarray
        List of floats representing the wind speed bins contained in the binned
        "histogram" wind climate.

    single_speed : bool, optional
        Should the weibull probability be calculed for a single wind speed,
        default False.

        - True : Calculate the probability for the single wind speed defined by a
            single float element in the speed_range list.

        - False : Calculate the probability for the hole wind speed range defined.

    Returns
    -------
    speeds : numpy.ndarray
        List of floats representing the wind speed bins.

    prob : numpy.ndarray
        List of floats representing the Weibull probability for each element of
        the speeds list.
    """
    if single_speed:
        speeds = speed_range
    else:
        speeds = np.linspace(speed_range[0], speed_range[1], 500)

    if A == 0:
        return "0"
    elif k > 1.0:
        prob = (
            (k / A) * np.power(speeds / A, k - 1.0) * np.exp(-np.power(speeds / A, k))
        )
    elif k == 1:
        prob = (k / A) * np.power(-np.power(speeds / A, k))
    else:
        prob = (
            (k / A) * np.power(A / speeds, 1.0 - k) * np.exp(-np.power(speeds / A, k))
        )
        prob = np.where(speeds == 0, np.zeros_like(speeds), prob)
    return speeds, prob
