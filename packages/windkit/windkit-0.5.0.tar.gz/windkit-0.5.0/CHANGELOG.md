# Changelog

All major changes are listed here.


##  Unreleased

### New Features
* Added functions for simple wind-related calculations:
   - `windkit.wind_speed_and_direction` calculates wind speed and direction from horizontal wind vectors U and V
   - `windkit.wind_vectors` calculates horizontal wind vectors U and V from wind speed and direction
   - `windkit.wind_direction_difference` calculates the smallest (signed) circular difference between wind directions in degrees.
   - `windkit.wind_speed` calculates horizontal wind speed from vectors U and V
   - `windkit.wind_direction` calculates horizontal wind direction from vectors U and V
   - `windkit.wd_to_sector` to calculate the bin-index for wind directions for a given number of bins/sectors
* Support for new Xarray-based Wind Turbine Generator (WTG) object added
*  New wind climate dataset validator function and decorator.
   - The function receives an `xarray.Dataset` and returns `True` or `False`.
   - The decorator wraps a function that receives a wind climate dataset and raises a `WindClimateValidationError` if the dataset is not valid.
   - It checks dimensions, attributes and data variables.
   - The functions available are:
     - `bwc_validate`,`bwc_validate_wrapper` for binned wind climate dataset, imported from `windkit.binned_wind_climate`
     - `wwc_validate`,`wwc_validate_wrapper` for weibull wind climate dataset, imported from `windkit.weibull_wind_climate`
     - `gwc_validate`,`gwc_validate_wrapper` for generalized wind climate dataset, imported from `windkit.generalized_wind_climate`
     - `ts_validate`,`ts_validate_wrapper` for time series wind climate dataset, imported from `windkit.time_series_wind_climate`

* New `WindClimateValidationError`, raised by the newly introduced wind climate dataset validators.
* New method `BBox.to_geoseries()` that converts Bounding box to `geopandas.Geoseries`
* New `empty` module that generates `xarray.Dataset` instances filled with either `NaN` or meaningful values.
   -  Suitable for testing.
   - Current available functions are:
     - `empty.empty_wasp_site_factors()`: Create empty site-factors dataset
     - `empty.empty_bwc()`: Create empty binned wind climate dataset filled with meaningul random numbers, i.e. they are generated
    with a weibull distribution, the sum of `wdfreq` is 1, etc.
     - `empty.empty_wwc()`: Create empty weibull wind climate dataset filled with meaningul random numbers, e.g.the values from `A`
    are generated from a uniform function between `5` and `10` and the values for `k` from a uniform function between `1.5` and `2.5`.
     - `empty.empty_gwc()`: Create empty generalized wind climate dataset with the data variables are filled with meaninful random
    numbers, e.g. the values from `A` are generated from a uniform function between `5` and `10` and the values for `k` from a uniform function between `1.5` and `2.5`.
     - `empty.empty_met_fields()`: Create empty dataset filed with `met_fields`
     - `empty.empty_z0meso()`: Create empty site_factors with only `z0meso` and `slfmeso`
     - `empty.empty_pwc()`: Create empty predicted wind climate with optional variables
* New plotting functions in module `windkit.plot`
   - `windkit.plot.vertical_profile()` plots the vertical profile of the dataArray or dataArrays introduced.
   - `windkit.plot.time_series()` creates a time series plot.
   - `windkit.plot.single_curve()` and `windkit.plot.power_ct_curves()` add plots for electrical power output curve, thrust curve, RPM, Ct, Cp or any other curve the user wants to pass through.

* New function `windkit.time_series.read_ts_windpro_txt`
   -  Reads windpro format txt file into a `xarray.Dataset`
### Removed
* Removed `windkit.binned_wind_climate.dir_to_sec` in favor of `windkit.wd_to_sector`
* Modules `WaspVectorMap` and `WaspRasterMap` were moved to `pywasp` and are no longer available.
 - Removed legacy WTG objet `WindTurbine`
### Changes
* `windkit/windturbine.py`
    - Added function `read_wtg` to create an `xarray.Dataset` representation of a turbine
    - Added `wtg_power` and `wtg_ct` to return power and ct for given wind speed
    - Added `wtg_to_pywake`, which makes a PyWake wind turbine class from the dataset
 - renamed `vectormap` to `vector_map`
 - renamed `rastermap` to `raster_map`
 - renamed `elevationmap` to `elevation_map`
 - renamed `roughnessmap` to `roughness_map`
 - `windkit.read_elevation_map` and `windkit.read_roughness_map` now reads both raster and vector maps.
 - Changed the default behavior of  `windkit.spatial.clip` for rasters/cuboids so small padding is added to the mask, ensuring that raster/cuboid pixels/cells on the edge of the mask are included in the clipping. The previous behavior can be achieved by setting `pad=False`
 - Updated `windkit.spatial.clip` for `point` `xr.dataset` to always include points that are on the edges of the mask (previously only points inside were included)
 - Updated BWC "header" and GWC "desc" to both be named "wasp_header" (only included for objects originating from WAsP files or methods).
 - Updated to always use "crs" as spatial reference argument name

### Improvements
 - Updated `windkit.spatial.clip` so it uses a faster clipping method (`_clip_to_bbox_raster`) when the masking is provided as a `BBox` object. This speeds up clipping speed significantly.
 - Allowed `ws_bins` to be python `range` in `windkit.binned_wind_climate._freqs_to_dataset()`
 - Functions `windkit.spatial.to_point` and `windkit.spatial.to_raster_point` now also work on scalar datasets.
- Landcover GMLs use custom reader/write to ensure compatibility with WAsP & Map Editor
- Fix bug in `metadata.update_var_attrs` to store "Object type" as the string "None" to properly write to netCDF

### Bug fixes

### Deprecations
### Added


### Changed


### Fixed
