"""Streamlit explorer for the synthetic, non-clinical Anatomy-as-Data demo."""

from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from src.measurements import measure_all_labels
from src.queries import centroid_distance_mm, find_label, largest_structure
from src.reporting import build_report
from src.volume_io import load_volume_npz, make_demo_volume


st.set_page_config(page_title="Anatomy-as-Data", page_icon="🧊", layout="wide")
st.title("🧊 Anatomy-as-Data")
st.caption("Synthetic segmentation measurement demo — not a clinical viewer or diagnostic system.")

uploaded = st.sidebar.file_uploader("Optional project-format .npz volume", type=["npz"])
if uploaded is None:
    volume = make_demo_volume()
    source = "deterministic synthetic demo"
else:
    cache_path = Path(".streamlit_upload.npz")
    cache_path.write_bytes(uploaded.getvalue())
    try:
        volume = load_volume_npz(cache_path)
        source = uploaded.name
    except (ValueError, TypeError) as error:
        st.error(f"Could not read project-format NPZ: {error}")
        st.stop()
    finally:
        cache_path.unlink(missing_ok=True)

measurements = measure_all_labels(volume)
report = build_report(volume, measurements)
st.sidebar.success(f"{source}: {len(measurements)} non-background labels")
st.sidebar.json({"shape_zyx": report["volume_shape_zyx"], "spacing_mm_zyx": report["spacing_mm_zyx"]})

left, right = st.columns([1.25, 1])
with left:
    slice_index = st.slider("z slice", 0, volume.labels.shape[0] - 1, volume.labels.shape[0] // 2)
    figure = go.Figure(go.Heatmap(z=volume.labels[slice_index], colorscale="Viridis", colorbar_title="Label"))
    figure.update_layout(title=f"Label slice z={slice_index}", yaxis_scaleanchor="x", height=430)
    st.plotly_chart(figure, use_container_width=True)
with right:
    st.subheader("Object measurements")
    st.dataframe([item.to_dict() for item in measurements], use_container_width=True)
    biggest = largest_structure(measurements)
    st.metric("Largest structure", f"Label {biggest.label}", f"{biggest.physical_volume_mm3:.1f} mm³")

if len(measurements) >= 2:
    labels = [item.label for item in measurements]
    first = st.selectbox("First label", labels, index=0)
    second = st.selectbox("Second label", labels, index=1)
    a, b = find_label(measurements, first), find_label(measurements, second)
    st.metric("Centroid distance", f"{centroid_distance_mm(a, b):.2f} mm")

st.download_button(
    "Download measurement JSON",
    data=__import__("json").dumps(report, indent=2),
    file_name="measurements.json",
    mime="application/json",
)
