import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# RAPIDO RIDE INTELLIGENCE
# Professional yellow / black analytics dashboard
# ============================================================

st.set_page_config(
    page_title="Rapido Ride Intelligence",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Theme
# -----------------------------
st.markdown("""
<style>
:root {
    --yellow: #FFD21F;
    --black: #111111;
    --dark: #1B1B1B;
    --text: #222222;
    --muted: #6F6F6F;
    --line: #E6E6E6;
    --card: #FFFFFF;
    --page: #F5F6F7;
}

[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

.stApp {
    background: var(--page);
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding: 0.8rem 1.5rem 2rem 1.5rem;
}

/* Header */
.main-header {
    background: var(--black);
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
}

.brand {
    color: white;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: -0.5px;
}

.brand span {
    color: var(--yellow);
}

.brand-sub {
    color: #BDBDBD;
    font-size: 9px;
    margin-top: 2px;
}

/* Navigation */
div[data-testid="stRadio"] > div {
    gap: 5px;
    justify-content: center;
    flex-wrap: wrap;
}

div[data-testid="stRadio"] label {
    background: transparent !important;
    border-radius: 7px !important;
    padding: 5px 10px !important;
    color: #D0D0D0 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    border: 1px solid transparent !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--yellow) !important;
    color: #111111 !important;
    border-color: var(--yellow) !important;
}

div[data-testid="stRadio"] label p {
    color: inherit !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

div[data-testid="stRadio"] input {
    display: none !important;
}

/* Profile */
.profile {
    text-align: right;
    color: white;
    font-size: 10px;
    font-weight: 700;
}

.profile-circle {
    display: inline-flex;
    width: 28px;
    height: 28px;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--yellow);
    color: #111111;
    font-weight: 900;
    margin-right: 5px;
}

/* Page title */
.page-title {
    font-size: 25px;
    font-weight: 900;
    color: #181818;
    margin: 7px 0 2px 0;
}

.page-subtitle {
    color: var(--muted);
    font-size: 11px;
    margin-bottom: 13px;
}

/* Filter card */
.filter-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 11px;
    padding: 10px 13px 2px 13px;
    margin-bottom: 12px;
    box-shadow: 0 2px 9px rgba(0,0,0,0.035);
}

.filter-title {
    font-size: 9px;
    font-weight: 900;
    color: #777;
    letter-spacing: 0.8px;
    margin-bottom: 3px;
}

/* KPI cards */
.kpi {
    background: white;
    border: 1px solid #E3E3E3;
    border-radius: 11px;
    padding: 12px 13px;
    min-height: 91px;
    box-shadow: 0 2px 9px rgba(0,0,0,0.035);
}

.kpi-label {
    color: #777;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: .6px;
}

.kpi-value {
    color: #111;
    font-size: 21px;
    font-weight: 900;
    margin-top: 7px;
}

.kpi-value.yellow {
    color: #D49D00;
}

.kpi-note {
    color: #8A8A8A;
    font-size: 8px;
    margin-top: 2px;
}

/* Section */
.section-title {
    color: #171717;
    font-size: 14px;
    font-weight: 900;
    margin: 15px 0 6px 2px;
}

.section-title span {
    color: #D49D00;
}

.card-title {
    color: #222;
    font-size: 11px;
    font-weight: 850;
    margin-bottom: 2px;
}

/* Insight */
.insight {
    background: #FFF9D8;
    border-left: 4px solid var(--yellow);
    border-radius: 9px;
    padding: 11px 13px;
    color: #444;
    font-size: 10px;
    line-height: 1.55;
}

/* Streamlit controls */
div[data-baseweb="select"] > div {
    background: white !important;
    border-color: #DADADA !important;
    border-radius: 7px !important;
}

[data-testid="stDateInput"] input {
    background: white !important;
    border-color: #DADADA !important;
    color: #222 !important;
}

label {
    color: #777 !important;
    font-size: 9px !important;
    font-weight: 800 !important;
}

div[data-testid="stMetric"] {
    background: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #999;
    font-size: 8px;
    padding: 18px 0 3px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "rides_data.csv"

if not DATA_FILE.exists():
    st.error("rides_data.csv was not found. Put rides_data.csv in the same folder as this Python file.")
    st.stop()

df = pd.read_csv(DATA_FILE)

required = [
    "services", "date", "time", "ride_status", "source", "destination",
    "duration", "ride_id", "distance", "ride_charge", "misc_charge",
    "total_fare", "payment_method"
]

missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing columns in rides_data.csv: {missing}")
    st.stop()

# -----------------------------
# Data preparation
# -----------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["time"] = pd.to_datetime(df["time"], errors="coerce").dt.time

df["datetime"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d") + " " + df["time"].astype(str),
    errors="coerce"
)

for col in ["duration", "distance", "ride_charge", "misc_charge", "total_fare"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["hour"] = df["datetime"].dt.hour
df["day_name"] = df["date"].dt.day_name()

df["is_completed"] = (
    df["ride_status"].astype(str).str.lower().eq("completed")
)

df["is_cancelled"] = (
    df["ride_status"].astype(str).str.lower().str.contains("cancel", na=False)
)

# -----------------------------
# Header + clickable navigation
# -----------------------------
header_left, header_nav, header_right = st.columns([1.25, 2.7, 0.8])

with header_left:
    st.markdown("""
    <div class="brand">
        <span>Rapido</span> Ride Intelligence
    </div>
    <div class="brand-sub">Mobility analytics • operational performance • business insights</div>
    """, unsafe_allow_html=True)

with header_nav:
    nav = st.radio(
        "Navigation",
        ["Overview", "Demand", "Revenue", "Operations", "Locations"],
        horizontal=True,
        label_visibility="collapsed"
    )

with header_right:
    st.markdown("""
    <div class="profile">
        <span class="profile-circle">JJ</span>
        Analyst
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Page title
# -----------------------------
titles = {
    "Overview": ("Ride Performance Dashboard",
                 "A professional view of demand, trip outcomes, revenue and operational performance."),
    "Demand": ("Demand Intelligence",
               "Understand when, where and how ride demand changes."),
    "Revenue": ("Revenue Intelligence",
                "Track recorded fare value and payment behaviour from completed rides."),
    "Operations": ("Operations Intelligence",
                   "Monitor completion, cancellations, duration and service performance."),
    "Locations": ("Location Intelligence",
                  "Explore pickup and destination patterns across the ride network.")
}

title, subtitle = titles[nav]

st.markdown(
    f'<div class="page-title">{title}</div>'
    f'<div class="page-subtitle">{subtitle}</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Filters
# -----------------------------
services = ["All services"] + sorted(
    df["services"].dropna().astype(str).unique().tolist()
)
statuses = ["All statuses"] + sorted(
    df["ride_status"].dropna().astype(str).unique().tolist()
)
payments = ["All payments"] + sorted(
    df["payment_method"].dropna().astype(str).unique().tolist()
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

st.markdown('<div class="filter-card">', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns([1, 1, 1, 1.35])

with f1:
    service_filter = st.selectbox("SERVICE", services)

with f2:
    status_filter = st.selectbox("RIDE STATUS", statuses)

with f3:
    payment_filter = st.selectbox("PAYMENT", payments)

with f4:
    date_filter = st.date_input(
        "ANALYSIS PERIOD",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

st.markdown('</div>', unsafe_allow_html=True)

# NOTE:
# The filter-card HTML above is intentionally decorative only.
# Streamlit widgets are not placed inside the HTML element.

filtered = df.copy()

if service_filter != "All services":
    filtered = filtered[
        filtered["services"].astype(str) == service_filter
    ]

if status_filter != "All statuses":
    filtered = filtered[
        filtered["ride_status"].astype(str) == status_filter
    ]

if payment_filter != "All payments":
    filtered = filtered[
        filtered["payment_method"].astype(str) == payment_filter
    ]

if isinstance(date_filter, tuple) and len(date_filter) == 2:
    filtered = filtered[
        filtered["date"].dt.date.between(
            date_filter[0], date_filter[1]
        )
    ]

completed = filtered[filtered["is_completed"]].copy()

# -----------------------------
# KPI calculations
# -----------------------------
total_rides = len(filtered)
completed_rides = len(completed)
cancelled_rides = int(filtered["is_cancelled"].sum())

completion_rate = (
    completed_rides / total_rides * 100
    if total_rides else 0
)

cancellation_rate = (
    cancelled_rides / total_rides * 100
    if total_rides else 0
)

revenue = completed["total_fare"].sum()

avg_fare = (
    completed["total_fare"].mean()
    if completed_rides else 0
)

avg_distance = (
    completed["distance"].mean()
    if completed_rides else 0
)

avg_duration = (
    completed["duration"].mean()
    if completed_rides else 0
)

# -----------------------------
# KPI row
# -----------------------------
kpi_data = [
    ("TOTAL RIDES", f"{total_rides:,}", "Ride volume", False),
    ("TOTAL REVENUE", f"₹{revenue:,.0f}", "Completed rides only", True),
    ("COMPLETION RATE", f"{completion_rate:.1f}%", "Successful trips", True),
    ("CANCELLATIONS", f"{cancellation_rate:.1f}%", "Operational leakage", False),
    ("AVG FARE", f"₹{avg_fare:,.0f}", "Per completed ride", True),
]

cols = st.columns(5)

for col, (label, value, note, yellow) in zip(cols, kpi_data):
    with col:
        value_class = "kpi-value yellow" if yellow else "kpi-value"
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="{value_class}">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# Plot helper
# -----------------------------
def polish(fig, height=270):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=38, b=8),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#333333", size=10),
        hoverlabel=dict(
            bgcolor="#111111",
            font_color="white"
        ),
        legend=dict(
            font=dict(size=9),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#DDDDDD",
        tickfont=dict(size=9, color="#777777")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEEEEE",
        zeroline=False,
        tickfont=dict(size=9, color="#777777")
    )

    return fig


YELLOW = "#FFD21F"
DARK_YELLOW = "#E6B400"

# ============================================================
# OVERVIEW
# ============================================================
if nav == "Overview":

    st.markdown(
        '<div class="section-title"><span>01</span> Demand & Ride Outcomes</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.55, 1])

    with left:
        hourly = (
            filtered.groupby("hour")
            .size()
            .reset_index(name="Rides")
        )

        fig = px.line(
            hourly,
            x="hour",
            y="Rides",
            markers=True
        )

        fig.update_traces(
            line=dict(color=YELLOW, width=3),
            marker=dict(color=YELLOW, size=6),
            hovertemplate="%{x}:00<br>Rides: %{y:,}<extra></extra>"
        )

        fig = polish(fig, 285)
        fig.update_layout(
            title=dict(
                text="Ride Demand by Hour",
                font=dict(size=12, color="#222"),
                x=0.02
            ),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with right:
        status_counts = (
            filtered["ride_status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = ["Status", "Rides"]

        fig = px.pie(
            status_counts,
            names="Status",
            values="Rides",
            hole=0.63,
            color_discrete_sequence=[
                YELLOW, "#222222", "#777777", "#CFCFCF"
            ]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="%{label}<br>%{value:,} rides<extra></extra>"
        )

        fig = polish(fig, 285)
        fig.update_layout(
            title=dict(
                text="Ride Outcome Mix",
                font=dict(size=12, color="#222"),
                x=0.02
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    st.markdown(
        '<div class="section-title"><span>02</span> Service & Payment Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        service = (
            filtered["services"]
            .value_counts()
            .reset_index()
        )
        service.columns = ["Service", "Rides"]

        fig = px.bar(
            service,
            x="Rides",
            y="Service",
            orientation="h"
        )

        fig.update_traces(
            marker_color=YELLOW,
            hovertemplate="%{y}<br>Rides: %{x:,}<extra></extra>"
        )

        fig = polish(fig, 245)
        fig.update_layout(
            title=dict(
                text="Ride Volume by Service",
                font=dict(size=11, color="#222"),
                x=0.02
            ),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with c2:
        daily = (
            filtered.groupby("date")
            .size()
            .reset_index(name="Rides")
        )

        fig = px.area(
            daily,
            x="date",
            y="Rides"
        )

        fig.update_traces(
            line=dict(color=YELLOW, width=2),
            fillcolor="rgba(255,210,31,0.22)",
            hovertemplate="%{x|%d %b}<br>Rides: %{y:,}<extra></extra>"
        )

        fig = polish(fig, 245)
        fig.update_layout(
            title=dict(
                text="Daily Ride Trend",
                font=dict(size=11, color="#222"),
                x=0.02
            ),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with c3:
        payment = (
            filtered["payment_method"]
            .value_counts()
            .reset_index()
        )
        payment.columns = ["Payment", "Rides"]

        fig = px.bar(
            payment,
            x="Payment",
            y="Rides"
        )

        fig.update_traces(
            marker_color=YELLOW,
            hovertemplate="%{x}<br>Rides: %{y:,}<extra></extra>"
        )

        fig = polish(fig, 245)
        fig.update_layout(
            title=dict(
                text="Payment Method Usage",
                font=dict(size=11, color="#222"),
                x=0.02
            ),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

# ============================================================
# DEMAND
# ============================================================
elif nav == "Demand":

    st.markdown(
        '<div class="section-title"><span>01</span> Demand Patterns</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        hourly = filtered.groupby("hour").size().reset_index(name="Rides")
        fig = px.line(hourly, x="hour", y="Rides", markers=True)
        fig.update_traces(
            line=dict(color=YELLOW, width=3),
            marker=dict(color=YELLOW, size=6)
        )
        fig = polish(fig, 310)
        fig.update_layout(
            title=dict(text="Hourly Demand", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Hour",
            yaxis_title="Rides"
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]

        day_counts = (
            filtered["day_name"]
            .value_counts()
            .reindex(day_order)
            .fillna(0)
            .reset_index()
        )
        day_counts.columns = ["Day", "Rides"]

        fig = px.bar(day_counts, x="Day", y="Rides")
        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 310)
        fig.update_layout(
            title=dict(text="Demand by Day", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="",
            yaxis_title="Rides"
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div class="section-title"><span>02</span> Top Pickup & Destination Areas</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        pickups = filtered["source"].value_counts().head(10).sort_values()
        fig = px.bar(
            pickups,
            x=pickups.values,
            y=pickups.index,
            orientation="h"
        )
        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Top Pickup Locations", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Rides",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        destinations = filtered["destination"].value_counts().head(10).sort_values()
        fig = px.bar(
            destinations,
            x=destinations.values,
            y=destinations.index,
            orientation="h"
        )
        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Top Destination Locations", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Rides",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# REVENUE
# ============================================================
elif nav == "Revenue":

    st.markdown(
        '<div class="section-title"><span>01</span> Revenue Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1.5, 1])

    with c1:
        daily_rev = (
            completed.groupby("date")["total_fare"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            daily_rev,
            x="date",
            y="total_fare",
            markers=True
        )

        fig.update_traces(
            line=dict(color=YELLOW, width=3),
            marker=dict(color=YELLOW, size=5),
            hovertemplate="%{x|%d %b}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
        )

        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Daily Revenue", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="",
            yaxis_title="Revenue (₹)"
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        service_rev = (
            completed.groupby("services")["total_fare"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            service_rev,
            x="total_fare",
            y="services",
            orientation="h"
        )

        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Revenue by Service", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Revenue (₹)",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div class="section-title"><span>02</span> Fare & Payment Insights</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            completed,
            x="total_fare",
            nbins=30
        )
        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 300)
        fig.update_layout(
            title=dict(text="Fare Distribution", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Total Fare (₹)",
            yaxis_title="Completed Rides"
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        pay_rev = (
            completed.groupby("payment_method")["total_fare"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            pay_rev,
            names="payment_method",
            values="total_fare",
            hole=0.62,
            color_discrete_sequence=[YELLOW, "#222222", "#888888", "#CCCCCC"]
        )

        fig = polish(fig, 300)
        fig.update_layout(
            title=dict(text="Revenue by Payment Method", font=dict(size=12, color="#222"), x=0.02)
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# OPERATIONS
# ============================================================
elif nav == "Operations":

    st.markdown(
        '<div class="section-title"><span>01</span> Operational Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        service_status = pd.crosstab(
            filtered["services"],
            filtered["ride_status"]
        )

        fig = px.bar(
            service_status,
            barmode="group"
        )

        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Ride Status by Service", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Service",
            yaxis_title="Rides"
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        duration_service = (
            filtered.groupby("services")["duration"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig = px.bar(
            duration_service,
            x="duration",
            y="services",
            orientation="h"
        )

        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 320)
        fig.update_layout(
            title=dict(text="Average Trip Duration", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Minutes",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        '<div class="section-title"><span>02</span> Operational Snapshot</div>',
        unsafe_allow_html=True
    )

    peak_hour = (
        int(filtered["hour"].mode().iloc[0])
        if not filtered.empty and filtered["hour"].notna().any()
        else None
    )

    peak_text = f"{peak_hour}:00" if peak_hour is not None else "N/A"

    longest_service = (
        filtered.groupby("services")["duration"].mean().idxmax()
        if filtered["duration"].notna().any()
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="insight">
            <b>Operational snapshot:</b>
            The selected period contains <b>{total_rides:,}</b> rides.
            Completion is <b>{completion_rate:.1f}%</b> and cancellation is
            <b>{cancellation_rate:.1f}%</b>.
            Peak ride activity occurs around <b>{peak_text}</b>.
            The service with the highest average trip duration is
            <b>{longest_service}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# LOCATIONS
# ============================================================
elif nav == "Locations":

    st.markdown(
        '<div class="section-title"><span>01</span> Location Intelligence</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        pickups = (
            filtered["source"]
            .value_counts()
            .head(12)
            .sort_values()
        )

        fig = px.bar(
            pickups,
            x=pickups.values,
            y=pickups.index,
            orientation="h"
        )

        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 360)
        fig.update_layout(
            title=dict(text="Top Pickup Locations", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Rides",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with c2:
        destinations = (
            filtered["destination"]
            .value_counts()
            .head(12)
            .sort_values()
        )

        fig = px.bar(
            destinations,
            x=destinations.values,
            y=destinations.index,
            orientation="h"
        )

        fig.update_traces(marker_color=YELLOW)
        fig = polish(fig, 360)
        fig.update_layout(
            title=dict(text="Top Destination Locations", font=dict(size=12, color="#222"), x=0.02),
            xaxis_title="Rides",
            yaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------
# Ride explorer
# -----------------------------
st.markdown(
    '<div class="section-title"><span>03</span> Ride-Level Explorer</div>',
    unsafe_allow_html=True
)

with st.expander("Open detailed ride table", expanded=False):
    explorer_cols = [
        "date", "time", "services", "ride_status",
        "source", "destination", "distance",
        "duration", "total_fare", "payment_method"
    ]

    st.dataframe(
        filtered[explorer_cols].sort_values(
            "date", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

st.markdown(
    '<div class="footer">Rapido Ride Intelligence • Portfolio Analytics Project • Python + Streamlit + Plotly</div>',
    unsafe_allow_html=True
)
