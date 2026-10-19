# Model Flow, Interview Questions, and Resume Evidence

## Data flow

```text
Labelled 3D NPZ + spacing/origin/direction
  -> SpatialVolume validation
  -> per-label voxel extraction
  -> volume, centroids, half-open boxes
  -> spatial queries
  -> JSON/CSV export and optional Streamlit slice viewer
```

## Questions to prepare for

1. Why store both voxel-index and physical centroids?  Index coordinates make array operations auditable; physical coordinates make measurements meaningful across differing voxel spacings.
2. How do you avoid incorrect volumes?  Validate positive spacing and multiply voxel count by the product of all three spacings only after units have been explicitly declared.
3. Why not claim mesh surface area?  Surface area depends on extraction, interpolation, and smoothing choices; this MVP scopes itself to exact voxel-derived quantities.
4. What would production support require?  Format-specific readers, DICOM/NIfTI geometry validation, provenance, de-identification, access controls, and clinical validation.

## Resume evidence

Use measured figures after a final run, for example: “Built a tested 3D segmentation measurement pipeline that exports label volumes, centroids, bounding boxes, and distance queries with explicit spatial metadata.” Do not describe the synthetic-demo results as clinical findings.
