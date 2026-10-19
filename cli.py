"""Run the synthetic Anatomy-as-Data measurement pipeline without a UI."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.measurements import measure_all_labels
from src.queries import centroid_distance_mm, largest_structure
from src.reporting import build_report, export_csv, export_json
from src.volume_io import load_volume_npz, make_demo_volume, save_volume_npz


def run(input_path: Path | None, output_dir: Path, save_demo: bool = False) -> dict[str, object]:
    volume = load_volume_npz(input_path) if input_path else make_demo_volume()
    measurements = measure_all_labels(volume)
    report = build_report(volume, measurements)
    if len(measurements) >= 2:
        report["distance_between_first_two_labels_mm"] = centroid_distance_mm(measurements[0], measurements[1])
    report["largest_structure_label"] = largest_structure(measurements).label
    output_dir.mkdir(parents=True, exist_ok=True)
    export_json(report, output_dir / "measurements.json")
    export_csv(measurements, output_dir / "measurements.csv")
    if save_demo and input_path is None:
        save_volume_npz(volume, output_dir / "synthetic_demo_volume.npz")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure labelled 3D NPZ volumes with explicit geometry.")
    parser.add_argument("--input", type=Path, help="Path to a documented Anatomy-as-Data NPZ volume.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/latest"))
    parser.add_argument("--save-demo", action="store_true", help="Also write the generated synthetic demo volume.")
    args = parser.parse_args()
    report = run(args.input, args.output_dir, args.save_demo)
    print(f"Measured {len(report['measurements'])} labels; exports written to {args.output_dir}")


if __name__ == "__main__":
    main()
