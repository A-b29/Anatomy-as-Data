import numpy as np
import pytest

from src.geometry import indices_to_physical, voxel_volume_mm3
from src.volume_io import SpatialVolume


def test_index_to_physical_applies_spacing_origin_and_direction():
    volume = SpatialVolume(
        labels=np.zeros((2, 2, 2), dtype=np.int16),
        spacing_mm=(2.0, 3.0, 4.0),
        origin_mm=(10.0, 20.0, 30.0),
        direction=np.diag([-1.0, 1.0, 1.0]),
    )
    converted = indices_to_physical(np.array([[1.0, 2.0, 3.0]]), volume)
    assert converted.tolist() == [[8.0, 26.0, 42.0]]
    assert voxel_volume_mm3(volume) == 24.0


def test_volume_rejects_non_integer_or_invalid_geometry():
    with pytest.raises(TypeError):
        SpatialVolume(labels=np.zeros((2, 2, 2), dtype=float))
    with pytest.raises(ValueError):
        SpatialVolume(labels=np.zeros((2, 2, 2), dtype=np.int16), spacing_mm=(1.0, 0.0, 1.0))
