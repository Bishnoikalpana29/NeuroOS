from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# Resolve the repository root from this file's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "results" / "monitoring" / "system_metrics.csv"

st.set_page_config(
    page_title="NeuroOS Resource Dashboard",
    page_icon="ðŸ§ ",
    layout="wide",
)

st.title("NeuroOS Resource Utilization Dashboard")
st.caption("Live system measurements collected by the NeuroOS C++ monitor.")

with st.sidebar:
    st.header("Dashboard Controls")
    st.caption("Click Refresh data to reload saved measurements. Run the C++ monitor separately to collect new samples.")
    refresh_now = st.button("Refresh data", type="primary")

if refresh_now:
    st.rerun()

if not CSV_PATH.exists():
    st.warning("No monitoring data found yet.")
    st.code(
        r".\core\monitoring\system_monitor.exe 5 1000",
        language="powershell",
    )
    st.info(f"Expected CSV file: {CSV_PATH}")
    st.stop()

try:
    data = pd.read_csv(CSV_PATH)
except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
    st.error(f"Could not read the monitoring CSV: {error}")
    st.stop()

required_columns = [
    "timestamp",
    "data_source",
    "cpu_utilization_percent",
    "memory_utilization_percent",
    "total_memory_mb",
    "used_memory_mb",
    "available_memory_mb",
    "total_processes",
]

missing_columns = [column for column in required_columns if column not in data.columns]

if missing_columns:
    st.error("The monitoring CSV is missing required columns: " + ", ".join(missing_columns))
    st.stop()

if data.empty:
    st.info("The monitoring CSV exists but contains no samples yet.")
    st.stop()

numeric_columns = [
    "cpu_utilization_percent",
    "memory_utilization_percent",
    "total_memory_mb",
    "used_memory_mb",
    "available_memory_mb",
    "total_processes",
]

for column in numeric_columns:
    data[column] = pd.to_numeric(data[column], errors="coerce")

data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
data = data.dropna(
    subset=[
        "timestamp",
        "cpu_utilization_percent",
        "memory_utilization_percent",
    ]
).sort_values("timestamp")

if data.empty:
    st.error("No valid monitoring samples are available in the CSV.")
    st.stop()

latest = data.iloc[-1]

st.subheader("Latest System Snapshot")

cpu_col, ram_col, process_col, sample_col = st.columns(4)

cpu_col.metric(
    "CPU Utilization",
    f"{latest['cpu_utilization_percent']:.2f}%",
)

ram_col.metric(
    "RAM Utilization",
    f"{latest['memory_utilization_percent']:.2f}%",
)

process_col.metric(
    "Total Processes",
    f"{int(latest['total_processes']):,}",
)

sample_col.metric(
    "Recorded Samples",
    f"{len(data):,}",
)

st.caption(
    f"Latest sample: {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} "
    f"| Source: {latest['data_source']}"
)

st.divider()

st.subheader("CPU Utilization Over Time")

cpu_chart = px.line(
    data,
    x="timestamp",
    y="cpu_utilization_percent",
    markers=True,
    labels={
        "timestamp": "Time",
        "cpu_utilization_percent": "CPU Utilization (%)",
    },
)
cpu_chart.update_yaxes(range=[0, 100])
st.plotly_chart(cpu_chart, width="stretch")

st.subheader("Memory Utilization Over Time")

ram_chart = px.line(
    data,
    x="timestamp",
    y="memory_utilization_percent",
    markers=True,
    labels={
        "timestamp": "Time",
        "memory_utilization_percent": "RAM Utilization (%)",
    },
)
ram_chart.update_yaxes(range=[0, 100])
st.plotly_chart(ram_chart, width="stretch")

st.subheader("Physical Memory")

memory_col1, memory_col2, memory_col3 = st.columns(3)

memory_col1.metric(
    "Total RAM",
    f"{latest['total_memory_mb']:,.0f} MB",
)
memory_col2.metric(
    "Used RAM",
    f"{latest['used_memory_mb']:,.0f} MB",
)
memory_col3.metric(
    "Available RAM",
    f"{latest['available_memory_mb']:,.0f} MB",
)

st.subheader("Recent Measurements")

display_data = data.tail(20).copy()
display_data["timestamp"] = display_data["timestamp"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

st.dataframe(
    display_data[
        [
            "timestamp",
            "cpu_utilization_percent",
            "memory_utilization_percent",
            "total_memory_mb",
            "used_memory_mb",
            "available_memory_mb",
            "total_processes",
        ]
    ].rename(
        columns={
            "timestamp": "Timestamp",
            "cpu_utilization_percent": "CPU (%)",
            "memory_utilization_percent": "RAM (%)",
            "total_memory_mb": "Total RAM (MB)",
            "used_memory_mb": "Used RAM (MB)",
            "available_memory_mb": "Available RAM (MB)",
            "total_processes": "Processes",
        }
    ),
    width="stretch",
    hide_index=True,
)

st.caption(
    "Data source: the actual measurements saved by core/monitoring/system_monitor.cpp. "
    "Charts display recorded samples, not simulated system values."
)

st.caption(f"Data file: {CSV_PATH}")


