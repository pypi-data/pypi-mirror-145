# (c) 2022 DTU Wind Energy
"""
Module that downloads elevation and roughness maps

Currently driven by the google earth engine, which is a cloud interface service to access
landcover and elevation data, among other things.

Installation & Setup
--------------------

The earth engine is an optional install, you can install with conda::

    conda install earthengine-api

After installation you will have to do a one-time authentication
step from the command line: ``earthengine authenticate``

This will open a browser where you will have to allow google to use
you google account to retrieve data from the google servers. If you are on a machine
without the ability to use a browser (such as an HPC
cluster), you will have to use ``earthengine authenticate --quiet``, which requires you to
to manually copy the authentication code into the terminal.

In addition, you will have to `sign up
<https://signup.earthengine.google.com/#!/>`_ for the google earth engine and give
a reason why you want to use the program. Please pay particular attention to
their terms of service.

Automated Datasets
------------------

Currently, the databases that have been added are the Copernicus Global Land Cover
(CGLS-LC100), Copernicus CORINE land Cover (CORINE), MODIS Global Land Cover MCD12Q1
(MODIS), and Globcover as landcover databases and
NASA SRTM Digital Elevation 30m(SRTM) and ALOS DSM: Global 30 (ALOS) as elevation databases.
The landcover databases have standard conversion tables that are included in
``windkit/landcovertables``.

Google Earth Engine provides lists of
`elevation
<https://developers.google.com/earth-engine/datasets/tags/elevation>`_ and
`land cover
<https://developers.google.com/earth-engine/datasets/tags/landcover>`_
data sources, which provide additional details about the various datasources used
in this library.
"""
import logging
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import pyproj
from shapely.geometry import Point

from .landcover import LandCoverTable
from .raster_map import read_raster_map
from .spatial._utm import _mgrs_from_latlon, _utmzone2epsg

##### Initialize Google Earth Engine ######
try:
    import ee as earth_engine

    earth_engine.Initialize()  # very expensive so we want to only do this one time

except ImportError:
    earth_engine = None


logger = logging.getLogger(__name__)
LIST_DATA_SOURCES = ["CGLS-LC100", "CORINE", "MODIS", "Globcover", "SRTM", "ALOS"]


def _create_polygon(lon, lat, buffer_dist, crs_in="EPSG:4326", circle=False):
    """Create google earth engine polygon

    Creates polygon to retrieve a square map with center point
    `lat`, `lon` and which fits a circle with radius `buffer_dist`.

    Parameters
    ----------
    lat : float
        Center latitude from which we extract a map
    lon : float
        Center longitude from which we extract a map
    buffer_dist : int, optional
        Distance in meters from the given (lat,lon) where a map is extracted, by default 20000
    crs_in: str


    Returns
    -------
    geometry: ee.Geometry.Polygon
        Google earth engine Polygon geometry
    """

    if earth_engine is None:
        raise ValueError(
            "ee (earthengine-api) is required to get maps from Google Earth Engine"
        )

    utm_epsg = _utmzone2epsg(*_mgrs_from_latlon(lat, lon))
    crs_to = pyproj.CRS.from_epsg(utm_epsg)
    crs_from = pyproj.CRS.from_user_input(crs_in)

    # transformer for point in input project to original map projection
    transformer = pyproj.Transformer.from_crs(
        crs_from=crs_from, crs_to=crs_to, always_xy=True
    )
    # create buffer of certain distance around point x,y
    buf = Point(transformer.transform(lon, lat)).buffer(
        buffer_dist
    )  # distance in metres
    if circle:
        xt, yt = buf.exterior.coords.xy
    else:
        xt, yt = buf.envelope.exterior.coords.xy
    # transformer from square bounding box in original grid
    # to lat/lon required for geometry. Geometry in Google EE
    # is always lat/lon
    transformer = pyproj.Transformer.from_crs(
        crs_from=crs_to, crs_to=pyproj.CRS.from_user_input("EPSG:4326"), always_xy=True
    )
    lon, lat = transformer.transform(xt, yt)
    list_vs = [[[x, y] for x, y in zip(lon, lat)]]
    geometry = earth_engine.Geometry.Polygon(list_vs, "EPSG:4326", False)

    return geometry


def _get_image(datasource):
    """Get URL from google earth engine to retrieve spatial data

    Parameters
    ----------
    datasource : str {'CGLS-LC100', 'CORINE', 'MODIS','Globcover', 'SRTM', 'ALOS'}
            Landcover or elevation datasource

    Returns
    -------
    image: ee.Image
            Google earth engine image
    """
    if earth_engine is None:
        raise ValueError(
            "ee (earthengine-api) is required to get maps from Google Earth Engine"
        )

    if datasource == "CGLS-LC100":
        url = "COPERNICUS/Landcover/100m/Proba-V/Global/2015"
        band = "discrete_classification"
    elif datasource == "CORINE":
        url = "COPERNICUS/CORINE/V20/100m/2018"
        band = "landcover"
    elif datasource == "MODIS":
        url = "MODIS/006/MCD12Q1/2018_01_01"
        band = "LC_Type1"
    elif datasource == "SRTM":
        url = "USGS/SRTMGL1_003"
        band = "elevation"
    elif datasource == "ALOS":
        url = "JAXA/ALOS/AW3D30/V2_2"
        band = "AVE_DSM"
    elif datasource == "Globcover":
        url = "ESA/GLOBCOVER_L4_200901_200912_V2_3"
        band = "landcover"
    else:
        str_valid = ", ".join(LIST_DATA_SOURCES)
        raise ValueError(f"Please specify a valid data source from {str_valid}")
    dataset = earth_engine.Image(url)
    image = dataset.select(band)
    return image


def get_ee_map(lat, lon, buffer_dist=20000, source="SRTM"):
    """Extract map from a given lat, lon

    Extract the smallest square which fits a cirle with radius buffer_dist
    around the coordinates lat,lon.

    Parameters
    ----------
    lat : float
        Center latitude from which we extract a map
    lon : float
        Center longitude from which we extract a map
    buffer_dist : int, optional
        Distance in meters from the given (lat,lon) where a map is extracted, by default 20000
    source : str {"CGLS-LC100", "CORINE", "MODIS", "Globcover", "SRTM", "ALOS"}, optional
        Landcover or elevation datasource, by default "SRTM"
    """
    tmpfile = Path(tempfile.gettempdir()) / f"{source}.zip"
    tmpfile.unlink(missing_ok=True)
    utm_epsg = _utmzone2epsg(*_mgrs_from_latlon(lat, lon))
    ee_image = _get_image(source)
    geom = _create_polygon(lon, lat, buffer_dist, circle=False)

    logger.debug(f"Getting download URL from earth engine for {lat}, {lon}")
    final_url = ee_image.getDownloadURL(
        {
            "region": geom,
            "crs": "EPSG:" + str(utm_epsg),
            "scale": ee_image.projection().nominalScale().getInfo(),
        }
    )
    logger.debug(f"Downloading file {tmpfile}")
    urllib.request.urlretrieve(final_url, tmpfile)

    logger.debug(f"Unzipping and writing file {tmpfile}")
    with zipfile.ZipFile(tmpfile) as zf:  # open the zip file
        for file in zf.namelist():
            output_name = Path(f"{tmpfile.stem}.tif")  # output path
            with open(output_name, "wb") as f:  # open the output path for writing
                f.write(zf.read(file))  # save the contents of the file in it

    if source not in ["SRTM", "ALOS"]:
        ras = read_raster_map(output_name, map_type="landcover")
        lct = LandCoverTable.read_json(
            Path(__file__).resolve().parent / "landcovertables" / f"{source}.json"
        )
        output_name.unlink(missing_ok=True)  # remove
        return (ras, lct)
    else:
        ras = read_raster_map(output_name, map_type="elevation")
        output_name.unlink(missing_ok=True)  # remove
        return ras
