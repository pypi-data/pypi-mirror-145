# (c) 2022 DTU Wind Energy
"""
Plotting functionality for WindKit objects

Plots are largely broken into two categories statistical and maps. Statistical plots
are generally plotted at a single location, e.g. mast or turbine location, while
maps show an overview of the area.
"""

from .histogram import histogram as histogram
from .histogram import histogram_lines as histogram_lines
from .operational_curves import power_ct_curves as power_ct_curves
from .operational_curves import single_curve as single_curve
from .raster_plot import raster_plot as raster_plot
from .roughness_rose import roughness_rose as roughness_rose

# from .time_series import time_series as time_series
from .wind_rose import wind_rose as wind_rose
