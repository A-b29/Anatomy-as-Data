import pytest

from src.measurements import available_labels, measure_all_labels, measure_label
from src.queries import centroid_distance_mm, largest_structure
from src.volume_io import make_demo_volume


def test_demo_measurements_have_known_voxel_and_physical_volumes():
    volume = make_demo_volume()
    measurements = measure_all_labels(volume)
    assert available_labels(volume) == [1, 2]
    assert [item.voxel_count for item in measurements] == [60, 36]
    assert [item.physical_volume_mm3 for item in measurements] == [180.0, 108.0]
    assert largest_structure(measurements).label == 1
    assert centroid_distance_mm(*measurements) > 0


def test_missing_and_background_labels_are_explicit_errors():
    volume = make_demo_volume()
    with pytest.raises(ValueError):
        measure_label(volume, 0)
    with pytest.raises(KeyError):
        measure_label(volume, 99)
