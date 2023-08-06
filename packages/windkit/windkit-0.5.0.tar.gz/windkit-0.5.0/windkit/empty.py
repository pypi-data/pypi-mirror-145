# (c) 2022 DTU Wind Energy
"""
Create empty datasets for various WindKit structures.

The datasets have the correct shape, dimensions, coordinates and data variables and
can also be filled with meaningful random data.
"""

import numpy as np
import scipy.stats
import xarray as xr
from .metadata import (
    _MET_ATTRS,
    _TOPO_EFFECTS_ATTRS,
    _WEIB_ATTRS,
    _BWC_ATTRS,
    _HIS_ATTRS,
    ALL_VARS_META,
    update_var_attrs,
    update_history,
)
from .spatial import spatial_stack, spatial_unstack
from .sector import create_sector_coords, create_ws_bin_coords

_metvars_3d_nosec = [
    "wspd",
    "power_density",
    "air_density",
    "wspd_emergent",
    "power_density_emergent",
]
_metvars_4d = ["wspd_sector", "power_density_sector"]

# metadata for the generalized wind climate
_GEN_COORDS_META = {
    "gen_height": ALL_VARS_META["gen_height"],
    "gen_roughness": ALL_VARS_META["gen_roughness"],
    "sector": ALL_VARS_META["sector"],
}


def _define_std_arrays(output_locs, nsec):
    """Return standard 2D, 3D, and 4D arrays in point format"""
    out_std = spatial_stack(output_locs).drop_vars(output_locs.data_vars)

    # Setup sector
    sector_coords = create_sector_coords(nsec).coords
    dims = ("sector", "point")
    out_sec_std = out_std.assign_coords(sector_coords)
    values = np.full((nsec, out_std.dims["point"]), np.nan, np.float32)

    out_das = {}
    # x, y
    out_das["da_2d"] = xr.DataArray(
        values[0,], out_std.coords, dims[1:], attrs={"_pwio_data_is_2d": True}
    )

    # sector, x, y
    out_das["da_3d_nohgt"] = xr.DataArray(
        values, out_sec_std.coords, dims, attrs={"_pwio_data_is_2d": True}
    )

    # height, x, y
    out_das["da_3d_nosec"] = xr.DataArray(
        values[0,], out_std.coords, dims[1:], attrs={"_pwio_data_is_2d": False}
    )

    # Sector, height, x, y
    out_das["da_4d"] = xr.DataArray(values, out_sec_std.coords, dims, attrs={})

    return out_das, out_std.attrs


def _copy_chunks(in_ds, out_ds):
    """copy chunks from in_ds to out_ds"""
    # If input is not chunked it will have an emtpy chunks dict, so we need to build a
    # custom chunk_map based on the chunked dimensions of the original data.
    chunk_map = {}
    for i in in_ds.chunks:
        chunk_map[i] = in_ds.chunks[i][0]

    # Remember in Python empty dictionaries are False
    if chunk_map:
        return out_ds.chunk(chunk_map)
    else:
        return out_ds


def empty_wasp_site_factors(output_locs, nsec=12, **kwargs):
    """Create empty site-factors dataset.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors. Defaults to 12.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Empty site factors dataset.
    """
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)

    ds = xr.Dataset(
        {
            "z0meso": da_dict["da_3d_nohgt"],
            "slfmeso": da_dict["da_3d_nohgt"],
            "displ": da_dict["da_3d_nohgt"],
            "user_def_speedups": da_dict["da_4d"],
            "orographic_speedups": da_dict["da_4d"],
            "obstacle_speedups": da_dict["da_4d"],
            "roughness_speedups": da_dict["da_4d"],
            "user_def_turnings": da_dict["da_4d"],
            "orographic_turnings": da_dict["da_4d"],
            "obstacle_turnings": da_dict["da_4d"],
            "roughness_turnings": da_dict["da_4d"],
            "dirrix": da_dict["da_3d_nohgt"],
            "site_elev": da_dict["da_2d"],
            "rix": da_dict["da_2d"],
        },
        attrs=unstack_attrs,
    )

    ustack_ds = spatial_unstack(ds)

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _TOPO_EFFECTS_ATTRS)

    return update_history(ds)


def empty_bwc(output_locs, nsec=12, not_empty=True, seed=9876538):
    """
    Create empty binned wind climate dataset.

    If not_empty=True, the data variables are filled with meaninful random numbers,
    e.g. the sum of wdfreq is 1.

    Parameters
    ----------
    output_loc : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data.
    seed : int
        Seed for the random data, defaults to 9876538.

    Returns
    -------
    ds : xarray.Dataset
        Binned wind climate dataset either empty or filled with
        random numbers.
    """

    nbins = 30
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)
    ds = xr.Dataset(
        {"wdfreq": da_dict["da_4d"], "wsfreq": da_dict["da_4d"]}, attrs=unstack_attrs
    )
    wsbin_coords = create_ws_bin_coords(bin_width=1.0, nws=30)

    ds["wsfreq"] = ds["wsfreq"].expand_dims({"wsbin": wsbin_coords.values})
    ds = ds.assign_coords({**wsbin_coords.coords})
    n_pt = len(ds["point"])

    if not_empty:
        wsbin_n = np.linspace(1, nbins, nbins)
        rng = np.random.default_rng(seed)
        wsbin_full = wsbin_n.repeat(nsec * n_pt).reshape((nbins, nsec, n_pt))
        k = rng.uniform(1.5, 2.5, [nsec, n_pt])
        A = rng.uniform(5, 10, [nsec, n_pt])
        wsbin_freq_not1 = scipy.stats.weibull_min.pdf(wsbin_full, k, scale=A)
        wsbin_freq = wsbin_freq_not1 / wsbin_freq_not1.sum(0)

        ds["wsfreq"] = xr.DataArray(wsbin_freq, ds["wsfreq"].coords, ds["wsfreq"].dims)
        ds["wdfreq"] = xr.DataArray(
            np.random.dirichlet(np.ones(nsec), n_pt).T,
            ds["wdfreq"].coords,
            ds["wdfreq"].dims,
        )
    ustack_ds = spatial_unstack(ds)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _BWC_ATTRS)

    return update_history(ds)


def empty_wwc(output_locs, nsec=12, not_empty=True, seed=9876538, **kwargs):
    """Create empty weibull wind climate dataset.

    If not_empty=True,the data variables are filled with meaninful random numbers, e.g.
    the values from A are generated from a uniform function between 5
    and 10 and the values for k from a uniform function between 1.5 and 2.5.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Weibull wind climate dataset either empty or filled with
        random numbers.

    """
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)

    ds = xr.Dataset(
        {"A": da_dict["da_4d"], "k": da_dict["da_4d"], "wdfreq": da_dict["da_4d"]},
        attrs=unstack_attrs,
    )
    n_pt = len(ds["point"])
    if not_empty:
        rng = np.random.default_rng(seed)
        k = rng.uniform(1.5, 2.5, [nsec, n_pt])
        A = rng.uniform(5, 10, [nsec, n_pt])
        ds["A"] = xr.DataArray(A, ds["A"].coords, ds["A"].dims)
        ds["k"] = xr.DataArray(k, ds["k"].coords, ds["k"].dims)
        ds["wdfreq"] = xr.DataArray(
            np.random.dirichlet(np.ones(nsec), n_pt).T,
            ds["wdfreq"].coords,
            ds["wdfreq"].dims,
        )

    ustack_ds = spatial_unstack(ds)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _WEIB_ATTRS)

    return update_history(ds)


def empty_gwc(output_locs, nsec=12, not_empty=True, seed=9876538, **kwargs):
    """Create empty generalized wind climate dataset.

    If not_empty=True, the data variables are filled with meaninful random numbers, e.g.
    the values from A are generated from a uniform function between 5
    and 10 and the values for k from a uniform function between 1.5 and 2.5.

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data. Defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.
    kwargs : dict
        Additional arguments.
    Returns
    -------
    ds : xarray.Dataset
        Generalized wind climate dataset either empty or filled with
        random numbers.

    """
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)

    ds = xr.Dataset(
        {"A": da_dict["da_4d"], "k": da_dict["da_4d"], "wdfreq": da_dict["da_4d"]},
        attrs=unstack_attrs,
    )
    gen_rou_coords = np.array([0.0, 0.03, 0.1, 0.4, 1.5], dtype=float)
    gen_h_coords = np.array([50, 100.0, 200.0], dtype=float)
    n_gen_rou = len(gen_rou_coords)
    n_gen_h = len(gen_h_coords)
    ds = ds.expand_dims({"gen_roughness": gen_rou_coords,})
    ds["A"] = ds["A"].expand_dims({"gen_height": gen_h_coords})
    ds["k"] = ds["k"].expand_dims({"gen_height": gen_h_coords})

    n_pt = len(ds["point"])
    if not_empty:
        rng = np.random.default_rng(seed)
        k = rng.uniform(1.5, 2.5, [n_gen_h, n_gen_rou, nsec, n_pt])
        A = rng.uniform(5, 10, [n_gen_h, n_gen_rou, nsec, n_pt])
        ds["A"] = xr.DataArray(A, ds["A"].coords, ds["A"].dims)
        ds["k"] = xr.DataArray(k, ds["k"].coords, ds["k"].dims)
        # ds['wdfreq']=xr.DataArray(
        # np.random.dirichlet(np.ones(nsec), n_pt).T, ds['wdfreq'].coords, ds['wdfreq'].dims)
        ds["wdfreq"] = xr.DataArray(
            np.random.dirichlet(np.ones(nsec), (n_gen_rou, n_pt)),
            dims=("gen_roughness", "point", "sector"),
        )
    ds["gen_roughness"].attrs = {**_GEN_COORDS_META["gen_roughness"]}
    ds["gen_height"].attrs = {**_GEN_COORDS_META["gen_height"]}
    ds["sector"].attrs = {**_GEN_COORDS_META["sector"]}

    ustack_ds = spatial_unstack(ds)

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _WEIB_ATTRS)
    return update_history(ds)


def empty_met_fields(
    output_locs, nsec=12, met_fields=["wspd", "power_density"], **kwargs
):
    """Create empty dataset filled with met_fields

    Parameters
    ----------
    output_locs : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12
    met_fields : list of strings
        List of variables to include in the output, defaults to
        ["wspd", "power_dens"]
    kwargs : dict
        Additional arguments.
    Returns
    -------
    ds : xarray.Dataset
        empty met fields dataset
    """
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)

    out_vars = {}
    for var in met_fields:
        if var in _metvars_4d:
            out_vars[var] = da_dict["da_4d"]
        elif var in _metvars_3d_nosec:
            out_vars[var] = da_dict["da_3d_nosec"]
        else:
            raise ValueError(f"Unknown met_field {var}, cannot add to result")

    ds = xr.Dataset(out_vars, attrs=unstack_attrs,)

    ustack_ds = spatial_unstack(ds)

    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _MET_ATTRS)
    return update_history(ds)


def empty_z0meso(output_locs, nsec=12, **kwargs):
    """Empty site_factors with only z0meso and slfmeso.

    Parameters
    ----------
    out_grid : xarray.Dataset
        Output geospatial information.
    nsec : int
        Number of sectors, defaults to 12.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        Empty dataset.
    """

    empty_z0 = empty_wasp_site_factors(output_locs, nsec)[["z0meso", "slfmeso"]]

    return update_history(empty_z0)


def empty_pwc(
    output_locs, nsec=12, post_vars=None, include_site_factors=False, **kwargs
):
    """Empty predicted wind climate with optional variables.

    Parameters
    ----------
    out_grid : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    post_vars : list of strings
        List of variables to include in the output.
    include_site_factors : bool
        Include site_factors in result? Defaults to False.
    kwargs : dict
        Additional arguments.

    Returns
    -------
    ds : xarray.Dataset
        empty predicted wind climate dataset.
    """

    ds_list = [empty_wwc(output_locs, nsec)]
    if include_site_factors:
        ds_list.append(empty_wasp_site_factors(output_locs, nsec)[include_site_factors])
    if post_vars is not None:
        ds_list.append(empty_met_fields(output_locs, nsec, post_vars))

    pwc = xr.merge(ds_list, combine_attrs="no_conflicts")
    return update_history(pwc)


def empty_wv_count(output_locs, nsec=12, not_empty=True, seed=9876538):
    """
    Create empty wind vector count dataset.
    If not_empty=True, the data variables are filled with meaninful random numbers.

    Parameters
    ----------
    output_loc : xarray.Dataset
        Output geospatial information
    nsec : int
        Number of sectors, defaults to 12.
    not_empty : bool
        If true, the empty dataset is filled with random
        meaningful data, defaults to True.
    seed : int
        Seed for the random data, defaults to 9876538.

    Returns
    -------
    ds : xarray.Dataset
        Wind vector count dataset either empty or filled with
        random numbers.
    """

    nbins = 30
    da_dict, unstack_attrs = _define_std_arrays(output_locs, nsec)
    ds = xr.Dataset({"wv_count": da_dict["da_4d"]}, attrs=unstack_attrs)
    wsbin_coords = create_ws_bin_coords(bin_width=1.0, nws=30)

    ds["wv_count"] = ds["wv_count"].expand_dims({"wsbin": wsbin_coords.values})
    ds = ds.assign_coords({**wsbin_coords.coords})
    n_pt = len(ds["point"])

    if not_empty:
        count_values = np.array(
            [
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 2.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 7.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 5.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 4.0, 0.0, 1.0, 1.0, 6.0, 11.0, 3.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 1.0, 0.0, 4.0, 4.0, 3.0, 2.0, 11.0, 2.0, 0.0],
                [0.0, 0.0, 8.0, 0.0, 0.0, 5.0, 2.0, 1.0, 5.0, 11.0, 0.0, 1.0],
                [2.0, 0.0, 2.0, 0.0, 1.0, 6.0, 2.0, 2.0, 0.0, 0.0, 2.0, 3.0],
                [0.0, 0.0, 5.0, 20.0, 1.0, 9.0, 4.0, 8.0, 1.0, 2.0, 4.0, 4.0],
                [1.0, 0.0, 5.0, 10.0, 3.0, 11.0, 12.0, 11.0, 6.0, 0.0, 3.0, 6.0],
                [0.0, 0.0, 2.0, 0.0, 3.0, 0.0, 15.0, 11.0, 10.0, 4.0, 4.0, 5.0],
                [0.0, 4.0, 0.0, 0.0, 4.0, 5.0, 7.0, 9.0, 25.0, 12.0, 7.0, 9.0],
                [0.0, 2.0, 0.0, 0.0, 7.0, 36.0, 15.0, 12.0, 28.0, 9.0, 31.0, 2.0],
                [0.0, 1.0, 0.0, 0.0, 4.0, 39.0, 26.0, 18.0, 12.0, 15.0, 21.0, 0.0],
                [0.0, 3.0, 0.0, 0.0, 15.0, 34.0, 26.0, 10.0, 32.0, 34.0, 13.0, 0.0],
                [0.0, 4.0, 0.0, 0.0, 1.0, 39.0, 32.0, 30.0, 14.0, 33.0, 16.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 1.0, 82.0, 23.0, 2.0, 18.0, 28.0, 19.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 0.0, 1.0, 44.0, 13.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 15.0, 19.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 12.0, 9.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 3.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        ).reshape(nbins, nsec, 1)
        cv_p = np.tile(count_values, n_pt)

        ds["wv_count"] = xr.DataArray(cv_p, ds["wv_count"].coords, ds["wv_count"].dims)

    ustack_ds = spatial_unstack(ds)
    ds = update_var_attrs(_copy_chunks(output_locs, ustack_ds), _HIS_ATTRS)

    return update_history(ds)
