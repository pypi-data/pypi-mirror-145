# (c) 2022 DTU Wind Energy
"""
Contains class and class methods to manipulate topographic raster files

The data is read using rasterio, so all raster formats are supported, but only
GRD files are able for output. Data is stored in an xarray.DataArray.
"""
import logging
import os

import numpy as np
import pyproj
import xarray as xr

from .geospatial_imports import has_rasterio, requires_rasterio

if has_rasterio:
    import rasterio as rio

from .landcover import LandCoverTable
from .metadata import _MAP_TYPE_ATTRS, update_history, update_var_attrs
from .spatial import add_crs, clip, crs_are_equal
from .vector_map import _MAP_TYPE_CODES

logger = logging.getLogger(__name__)

RASTERMAP_FILE_EXTENSIONS = [".nc", ".grd", ".tif"]

__all__ = [
    "read_raster_map",
    "raster_map_to_file",
]


def _fix_rio_crs(crs):
    """rasterio is still returning the CRS as an attribute with the old format"""
    return crs.split("=")[1].upper() if crs.startswith("+init=epsg") else crs


# Read raster_maps from different formats
def _read_raster_map_rio(filename, crs=None, zip_file=None):
    """
    Create a raster from 1-band GIS files able to be read by rasterio.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to file (on disk or in zipfile)
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS` (Default: read from file)
    zip_file : ZipFile
        ZipFile object to extract mapfile from

    Returns
    -------
    xarray.DataArray
        Raster object converted to WindKit conventions
    """
    logger.info("Reading raster_map %s using _read_raster_map_rio", filename)
    filename = str(filename)

    # Format zipfile for user (This should move to a generic function windkit#98)
    if zip_file is not None:  # pragma: no cover unsure
        filename = "zip://{" + zip_file.filename + "}!" + filename

    # Open file and format the match our expected coordinate names
    da = xr.open_rasterio(filename).squeeze().drop_vars("band")
    da = da.rename({"x": "west_east", "y": "south_north"})

    # Ensure that data goes from south to north
    if da.attrs["transform"][4] < 0:
        da = da.sortby("south_north")

    # Add CRS to object using CF conventions
    if crs is None:
        if "crs" not in da.attrs:
            err = f"Need to supply crs for file {filename}."
            raise ValueError(err)
        else:
            crs = _fix_rio_crs(da.attrs["crs"])
    else:
        # Check that file crs matches provided
        if "crs" in da.attrs:
            if not crs_are_equal(_fix_rio_crs(da.attrs["crs"]), crs):
                err = f"Supplied crs {crs}, does not match file crs."
                raise ValueError(err)
            # Remove attribute crs so we can add it as a variable
            del da.attrs["crs"]

    add_crs(da, crs)

    # Check that raster is square
    dx = da.attrs["transform"][0]
    dy = da.attrs["transform"][4]
    if round(abs(dx), 8) != round(abs(dy), 8):  # needs_test
        info_mes = f"""For RasterMap's dx ({dx}) and dy ({dy}) must
        be equal. There are differences after the 7 digit, but we
        will continue. Make sure this is the desired behaviour"""
        logging.info(info_mes)
    if round(abs(dx), 4) != round(abs(dy), 4):  # needs_test
        raise ValueError(f"For RasterMap's dx ({dx}) and dy ({dy}) must be equal.")

    # Remove rasterio attributes
    da.attrs = {}

    return da


def _read_raster_map_netcdf(filename, crs=None, **kwargs):
    """
    Create a raster from 1-variable 1-band netcdf file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to file
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS` (Default: read from file)
    kwargs :
        Additional keyword arguments passed to open_dataarray

    Returns
    -------
    xarray.DataArray
        raster object
    """
    da = xr.open_dataarray(str(filename), **kwargs)

    # CRS check or add
    if crs is None:  # needs_test
        if "crs" not in da.coords:
            err = f"Need to supply crs for file {filename}."
            raise ValueError(err)
    else:  # needs_test
        # Check that file crs matches provided
        if "crs" in da.coords:
            if not crs_are_equal(da, crs):
                err = f"Supplied crs {crs}, does not match file crs."
                raise ValueError(err)
        else:
            add_crs(da, crs)

    return da


def read_raster_map(
    filename, crs=None, map_type=None, clip_bbox=None, dtype=None, **kwargs
):
    """
    Create a raster from 1-band rasterfile.

    GIS files are opened with rasterio
    .nc files are opened with xarray, but only single variable files are handled.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to file (on disk or in zipfile)
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS` (Default: read from file)
    map_type : str
        name of the map one of (elevation, roughness, or landcover). Defaults to None.
    clip_bbox : shapely.geometry.LinearRing
        Linear Ring that forms a bounding box, must have the same crs as
        the raster that is being read. Defaults to None.
    dtype : numpy.dtype
        The type of the output array. If dtype is not given the file will determine it.
        Defaults to None.
    **kwargs : dict
        Additonal keyword arguments passed to reader.

    Returns
    -------
    xarray.DataArray, LandCoverTable
        raster_map object, if roughness map_type specified it will also return a
        LandCoverTable that maps the roughness values to IDs.
    """
    file_ext = os.path.splitext(str(filename))[1]
    if file_ext == ".nc":
        da = _read_raster_map_netcdf(filename, crs=crs, **kwargs)
    else:
        da = _read_raster_map_rio(filename, crs=crs, **kwargs)

    # Set the map_type as the name of the DataArray
    map_types = _MAP_TYPE_CODES.keys()
    if map_type is None:
        if file_ext != ".nc" or da.name not in map_types:  # needs_test
            raise ValueError(
                "Unable to determine map_type from file, please set map_type."
            )
    else:
        if da.name in map_types and da.name != map_type:  # needs_test
            raise ValueError(
                f"Provided map_type {map_type}, does not match file map_type {da.name}"
            )
        da.name = map_type

    # Clip data if requested
    if clip_bbox is not None:  # pragma: no cover already_tested_in_other_module
        da = clip(da, clip_bbox)

    # Change datatype if requested
    if dtype is not None:
        da = da.astype(dtype)

    # We never deal with roughness maps internally, always landcover
    if da.name == "roughness":
        da, lct = _raster_map_to_landcover(da)

        return update_var_attrs(da, _MAP_TYPE_ATTRS), lct

    ds = update_var_attrs(da, _MAP_TYPE_ATTRS)
    return update_history(ds)


# Oputput raster_maps in different formats
def _raster_map_to_riofile(da, filename):
    """
    Write raster to a GRD or geotiff file using rasterio.

    Parameters
    ----------
    da : xarray.DataArray
        Raster to write.
    filename : str or pathlib.Path
        Path to file.
    """
    requires_rasterio()

    filename = str(filename)
    file_ext = os.path.splitext(filename)[1]

    if file_ext == ".tif":
        driver = "GTiff"
    elif file_ext == ".grd":
        driver = "GSAG"

    x, y = da.west_east.values, da.south_north.values

    resx = x[1] - x[0]
    resy = y[1] - y[0]

    if np.abs(resx) != np.abs(resy):  # needs_test
        logging.warning("Resolution in x and y are not the same!")

    nx, ny = len(x), len(y)
    minx = x[0]
    miny = y[0]

    # Build Affine Transformation
    hresx = resx / 2.0
    hresy = resy / 2.0

    affine = rio.Affine(resx, 0, minx - hresx, 0, resy, miny - hresy)

    f_crs = pyproj.CRS.from_cf(da.crs.attrs)
    crs = rio.crs.CRS.from_user_input(f_crs.to_string())

    with rio.open(
        filename,
        "w",
        driver=driver,
        height=ny,
        width=nx,
        count=1,
        dtype=da.dtype,
        crs=crs,
        transform=affine,
    ) as new_ds:
        new_ds.write(da, 1)


def _raster_map_to_netcdf(da, filename, **kwargs):
    """
    Write raster to a netcdf file using xarray.

    Parameters
    ----------
    da : xarray.DataArray
        Raster to write.
    filename : str or pathlib.Path
        Path to file.

    """
    ds = update_var_attrs(da.to_dataset(), _MAP_TYPE_ATTRS)

    ds.to_netcdf(filename, **kwargs)


def raster_map_to_file(
    da, filename, lctable=None, lctable_var="id", save_lctable=False, **kwargs
):
    """
    Write raster to a Surfer ASCII Grid (GRD), geotiff or netcdf file.

    We recommend that unless you have a need for another format, that you write to
    netcdf, as this preserves all the metadata of the file. Next would be geotiff, and
    finally use GRD if you need compatability with tools that only support that format.

    Parameters
    ----------
    da : xarray.DataArray
        Raster to write.
    filename : str or pathlib.Path
        Path to file.
    lctable : LandCoverTable
        LandCoverTable used to write out landcover fields, required for landcover maps.
        Defaults to None.
    lctable_var : str
        If writing an lctable, you can specify the variable that you want to write
        to file. Defaults to "id".
    save_lctable : bool
        Save lctable table to a json file of the same name as the output file to retain
        all landcover metadata?. Defaults to False.
    kwargs : dict
        Extra arguments.
    """

    filename = str(filename)
    file_root, file_ext = os.path.splitext(filename)

    # Handle special case of landcover
    if da.name == "landcover":
        da = da.copy()
        out_vals = _landcover_to_roughness(da, lctable, lctable_var)
        da.values = out_vals

        if save_lctable:
            lctable.to_json(file_root + ".json")

    if file_ext in [".grd", ".tif"]:
        _raster_map_to_riofile(da, filename, **kwargs)
    elif file_ext == ".nc":
        _raster_map_to_netcdf(da, filename, **kwargs)
    else:
        raise ValueError(
            f"Filename extension is '{file_ext}' must be "
            + "one of '.nc', '.grd' or '.tif'."
        )


# Deal with roughness maps
def _roughness_to_landcover(arr):
    """converts a roughness map to landcover returns da, lctable

    Returns
    -------
    np.array, LandCoverTable
    """
    z0s = np.unique(arr)
    lct = LandCoverTable._from_z0s(z0s)
    out = np.empty_like(arr)

    # There is an error when trying to subset a numpy array by a data array
    if isinstance(arr, xr.DataArray):
        arr = arr.values

    for i, z0 in enumerate(z0s):
        out[arr == z0] = i + 1

    return out, lct


def _landcover_to_roughness(arr, lctable, field="z0"):
    """Returns array with values of field filling the array"""
    if field == "id":
        return arr.values

    out = np.empty_like(arr, dtype="float32")

    # There is an error when trying to subset a numpy array by a data array
    if isinstance(arr, xr.DataArray):
        arr = arr.values

    # We only want to output values that are in the file
    ids = np.unique(arr)
    for k, v in lctable.items():
        if k in ids:
            out[arr == k] = v[field]

    return out


def _raster_map_to_landcover(da):
    """Convert a roughness raster_map to landcover raster_map

    Returns
    -------
    xarray.DataArray, LandCoverTable
    """
    out_vals, lct = _roughness_to_landcover(da)

    da.values = out_vals
    da.name = "landcover"

    return da, lct
