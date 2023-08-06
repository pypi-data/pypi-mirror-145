# (c) 2022 DTU Wind Energy
"""
WindKit Bounding Box.

This is an object that represents the extent of a GIS object in its native
projection.

It is currently used for clipping raster Datasets and RasterMaps
"""
import numpy as np
import pyproj
from shapely.geometry import LinearRing, Polygon
from shapely.ops import transform

from windkit.geospatial_imports import requires_geopandas

from ..metadata import update_history


class BBox:
    """WindKit Bounding Box

    WindKit Bounding boxes are defined by the center coordinates of the grid rather than
    the corner coordinates like in GDAL.

    Parameters
    ----------
    ring : shapely.geometry.LinearRing
        Square ring that envelopes the boundaries of the data
    crs : int, dict, str or pyproj.crs.CRS
        Value to initialize `pyproj.crs.CRS`
    """

    def __init__(self, ring, crs):
        self.ring = ring
        self.crs = pyproj.CRS.from_user_input(crs)

    def __str__(self):  # pragma:no cover str_fmt
        bnds = self.bounds()
        return (
            f"Bounds: ({bnds[0]}, {bnds[1]}) ({bnds[2]}, {bnds[3]})\n"
            + f"CRS: {self.crs.to_wkt()}"
        )

    def bounds(self):
        """Return bounds of bounding box."""
        return self.ring.bounds

    @classmethod
    def from_cornerpts(
        cls, minx=0.0, miny=0.0, maxx=1000.0, maxy=1000.0, crs="epsg:32632"
    ):  # pylint:disable=too-many-arguments
        """Create a bounding box object from min and max values

        Parameters
        ----------
        minx : float
            Minimum values of the east-west direction. Defaults to  0.0.
        maxx : float
            Maximum values of the east-west direction. Defaults to 1000.0.
        miny : float
            Minimum values of the south-north direction. Defaults to 0.0.
        maxy : float
            Maximum values of the south-north direction. Defaults to 1000.0.
        crs : int, dict, str or pyproj.crs.CRS
            Value to initialize `pyproj.crs.CRS`
            Defaults to "epsg:32632".

        Returns
        -------
        BBox
            A bounding box of the requested coordinates.
        """
        if minx >= maxx:
            raise ValueError(f"minx: {minx} is larger than maxx: {maxx}")
        if miny >= maxy:
            raise ValueError(f"miny: {miny} is larger than maxy: {maxy}")

        ring = LinearRing(((minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)))

        return cls(ring, crs)

    @classmethod
    def from_ds(cls, ds):
        """Create a bounding box object from a WindKit Dataset.

        Parameters
        ----------
        ds : xarray.Dataset
            WindKit formatted GIS dataset.

        Returns
        -------
        BBox
            A bounding box of the dataset.
        """
        we = ds.west_east
        sn = ds.south_north

        ring = LinearRing(
            (
                (we.min(), sn.min()),
                (we.max(), sn.min()),
                (we.max(), sn.max()),
                (we.min(), sn.max()),
            )
        )

        crs = pyproj.CRS.from_wkt(ds.crs.attrs["crs_wkt"])

        return cls(ring, crs)

    def reproject(self, to_crs):
        """Reproject a bounding box object.

        Parameters
        ----------
        to_crs : int, dict, str or pyproj.crs.CRS
            Value to initialize `pyproj.crs.CRS`

        Returns
        -------
        BBox
            The linestring in the requested projection.
        """
        to_crs = pyproj.CRS.from_user_input(to_crs)

        transformer = pyproj.Transformer.from_crs(
            self.crs, to_crs, always_xy=True, skip_equivalent=True
        )
        ring = transform(transformer.transform, self.ring)

        return self.__class__(ring, to_crs)

    def buffer(self, distance):
        """Buffer bounding box by fixed distance.

        Parameters
        ----------
        Distance : float
            Distance to buffer each direction.

        Returns
        -------
        BBox
            New Bounding box object buffered by requested amount.
        """
        bounds = list(self.bounds())
        bounds[0] -= distance
        bounds[1] -= distance
        bounds[2] += distance
        bounds[3] += distance
        return self.__class__.from_cornerpts(*bounds, self.crs)

    def to_grid(self, spacing, heights):
        """Create a WindKit Grid starting from the minimum points of the bbox.

        Parameters
        ----------
        spacing : float
            Distance between each point.
        heights : float or 1D array
            Heights to include in the grid.

        Returns
        -------
        xarray.Dataset
            WindKit xarray dataset with dummy variable.

        Notes
        -----
        This assumes a "fence-post" approach to creating the grid, meaning that there may
        be a point that falls outside of the bounding box on the positive side.
        """
        from .spatial import create_dataset  # here to avoid circular import

        # Get x0, y0
        minx, miny, maxx, maxy = self.bounds()

        # get number of points in x and y dimension
        nx = int(np.round((maxx - minx) / spacing)) + 1
        ny = int(np.round((maxy - miny) / spacing)) + 1

        out_ds = create_dataset(
            np.arange(nx) * spacing + minx,
            np.arange(ny) * spacing + miny,
            heights,
            self.crs,
        )

        return update_history(out_ds)

    def to_geoseries(self, geo_as_polygon=False):
        """Convert Bounding box to geopandas.Geoseries.

        Parameters
        ----------
        geo_as_polygon : bool, optional
            Convert the LinearRing to Polygon first, by default False.

        Returns
        -------
        geopandas.GeoSeries
            Bounding box converted to geoseries.
        """
        gpd = requires_geopandas()
        if geo_as_polygon:
            geo = Polygon(self.ring.coords)
        else:
            geo = self.ring
        return gpd.GeoSeries(geo, crs=self.crs)
