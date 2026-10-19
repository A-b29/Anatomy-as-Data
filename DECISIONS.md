# Decisions — Anatomy-as-Data

## Explicit `z/y/x` coordinate convention

All arrays, spacing, origins, direction matrices, and reported coordinates use `z/y/x` ordering. Medical-imaging libraries vary in their conventions, so naming the ordering everywhere prevents a silent axis swap. Physical coordinates are computed as `origin + direction @ (index * spacing)` and reported in millimetres.

## Synthetic cuboids before clinical files

The MVP starts with two known synthetic cuboids rather than a bundled scan. This makes numerical assertions exact, avoids privacy/licensing issues, and proves the geometry engine before any format-specific image I/O is introduced.

## Small NPZ interchange contract

Only an NPZ with labels and all geometry fields is accepted. Accepting loosely specified arrays would tempt callers to assume default units, origins, or orientations; refusing incomplete metadata is safer and more reproducible.

## Core library separated from Streamlit

Measurement, query, and export functions do not import UI libraries. Tests and batch use therefore exercise the same deterministic functions as the visual explorer.

## Bounding boxes are half-open

`min` is inclusive and `max` is exclusive, mirroring NumPy slicing. This makes a box directly reusable as `array[z0:z1, y0:y1, x0:x1]` without off-by-one conversions.
