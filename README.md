# Anatomy-as-Data

Turn a labelled 3D segmentation into reproducible geometry measurements. The default input is a deterministic synthetic volume with two cuboids; it contains no patient data and is for software demonstration only.

## What it measures

- non-background label IDs and voxel counts;
- physical volumes in `mm³`;
- voxel-index and physical centroids in an explicit `z/y/x` convention;
- half-open bounding boxes (`min` inclusive, `max` exclusive); and
- largest-object and centroid-distance queries.

Physical coordinates use `origin + direction @ (index * spacing)`. The project-format NPZ must contain `labels`, `spacing_mm`, `origin_mm`, and `direction` fields; label arrays are integer 3D arrays and units are millimetres.

## Run

```powershell
python -m pytest -q
python cli.py --output-dir reports/demo --save-demo
streamlit run app.py
```

To measure a saved project-format volume:

```powershell
python cli.py --input reports/demo/synthetic_demo_volume.npz --output-dir reports/reloaded
```

The CLI writes `measurements.json` (geometry metadata plus measurements) and `measurements.csv`.

## Limits

This is a measurement prototype, not a segmentation model, medical-image reader, clinical viewer, or validated anatomical-analysis tool. It deliberately supports only the small NPZ interchange contract so every geometric assumption stays visible and testable.
