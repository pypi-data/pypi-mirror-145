.. _topographic_data:

Topographic Data
================

Topographic data in WindKit comes in two formats, vector `vector_map` and raster `raster_map`, and is stored with two variables of interest, elevation and land-cover, sometimes known as land-use.

Topographic Data Structures
---------------------------

Vector Data
^^^^^^^^^^^

Vector Data represents objects as points, lines, or polygons, and is the data that you are used to working with in WAsP, which treats elevation as contours and uses change lines to identify areas of different roughness. Vector data is stored in memory using the `geopandas.GeoDataFrame` objects, which allows you to apply many common GIS functions to the data.

WindKit's vector_map functions work with the common `WAsP .map (WAsP) <https://gdal.org/drivers/vector/wasp.html#vector-wasp>`_ file format, as well as many other common GIS formats. We have relied mostly on custom `Geography Markup Language (GML) <https://gdal.org/drivers/vector/gml.html>`_ formats for data exchange with WAsP and the WAsP Map Editor, but recommend using `GeoPackage (GPKG) <https://gdal.org/drivers/vector/gpkg.html#vector-gpkg>`_ for working with GIS programs.

Raster Data
^^^^^^^^^^^

Raster data is data that is on a regular grid, which in windkit means that it is made up of square pixels, dx is equal to dy. The data may be either in projected or geographic space, but each pixel contains a value of the variable that the object stores.

Many online resources, such as SRTM elevation or the `Copernicus Global Land Cover <https://doi.org/10.5281/zenodo.3243509>`_, provide data in raster format. WindKit has been extensively tested using the `Golden Software ASCII Grid <https://gdal.org/drivers/raster/gsag.html>`_ and `GeoTIFF <https://gdal.org/drivers/raster/gtiff.html>`_ file formats, but most GIS formats should work. Raster data is stored in memory using xarray.DataArrays, and has some GIS functionality added using the `Rasterio <https://rasterio.readthedocs.io/en/latest/>`_ library.

Topographic Data Variables
--------------------------

Elevation Data
^^^^^^^^^^^^^^

Elevation data is data that describes the height of the surface of the Earth above sea level. It is also common called terrain data, or orography data.

Atmospheric Roughness Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

Atmospheric roughness data is a proxy for the roughness of the surface. It is defined as the height at which the wind speed reaches 0 m/s. In WindKit, we do not define this data directly, but instead rely on a combination of land cover maps, and LandCoverTables to determine the value of this field.

Land cover Data
^^^^^^^^^^^^^^^

Land cover data is data that describes the surface of the land in broad descriptive categories. For example, you may list the land as urban, cropland or forest.

In WindKit, land-cover maps are used in place of roughness maps. These maps are also able to be used in WAsP since 12.7. Instead of storing the roughness value directly on the lines, land-cover change lines use integer IDs to identify the land-cover class of a region, this is then combined with a `LandCoverTable` to get the necessary aerodynamic fields. This allows additional data, including displacement height, to be used in flow calculations, to provide improved descriptions of the land surface. However, it also means that for roughness data you will need to keep track of both you map, which specifies the categories of the data, and the `LandCoverTable`, which specifies the values that should replace the categories before any calculations can take place.

Topographic Data Download
--------------------------

WindKit provides an interface to the `Google Earth Engine
<https://earthengine.google.com/>`_, which provides several land cover and elevation datasets for download. These can be accessed run through the :py:mod:`windkit.get_map.get_ee_map` function.

.. note:: :py:func:`windkit.get_map.get_ee_map` is not imported by default as it relies on the      `earthengine-api
    <https://developers.google.com/earth-engine/guides/python_install>`_, which is not a dependency and needs to be installed if you wish to use this functionality. Additionally you will need to sign up for a Google Account, and accept their terms of service for the Google Earth Engine.
