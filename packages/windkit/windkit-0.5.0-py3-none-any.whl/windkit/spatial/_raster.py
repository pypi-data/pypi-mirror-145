# (c) 2022 DTU Wind Energy
"""
Module for raster functions.
"""
import logging

import numpy as np
import pyproj
import shapely
import xarray as xr

from ..geospatial_imports import (
    has_rasterio,
    is_GeoDataFrame,
    is_GeoSeries,
    requires_geopandas,
    requires_rasterio,
)

if has_rasterio:
    import rasterio as rio
    import rasterio.features  # used as rio.features
    from affine import Affine

from ..metadata import _MAP_TYPE_ATTRS, update_history, update_var_attrs
from ._bbox import BBox
from ._crs import add_crs, get_crs
from ._dimensions import (
    _get_point_dim,
    _get_spatial_dims,
    _get_stacked_point_dim,
    _get_vertical_dim,
)
from ._struct import is_cuboid, is_point, is_raster, is_stacked_point, is_vertical
from ._vertical import has_height_coord


def _shape(obj):
    """
    Get shape of raster part of xarray.Dataset or xarray.DataArray.

    Parameters
    ----------
    obj : xarray.DataSet, xarray.DataArray
        object to calcuate raster shape from.

    Returns
    -------
    tuple: shape
        (nx, ny)

    """
    x_dim, y_dim = _get_spatial_dims()
    return obj[x_dim].values.size, obj[y_dim].values.size


def _internal_bounds(obj):
    """
    Get internal coordinate bounds (left, bottom, right, top)
    of raster part of xarray.Dataset or xarray.DataArray

    Parameters
    ----------
    obj : xarray.DataSet, xarray.DataArray
        xarray object with raster-like dimensions.

    Returns
    -------
    tuple: bounds
        (left, bottom, right, top)

    """
    x_dim, y_dim = _get_spatial_dims()
    left, right = obj[x_dim].values[0], obj[x_dim].values[-1]
    bottom, top = obj[y_dim].values[0], obj[y_dim].values[-1]
    return left, bottom, right, top


def _resolution(obj):
    """
    Get resolution of raster part of xarray.Dataset
    or xarray.DataArray.

    Parameters
    ----------
    da : xarray.DataSet, xarray.DataArray
        Raster

    Returns
    -------
    tuple: (res_we, res_sn)
        Resolution in west_east and south_north directions.

    """
    left, bottom, right, top = _internal_bounds(obj)
    nx, ny = _shape(obj)
    res_x = (right - left) / (nx - 1)
    res_y = (top - bottom) / (ny - 1)
    return res_x, res_y


def _bounds(obj):
    """
    Get bounds of raster at cell edges.

    Parameters
    ----------
    da : xarray.DataArray
        Raster

    Returns
    -------
    bounds: tuple of floats
        (left, bottom, right, top)

    """
    left, bottom, right, top = _internal_bounds(obj)
    res_x, res_y = _resolution(obj)
    left -= res_x / 2.0
    bottom -= res_y / 2.0
    right += res_x / 2.0
    top += res_y / 2.0
    return left, bottom, right, top


def _spacing(obj):
    """
    Get spacing of raster.
    Assumes that dx and dy are the same. Fails if not.

    Parameters
    ----------
    da : xarray.DataArray
        Raster

    Returns
    -------
    spacing: float
        spacing of raster

    """
    dx, dy = map(abs, _resolution(obj))
    if not np.isclose(dx, dy):
        raise ValueError("DX and DY are not equal.")
    return dx


def _transform(obj):
    """
    Caculate transform from xarray.Dataset or xarray.DataArray
    with raster-like dimensions.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        Raster

    Returns
    -------
    affine.Affine: transform
        Affine transform from the objects raster-like dimensions

    """
    left, bottom, right, top = _bounds(obj)
    res_x, res_y = _resolution(obj)
    return Affine.translation(left, bottom) * Affine.scale(res_x, res_y)


def _warp_raster(
    obj, to_crs, resolution=None, method="nearest", nodata=np.nan
):  # pragma: no cover covered_in_public_method
    """
    Warp xarray.Dataset or xarray.DataArray raster-like part to
    new raster-like object in new projection.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        Object with raster-like part to warp to new projection.
    to_crs : int, str, dict, tuple, CRS
        Coordinate Reference System to warp raster-like part to.
    resolution : float, optional
        Resolution of the target raster. Derived from input by default.
    method : str, optional
        Interpolation method, "nearest" method used by default.
        Options are: "nearest", "bilinear", "cubic", "cubic_spline",
        "lanczos", "average", "mode", and "gauss"
    nodata : float, optional
        Value to use for cells outside the input space. np.nan by defualt.

    Returns
    -------
    xarray.Dataset, xarray.DataArray: warped_object
        Warped object in new projection.

    """
    requires_rasterio()

    def _warp(
        raster,
        dst_shape=None,
        src_transform=None,
        src_crs=None,
        dst_transform=None,
        dst_crs=None,
        dst_nodata=None,
        resampling=None,
    ):

        dst_data = np.zeros(dst_shape, dtype=raster.dtype.type)
        dst_nodata = raster.dtype.type(nodata)

        rio.warp.reproject(
            source=np.copy(raster.data),
            destination=dst_data,
            src_transform=src_affine,
            src_crs=src_crs,
            dst_transform=dst_affine,
            dst_crs=dst_crs,
            dst_nodata=dst_nodata,
            resampling=resampling,
        )

        return dst_data

    obj = obj.copy()
    x_dim, y_dim = _get_spatial_dims()

    resampling = getattr(rio.enums.Resampling, method)

    src_crs = rio.crs.CRS.from_user_input(get_crs(obj))
    dst_crs = rio.crs.CRS.from_user_input(to_crs)

    src_affine = _transform(obj)
    src_bounds = _bounds(obj)
    src_nx, src_ny = _shape(obj)
    src_res_x, src_res_y = _resolution(obj)

    dst_affine, dst_nx, dst_ny = rio.warp.calculate_default_transform(
        src_crs, dst_crs, src_nx, src_ny, *src_bounds, resolution=resolution
    )

    dst_x, _ = dst_affine * (np.arange(dst_nx) + 0.5, np.zeros(dst_nx) + 0.5)
    _, dst_y = dst_affine * (np.zeros(dst_ny) + 0.5, np.arange(dst_ny) + 0.5)

    coords_new = {y_dim: dst_y, x_dim: dst_x}

    kwargs = dict(
        dst_shape=(dst_ny, dst_nx),
        src_transform=src_affine,
        src_crs=src_crs,
        dst_transform=dst_affine,
        dst_crs=dst_crs,
        resampling=resampling,
    )

    obj_new = xr.apply_ufunc(
        _warp,
        obj,
        input_core_dims=[[y_dim, x_dim]],
        output_core_dims=[[y_dim + "_tmp_new", x_dim + "_tmp_new"]],
        kwargs=kwargs,
        vectorize=True,
        keep_attrs=True,
    )
    obj_new = obj_new.rename({y_dim + "_tmp_new": y_dim, x_dim + "_tmp_new": x_dim})
    obj_new = obj_new.assign_coords(**coords_new)
    obj_new = add_crs(obj_new, to_crs)

    if isinstance(obj, xr.Dataset):
        obj_new = update_history(obj_new)
    return obj_new


def _mask_raster(
    obj,
    mask,
    all_touched=False,
    drop=False,
    invert=False,
    nodata=None,
    pad=True,
    pad_width=0.001,
):  # pragma: no cover covered_in_public_method
    """
    Mask WindKit xarray raster-like object based on
    geometric features. Data outside the features are masked out.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        Object with raster-like dimensions to clip with mask.
    mask : geopandas.GeoDataFrame, geopandas.GeoSeries
        Geometric features to clip out of object.
    all_touched : bool, optional
        If True, all cells touched by the mask is included. Otherwise,
        only the cells with the center point inside the mask or cells included
        by "Bresenhams line algorithm" will be included. False by default.
    drop : bool, optional
        If True, coordinates with all missing values will be dropped. False by default.
    invert : bool, optional
        If True, instead of keeping cells inside the mask, the cells outside will be kept.
        False by default.
    nodata : int, float, optional
        Value to use for missing data. nan by default.
    pad : bool, optional
        If True, the mask will be bufferred  by "pad_width" size before masking the array.
        This can help e.g. to ensure that raster points on the edge of the mask is included.
    pad_width : float, optional
        Width used to pad/buffer the mask in units of raster pixel/cell widths. So a
        pad_width of 1 will mean that the mask is buffered by the size of the raster pixel/cell.

    Returns
    -------
    xarray.Dataset, xarray.DataArray: clipped_obj
        Object clipped by geometric features.

    Notes
    -----
    When the mask edges intersects with the cell centers they are not guaranteed to be
    included. It is recommend to use a buffer or all_touched=True to be sure.

    """
    requires_rasterio()
    gpd = requires_geopandas()

    obj = obj.copy()
    crs_obj = get_crs(obj)

    # windkit.spatial.bbox.BBox objects are converted to gpd.GeoSeries
    # where the LinearRing is converted to Polygon
    if isinstance(mask, (BBox)):
        poly = shapely.geometry.Polygon(mask.ring.coords)
        mask = gpd.GeoSeries(poly, crs=mask.crs)

    if isinstance(mask, (shapely.geometry.Polygon)):
        mask = gpd.GeoSeries(mask, crs=crs_obj)

    # If mask is tuple or list we assume bounds (minx, miny, maxx, maxy)
    # With same CRS as obj
    if isinstance(mask, (tuple, list)):
        if len(mask) != 4:
            raise ValueError(
                "Got tuple/list of size {len(mask)}. "
                + "Bounds (minx, miny, maxx, maxy)"
                + " should be size 4!"
            )
        minx, miny, maxx, maxy = mask
        poly = shapely.geometry.Polygon(
            ((minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy))
        )
        mask = gpd.GeoSeries(poly, crs=crs_obj)

    # Ensure mask is gpd.GeoSeries or gpd.GeoDataFrame
    if not isinstance(mask, (gpd.GeoDataFrame, gpd.GeoSeries)):
        raise ValueError(
            f"mask type {type(mask)} not supported!"
            + " must be tuple of bounds (minx, miny, maxx, maxy), "
            + " windkit.BBox, geopandas.GeoDataFrame, "
            + " geopandas.GeoSeries or shapely.geometry.Polygon"
        )

    x_dim, y_dim = _get_spatial_dims()
    nx, ny = _shape(obj)
    transform_ = _transform(obj)
    crs_mask = pyproj.CRS.from_user_input(mask.crs)

    if not crs_obj.is_exact_same(crs_mask):
        raise ValueError(
            "Raster CRS and mask CRS are not identical!" + " please reproject first!"
        )

    if pad:
        res_x, res_y = _resolution(obj)
        mask = mask.buffer(pad_width * res_x, cap_style=3)

    features = mask.__geo_interface__["features"]
    geometries = list(f["geometry"] for f in features)

    mask_arr = rio.features.geometry_mask(
        geometries=geometries,
        out_shape=(ny, nx),
        transform=transform_,
        invert=not invert,
        all_touched=all_touched,
    )

    mask_xray = xr.DataArray(
        mask_arr,
        coords={x_dim: obj.coords[x_dim], y_dim: obj.coords[y_dim]},
        dims=(y_dim, x_dim),
    )

    cropped_obj = obj.where(mask_xray, drop=drop)

    if nodata is not None:
        cropped_obj = cropped_obj.fillna(nodata)

    if isinstance(cropped_obj, xr.Dataset):
        cropped_obj = update_history(cropped_obj)
    return cropped_obj


def _clip_to_bbox_raster(obj, bbox):  # pragma: no cover covered_in_public_method
    """
    Clip WindKit xarray raster-like object to
    the bounds of a bounding box or geometry.

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        Object with raster-like dimensions to clip with bounding box.
    bbox : tuple, BBox, geopandas.GeoDataFrame, geopandas.GeoSeries, LinearRing
        Geometric features or bounding box to clip out of object.
        If bbox is a geometric feature, it's bounds method is used
        to obtain the bounding box bounds.

    Returns
    -------
    xarray.Dataset, xarray.DataArray: clipped_obj
        Object clipped by geometric features.

    """
    obj = obj.copy()

    x_dim, y_dim = _get_spatial_dims()

    crs_raster = get_crs(obj)

    if isinstance(bbox, (BBox)) or is_GeoDataFrame(bbox) or is_GeoSeries(bbox):
        crs_mask = pyproj.CRS.from_user_input(bbox.crs)
        if not crs_raster.is_exact_same(crs_mask):
            raise ValueError(
                "Raster CRS and mask CRS are not identical!"
                + " please reproject first!"
            )
        if isinstance(bbox, BBox):
            bounds = bbox.bounds()
        elif is_GeoDataFrame(bbox) or is_GeoSeries(bbox):
            bounds = bbox.total_bounds
    elif isinstance(bbox, shapely.geometry.LinearRing):
        bounds = bbox.bounds
    elif len(bbox) == 4:
        bounds = bbox
    else:
        raise ValueError(
            f"bbox type {type(bbox)} not supported!"
            + " must be tuple of bounds (minx, miny, maxx, maxy), "
            + " windkit.BBox, geopandas.GeoDataFrame, "
            + " geopandas.GeoSeries or shapely.geometry.LinearRing!"
        )

    minx, miny, maxx, maxy = bounds

    res_x, res_y = _resolution(obj)

    clip_minx = minx  # - abs(res_x) / 2.0
    clip_miny = miny  # - abs(res_y) / 2.0
    clip_maxx = maxx  # + abs(res_x) / 2.0
    clip_maxy = maxy  # + abs(res_y) / 2.0

    if res_x < 0:
        x_slice = slice(clip_maxx, clip_minx)
    else:
        x_slice = slice(clip_minx, clip_maxx)

    if res_y < 0:
        y_slice = slice(clip_maxy, clip_miny)
    else:
        y_slice = slice(clip_miny, clip_maxy)

    select = {y_dim: y_slice, x_dim: x_slice}

    obj_new = obj.sel(indexers=select)
    if isinstance(obj, xr.Dataset):
        obj_new = update_history(obj_new)
    return obj_new


def _can_be_raster(west_east, south_north, thresh=1e-9):
    """Test if an array of coordinate values could
    possibly be converted into a raster

    Parameters
    ----------
    west_east : (N,) array_like
        A 1-D array containing west_east coordinates
    south_north : (N,) array_like
        A 1-D array containing south_north coordinates
    thresh : float
        Threshold value for checking spatial separation between coordinates
        Default set to 1e-9 m

    Returns
    -------
    bool
        True if it is a raster or can be converted to one. False otherwise.

    Notes
    -----
    Check that the south_north and west_east dimensions are such that
    the data could be converted into a raster object rather than a
    point object.
    """

    # We should only be looking at unique values of the coordinates
    we = np.sort(np.unique(west_east))
    sn = np.sort(np.unique(south_north))

    # More than one point
    if we.size == 1 or sn.size == 1:
        logging.debug("FAIL: One of the dimensions contains only 1 value.")
        return False

    # Difference between each point is approximately equal
    diff_we = np.diff(we)
    diff_we = np.where(diff_we <= thresh, diff_we.max(), diff_we)
    diff_sn = np.diff(sn)
    diff_sn = np.where(diff_sn <= thresh, diff_sn.max(), diff_sn)

    space_equal = ((diff_we.max() - diff_we.min()) <= thresh) and (
        (diff_sn.max() - diff_sn.min()) <= thresh
    )

    if not space_equal:
        logging.debug(
            "FAIL: Distance between points is not " + "the same for all points."
        )
        return False

    # Pixel is square
    is_square = abs(diff_sn.max() - diff_we.max()) <= thresh
    if not is_square:
        logging.debug("FAIL: Pixels are not square.")
        return False

    # logging.info("Done checking if dataset could be a raster.")
    return True


def to_raster(obj, ignore_raster_check=False):
    """Converts a point based object to a raster based object

    Parameters
    ----------
    obj : xarray.Dataset, xarray.DataArray
        WindKit xarray dataset or dataarray containing spatial
        dimensions and CRS variable
    ignore_raster_check : bool
        Check if the object satisfy the requirements to become a raster
        Default set to False (i.e., not to check)

    Returns
    -------
    xarray.Dataset, xarray.DataArray
        Raster version of WindKit xarray dataset or dataarray

    Raises
    ------
    ValueError
        If dataset cannot be converted to raster
    """
    x_dim, y_dim = _get_spatial_dims()
    point_dim = _get_point_dim()
    stacked_point_dim = _get_stacked_point_dim()
    vertical_dim = _get_vertical_dim()

    # If object is already raster-like, return early.
    if (is_raster(obj) or is_cuboid(obj)) and _can_be_raster(obj[x_dim], obj[y_dim]):
        return obj

    # Only structures that need conversion
    if _can_be_raster(obj[x_dim], obj[y_dim]) or ignore_raster_check:

        stack_dims = (y_dim, x_dim)

        if is_stacked_point(obj):

            if isinstance(obj, xr.Dataset):
                if all(var in obj.data_vars for var in stack_dims):
                    out_obj = obj.copy().set_index(**{stacked_point_dim: stack_dims})

            if all(coord in obj.coords for coord in stack_dims):
                out_obj = obj.copy().set_index(**{stacked_point_dim: stack_dims})

            out_obj = out_obj.unstack(stacked_point_dim)

        elif is_point(obj):

            hgt_dim = (vertical_dim,) if has_height_coord(obj) else ()
            stack_dims = hgt_dim + stack_dims
            if isinstance(obj, xr.Dataset):
                if all(dim in obj.data_vars for dim in stack_dims):
                    out_obj = obj.copy().set_index(**{point_dim: stack_dims})

            if all(coord in obj.coords for coord in stack_dims):
                out_obj = obj.copy().set_index(**{point_dim: stack_dims})

            out_obj = out_obj.unstack(point_dim)

            # Correct 2d variables if necessary
            if len(hgt_dim) == 1:

                if isinstance(out_obj, xr.Dataset):

                    for var in out_obj.data_vars:
                        if "_pwio_data_is_2d" in out_obj[var].attrs:
                            if out_obj[var].attrs["_pwio_data_is_2d"]:
                                out_obj[var] = out_obj[var].isel(
                                    **{hgt_dim[0]: 0}, drop=True
                                )
                            del out_obj[var].attrs["_pwio_data_is_2d"]

                elif isinstance(out_obj, xr.DataArray):
                    if "_pwio_data_is_2d" in out_obj.attrs:
                        if out_obj.attrs["_pwio_data_is_2d"]:
                            out_obj = out_obj.isel(**{hgt_dim[0]: 0}, drop=True)
                        del out_obj.attrs["_pwio_data_is_2d"]

        # Add spatial metadata back to object
        for coord in stack_dims:
            out_obj[coord].attrs = obj[coord].attrs

        out_obj = update_var_attrs(out_obj, _MAP_TYPE_ATTRS)
        if isinstance(out_obj, xr.Dataset):
            out_obj = update_history(out_obj)

        return out_obj

    raise ValueError(f"Cannot convert {type(obj)} to raster.")
