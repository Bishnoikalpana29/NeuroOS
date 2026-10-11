from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "results" / "monitoring" / "system_metrics.csv"

st.set_page_config(
    page_title="NeuroOS | Resource Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #10182b;
        border-right: 1px solid #263249;
    }

    [data-testid="stHeader"] {
        background-color: rgba(11, 16, 32, 0.9);
    }

    .hero {
        padding: 26px 30px;
        border: 1px solid #293750;
        border-radius: 18px;
        background:
            linear-gradient(120deg, #172554 0%, #111827 55%, #102a43 100%);
        margin-bottom: 25px;
    }

    .hero-label {
        color: #93c5fd;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        margin: 8px 0;
        color: #f8fafc;
    }

    .hero-description {
        color: #b8c5d9;
        font-size: 14px;
        margin-bottom: 0;
    }

    .section-label {
        color: #93c5fd;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .section-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        background: #111a2d;
        border: 1px solid #293750;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9caec8;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
        font-weight: 800;
    }

    .status-pill {
        display: inline-block;
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 700;
    }

    .status-good {
        color: #86efac;
        background: #123626;
        border: 1px solid #166534;
    }

    .status-warning {
        color: #fde68a;
        background: #422006;
        border: 1px solid #92400e;
    }

    .status-critical {
        color: #fca5a5;
        background: #450a0a;
        border: 1px solid #991b1b;
    }

    .info-card {
        background: #111a2d;
        border: 1px solid #293750;
        padding: 18px;
        border-radius: 14px;
        min-height: 110px;
    }

    .info-title {
        color: #9caec8;
        font-size: 12px;
        margin-bottom: 8px;
    }

    .info-value {
        color: #f8fafc;
        font-size: 23px;
        font-weight: 800;
    }

    .info-subtitle {
        color: #8293ad;
        font-size: 11px;
        margin-top: 6px;
    }

    .footer {
        color: #718096;
        font-size: 11px;
        text-align: center;
        padding: 22px 0 8px 0;
        border-top: 1px solid #263249;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #293750;
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🧠 NeuroOS")
    st.caption("AI-Driven Operating System Resource Manager")

    st.divider()

    st.markdown("### Navigation")
    st.caption("SYSTEM OVERVIEW")
    st.caption("RESOURCE MONITORING")
    st.caption("MEMORY ANALYTICS")
    st.caption("MONITORING HISTORY")

    st.divider()

    st.markdown("### Dashboard Controls")
    st.caption("Reload measurements saved by the C++ monitor.")

    if st.button("↻ Refresh dashboard", use_container_width=True):
        st.rerun()

    st.divider()

    st.markdown("### Data Source")
    st.code("results/monitoring/system_metrics.csv", language="text")

    st.caption(
        "Run the C++ monitoring program separately to collect new measurements."
    )


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not CSV_PATH.exists():
    st.error("Monitoring data has not been created yet.")
    st.code(
        r".\core\monitoring\system_monitor.exe 5 1000",
        language="powershell",
    )
    st.stop()

try:
    data = pd.read_csv(CSV_PATH)
except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
    st.error(f"Could not read monitoring data: {error}")
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

missing_columns = [
    column for column in required_columns if column not in data.columns
]

if missing_columns:
    st.error(
        "The monitoring CSV is missing these columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

if data.empty:
    st.warning("The monitoring CSV does not contain any samples.")
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

data["timestamp"] = pd.to_datetime(
    data["timestamp"],
    errors="coerce",
)

data = data.dropna(
    subset=[
        "timestamp",
        "cpu_utilization_percent",
        "memory_utilization_percent",
    ]
).sort_values("timestamp")

if data.empty:
    st.error("No valid monitoring measurements were found.")
    st.stop()

latest = data.iloc[-1]


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def health_status(value):
    """Classify utilization using transparent fixed thresholds."""
    if value < 70:
        return "Normal", "status-good"
    if value < 90:
        return "Elevated", "status-warning"
    return "High", "status-critical"


def format_mb(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f} MB"


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111a2d",
        plot_bgcolor="#111a2d",
        font=dict(
            family="Inter, sans-serif",
            color="#cbd5e1",
            size=12,
        ),
        margin=dict(l=15, r=15, t=35, b=15),
        height=320,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        title=None,
    )

    fig.update_yaxes(
        gridcolor="#263249",
        zerolinecolor="#263249",
    )

    return fig


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">Operating System Intelligence Platform</div>
        <div class="hero-title">NeuroOS Resource Intelligence</div>
        <p class="hero-description">
            Monitor system resources, inspect memory utilization, and explore
            operating-system performance using recorded measurements.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SYSTEM OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-label">01 / Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">System Snapshot</div>',
    unsafe_allow_html=True,
)

cpu = float(latest["cpu_utilization_percent"])
ram = float(latest["memory_utilization_percent"])
processes = latest["total_processes"]

cpu_status, cpu_class = health_status(cpu)
ram_status, ram_class = health_status(ram)

cpu_col, ram_col, process_col, sample_col = st.columns(4)

with cpu_col:
    st.metric(
        "CPU UTILIZATION",
        f"{cpu:.2f}%",
        help="CPU utilization reported by the monitoring program.",
    )
    st.markdown(
        f'<span class="status-pill {cpu_class}">{cpu_status}</span>',
        unsafe_allow_html=True,
    )

with ram_col:
    st.metric(
        "MEMORY UTILIZATION",
        f"{ram:.2f}%",
        help="Memory utilization reported by the monitoring program.",
    )
    st.markdown(
        f'<span class="status-pill {ram_class}">{ram_status}</span>',
        unsafe_allow_html=True,
    )

with process_col:
    process_text = (
        f"{int(processes):,}"
        if pd.notna(processes)
        else "N/A"
    )
    st.metric("TOTAL PROCESSES", process_text)

with sample_col:
    st.metric("RECORDED SAMPLES", f"{len(data):,}")

st.caption(
    f"Last recorded measurement: "
    f"{latest['timestamp'].strftime('%d %b %Y, %H:%M:%S')} "
    f"| Source: {latest['data_source']}"
)

st.divider()


# --------------------------------------------------
# RESOURCE MONITORING
# --------------------------------------------------

st.markdown(
    '<div class="section-label">02 / Resource Monitoring</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Resource Performance</div>',
    unsafe_allow_html=True,
)

cpu_avg = data["cpu_utilization_percent"].mean()
cpu_max = data["cpu_utilization_percent"].max()
ram_avg = data["memory_utilization_percent"].mean()

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.metric("Average CPU", f"{cpu_avg:.2f}%")
summary_col2.metric("Peak CPU", f"{cpu_max:.2f}%")
summary_col3.metric("Average RAM", f"{ram_avg:.2f}%")

chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown("#### CPU Utilization")

    cpu_chart = px.line(
        data,
        x="timestamp",
        y="cpu_utilization_percent",
        markers=True,
        labels={
            "timestamp": "Time",
            "cpu_utilization_percent": "CPU (%)",
        },
    )

    cpu_chart.update_traces(
        line=dict(color="#60a5fa", width=3),
        marker=dict(size=7),
    )

    cpu_chart.update_yaxes(
        range=[0, 100],
        ticksuffix="%",
    )

    st.plotly_chart(
        style_chart(cpu_chart),
        use_container_width=True,
    )

with chart_right:
    st.markdown("#### Memory Utilization")

    ram_chart = px.line(
        data,
        x="timestamp",
        y="memory_utilization_percent",
        markers=True,
        labels={
            "timestamp": "Time",
            "memory_utilization_percent": "Memory (%)",
        },
    )

    ram_chart.update_traces(
        line=dict(color="#34d399", width=3),
        marker=dict(size=7),
    )

    ram_chart.update_yaxes(
        range=[0, 100],
        ticksuffix="%",
    )

    st.plotly_chart(
        style_chart(ram_chart),
        use_container_width=True,
    )


# --------------------------------------------------
# PHYSICAL MEMORY
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">03 / Memory Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Physical Memory</div>',
    unsafe_allow_html=True,
)

memory_col1, memory_col2 = st.columns([1, 1.4])

with memory_col1:
    st.metric(
        "Total RAM",
        format_mb(latest["total_memory_mb"]),
    )

    st.metric(
        "Used RAM",
        format_mb(latest["used_memory_mb"]),
    )

    st.metric(
        "Available RAM",
        format_mb(latest["available_memory_mb"]),
    )

with memory_col2:
    used_memory = latest["used_memory_mb"]
    available_memory = latest["available_memory_mb"]

    if (
        pd.notna(used_memory)
        and pd.notna(available_memory)
        and used_memory >= 0
        and available_memory >= 0
        and used_memory + available_memory > 0
    ):
        memory_fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Used Memory", "Available Memory"],
                    values=[used_memory, available_memory],
                    hole=0.68,
                    marker=dict(
                        colors=["#60a5fa", "#25334b"],
                    ),
                    textinfo="label+percent",
                    hovertemplate=(
                        "%{label}<br>"
                        "%{value:,.0f} MB<br>"
                        "%{percent}<extra></extra>"
                    ),
                )
            ]
        )

        memory_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111a2d",
            plot_bgcolor="#111a2d",
            font=dict(
                family="Inter, sans-serif",
                color="#e2e8f0",
            ),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            showlegend=False,
        )

        st.plotly_chart(
            memory_fig,
            use_container_width=True,
        )
    else:
        st.info("Physical-memory breakdown is unavailable.")


# --------------------------------------------------
# MONITORING HISTORY
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">04 / Monitoring History</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Recent Measurements</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Showing the latest 20 valid records from the monitoring CSV."
)

display_data = data.tail(20).copy()

display_data["timestamp"] = display_data["timestamp"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

display_data = display_data.rename(
    columns={
        "timestamp": "Timestamp",
        "cpu_utilization_percent": "CPU (%)",
        "memory_utilization_percent": "RAM (%)",
        "total_memory_mb": "Total RAM (MB)",
        "used_memory_mb": "Used RAM (MB)",
        "available_memory_mb": "Available RAM (MB)",
        "total_processes": "Processes",
    }
)

visible_columns = [
    "Timestamp",
    "CPU (%)",
    "RAM (%)",
    "Total RAM (MB)",
    "Used RAM (MB)",
    "Available RAM (MB)",
    "Processes",
]

st.dataframe(
    display_data[visible_columns],
    use_container_width=True,
    hide_index=True,
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        NeuroOS | AI-Driven Adaptive Operating System Resource Manager
        <br>
        Recorded system measurements · Streamlit Dashboard
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(f"Monitoring data: {CSV_PATH}")

# --------------------------------------------------
# AI WORKLOAD PREDICTION
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">05 / Artificial Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">AI Workload Intelligence</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Predict the CPU burst time of a process using the trained NeuroOS model."
)

from ai.src.predict_workload import predict_workload

with st.form("workload_prediction_form"):
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        arrival_time = st.number_input(
            "Arrival Time",
            min_value=0,
            value=4,
            step=1,
        )

        priority = st.number_input(
            "Priority",
            min_value=1,
            value=1,
            step=1,
        )

    with input_col2:
        memory = st.number_input(
            "Memory Requirement (MB)",
            min_value=1,
            value=140,
            step=10,
        )

        io_value = st.number_input(
            "I/O Requirement",
            min_value=0,
            value=30,
            step=1,
        )

    predict_button = st.form_submit_button(
        "Predict CPU Burst",
        type="primary",
        use_container_width=True,
    )

if predict_button:
    try:
        predicted_burst = predict_workload(
            arrival_time=arrival_time,
            priority=priority,
            memory=memory,
            io=io_value,
        )

        st.success("Prediction completed successfully.")

        result_col1, result_col2 = st.columns(2)

        result_col1.metric(
            "Predicted CPU Burst Time",
            f"{predicted_burst:.2f}",
        )

        result_col2.metric(
            "Process Priority",
            int(priority),
        )

        st.info(
            "This result is a model prediction, not a measured CPU execution time. "
            "Prediction quality depends on the training data."
        )

    except Exception as error:
        st.error(f"Prediction failed: {error}")

        # --------------------------------------------------
# AI DEADLOCK RISK PREDICTION
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">06 / SYSTEM SAFETY</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">AI Deadlock Risk Analysis</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Estimate the probability of an unsafe resource-allocation state "
    "using the trained NeuroOS deadlock-risk model."
)

from ai.prediction.predict_deadlock import (
    EXAMPLES,
    MODEL_PATH,
    describe,
    predict_risk,
)
import joblib

if MODEL_PATH.exists():

    example_names = [example[0] for example in EXAMPLES]

    selected_example = st.selectbox(
        "Select a resource-allocation scenario",
        options=range(len(EXAMPLES)),
        format_func=lambda index: example_names[index],
        key="deadlock_example",
    )

    selected = EXAMPLES[selected_example]

    _, allocation, maximum, available = selected

    with st.expander("View resource-allocation details"):
        st.write("**Allocation Matrix**")
        st.dataframe(
            pd.DataFrame(allocation),
            hide_index=True,
        )

        st.write("**Maximum Resource Matrix**")
        st.dataframe(
            pd.DataFrame(maximum),
            hide_index=True,
        )

        st.write("**Available Resources**")
        st.write(available)

    if st.button(
        "Analyze Deadlock Risk",
        type="primary",
        key="analyze_deadlock",
    ):
        try:
            model = joblib.load(MODEL_PATH)

            risk = predict_risk(
                model,
                allocation,
                maximum,
                available,
            )

            risk_percent = risk * 100

            result_col1, result_col2 = st.columns(2)

            result_col1.metric(
                "Estimated Unsafe Probability",
                f"{risk_percent:.2f}%",
            )

            result_col2.metric(
                "AI Risk Classification",
                describe(risk),
            )

            st.progress(
                min(max(risk, 0.0), 1.0),
                text=f"Estimated risk: {risk_percent:.2f}%",
            )

            st.warning(
                "This is an AI-based risk estimate, not a definitive "
                "deadlock determination. Always verify resource-allocation "
                "safety using the Banker's Algorithm."
            )

        except Exception as error:
            st.error(f"Deadlock risk prediction failed: {error}")

else:
    st.error(
        f"Deadlock risk model not found: {MODEL_PATH}"
    )
    # ==========================================================
# CUSTOM BANKER'S ALGORITHM + AI DEADLOCK RISK ANALYSIS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">07 / RESOURCE SAFETY</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Custom Resource Allocation Analysis</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Enter your own resource-allocation state. "
    "NeuroOS will run the actual C++ Banker's Algorithm "
    "and estimate risk using the trained AI model."
)

st.info(
    "Each matrix row represents one process. "
    "Each matrix column represents one resource type. "
    "Use non-negative integers separated by spaces."
)

# ----------------------------------------------------------
# INPUT SECTION
# ----------------------------------------------------------

custom_process_count = st.number_input(
    "Number of processes",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
    key="custom_banker_process_count",
)

custom_resource_count = st.number_input(
    "Number of resource types",
    min_value=1,
    max_value=5,
    value=3,
    step=1,
    key="custom_banker_resource_count",
)

st.markdown("### Allocation Matrix")

st.caption(
    "Resources currently allocated to each process. "
    "Enter one row per process."
)

custom_allocation_text = st.text_area(
    "Allocation",
    value=(
        "0 1 0\n"
        "2 0 0\n"
        "3 0 2\n"
        "2 1 1\n"
        "0 0 2"
    ),
    height=150,
    key="custom_banker_allocation",
)

st.markdown("### Maximum Resource Matrix")

st.caption(
    "Maximum resources each process may require. "
    "Enter one row per process."
)

custom_maximum_text = st.text_area(
    "Maximum",
    value=(
        "7 5 3\n"
        "3 2 2\n"
        "9 0 2\n"
        "2 2 2\n"
        "4 3 3"
    ),
    height=150,
    key="custom_banker_maximum",
)

st.markdown("### Available Resources")

st.caption(
    "Currently available instances of each resource type. "
    "Enter one space-separated row."
)

custom_available_text = st.text_input(
    "Available",
    value="3 3 2",
    key="custom_banker_available",
)

# ----------------------------------------------------------
# ANALYSIS BUTTON
# ----------------------------------------------------------

if st.button(
    "Analyze Custom Resource State",
    type="primary",
    key="run_custom_banker_analysis",
):

    try:
        # Parse Allocation matrix.
        custom_allocation = [
            [int(value) for value in row.split()]
            for row in custom_allocation_text.strip().splitlines()
            if row.strip()
        ]

        # Parse Maximum matrix.
        custom_maximum = [
            [int(value) for value in row.split()]
            for row in custom_maximum_text.strip().splitlines()
            if row.strip()
        ]

        # Parse Available vector.
        custom_available = [
            int(value)
            for value in custom_available_text.split()
        ]

        # Validate process count.
        if len(custom_allocation) != custom_process_count:
            raise ValueError(
                f"Allocation must contain exactly "
                f"{custom_process_count} rows."
            )

        if len(custom_maximum) != custom_process_count:
            raise ValueError(
                f"Maximum must contain exactly "
                f"{custom_process_count} rows."
            )

        # Validate resource count.
        if len(custom_available) != custom_resource_count:
            raise ValueError(
                f"Available must contain exactly "
                f"{custom_resource_count} values."
            )

        for row_number, row in enumerate(custom_allocation):
            if len(row) != custom_resource_count:
                raise ValueError(
                    f"Allocation row {row_number + 1} must contain "
                    f"{custom_resource_count} values."
                )

        for row_number, row in enumerate(custom_maximum):
            if len(row) != custom_resource_count:
                raise ValueError(
                    f"Maximum row {row_number + 1} must contain "
                    f"{custom_resource_count} values."
                )

        # --------------------------------------------------
        # RUN THE ACTUAL C++ BANKER'S ALGORITHM
        # --------------------------------------------------

        from dashboard.banker_bridge import check_safety

        banker_result = check_safety(
            custom_allocation,
            custom_maximum,
            custom_available,
        )

        st.markdown("## Banker's Algorithm Result")

        # Display calculated Need matrix.
        st.markdown("### Calculated Need Matrix")

        st.dataframe(
            pd.DataFrame(
                banker_result["need"],
                columns=[
                    f"R{i}"
                    for i in range(custom_resource_count)
                ],
                index=[
                    f"P{i}"
                    for i in range(custom_process_count)
                ],
            ),
            use_container_width=True,
        )

        # Display actual algorithm result.
        if banker_result["safe"]:

            st.success(
                "SAFE STATE — The C++ Banker's Algorithm "
                "found a safe execution sequence."
            )

            st.metric(
                "System Safety",
                "SAFE",
            )

            st.markdown("### Safe Execution Sequence")

            st.code(
                banker_result["safe_sequence"],
                language="text",
            )

        else:

            st.error(
                "UNSAFE STATE — The C++ Banker's Algorithm "
                "could not find a safe execution sequence."
            )

            st.metric(
                "System Safety",
                "UNSAFE",
            )

            st.warning(
                "The current resource-allocation state is unsafe. "
                "An unsafe state does not necessarily mean that "
                "a deadlock has already occurred."
            )

        # --------------------------------------------------
        # AI DEADLOCK RISK ESTIMATION
        # --------------------------------------------------

        st.markdown("## AI Deadlock Risk Estimate")

        from ai.prediction.predict_deadlock import (
            MODEL_PATH,
            describe,
            predict_risk,
        )

        import joblib

        if MODEL_PATH.exists():

            deadlock_model = joblib.load(MODEL_PATH)

            custom_risk = predict_risk(
                deadlock_model,
                custom_allocation,
                custom_maximum,
                custom_available,
            )

            custom_risk_percent = custom_risk * 100

            risk_col1, risk_col2 = st.columns(2)

            risk_col1.metric(
                "Estimated Risk Score",
                f"{custom_risk_percent:.2f}%",
            )

            risk_col2.metric(
                "AI Risk Classification",
                describe(custom_risk),
            )

            st.progress(
                min(max(custom_risk, 0.0), 1.0),
                text=(
                    f"AI estimated risk: "
                    f"{custom_risk_percent:.2f}%"
                ),
            )

            st.caption(
                "Important: This score is a model estimate based on "
                "synthetic training data. It is not a calibrated "
                "real-world probability of deadlock and does not "
                "replace the Banker's Algorithm."
            )

        else:

            st.warning(
                "The AI deadlock model was not found. "
                "The Banker's Algorithm result above is still valid."
            )

    except ValueError as error:

        st.error(f"Invalid input: {error}")

    except FileNotFoundError as error:

        st.error(
            f"Required executable or model not found: {error}"
        )

    except Exception as error:

        st.error(
            f"Analysis failed: {error}"
        )