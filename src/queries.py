"""Small query API over structured label measurements."""

from __future__ import annotations

import math

from .measurements import LabelMeasurement


def find_label(measurements: list[LabelMeasurement], label: int) -> LabelMeasurement:
    for measurement in measurements:
        if measurement.label == label:
            return measurement
    raise KeyError(f"label {label} is not present in the measurement set")


def largest_structure(measurements: list[LabelMeasurement]) -> LabelMeasurement:
    if not measurements:
        raise ValueError("cannot identify a largest structure from an empty measurement set")
    return max(measurements, key=lambda item: (item.physical_volume_mm3, -item.label))


def centroid_distance_mm(first: LabelMeasurement, second: LabelMeasurement) -> float:
    return math.dist(first.centroid_physical_mm_zyx, second.centroid_physical_mm_zyx)
