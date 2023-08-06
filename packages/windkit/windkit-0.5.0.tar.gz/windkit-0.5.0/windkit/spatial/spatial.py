# (c) 2022 DTU Wind Energy
"""
Public interface to all of the spatial tools in WindKit
"""
import logging
import numpy as np
import xarray as xr
import pyproj
from scipy.spatial import KDTree

from windkit.geospatial_imports import is_GeoDataFrame, is_GeoSeries

from ._bbox import BBox
from ._crs import add_crs, get_crs, crs_are_equal
from ..metadata import ALL_VARS_META, _GLOBAL_CONVENTIONS, update_history

from ._utm import (
    _utmzone2epsg,
    _getsitecorners,
    _mgrs_from_latlon,
    _get_mgrs_letter_from_lat,
)

from ._dimensions import (
    _get_spatial_dims,
    _get_point_dim,
    _get_stacked_point_dim,
    _get_vertical_dim,
)

from ._raster import (
    _can_be_raster,
    _warp_raster,
    _mask_raster,
    _clip_to_bbox_raster,
    is_raster,
    to_raster,
)

from ._point import _mask_point, to_point, is_point, is_stacked_point, to_stacked_point

from ._struct import get_spatial_struct
from ._vertical import has_height_coord, has_height_dim
from ._vector import _clip_vector


__all__ = [
    "add_crs",
    "are_spatially_equal",
    "BBox",
    "clip",
    "crs_are_equal",
    "create_dataset",
    "get_crs",
    "mask",
    "reproject",
    "spatial_stack",
    "spatial_unstack",
    "warp",
    "nearest_points",
]

logger = logging.getLogger(__name__)


def are_spatially_equal(obj_a, obj_b):
    """Checks that the spatial points are equivalent for both datasets

    Parameters
    ----------
    obj_a, obj_b : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial
        dimensions and CRS variable

    Returns
    -------
    bool
        True if spatial coords are numpy.allclose

    """
    x_dim, y_dim = _get_spatial_dims()

    if obj_a.coords[x_dim].size != obj_b.coords[x_dim].size:
        return False
    if obj_a.coords[y_dim].size != obj_b.coords[y_dim].size:
        return False
    return np.allclose(obj_a[x_dim], obj_b[x_dim]) and np.allclose(
        obj_a[y_dim], obj_b[y_dim]
    )


def create_dataset(west_east, south_north, height, crs, struct="auto", thresh=1e-9):
    """Create a WindKit dataset given a set of locations.

    Parameters
    ----------
    west_east : array_like
        1D array of west_east locations of interest
    south_north : array_like
        1D array of south_north locations of interest
    height : array_like
        Array of heights to create in output WindKit xarray dataset
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    struct : str
        Used to specify the type of dataset that is desired
        Valid values are 'auto', 'cuboid', 'point' and
        'stacked_point'. The default value of 'auto' tries to create a cuboid,
        but falls back to point depending on the values specified.
    thresh : float
        Threshold value for raster detection
        Default set to 1e-9 m

    Returns
    -------
    xarray.Dataset
        WindKit formated zero-filled Dataset with one variable "output"
        and with the grid dimensions specified

    Notes
    -----
    This function will create a WindKit formatted dataset including all of the
    geospatial information that is desired.

    If ds_fmt is set to "auto", the function will attempt to create a cuboid,
    if the deviation between the largest and smallest interval along west_east
    and south_north are lower than value in thresh (west_east and south north
    can be different lengths). Otherwise, the function will attempt to make a
    point dataset. Specifically, it will create a 3D point object,
    if west_east, south_north and heights have the same lengths.
    If west_east and south_north have the same lengths but heights length is
    different the function will create a 2D point object.

    Alternatively, ds_fmt can be set to desired output format, that is  'cuboid',
    'stacked_point' and 'point', which accordingly requires specific structures
    of west_east, south_north and heights (as described above):

        * ``cuboid``:
            west_east, south_north, and heights must contain unique points along their
            dimension, and west_east and south_north are evenly spaced

        * ``stacked_point``:
            west_east and south_north must have the same length, but heights will have
            unique values representing the dimension values

        * ``point``:
            west_east, south_north and heights must have same lengths

    """

    # Ensure that all input arrays are 1d
    x, y, z = np.atleast_1d(west_east, south_north, height)

    if struct.lower() == "auto":

        if _can_be_raster(x, y):
            struct = "cuboid"
        elif (y.size == x.size) and (x.size != z.size):
            struct = "stacked_point"
        elif (y.size == x.size) and (y.size == z.size):
            struct = "point"
        else:
            raise ValueError("Cannot identify struct of input data.")

    # Get names of dimensions
    x_dim, y_dim = _get_spatial_dims()
    z_dim = _get_vertical_dim()
    pt_dim = _get_point_dim()
    stacked_pt_dim = _get_stacked_point_dim()

    if struct.lower() == "cuboid":

        if not _can_be_raster(x, y):
            raise ValueError("Data cannot be converted to raster or cuboid dataset.")

        # Create spatial data arrays
        shape = z.size, y.size, x.size
        dims = (z_dim, y_dim, x_dim)
        z_coord = ((z_dim,), z)
        y_coord = ((y_dim,), y)
        x_coord = ((x_dim,), x)

    elif struct.lower() == "stacked_point":

        # Raise error if point array cannot be made
        if y.size != x.size:
            err_str = "south_north and west_east sizes do not match."
            raise ValueError(err_str)

        # Create spatial data arrays
        shape = z.size, x.size
        dims = (z_dim, stacked_pt_dim)
        z_coord = ((z_dim,), z)
        y_coord = ((stacked_pt_dim,), y)
        x_coord = ((stacked_pt_dim,), x)

    elif struct.lower() == "point":

        # Raise error if point array cannot be made
        if (y.size != x.size) | (y.size != z.size):
            err_str = (
                "point dataset cannot be made with input " + "arrays of differing sizes"
            )
            raise ValueError(err_str)

        # Create spatial data arrays
        shape = (x.size,)
        dims = (pt_dim,)
        z_coord = ((pt_dim,), z)
        y_coord = ((pt_dim,), y)
        x_coord = ((pt_dim,), x)

    else:
        raise ValueError("Unknown struct provided.")

    # Build DataArray
    data = np.zeros(shape)
    coords = {z_dim: z_coord, y_dim: y_coord, x_dim: x_coord}
    out_da = xr.DataArray(data=data, dims=dims, coords=coords)

    # Build dataset with crs for storing results
    out_ds = out_da.to_dataset(name="output")
    out_ds = add_crs(out_ds, crs)

    out_ds[z_dim].attrs = ALL_VARS_META[z_dim]
    out_ds.attrs = _GLOBAL_CONVENTIONS
    return update_history(out_ds)


def _replace_close(arr, thresh=1e-9):  # pragma:no cover internal
    """Replace all values that are close to each other with an identical value

    Parameters
    ----------
    arr : array_like
        Array to be examined
    thresh : float
        Threshold value for checking spatial separation between coordinates
        Default set to 1e-9 m


    Returns
    -------
    array_like
        Array of the same shape and dtype as arr,
        but with close values replaced
    """

    unq = np.sort(np.unique(arr))
    diff_unq = np.diff(unq)
    if any(diff_unq <= thresh):
        for i, diff in enumerate(diff_unq):
            if diff <= thresh:
                val = unq[i]
                arr = np.where(np.isclose(arr, val), val, arr)

    return arr


def reproject(obj, to_crs, copy=True):
    """Reprojects WindKit object a new CRS without changing the data.

    If the input is a xarray.Dataset or xarray.DataArray with
    a 'cuboid' spatial structure, the spatial
    structure will be changed to 'point', since the coordiates of the new
    dataset will no longer be regularly spaced.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, xarray.DataArray, xarray.Dataset, or BBox
        WindKit object that will be reprojected.
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    copy : bool
       If true, the object is copied. Defaults to True.

    Returns
    -------
    geopandas.GeoDataFrame, xarray.DataArray,xarray.Dataset, or BBox
        WindKit object with new projection

    See Also
    --------
    warp

    Notes
    -----
    This script reprojects the coordinates of the data, and potentially
    reshapes the data from 2D to 1D in geographic space. This is done
    so that none of the data is interpolated, but rather the coordinates
    are just changed to match those of the new projection.
    """

    #
    if is_GeoDataFrame(obj) or is_GeoSeries(obj):
        return obj.to_crs(to_crs)
    elif isinstance(obj, BBox):
        return obj.reproject(to_crs)

    # From here we know that the input object is
    # a xarray.Dataset or xarray.DataArray

    if copy:
        obj = obj.copy()

    # Get input CRS object
    try:
        from_crs = get_crs(obj)
    except ValueError:
        raise ValueError(
            "No CRS found on object! Please set with:" + " obj = add_crs(obj, crs)!"
        )

    # Get spatial dim names
    x_dim, y_dim = _get_spatial_dims()

    # Get output CRS object
    to_crs = pyproj.CRS.from_user_input(to_crs)

    # Reproject dimensions
    transformer = pyproj.Transformer.from_crs(
        from_crs, to_crs, skip_equivalent=True, always_xy=True
    )

    struct = get_spatial_struct(obj)

    if struct in ["raster", "cuboid"]:
        obj = to_point(obj)
        struct = "point"
    elif struct == "stacked_point":
        struct = "stacked_point"
    elif struct is None:
        struct = "point"

    # Ensure that all input arrays are 1d
    x, y = np.atleast_1d(obj[x_dim].values, obj[y_dim].values)

    x_new, y_new = transformer.transform(x, y)

    x_new = _replace_close(x_new)
    y_new = _replace_close(y_new)

    obj = obj.assign_coords({x_dim: ((struct), x_new), y_dim: ((struct), y_new)})

    obj = add_crs(obj, to_crs)

    return obj


def warp(obj, to_crs, resolution=None, method="nearest", nodata=np.nan):
    """Warp cuboid WindKit object to another in a new CRS using data interpolation.

    Parameters
    ----------
    obj : xarray.DataArray or xarray.Dataset
        WindKit object to warp.
    to_crs : int, dict, str or CRS
        Value to create CRS object or an existing CRS object
    resolution :  tuple (x resolution, y resolution) or float, optional
        Target resolution, in units of target coordinate reference
        system. Default: None calculates a resolution in the target crs similar
        to the resolution of the original crs.
    method : str
        Interpolation method, passed to rasterio.warp.reproject. Defaults to "nearest".
    nodata : scalar
        Initial data to fill output arrays, passed to rasterio.warp.reproject. Defaults to
        numpy.nan.

    Returns
    -------
    xarray.DataArray or xarray.Dataset
        Warped WindKit object.

    See Also
    --------
    reproject
    """
    kwargs = {"resolution": resolution, "method": method, "nodata": nodata}
    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            obj = _warp_raster(obj, to_crs, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError(
                "Only 'raster' and 'cuboid' objects currently" + " supports warping!"
            )
    else:
        raise ValueError(
            "Only xarray Dataset and DataArray objects "
            + "currently supported for warping"
        )


def mask(obj, mask, all_touched=False, invert=False, nodata=None, **kwargs):
    """Mask WindKit object with geometric mask.

    Masking an object returns the same object with values outside of the masked
    region filled with NaN.

    Parameters
    ----------
    obj : xarray.Dataset,xarray.DataArray
        WindKit object to mask.
    mask : geopandas.GeoDataFrame or BBox
        Mask to mask object by.
    all_touched : bool
        *raster* or *cuboid* only: Include all pixels touched by the mask? False
        includes only those that pass through the center. Passed to
        rasterio.features.geometry_mask. Defaults to False.
    invert : bool
        *raster* or *cuboid* only: If true values outside of the mask will be nulled,
        if False values inside the mask are nulled. Opposite is passed to
        rio.features.geometry_mask. Defaults to False.
    nodata : float
        *raster* or *cuboid* only: If no data is not None, all masked data will be filled
        with this value. Default, masked data is set to NaN.

    Returns
    -------
    same as obj
        Clipped WindKit object.

    See Also
    --------
    clip

    Note
    ----
    This function behaves the opposite of rasterio.features.geometry_mask by default, in
    that it nulls areas outside of the area of interest rather than inside.
    For rasters, when the mask edges intersects with the cell centers they are not guaranteed to be
    included. It is recommend to use a buffer or all_touched=True to be sure.
    """
    kwargs = {
        **kwargs,
        "all_touched": all_touched,
        "invert": invert,
        "nodata": nodata,
    }
    if isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            obj = _mask_raster(obj, mask, drop=False, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        elif struct in ["point", "stacked_point"]:
            obj = _mask_point(obj, mask, drop=False, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError("Spatial structure not supported!")
    else:
        raise ValueError("Object not supported!")


def clip(obj, mask, all_touched=False, invert=False, nodata=None, **kwargs):
    """Clip object to mask.

    Clipping returns an object that has been reduced to the requested shape. Dropping
    data that falls outside of the masked region.

    Parameters
    ----------
    obj : geopandas.GeoDataFrame, xarray.DataArray or xarray.Dataset
        Object with raster-like dimensions to clip with mask.
    mask : geopandas.GeoDataFrame or BBox
        Geometric features to clip out of object.
    all_touched : bool
        *raster* or *cuboid* only: Include all pixels touched by the mask? False
        inclodes only those that pass through the center. Passed to
        rasterio.features.geometry_mask. Defaults to False.
    invert : bool
        *raster* or *cuboid* only: If true values outside of the mask will be nulled,
        if False values inside the mask are nulled. Opposite is passed to
        rio.features.geometry_mask. Defaults to False.
    nodata : float
        *raster* or *cuboid* only: If no data is not None, all masked data will be filled
        with this value. Default, masked data is set to NaN.
    kwargs : dict
        Other keyword-arguments are passed to the underlying function, depending
        on the type of object.

    Returns
    -------
    geopandas.GeoDataFrame, xarray.DataArray,xarray.Dataset
        Object of the same type as obj clipped by geometric features.

    See Also
    --------
    mask

    Notes
    -----
    This function behaves the opposite of rasterio.features.geometry_mask by default, in
    that it nulls areas outside of the area of interest rather than inside.
    For rasters, when the mask edges intersects with the cell centers they are not guaranteed to be
    included. It is recommend to use a buffer or all_touched=True to be sure.
    """
    kwargs = {**kwargs, "all_touched": all_touched, "invert": invert, "nodata": nodata}

    if is_GeoDataFrame(obj) or is_GeoSeries(obj):
        return _clip_vector(obj, mask, **kwargs)
    elif isinstance(obj, (xr.Dataset, xr.DataArray)):
        struct = get_spatial_struct(obj)
        if struct in ["raster", "cuboid"]:
            if isinstance(mask, BBox):
                obj = _clip_to_bbox_raster(obj, mask)
            else:
                obj = _mask_raster(obj, mask, drop=True, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        elif struct in ["point", "stacked_point"]:
            obj = _mask_point(obj, mask, drop=True, **kwargs)
            if isinstance(obj, xr.Dataset):
                return update_history(obj)
            else:
                return obj
        else:
            raise ValueError("Spatial structure not supported!")
    else:
        raise ValueError(f"Object not supported!")


_STACK_ATTRS = ("_pwio_was_stacked_point", "_pwio_was_cuboid", "_pwio_orig_srs_wkt")


def spatial_stack(
    source, target_crs=None, revertable=True, copy=True, remove_height=False
):
    """Returns source in a revertable version of the "point" format

    This routine can be used to ensure a consistent input form to external routines, by
    always returning in "point" format. It can also do reprojection, and remove the
    height field to make the result a 2D spatial object.

    Parameters
    ----------
    source : xarray.DataSet
        WindKit dataset containing spatial dimensions and CRS variable to convert
    target_crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
        (Default is to not reproject.)
    revertable : bool
        Should we retain information about the original datastructure so we can revert
        this process? This is typically True, but should be False when interpolating
        the data to a new projection.
    copy : bool
        Should we make a copy of the initial dataset? This is typically true as we don't
        want to manipulate the original object, but work on a new version.
    remove_height : bool
        Is the resulting object always 2D? This is typically false, but can be useful in
        some instances.

    Returns
    -------
    stacked : xarray.DataSet
        WindKit formated xr.DataSet as a point object on the new projection and
        with additional that allow it to be converted back to its original form
        using spatial_unstack.

    Notes
    -----
    This routine serves two purposes:
    1. Convert source to a point object, storing its former structure.
    2. Reproject to the target_crs if provided, and not already met.
    """
    if copy:
        source = source.copy(deep=True)

    # For some routines, we don't want to pass a height dimesion, so remove it if asked
    if remove_height:
        if has_height_dim(source):
            source = source.isel(height=0, drop=True)
        if has_height_coord(source):
            del source["height"]

    # Remove attributes from previous call if found
    if not is_point(source):
        for attr in _STACK_ATTRS:
            if attr in source.attrs:
                del source.attrs[attr]

    # Label original format and get 2D variables if not "point"
    orig_format = get_spatial_struct(source)
    if revertable and orig_format in ("stacked_point", "cuboid", "raster"):
        logger.debug("Converting from original format %s", orig_format)
        source.attrs[f"_pwio_was_{orig_format}"] = True
        # Identify 2D variables
        if has_height_dim(source):
            hgt_dim = _get_vertical_dim()
            for var in source.data_vars:
                logger.debug("Flagging variable %s as 2d variable", var)
                source[var].attrs["_pwio_data_is_2d"] = hgt_dim not in source[var].dims

    # Reproject if requested
    source_crs = get_crs(source)
    if target_crs is not None:
        target_crs = pyproj.CRS.from_user_input(target_crs)
        if source_crs != target_crs:
            if revertable:
                source.attrs["_pwio_orig_srs_wkt"] = source_crs.to_wkt()
            return reproject(to_point(source), target_crs)

    ds = to_point(source)
    return update_history(ds)


def spatial_unstack(source):
    """Unstacks a point object that was created using spatial_stack

    Parameters
    ----------
    source : xarray.DataSet
        WindKit dataset containing spatial dimensions and CRS variable to revert

    Returns
    -------
    WindKit dataset
        Source dataset structured as it was originally.

    Notes
    -----
    This is the companion function to spatial_stack and does 2 things:
    1. Converts 3D-point object to either raster or 2D-point object
    2. Reprojects converted object back to its original projection
    """
    # Check that source was previously reprojected
    if "_pwio_orig_srs_wkt" in source.attrs:
        source = reproject(source, source.attrs["_pwio_orig_srs_wkt"])
        del source.attrs["_pwio_orig_srs_wkt"]

    # Convert back to original format
    if "_pwio_was_raster" in source.attrs:
        source = to_raster(source, True)
        geo_dims_order = ("south_north", "west_east")
        del source.attrs["_pwio_was_raster"]
    elif "_pwio_was_cuboid" in source.attrs:
        source = to_raster(source, True)
        geo_dims_order = ("height", "south_north", "west_east")
        del source.attrs["_pwio_was_cuboid"]
    elif "_pwio_was_stacked_point" in source.attrs:
        geo_dims_order = (
            "height",
            "stacked_point",
        )
        source = to_stacked_point(source)
        del source.attrs["_pwio_was_stacked_point"]

    # Transpose the coordinates to match netCDF best practices
    hgt_dim = _get_vertical_dim()
    if is_stacked_point(source):
        geo_dims_order = (hgt_dim,) + ("stacked_point",)
    elif is_point(source):
        geo_dims_order = ("point",)
    elif is_raster(source):
        geo_dims_order = ("south_north", "west_east")
    else:
        geo_dims_order = ("point",)

    # Removing _pwio_data_is_2d attr from dataset
    for var in source.data_vars.keys():
        if "_pwio_data_is_2d" in source[var].attrs:
            source[var].attrs.pop("_pwio_data_is_2d", None)

    ds = source.transpose(..., *geo_dims_order)
    return update_history(ds)


def nearest_points(
    ds: xr.Dataset,
    ds_target: xr.Dataset,
    dims=["west_east", "south_north", "height"],
    n_nearest=1,
    return_rank=False,
    return_distance=False,
):
    """Get nearest points from x,y,z point dataset

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset of which we want to select nearest points
    ds_target : xr.Dataset
        Target dataset of the points we want to obtain from the input
    dims : list of strings
        Dimensions which we want to use for nearest neighbour lookup
    n_nearest: int
        Number of closest points to return for each point in ds_target
    return_rank: bool
        Return the rank of closeness
    return_distance: bool
        Return the distance to closest point

    Returns
    -------
    xr.Dataset
        ds but with the nearest points provided in ds_target (i.e. ds will have the shape of ds_target)
    """
    if get_crs(ds).is_geographic or get_crs(ds_target).is_geographic:
        raise ValueError(
            "Can only do nearest neighbour lookup in metric coordinate systems!"
        )
    if get_crs(ds) != get_crs(ds_target):
        raise ValueError("Datasets must have the same coordinate system!")

    # stack so that we also work with point structure
    ds = spatial_stack(ds)

    # if we ask for only the nearest 1 point the data structure
    # remains the same as ds_target, so we can recover the original
    # by spatial_unstack.
    if n_nearest == 1:
        ds_target = spatial_stack(ds_target)
    else:
        ds_target = to_point(ds_target)

    arrays = np.array([ds[x].values for x in dims]).T
    arrays_target = np.array([ds_target[x].values for x in dims]).T
    tree = KDTree(arrays)
    dd, ii = tree.query(arrays_target, k=n_nearest)

    if n_nearest == 1:
        dims = ("point",)
    else:
        dims = ("point", "rank")

    idx = xr.DataArray(ii, dims=dims)

    nearest = ds.isel(point=idx)

    if "rank" in dims and return_rank:
        nearest["rank"] = (("rank",), np.arange(n_nearest))

    if return_distance:
        nearest["distance"] = (dims, dd)

    if n_nearest == 1:
        ds = spatial_unstack(nearest)
        return update_history(ds)
    else:
        nearest = (
            nearest.rename({"point": "point_tmp"})
            .stack(point=("point_tmp", "rank"))
            .reset_index("point")
            .drop_vars("point_tmp")
        )
        if not return_rank:
            nearest = nearest.drop("rank")
        return update_history(nearest)
