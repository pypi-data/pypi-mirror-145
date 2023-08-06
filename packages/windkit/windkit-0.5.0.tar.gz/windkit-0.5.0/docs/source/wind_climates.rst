.. _wind_climates:

Wind Climate Objects
====================

As described in the :ref:`windkit_intro`, WindKit relies on specifically structured xarray datasets in addition to classes to store data in memory. Below you will find out about the different types of objects that are present in WindKit.

Time Series Wind Climate
--------------------

The `time_series_wind_climate` (**twc**) contains a time series of `wind speed` and `wind direction`. It is a the most basic wind climate from which the ones listed below can be derived.

In addition to the :ref:`core_coordinates`, **twc** objects also contain the dimension ``time``, which identifies the time.


Binned Wind Climate
--------------------

The `binned_wind_climate` (**bwc**) contains a histogram representation of the wind, for different wind direction sectors. Historically these have been used for encoding observational data, however there is no reason that they couldn't be used for other wind data as well. In WAsP, these are stored in ".tab" and ".owc" files, which can be read using WindKit.

In addition to the :ref:`core_coordinates`, **bwc** objects also contain the dimension ``wsbin``, which identifies the wind speed bins of the histogram. Wind speed bins are characterized by their upper boundary, e.g. a wind speed bin from 0-1 would be identified with a wind speed value of 1.

In addition to reading **bwc**'s from files, you can create them from weibull distrubtions or time-series as well.


Generalized Wind Climate
------------------------

A Generalized Wind Climate is a key part of the WAsP Methodology. The `generalized_wind_climate` (**gwc**) contains the wind in a virtual world, where there is no terrain and there are homogeneous roughness values, i.e. no roughness changes. Generalized wind climates are represented as Weibull distributions (scale [A]; shape [k]) and sector-wise frequency values. Because the **gwc** exists in a virtual world, it contains several additional dimensions compared to the other wind climate files. ``gen_height`` is the height above the constant terrain in the generalized atmosphere, and ``gen_roughness`` is the homogeneous roughness length. In WAsP, you were limited to exactly five of each of these parameters, however in PyWAsP you can use as many or as few as you wish.

WindKit provides the ability to create **gwc** objects from ".lib" and ".gwc" files, but if you want to create a **gwc** from a **bwc**, you will need to purchase and install `pywasp`.


Weibull Wind Climate
--------------------

The `weibull_wind_climate` (**wwc**) is related to the `Binned Wind Climate`_, but instead of a histogram, it is represented solely as the weibull parameters for the different sectors. In WAsP, this was often stored as ".rsf" files, which can be read from WindKit. These are the objects that most often store the results of a WAsP simulation.

.. note:: If you have a license for `pywasp`, you can create **wwc** objects by fitting **bwc** with a Weibull distribution, or by downscaling a **gwc** object.
