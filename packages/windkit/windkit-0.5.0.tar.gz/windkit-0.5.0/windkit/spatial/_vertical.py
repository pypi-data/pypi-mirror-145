# (c) 2022 DTU Wind Energy
"""
Height related functions.
"""
from ._dimensions import _get_vertical_dim


def has_height_coord(obj):
    vertical_dim = _get_vertical_dim()
    return vertical_dim in obj.coords


def has_height_dim(obj):
    vertical_dim = _get_vertical_dim()
    return vertical_dim in obj.dims
