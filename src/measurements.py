"""Deterministic label-object measurements."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .geometry import indices_to_physical, voxel_volume_mm3
from .volume_io import SpatialVolume


@dataclass(frozen=True)
class LabelMeasurement:
    label: int
    voxel_count: int
    physical_volume_mm3: float
    centroid_index_zyx: tuple[float, float, float]
    centroid_physical_mm_zyx: tuple[float, float, float]
    bbox_min_index_zyx: tuple[int, int, int]
    bbox_max_exclusive_index_zyx: tuple[int, int, int]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def available_labels(volume: SpatialVolume) -> list[int]:
    """List non-background label IDs in ascending order."""

    return [int(value) for value in np.unique(volume.labels) if value != 0]


def measure_label(volume: SpatialVolume, label: int) -> LabelMeasurement:
    """Measure a single present label; background and absent labels are rejected."""

    if label == 0:
        raise ValueError("label 0 is background and cannot be measured as an object")
    indices = np.argwhere(volume.labels == label)
    if len(indices) == 0:
        raise KeyError(f"label {label} is not present in the volume")
    centroid = indices.mean(axis=0)
    physical_centroid = indices_to_physical(centroid[None, :], volume)[0]
    minimum = indices.min(axis=0)
    maximum_exclusive = indices.max(axis=0) + 1
    return LabelMeasurement(
        label=int(label),
        voxel_count=int(len(indices)),
        physical_volume_mm3=float(len(indices) * voxel_volume_mm3(volume)),
        centroid_index_zyx=tuple(float(v) for v in centroid),
        centroid_physical_mm_zyx=tuple(float(v) for v in physical_centroid),
        bbox_min_index_zyx=tuple(int(v) for v in minimum),
        bbox_max_exclusive_index_zyx=tuple(int(v) for v in maximum_exclusive),
    )


def measure_all_labels(volume: SpatialVolume) -> list[LabelMeasurement]:
    return [measure_label(volume, label) for label in available_labels(volume)]
