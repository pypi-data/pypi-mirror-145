# (c) 2022 DTU Wind Energy
"""
Generalized wind climate module

This module contains the various functions for working with generalized wind climates.

Currently this only supports creating gwc datasets from .lib files or from
NetCDF files. In the future we will also support the ability to read in .gwc
files.
"""

import logging
from pathlib import Path
from functools import wraps
import re
from turtle import up

from lxml import etree
import numpy as np
import xarray as xr
from ._validate import create_validator
from .metadata import (
    ALL_VARS_META,
    _WEIB_ATTRS,
    create_coords,
    update_var_attrs,
    update_history,
)
from .sector import create_sector_coords
from .spatial import create_dataset, crs_are_equal, to_point, reproject

_GEN_COORDS_META = {
    "gen_height": ALL_VARS_META["gen_height"],
    "gen_roughness": ALL_VARS_META["gen_roughness"],
}

DATA_VAR_DICT_GWC = {
    "A": ["sector", "gen_height", "gen_roughness"],
    "wdfreq": ["sector", "gen_roughness"],
    "k": ["sector", "gen_height", "gen_roughness"],
}

REQ_DIMS_GWC = ["sector", "gen_height", "gen_roughness"]

REQ_COORDS_GWC = [
    "south_north",
    "west_east",
    "gen_height",
    "gen_roughness",
    "sector_ceil",
    "sector_floor",
    "sector",
    "crs",
]

gwc_validate, gwc_validate_wrapper = create_validator(
    DATA_VAR_DICT_GWC, REQ_DIMS_GWC, REQ_COORDS_GWC
)


@gwc_validate_wrapper
def lib_string(gwc):
    """Generates string representation of gwc dataset.

    Parameters
    ----------
    gwc: xarray.Dataset
        Dataset containing A, k, and wdfreq.
        Dimensions should be ('gen_height', 'gen_roughness', 'sector')

    Returns
    -------
    str
        String representation of gwc dataset.

    """

    def _fmt_floats(dat, prec=3, extra=False):
        """
        Format a list of floats into a common format

        Parameters
        ----------
        dat: list
            List of floats to be formatted
        prec: int
            Precision of output string
            Default set to 3
        extra: bool
            Extra space between characters
            Default set to False (i.e., no extra space)

        Returns
        -------
        str
            String containing space separated floats
        """

        sep = " " if extra else ""
        fmt = "{0:9.%df}" % prec

        return sep.join([fmt.format(i) for i in dat])

    def _to_string(node):
        """Generates string representation of gwc dataset

        Parameters
        ----------
        node : xarray.Dataset
            Dataset containing A, k, and wdfreq.
            Dimesions should be ('height', 'roughness', 'sector')

        Returns
        -------
        str
            String representation of xarray dataset
        """

        nrough = node.dims["gen_roughness"]
        nhgt = node.dims["gen_height"]
        nsec = node.dims["sector"]
        node = node.transpose(..., "gen_height", "gen_roughness", "sector")
        node = reproject(node, 4326)
        string = ""
        lend = "\n"  # Always use windows line ending

        try:
            height = node.height
        except AttributeError:
            height = 0.0

        # Write the header
        header_without_coord = re.sub(
            "<coordinates>(.*)</coordinates>", "", node.attrs["wasp_header"]
        )
        string += (
            header_without_coord
            + f"<coordinates>{float(node.west_east)},{float(node.south_north)},{float(height)}</coordinates>{lend}"
        )

        # Write the dimensions nz0,nz,nsec
        string += " ".join([str(i) for i in (nrough, nhgt, nsec)]) + lend

        # Write the roughness classes
        string += _fmt_floats(node.gen_roughness.values, 3, True) + lend

        # Write the heights
        string += _fmt_floats(node.gen_height.values, 1, True) + lend

        # Write the data arrays
        for i, _ in enumerate(node.gen_roughness.values):

            # sectorwise frequency
            string += _fmt_floats(node.wdfreq.isel(gen_roughness=i).values, 2) + lend

            for j, _ in enumerate(node.gen_height.values):

                # Sectorwise A's
                string += (
                    _fmt_floats(node.A.isel(gen_height=j, gen_roughness=i).values, 2)
                    + lend
                )

                # Sectorwise k's
                string += (
                    _fmt_floats(node.k.isel(gen_height=j, gen_roughness=i).values)
                    + lend
                )

        return string

    if gwc.squeeze().A.ndim == 3:
        return _to_string(gwc.squeeze())

    dims_extra = [
        d for d in gwc.A.dims if d not in ["gen_height", "gen_roughness", "sector"]
    ]
    stacked = gwc.stack(point=dims_extra)

    # Get numbers of sectors, roughness classes and
    strings = []
    for ipt in range(stacked.dims["point"]):
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        strings.append(_to_string(node))

    return strings


@gwc_validate_wrapper
def to_libfile(gwc, path=None):
    """Creates lib-style ascii file from gwc dataset

    Parameters
    ----------
    gwc : xarray.Dataset
        Generalized wind climate dataset.
    path : str
        dir or file path for storing lib file
        Default value set to the current working directory.
    """

    def _write(node, fpath):
        with open(fpath, "w", newline="\r\n") as fobj:
            fobj.write(lib_string(node))

    if path is None:
        path = Path.cwd()

    if gwc.squeeze().A.ndim == 3:
        if Path(path).is_dir():
            fpath = Path(path) / "gwc.lib"
        else:
            fpath = path
        _write(gwc.squeeze(), fpath)
        return

    # If dataset has extra dimensions (of size > 1):
    # Stack extra dimensions, loop over them, and write to tab files
    # Using file_name that contains coordinate information.
    dims_extra = [
        d for d in gwc.A.dims if d not in ["gen_height", "gen_roughness", "sector"]
    ]
    stacked = gwc.stack(point=dims_extra)

    # Create file_name format string
    if Path(path).is_dir():
        file_name_fmt = (
            "_".join(["gwc"] + [f"{d}" + "{" + f"{d}" + "}" for d in dims_extra])
            + ".lib"
        )

    # Loop and write to tab files
    for ipt in range(stacked.dims["point"]):
        node = stacked.isel(point=slice(ipt, ipt + 1)).reset_index("point").squeeze()
        kwds = {d: node[d].values for d in dims_extra}
        fpath = path / file_name_fmt.format(**kwds)
        _write(node, fpath)

    return


def read_gwc(file_or_obj, crs=None, coords=None):
    """Create gwc xarray.Dataset from file.

    Parameters
    ----------
    file : str or Path
        Path to a file that can be opened a gwc. This includes .lib, .gwc, and
        .nc files that were created as gwc files. The script will use the file
        extension to determine the file type and then parse it into a gwc object.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum). for .lib and .gwc.
    coords : tuple
        Coordinates of the .lib file. (west_east, south_north, height)
        By default this will try to read a coordinates field from the header.

    Returns
    -------
    xarray.Dataset
        Generalized wind climate dataset.
    """
    file_or_obj = Path(file_or_obj)
    ext = file_or_obj.suffix

    if ext == ".lib":
        if crs is None:
            crs = 4326
        ds = _open_libfile(file_or_obj, crs, coords)
    elif ext in [".gwc"]:
        if crs is None:
            crs = 4326
        tree = etree.parse(str(file_or_obj))
        ds = _parse_gwc(tree.getroot(), crs)
    elif ext in [".nc"]:
        ds = xr.open_dataset(file_or_obj)
        gwc_validate(ds)
        if crs is not None and not crs_are_equal(ds, crs):
            raise ValueError(f"Requested crs does not match dataset crs")
        ds
    else:
        raise ValueError(
            f"Unable to detect type of gwc file {file_or_obj} with extension {ext}."
        )

    ds = update_var_attrs(ds, _WEIB_ATTRS)
    return update_history(ds)


def _open_libfile(lib_file, crs=4326, xyz_coords=None):
    """
    Create GenWindClimate object from WAsP .lib file

    Parameters
    ----------
    lib_file : str, pathlib.Path
        Path to lib file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon on the WGS84 geodetic datum)
    xyz_coords : tuple
        Coordinates of of the .lib file. (west_east, south_north, height)
        By default this will try to read a coordinates field from the header

    Returns
    -------
    xr.DataSet
        xarray DataSet that is formatted to match the gwc description

    Notes
    -----
    Automatically adds lat, lon coords if present inside
    <coordinates>lon,lat,height<\coordinates> brackets
    """

    def _read_float_(f):
        """Reads a line of space separated data and splits it into floats

        Parameters
        ----------
        f : file
            Object with method readline

        Returns
        -------
        list
            List of floats
        """
        return [np.float32(i) for i in f.readline().strip().split()]

    def _read_int_(f):
        """Reads a line of space-separated data and splits it into integers

        Parameters
        ----------
        f : file
            Object with method readline

        Returns
        -------
        list
            List of integers
        """
        return [np.int32(i) for i in f.readline().strip().split()]

    # Open libfile
    with open(lib_file, newline="\r\n") as f:

        # Read header information one line at a time
        desc = f.readline().strip()  # File Description
        nrough, nhgt, nsec = _read_int_(f)  # dimensions
        roughnesses = _read_float_(f)  # Roughness classes
        heights = _read_float_(f)  # heights

        # Initialize arrays
        freq = np.zeros([nrough, nsec], dtype="f4", order="F")
        k = np.zeros([nhgt, nrough, nsec], dtype="f4", order="F")
        A = np.zeros([nhgt, nrough, nsec], dtype="f4")

        ##################################################################
        # The remainder of the file is made up of rows with nsec columns.
        # For each height there is first a frequency row, then pairs of
        # A & k rows for each height.
        ##################################################################
        # Loop over roughness classes to read frequency line
        for i, dummy in enumerate(roughnesses):
            freq[i, :] = _read_float_(f)
            # Loop over heights to read in all A & k values
            for j, dummy in enumerate(heights):
                A[j, i, :] = _read_float_(f)
                k[j, i, :] = _read_float_(f)

    ak_dims = ("gen_height", "gen_roughness", "sector", "point")
    f_dims = ("gen_roughness", "sector", "point")

    # Find the coordinates if they aren't provided
    if xyz_coords is None:
        # Find the coordinates
        latlons = re.search("<coordinates>(.*)</coordinates>", desc)
        if latlons:
            lon, lat, height = map(np.float32, latlons.group(1).split(","))
        else:
            raise ValueError(
                f"Coordinates array not found in file {lib_file}, "
                + "please set coords argument."
            )
    else:  # Use user provided coordinates
        lon, lat, height = xyz_coords

    # Create dataset
    ds = create_dataset(lon, lat, height, crs).drop_vars("output")
    ds.attrs = {"wasp_header": desc}

    # Add variables
    ds["A"] = (ak_dims, np.reshape(A, A.shape + (1,)))
    ds["k"] = (ak_dims, np.reshape(k, k.shape + (1,)))
    ds["wdfreq"] = (f_dims, np.reshape(freq, freq.shape + (1,)))

    # Add coordinates
    ds = ds.assign_coords(
        {
            **create_coords(heights, "gen_height", _GEN_COORDS_META).coords,
            **create_coords(roughnesses, "gen_roughness", _GEN_COORDS_META).coords,
            **create_sector_coords(nsec).coords,
        }
    )

    return ds


def _weibull_to_dataset(
    wdfreq,
    A,
    k,
    gen_roughness,
    gen_height,
    south_north,
    west_east,
    height,
    crs,
    **kwargs,
):
    """
    Converts parsed xml gwc object to WindKit gwc xarray dataset

    Parameters
    ----------
    wdfreq : numpy
        Wind direction frequency by sector and generalized roughnesses
    A : numpy
        Weibull A parameter by sector and generalized roughness and height
    k : numpy
        Weibull k parameter by sector and generalized roughness and height
    gen_roughness : numpy
        Array of generalized roughnesses
    gen_height : numpy
        Array of generalized heights
    south_north: float64
        Coordinate value in y-direction
    west_east: float64
        Coordinate value in x-direction
    height: float64
        Height above ground
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    kwargs : dict, optional
        Other key-word arguments are added as attributes to the dataset.

    Returns
    -------
    xarray.Dataset
        WindKit GWC dataset
    """

    nsec, _ = wdfreq.shape

    na = np.newaxis

    wdfreq /= np.sum(wdfreq)

    # Create dataset
    ds = create_dataset(west_east, south_north, height, crs).drop_vars("output")
    ds.attrs = kwargs

    # Add variables
    ak_dims = ("sector", "gen_height", "gen_roughness", "point")
    f_dims = ("sector", "gen_roughness", "point")
    ds["A"] = (ak_dims, A[:, :, :, na])
    ds["k"] = (ak_dims, k[:, :, :, na])
    ds["wdfreq"] = (f_dims, wdfreq[:, :, na])

    # Add coordinates
    ds = ds.assign_coords(
        {
            **create_coords(gen_height, "gen_height", _GEN_COORDS_META).coords,
            **create_coords(gen_roughness, "gen_roughness", _GEN_COORDS_META).coords,
            **create_sector_coords(nsec).coords,
        }
    )

    return ds.transpose("gen_height", "gen_roughness", "sector", "point")


def _parse_gwc(gwc, crs=4326):
    """
    Parses an gwc XML file into a gwc object

    Parameters
    ----------
    gwc : xml tree
        An XML element loaded by lxml
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        Defaults to 4326 (Lat-Lon/WGS84 geodetic datum)

    Returns
    -------
    xr.DataSet
        xarray DataSet that is formatted to match the gwc description
    """
    # Get site info
    site_info = gwc.xpath("//RveaAnemometerSiteDetails")[0].attrib
    height = float(site_info["HeightAGL"])
    header = site_info["Description"]
    lat = float(site_info["LatitudeDegrees"])
    lon = float(site_info["LongitudeDegrees"])

    # Subset GWC to only GWC information (drop children)
    gwc = gwc.xpath("./MemberData/RveaGeneralisedMeanWindClimate")[0]

    # Get main dimensions
    num_sec = int(gwc.attrib["CountOfSectors"])
    num_gen_height = int(gwc.attrib["CountOfReferenceHeights"])
    num_gen_roughness = int(gwc.attrib["CountOfReferenceRoughnessLengths"])

    # Create arrays
    wdfreq = np.zeros((num_sec, num_gen_roughness))
    A = np.zeros((num_sec, num_gen_height, num_gen_roughness))
    k = np.zeros((num_sec, num_gen_height, num_gen_roughness))
    cen_angle = np.zeros(num_sec)
    gen_roughness = np.zeros(num_gen_roughness)
    gen_height = np.zeros(num_gen_height)

    # Get wind speed histogram
    for wawwr in gwc.xpath("WindAtlasWeibullWindRose"):
        # Get array info information

        rough_no = int(wawwr.attrib["RoughnessLengthNumber"]) - 1
        height_no = int(wawwr.attrib["ReferenceHeightNumber"]) - 1

        gen_height[height_no] = float(wawwr.attrib["ReferenceHeight"])
        gen_roughness[rough_no] = float(wawwr.attrib["RoughnessLength"])
        for ww in wawwr.xpath("WeibullWind"):
            sec = int(ww.attrib["Index"]) - 1
            cen_angle[sec] = float(ww.attrib["CentreAngleDegrees"])
            A[sec, height_no, rough_no] = float(ww.attrib["WeibullA"])
            k[sec, height_no, rough_no] = float(ww.attrib["WeibullK"])
            wdfreq[sec, rough_no] = float(ww.attrib["SectorFrequency"])

    kwargs = {
        "gen_roughness": gen_roughness,
        "gen_height": gen_height,
        "south_north": lat,
        "west_east": lon,
        "height": height,
        "wasp_header": header,
        "crs": crs,
    }
    return _weibull_to_dataset(wdfreq, A, k, **kwargs)


@gwc_validate_wrapper
def reproject_gwc(gwc, to_crs):
    """Reprojects Generalized wind climate dataset.

    Parameters
    ----------
    gwc: xarray.Dataset
        Valid GWC dataset.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`

    Returns
    -------
    xarray.Dataset
        Point based generalized wind climate dataset in new projection.
    """
    if not crs_are_equal(gwc, to_crs):
        return reproject(gwc, to_crs)

    # Return point based dataset even if not reprojected
    ds = to_point(gwc)
    return update_history(ds)
