"""Portable, unit-labelled exports for a measurement run."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .measurements import LabelMeasurement
from .volume_io import SpatialVolume


def build_report(volume: SpatialVolume, measurements: list[LabelMeasurement]) -> dict[str, object]:
    return {
        "coordinate_convention": "z/y/x voxel-centre indices transformed to z/y/x physical millimetres",
        "spacing_mm_zyx": list(volume.spacing_mm),
        "origin_mm_zyx": list(volume.origin_mm),
        "direction_zyx": volume.direction.tolist(),
        "volume_shape_zyx": list(volume.labels.shape),
        "measurements": [measurement.to_dict() for measurement in measurements],
    }


def export_json(report: dict[str, object], path: Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return destination


def export_csv(measurements: list[LabelMeasurement], path: Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    rows = [measurement.to_dict() for measurement in measurements]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["label"])
        writer.writeheader()
        writer.writerows(rows)
    return destination
