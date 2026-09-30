import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# RAPIDO RIDE INTELLIGENCE — DASHBOARD V2
# No sidebar • Top navigation • Responsive executive layout
# ============================================================

st.set_page_config(
    page_title="Rapido Ride Intelligence",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Theme / layout
# -----------------------------
st.markdown("""
<style>
[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

[data-testid="stToolbar"] {
    display: none;
}

[data-testid="stDecoration"] {
    display: none;
}
/* Hide Streamlit chrome / sidebar completely */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

.stApp {
    background: #080808;
    color: #FFFFFF;
}

.block-container {
    max-width: 1480px;
    padding: 1.1rem 1.6rem 2rem 1.6rem;
}

/* Header */
.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
    padding: 10px 4px 16px 4px;
    border-bottom: 1px solid #262626;
    margin-bottom: 14px;
}
.brand-wrap { display:flex; align-items:center; gap:11px; }
.brand-mark {
    width:34px; height:34px; border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    background:#FFD21F;
    box-shadow:0 7px 22px rgba(255,210,31,.22);
    font-size:18px;
}
.brand { font-size:16px; font-weight:850; letter-spacing:-.3px; }
.brand-sub { color:#A6A6A6; font-size:10px; margin-top:2px; }
.nav { display:flex; align-items:center; gap:7px; flex:1; justify-content:center; }
.nav-item {
    padding:8px 13px; border-radius:9px; color:#A0A0A0;
    font-size:11px; font-weight:700;
}
.nav-item.active { background:#FFD21F; color:#080808; box-shadow:0 4px 14px rgba(255,210,31,.18); }
.profile {
    display:flex; align-items:center; gap:8px;
    color:#C8C8C8; font-size:11px; font-weight:650;
}
.avatar {
    width:28px; height:28px; border-radius:50%;
    background:#FFD21F;
    display:flex; align-items:center; justify-content:center;
    font-size:11px; color:white; font-weight:800;
}

/* Hero */
.hero {
    display:flex; justify-content:space-between; align-items:flex-end;
    gap:20px; padding:12px 4px 14px 4px;
}
.hero-title { color:#FFFFFF; font-size:27px; font-weight:850; letter-spacing:-.8px; }
.hero-sub { color:#A0A0A0; font-size:11px; margin-top:4px; }
.live {
    display:inline-flex; align-items:center; gap:7px;
    padding:7px 10px; border:1px solid #333333; border-radius:9px;
    background:#111111; color:#AAB5C6; font-size:10px; font-weight:700;
}
.dot { width:6px; height:6px; border-radius:50%; background:#FFD21F; box-shadow:0 0 9px #FFD21F; }

/* Filter row */
.filterbar {
    background:#0D0D0D; border:1px solid #262626;
    border-radius:13px; padding:8px 10px; margin-bottom:13px;
}
.filter-label { color:#8E8E8E; font-size:9px; font-weight:800; letter-spacing:.7px; margin-bottom:3px; }

/* KPI cards */
.kpi-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-bottom:13px; }
.kpi {
    background:linear-gradient(145deg,#111111,#0E0E0E);
    border:1px solid #262626; border-radius:13px;
    padding:13px 14px; min-height:93px;
}
.kpi-top { display:flex; justify-content:space-between; align-items:center; }
.kpi-label { color:#999999; font-size:9px; font-weight:850; letter-spacing:.7px; }
.kpi-icon { color:#BDBDBD; font-size:13px; }
.kpi-value { color:#FFD21F; font-size:22px; font-weight:850; margin-top:8px; letter-spacing:-.5px; }
.kpi-note { color:#777777; font-size:9px; margin-top:3px; }

/* Panels */
.panel {
    background:#111111; border:1px solid #262626;
    border-radius:14px; padding:9px 10px 7px 10px;
}
.section-head {
    display:flex; justify-content:space-between; align-items:center;
    padding:5px 4px 4px 4px;
}
.section-title { color:#FFD21F; font-size:13px; font-weight:800; }
.section-meta { color:#858585; font-size:9px; }

/* Streamlit controls */
div[data-baseweb="select"] > div {
    background:#171717 !important;
    border-color:#333333 !important;
    border-radius:8px !important;
    min-height:32px !important;
}
[data-testid="stDateInput"] input {
    background:#171717 !important;
    border-color:#333333 !important;
    color:#F2F2F2 !important;
}
label { color:#9B9B9B !important; font-size:9px !important; }

/* Remove excess chart padding */
.stPlotlyChart { margin:0 !important; }

/* Insight */
.insight {
    background:linear-gradient(135deg,#191919,#111111);
    border:1px solid #333333; border-radius:13px;
    padding:13px 15px; color:#C8C8C8; font-size:11px; line-height:1.55;
}
.insight b { color:#FFFFFF; }

.footer { text-align:center; color:#666666; font-size:9px; padding:18px 0 4px; }

@media (max-width: 900px) {
    .nav { display:none; }
    .topbar { align-items:flex-start; }
    .kpi-grid { grid-template-columns:repeat(2,1fr); }
}
@media (max-width: 600px) {
    .block-container { padding: .7rem .7rem 1.4rem; }
    .kpi-grid { grid-template-columns:1fr 1fr; gap:7px; }
    .hero-title { font-size:21px; }
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "rides_data.csv"

if not DATA_FILE.exists():
    st.error("rides_data.csv was not found. Put it in the same folder as this Python file.")
    st.stop()

# -----------------------------
# Load + prepare data
# -----------------------------
df = pd.read_csv(DATA_FILE)

required = [
    "services", "date", "time", "ride_status", "source", "destination",
    "duration", "ride_id", "distance", "ride_charge", "misc_charge",
    "total_fare", "payment_method"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["time"] = pd.to_datetime(df["time"], errors="coerce").dt.time
df["datetime"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d") + " " + df["time"].astype(str),
    errors="coerce"
)

for c in ["duration", "distance", "ride_charge", "misc_charge", "total_fare"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["hour"] = df["datetime"].dt.hour
df["day_name"] = df["date"].dt.day_name()
df["month"] = df["date"].dt.strftime("%b")
df["is_completed"] = df["ride_status"].astype(str).str.lower().eq("completed")
df["is_cancelled"] = df["ride_status"].astype(str).str.lower().str.contains("cancel", na=False)

# -----------------------------
# Top navigation
# -----------------------------
st.markdown("""
<div class="topbar">
  <div class="brand-wrap">
    <div class="brand-mark">🛵</div>
    <div>
      <div class="brand">Rapido Ride Intelligence</div>
      <div class="brand-sub">Mobility analytics & operational performance</div>
    </div>
  </div>
  <div class="nav">
    <div class="nav-item active">Overview</div>
    <div class="nav-item">Demand</div>
    <div class="nav-item">Revenue</div>
    <div class="nav-item">Operations</div>
    <div class="nav-item">Locations</div>
  </div>
  <div class="profile"><div class="avatar">JJ</div> Analyst</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
  <div>
    <div class="hero-title">Ride Performance Dashboard</div>
    <div class="hero-sub">Monitor demand, trip outcomes, fare performance and operational pressure.</div>
  </div>
  <div class="live"><span class="dot"></span> Analytics view</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Filters — top bar, not sidebar
# -----------------------------
services = ["All services"] + sorted(df["services"].dropna().astype(str).unique().tolist())
statuses = ["All statuses"] + sorted(df["ride_status"].dropna().astype(str).unique().tolist())
payments = ["All payments"] + sorted(df["payment_method"].dropna().astype(str).unique().tolist())

min_date = df["date"].min().date()
max_date = df["date"].max().date()

with st.container():
    st.markdown('<div class="filterbar">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([1.15, 1.15, 1.15, 1.5])
    with f1:
        service_filter = st.selectbox("SERVICE", services, index=0, label_visibility="visible")
    with f2:
        status_filter = st.selectbox("RIDE STATUS", statuses, index=0, label_visibility="visible")
    with f3:
        payment_filter = st.selectbox("PAYMENT", payments, index=0, label_visibility="visible")
    with f4:
        date_filter = st.date_input(
            "ANALYSIS PERIOD", value=(min_date, max_date),
            min_value=min_date, max_value=max_date, label_visibility="visible"
        )
    st.markdown('</div>', unsafe_allow_html=True)

filtered = df.copy()
if service_filter != "All services":
    filtered = filtered[filtered["services"].astype(str) == service_filter]
if status_filter != "All statuses":
    filtered = filtered[filtered["ride_status"].astype(str) == status_filter]
if payment_filter != "All payments":
    filtered = filtered[filtered["payment_method"].astype(str) == payment_filter]

if isinstance(date_filter, tuple) and len(date_filter) == 2:
    filtered = filtered[filtered["date"].dt.date.between(date_filter[0], date_filter[1])]

completed = filtered[filtered["is_completed"]].copy()

# -----------------------------
# KPIs
# -----------------------------
total_rides = len(filtered)
completed_rides = len(completed)
cancelled_rides = int(filtered["is_cancelled"].sum())
completion_rate = completed_rides / total_rides * 100 if total_rides else 0
cancellation_rate = cancelled_rides / total_rides * 100 if total_rides else 0
revenue = completed["total_fare"].sum()
avg_fare = completed["total_fare"].mean() if completed_rides else 0
avg_distance = completed["distance"].mean() if completed_rides else 0
avg_duration = completed["duration"].mean() if completed_rides else 0

kpis = [
    ("TOTAL RIDES", f"{total_rides:,}", "Ride volume", "↗"),
    ("COMPLETION RATE", f"{completion_rate:.1f}%", "Completed trips", "✓"),
    ("CANCELLATION RATE", f"{cancellation_rate:.1f}%", "Operational leakage", "!"),
    ("TOTAL REVENUE", f"₹{revenue:,.0f}", "Completed rides", "₹"),
    ("AVG FARE", f"₹{avg_fare:,.0f}", "Per completed ride", "◉"),
]

cards = []
for label, value, note, icon in kpis:
    cards.append(
        f'<div class="kpi"><div class="kpi-top"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-icon">{icon}</div></div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>'
    )

st.markdown('<div class="kpi-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)

# -----------------------------
# Plotly theme helper
# -----------------------------
PAPER = "#111111"
GRID = "#2A2A2A"
TEXT = "#D8D8D8"
MUTED = "#999999"
YELLOW = "#FFD21F"
YELLOW_DARK = "#FFB800"


def polish(fig, height=270, title=None):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=35 if title else 8, b=8),
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(color=TEXT, size=10),
        title=dict(text=title or "", font=dict(size=12, color="#FFFFFF"), x=0.02, xanchor="left"),
        hoverlabel=dict(bgcolor="#171717", font_color="#FFFFFF"),
        legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        colorway=[YELLOW, YELLOW_DARK, "#F2E6A2", "#C9A900"]
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID, tickfont=dict(size=9, color=MUTED))
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(size=9, color=MUTED))
    return fig

# -----------------------------
# Main dashboard grid
# -----------------------------
st.markdown('<div class="section-head"><div class="section-title">Demand Overview</div><div class="section-meta">Hourly ride activity</div></div>', unsafe_allow_html=True)

left, right = st.columns([1.65, 1])

with left:
    hourly = filtered.groupby("hour", as_index=False).size().rename(columns={"size": "Rides"})
    if not hourly.empty:
        fig = px.line(hourly, x="hour", y="Rides", markers=True)
        fig.update_traces(
            line=dict(width=2.5, color=YELLOW), marker=dict(size=5, color=YELLOW),
            hovertemplate="%{x}:00<br>Rides: %{y:,}<extra></extra>"
        )
        fig = polish(fig, 285, "Ride Demand by Hour")
        fig.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No ride data for the selected filters.")

with right:
    status_counts = filtered["ride_status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Rides"]
    if not status_counts.empty:
        fig = px.pie(status_counts, names="Status", values="Rides", hole=0.67, color_discrete_sequence=[YELLOW, "#333333", YELLOW_DARK, "#777777"])
        fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>%{value:,} rides<extra></extra>")
        fig = polish(fig, 285, "Ride Outcome Mix")
        fig.update_layout(legend=dict(orientation="h", y=-0.08, x=0.02))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------
# Second row
# -----------------------------
st.markdown('<div class="section-head"><div class="section-title">Performance Trends</div><div class="section-meta">Service • Revenue • Payments</div></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    service = filtered["services"].value_counts().reset_index()
    service.columns = ["Service", "Rides"]
    fig = px.bar(service, x="Rides", y="Service", orientation="h", color_discrete_sequence=[YELLOW])
    fig.update_traces(hovertemplate="%{y}<br>Rides: %{x:,}<extra></extra>")
    fig = polish(fig, 245, "Ride Volume by Service")
    fig.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    daily = filtered.groupby("date", as_index=False).size().rename(columns={"size": "Rides"})
    fig = px.area(daily, x="date", y="Rides", color_discrete_sequence=[YELLOW])
    fig.update_traces(hovertemplate="%{x|%d %b}<br>Rides: %{y:,}<extra></extra>")
    fig = polish(fig, 245, "Daily Ride Trend")
    fig.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c3:
    payment = filtered["payment_method"].value_counts().reset_index()
    payment.columns = ["Payment", "Rides"]
    fig = px.bar(payment, x="Payment", y="Rides", color_discrete_sequence=[YELLOW])
    fig.update_traces(hovertemplate="%{x}<br>Rides: %{y:,}<extra></extra>")
    fig = polish(fig, 245, "Payment Method Usage")
    fig.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------
# Revenue + locations
# -----------------------------
st.markdown('<div class="section-head"><div class="section-title">Revenue & Location Intelligence</div><div class="section-meta">Completed rides only for revenue</div></div>', unsafe_allow_html=True)

r1, r2 = st.columns([1.55, 1])

with r1:
    daily_rev = completed.groupby("date", as_index=False)["total_fare"].sum().rename(columns={"total_fare": "Revenue"})
    if not daily_rev.empty:
        fig = px.line(daily_rev, x="date", y="Revenue", markers=True, color_discrete_sequence=[YELLOW])
        fig.update_traces(hovertemplate="%{x|%d %b}<br>Revenue: ₹%{y:,.0f}<extra></extra>")
        fig = polish(fig, 275, "Daily Revenue Performance")
        fig.update_layout(xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No completed rides available for revenue analysis.")

with r2:
    top_pickups = filtered["source"].value_counts().head(7).sort_values().reset_index()
    top_pickups.columns = ["Pickup", "Rides"]
    fig = px.bar(top_pickups, x="Rides", y="Pickup", orientation="h", color_discrete_sequence=[YELLOW])
    fig.update_traces(hovertemplate="%{y}<br>Rides: %{x:,}<extra></extra>")
    fig = polish(fig, 275, "Top Pickup Locations")
    fig.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------
# Operational insight + explorer
# -----------------------------
st.markdown('<div class="section-head"><div class="section-title">Operational Snapshot</div><div class="section-meta">Decision-support summary</div></div>', unsafe_allow_html=True)

peak_hour = int(filtered["hour"].mode().iloc[0]) if not filtered.empty and filtered["hour"].notna().any() else None
peak_text = f"{peak_hour}:00" if peak_hour is not None else "N/A"
longest_service = (
    filtered.groupby("services")["duration"].mean().idxmax()
    if filtered["duration"].notna().any() and filtered["services"].notna().any()
    else "N/A"
)

st.markdown(
    f'<div class="insight">'
    f'<b>Business snapshot:</b> The selected period contains <b>{total_rides:,}</b> rides, '
    f'with a <b>{completion_rate:.1f}%</b> completion rate and <b>{cancellation_rate:.1f}%</b> cancellation rate. '
    f'Peak ride activity occurs around <b>{peak_text}</b>. '
    f'The service with the highest average trip duration in the current selection is <b>{longest_service}</b>. '
    f'Completed rides generated <b>₹{revenue:,.0f}</b> in recorded fare value.'
    f'</div>', unsafe_allow_html=True
)

with st.expander("Open ride-level explorer", expanded=False):
    explorer_cols = [
        "date", "time", "services", "ride_status", "source", "destination",
        "distance", "duration", "total_fare", "payment_method"
    ]
    st.dataframe(
        filtered[explorer_cols].sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

st.markdown('<div class="footer">Rapido Ride Intelligence • Portfolio analytics project • Built with Streamlit & Plotly</div>', unsafe_allow_html=True)
