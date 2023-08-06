# (c) 2022 DTU Wind Energy
"""
Wind Turbine classs defines the parameters of a certain type of wind turbine.
rofl copied this from the FARMOPT repository.

Created on Wed Sep  6 14:30:28 2017

@author: jufen

UPDATE 8 July 2021 by @btol: added xarray.dataset wind turbine structure
"""
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import xarray as xr


def _read_windpro_wtg_element(wt_element):
    """Parse the ET element from WindPRO to initilize an WT_cls object.

    Parameters
    ----------
    WT_element : ET element
        Extracted from .xml file in the .optireq file from WindPRO.

    Returns
    -------
    WT : an object of WT_cls
    """
    name = wt_element.attrib["TurbineTypeUID"]
    diameter = np.float64(wt_element.attrib["RotorDiameter"])
    hub_height = np.float64(wt_element.attrib["HubHeight"])

    turbine_modes = wt_element.findall("TurbineMode")
    num_modes = len(turbine_modes)
    wind_speed_cutin = [0.0 for i in range(num_modes)]
    wind_speed_cutout = [0.0 for i in range(num_modes)]
    air_density = [1.225 for i in range(num_modes)]
    dts = [None for i in range(num_modes)]
    mode_ids = [None for i in range(num_modes)]
    for i in range(num_modes):
        turbine_mode = turbine_modes[i]
        air_density[i] = np.float64(turbine_mode.attrib["AirDensity"])
        mode_ids[i] = turbine_mode.attrib["ModeID"]
        wind_speed_cutout[i] = turbine_mode.attrib["StopWindSpeed"]

        power_curve = turbine_mode.find("PowerCurve")
        thrust_curve = turbine_mode.find("ThrustCurve")

        pc = []
        for data in power_curve.findall("Data"):
            ws = np.float64(data.attrib["windSpeed"])
            power = np.float64(data.attrib["power"])
            pc.append([ws, power])

        tc = []
        for data in thrust_curve.findall("Data"):
            ws = np.float64(data.attrib["windSpeed"])
            Ct = np.float64(data.attrib["CT"])
            tc.append([ws, Ct])

        if pc[0][1] == 0:
            pc = pc[1:]

        assert len(pc) == len(tc)
        pc = np.array(pc)
        tc = np.array(tc)

        dt = np.hstack((tc, pc))
        dt = dt[:, (0, 1, 3)]

        dts[i] = dt
        wind_speed_cutin[i] = tc[0, 0]

    rated_power = np.max(dts[0][:, 2])

    # change kW to W for wind speed
    if rated_power > 100:
        rated_power = rated_power * 1000
        for dt in dts:
            dt[:, -1] = dt[:, -1] * 1000

    rated_power = np.max(dts[0][:, 2])

    wind_speed_curves = np.array(dts)

    n_modes, n_wspd, n_vars = wind_speed_curves.shape
    wind_speed = wind_speed_curves[0, :, 0]
    thrust_coefficient = wind_speed_curves[:, :, 1]
    power_output = wind_speed_curves[:, :, 2]

    wtg = xr.Dataset(
        data_vars={
            "name": name,
            "rotor_diameter": diameter,
            "hub_height": hub_height,
            "wind_speed_cutin": (("mode",), wind_speed_cutin),
            "wind_speed_cutout": (("mode",), wind_speed_cutout),
            "rated_power": (("mode",), rated_power),
            "power_output": (("mode", "wind_speed"), power_output),
            "thrust_coefficient": (("mode", "wind_speed"), thrust_coefficient),
        },
        coords={
            "wind_speed": (("wind_speed",), wind_speed),
            "mode": (("mode",), np.arange(n_modes)),
            "air_density": (("mode",), air_dens),
        },
    )

    return wtg


def _read_windpro_wtg(wtg_file):
    """Read a windpro-formatted XML ".wtg" file.

    Parameters
    ----------
    wtg_file : string, pathlib.Path
        A string or pathlib.Path denoting the location of the .wtg file

    Returns
    -------
    xr.Dataset
        Wind Turbine Generator dataset as an xarray.Dataset

    """
    tree = ET.parse(wtg_file)
    root = tree.getroot()
    return _read_windpro_wtg_element(root)


def _wasp_wtg_data_points_to_dataset(data_points):
    """Read power and ct curves from the
    "DataPoint" part of a wasp xml WTG object

    Parameters
    ----------
    data_points : ET element
        "DataPoint" element from WAsP WTG ET

    Returns
    -------
    xr.Dataset
        power and ct curves formatted as xarray.Dataset for a
        specific turbine mode
    """
    wind_speed = []
    power_output = []
    thrust_coeff = []
    for row in data_points:
        wind_speed.append(float(row.attrib["WindSpeed"]))
        power_output.append(float(row.attrib["PowerOutput"]))
        thrust_coeff.append(float(row.attrib["ThrustCoEfficient"]))
    return xr.Dataset(
        {
            "power_output": (("wind_speed",), power_output),
            "thrust_coefficient": (("wind_speed",), thrust_coeff),
        },
        coords={"wind_speed": (("wind_speed",), wind_speed)},
    )


def _read_wasp_wtg_element(wtg_element):
    """Convert a wasp-formatted XML WindTurbineGenator element
    to a WindKit wtg xarray.Dataset.

    Parameters
    ----------
    wtg_element : WTG  ET element
        Extracted from WindTurbineGenerator element of
        the .xml object in the .wwh file.

    Returns
    -------
    xr.Dataset
        Wind Turbine Generator dataset as an xarray.Dataset

    """
    datasets = []
    for mode, table in enumerate(wtg_element.iter("PerformanceTable")):
        ds = _wasp_wtg_data_points_to_dataset(table.iter("DataPoint"))
        ds = ds.assign_coords(mode=(("mode",), [mode]))
        ds["air_density"] = np.float64(table.attrib["AirDensity"])
        if "StationaryThrustCoEfficient" in table.attrib:
            ds["stationary_thrust_coefficient"] = np.float64(
                table.attrib["StationaryThrustCoEfficient"]
            )
        ds["wind_speed_cutin"] = np.float64(
            table.find("StartStopStrategy").attrib["LowSpeedCutIn"]
        )
        ds["wind_speed_cutout"] = np.float64(
            table.find("StartStopStrategy").attrib["HighSpeedCutOut"]
        )
        ds["rated_power"] = ds["power_output"].max()
        datasets.append(ds)

    merged = xr.concat(datasets, dim="mode")
    merged["name"] = wtg_element.attrib["Description"]
    merged["rotor_diameter"] = np.float64(wtg_element.attrib["RotorDiameter"])
    merged["hub_height"] = np.float64(
        wtg_element.find("SuggestedHeights").find("Height").text
    )

    return merged


def _read_wasp_wt_element(wt_element):
    """Convert a wasp-formatted XML element to a WindKit wtg xr.Dataset.

    Parameters
    ----------
    wt_element : ET WT element
        Extracted from .xml object in the .wwh file.

    Returns
    -------
    xr.Dataset
        Wind Turbine Generator dataset as an xarray.Dataset

    """
    root = wt_element.find(".//WindTurbineGenerator")
    return _read_wasp_wtg_element(root)


def _read_wasp_wtg(wtg_file):
    """Read a wasp-formatted XML ".wtg" file.

    Parameters
    ----------
    wtg_file : string, pathlib.Path
        A string or pathlib.Path denoting the location of the .wtg file

    Returns
    -------
    xr.Dataset
        Wind Turbine Generator dataset as an xarray.Dataset

    """
    tree = ET.parse(wtg_file)
    root = tree.getroot()

    return _read_wasp_wtg_element(root)


def read_wtg(wtg_file, file_format="wasp"):
    """Read in Wind Turbine Generator (WTG) data from a file.

    A WTG dataset contains the following:

    coordinates(dim):
        wind_speed(wind_speed) : wind speed
        mode(mode)             : each mode reprents different ct/power curves
        air_density(mode)      : Air density of mode

    variables(dims):
        name                                  : name of the WTG
        rotor_diameter                        : rotor diameter in meters
        hub_height                            : hub height a.g.l. in meters
        wind_speed_cutin(mode)                : Wind speed cutin
        wind_speed_cutout(mode)               : Wind speed cutout
        rated_power(mode)                     : Rated power
        power_output(mode, wind_speed)        : Power output
        thrust_coefficient(mode, wind_speed)  : Thrust coefficient

    Parameters
    ----------
    wtg_file : str, pathlib.Path
        WTG file to read

    file_format : str
        XML file format to use. Only "wasp" formatting is
        supported currently.

    Returns
    -------
    xr.Dataset
        WTG dataset

    """
    wtg_file = Path(wtg_file)
    ext = wtg_file.suffix
    if ext == ".wtg":
        if file_format == "wasp":
            return _read_wasp_wtg(wtg_file)
        # elif file_format == "windpro":
        #     return _read_windpro_wtg(wtg_file)
    else:
        raise ValueError(
            f"File extension: {ext} not recognized as wind turbine generator!"
        )


def wtg_power(wtg, ws, mode=None, interp_method="linear"):
    """Get power output when the inflow wind speed is ws. If the
    given wind speed does not have an associated power output,
    it is linearly interpolated between data points.

    Parameters
    ----------
    wtg : xr.Dataset
        WindKit Wind Turbine Generator (WTG) Dataset
    ws : array_like, floats
        Wind speeds to obtain WTG power for.
    mode : integer, optional
        Operation mode, None by default
    interp_method : str
        Interpolation method to use between provided table values.
        Uses xr.DataArray.interp

    Returns
    -------
    xr.DataArray
        Power for the given wind speeds

    Raises
    ------
    ValueError
        If the wtg contains more than one mode and no mode is set, raises error.
    """

    if "mode" in wtg.dims:
        if mode is None:
            n_mode = wtg["mode"].size
            if n_mode > 1:
                raise ValueError(
                    "wtg objects has more than one mode. "
                    + "Please select the mode using the 'mode' kwarg!"
                )
            mode = 0
        wtg = wtg.isel(mode=mode)

    return wtg["power_output"].interp(
        wind_speed=ws,
        method=interp_method,
        kwargs={"fill_value": 0.0, "bounds_error": False},
    )


def wtg_ct(wtg, ws, mode=None, interp_method="linear"):
    """Get the thrust coefficient of a Wind Turbine Generator
    for given wind speed(s). If the given wind speed(s) do not
    have an associated thrust coefficient, it is interpolated
    between data points.

    Parameters
    ----------
    wtg : xr.Dataset
        WindKit Wind Turbine Generator (WTG) Dataset
    ws : array_like, floats
        Wind speeds to obtain WTG power for.
    mode : integer, optional
        Operation mode, None by default
    interp_method : str
        Interpolation method to use between provided table values.
        Uses xr.DataArray.interp

    Returns
    -------
    xr.DataArray
        Thrust coefficients for the given wind speeds

    Raises
    ------
    ValueError
        If the wtg contains more than one mode and no mode is set, raises error.
    """
    if "mode" in wtg.dims:
        if mode is None:
            n_mode = wtg["mode"].size
            if n_mode > 1:
                raise ValueError(
                    "wtg objects has more than one mode. "
                    + "Please select the mode using the 'mode' kwarg!"
                )
            mode = 0
        wtg = wtg.isel(mode=mode)

    if "stationary_thrust_coefficient" in wtg.data_vars:
        ct_min = wtg["stationary_thrust_coefficient"]
    else:
        ct_min = wtg["thrust_coefficient"].min(dim="wind_speed")

    return wtg["thrust_coefficient"].interp(
        wind_speed=ws,
        method=interp_method,
        kwargs={"fill_value": ct_min, "bounds_error": False},
    )
