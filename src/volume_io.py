"""Volume containers and deterministic synthetic demonstration data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class SpatialVolume:
    """A labelled 3D array with explicit z/y/x physical geometry in millimetres."""

    labels: np.ndarray
    spacing_mm: tuple[float, float, float] = (1.0, 1.0, 1.0)
    origin_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)
    direction: np.ndarray | None = None

    def __post_init__(self) -> None:
        array = np.asarray(self.labels)
        if array.ndim != 3:
            raise ValueError("labels must be a three-dimensional z/y/x array")
        if not np.issubdtype(array.dtype, np.integer):
            raise TypeError("labels must use an integer dtype")
        if any(value <= 0 for value in self.spacing_mm):
            raise ValueError("spacing_mm must contain three positive values")
        if len(self.spacing_mm) != 3 or len(self.origin_mm) != 3:
            raise ValueError("spacing_mm and origin_mm must each have three values")
        matrix = np.eye(3, dtype=float) if self.direction is None else np.asarray(self.direction, dtype=float)
        if matrix.shape != (3, 3) or not np.isfinite(matrix).all():
            raise ValueError("direction must be a finite 3x3 matrix")
        if np.isclose(np.linalg.det(matrix), 0.0):
            raise ValueError("direction must be invertible")
        object.__setattr__(self, "labels", array)
        object.__setattr__(self, "direction", matrix)


def make_demo_volume() -> SpatialVolume:
    """Create a small deterministic synthetic segmentation with two structures.

    Label 1 is a 3x4x5 cuboid and label 2 is a 4x3x3 cuboid.  The known shape
    makes the sample appropriate for demonstrations and numerical tests; it is
    not patient data and carries no anatomical interpretation.
    """

    labels = np.zeros((12, 14, 16), dtype=np.int16)
    labels[1:4, 2:6, 3:8] = 1
    labels[6:10, 8:11, 10:13] = 2
    return SpatialVolume(
        labels=labels,
        spacing_mm=(2.0, 1.5, 1.0),
        origin_mm=(10.0, -5.0, 20.0),
    )


def save_volume_npz(volume: SpatialVolume, path: Path) -> Path:
    """Save the documented portable NPZ interchange format."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        destination,
        labels=volume.labels,
        spacing_mm=np.asarray(volume.spacing_mm, dtype=float),
        origin_mm=np.asarray(volume.origin_mm, dtype=float),
        direction=np.asarray(volume.direction, dtype=float),
    )
    return destination


def load_volume_npz(path: Path) -> SpatialVolume:
    """Load only the project's safe, documented NPZ volume format."""

    with np.load(Path(path), allow_pickle=False) as data:
        required = {"labels", "spacing_mm", "origin_mm", "direction"}
        missing = required.difference(data.files)
        if missing:
            raise ValueError(f"Missing required NPZ fields: {', '.join(sorted(missing))}")
        return SpatialVolume(
            labels=data["labels"],
            spacing_mm=tuple(float(v) for v in data["spacing_mm"]),
            origin_mm=tuple(float(v) for v in data["origin_mm"]),
            direction=data["direction"],
        )
