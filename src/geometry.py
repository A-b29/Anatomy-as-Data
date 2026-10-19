"""Coordinate conversion routines shared by measurements and visualisations."""

from __future__ import annotations

import numpy as np

from .volume_io import SpatialVolume


def indices_to_physical(points_zyx: np.ndarray, volume: SpatialVolume) -> np.ndarray:
    """Convert z/y/x voxel-centre indices to physical millimetre coordinates.

    The output ordering deliberately matches the input ordering (z, y, x). The
    direction matrix is therefore defined in that same axis order.
    """

    points = np.asarray(points_zyx, dtype=float)
    if points.shape[-1] != 3:
        raise ValueError("points_zyx must end in three coordinates")
    scaled = points * np.asarray(volume.spacing_mm, dtype=float)
    return scaled @ np.asarray(volume.direction, dtype=float).T + np.asarray(volume.origin_mm, dtype=float)


def voxel_volume_mm3(volume: SpatialVolume) -> float:
    """Return the physical volume represented by one voxel in mm³."""

    return float(np.prod(volume.spacing_mm))
