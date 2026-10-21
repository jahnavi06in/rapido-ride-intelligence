from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# RAPIDO RIDE INTELLIGENCE — CLEAN 10/10 VERSION
# ============================================================

st.set_page_config(
    page_title="Rapido Ride Intelligence",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "rides_data.csv"

EXPECTED_COLUMNS = [
    "services", "date", "time", "ride_status", "source", "destination",
    "duration", "ride_id", "distance", "ride_charge", "misc_charge",
    "total_fare", "payment_method",
]

NUMERIC_COLUMNS = [
    "duration", "distance", "ride_charge", "misc_charge", "total_fare"
]


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background:#080808;
        color:#F5F5F5;
    }
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display:none !important;
    }
    .block-container {
        max-width:1500px;
        padding-top:2rem;
        padding-bottom:2rem;
    }
    html, body, [class*="css"] {
        font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    }
    .brand-main {
        color:#F5F5F5;
        font-size:1.35rem;
        font-weight:750;
        letter-spacing:-.04em;
    }
    .brand-main .yellow, .page-kicker {
        color:#FFD21F;
    }
    .brand-subtitle {
        color:#777;
        font-size:.68rem;
        font-weight:600;
        letter-spacing:.14em;
        text-transform:uppercase;
        margin-top:.35rem;
    }
    div[role="radiogroup"] {
        display:flex !important;
        flex-wrap:wrap !important;
        gap:.35rem !important;
        justify-content:center !important;
    }
    div[role="radiogroup"] > label {
        background:#111 !important;
        border:1px solid #292929 !important;
        border-radius:8px !important;
        padding:.38rem .82rem !important;
        min-height:34px;
        cursor:pointer !important;
    }
    div[role="radiogroup"] > label input[type="radio"] {
        position:absolute !important;
        opacity:0 !important;
        width:1px !important;
        height:1px !important;
        pointer-events:none !important;
    }
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) {
        background:#FFD21F !important;
        border-color:#FFD21F !important;
    }
    div[role="radiogroup"] > label:has(input[type="radio"]:checked) p {
        color:#080808 !important;
        font-weight:750 !important;
    }
    div[role="radiogroup"] > label p {
        color:#BDBDBD !important;
        font-size:.82rem !important;
        font-weight:600 !important;
        margin:0 !important;
        white-space:nowrap !important;
    }
    .section-divider {
        height:1px;
        background:#292929;
        margin:1rem 0 1.25rem;
    }
    .page-kicker {
        font-size:.69rem;
        font-weight:700;
        letter-spacing:.12em;
        text-transform:uppercase;
        margin-bottom:.18rem;
    }
    .page-title {
        color:#F5F5F5;
        font-size:1.5rem;
        font-weight:750;
        letter-spacing:-.03em;
        margin-bottom:.2rem;
    }
    .page-description {
        color:#858585;
        font-size:.84rem;
        margin-bottom:1rem;
    }
    .filter-label, .kpi-label, .insight-label {
        color:#858585;
        font-size:.69rem;
        font-weight:700;
        letter-spacing:.08em;
        text-transform:uppercase;
    }
    div[data-baseweb="select"] > div {
        background:#111 !important;
        border-color:#292929 !important;
    }
    div[data-baseweb="select"] span {
        color:#F5F5F5 !important;
    }
    [data-testid="stDateInput"] input {
        color:#F5F5F5 !important;
        background:#111 !important;
        border-color:#292929 !important;
    }
    .kpi-card, .insight-card, .empty-state {
        background:#111;
        border:1px solid #292929;
        border-radius:10px;
    }
    .kpi-card {
        padding:1rem;
        min-height:108px;
    }
    .kpi-value {
        color:#F5F5F5;
        font-size:1.5rem;
        font-weight:750;
        margin-top:.35rem;
    }
    .kpi-value.accent { color:#FFD21F; }
    .kpi-caption {
        color:#666;
        font-size:.7rem;
        margin-top:.25rem;
    }
    .insight-card {
        padding:.9rem 1rem;
        min-height:85px;
    }
    .insight-value {
        color:#F5F5F5;
        font-size:1rem;
        font-weight:700;
        margin-top:.35rem;
    }
    .chart-title {
        color:#F5F5F5;
        font-size:.94rem;
        font-weight:680;
        margin-bottom:.2rem;
    }
    .empty-state {
        padding:1.35rem;
        color:#858585;
        text-align:center;
        margin:.4rem 0 1rem;
    }
    [data-testid="stDataFrame"] {
        border:1px solid #292929;
        border-radius:8px;
        overflow:hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)

    for col in EXPECTED_COLUMNS:
        if col not in data.columns:
            data[col] = pd.NA

    data = data[EXPECTED_COLUMNS].copy()

    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    time_text = data["time"].astype("string").str.strip()
    parsed_time = pd.to_datetime(time_text, errors="coerce")
    numeric_time = pd.to_numeric(time_text, errors="coerce")

    data["_hour"] = parsed_time.dt.hour
    data["_hour"] = data["_hour"].fillna(
        numeric_time.where(numeric_time.between(0, 23), np.nan)
    )

    extracted_hour = pd.to_numeric(
        time_text.str.extract(r"^(\d{1,2})(?::\d{1,2})?", expand=False),
        errors="coerce",
    )
    data["_hour"] = pd.to_numeric(
        data["_hour"].fillna(extracted_hour), errors="coerce"
    )

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    text_columns = [
        "services", "ride_status", "source", "destination",
        "ride_id", "payment_method"
    ]
    for col in text_columns:
        data[col] = data[col].astype("string").str.strip()

    status = (
        data["ride_status"]
        .fillna("")
        .astype("string")
        .str.strip()
        .str.lower()
    )

    data["_is_completed"] = status.eq("completed")
    data["_is_cancelled"] = status.eq("cancelled")

    data["_status_clean"] = (
        data["ride_status"].fillna("Unknown").astype("string").str.strip()
    )
    data.loc[data["_status_clean"].eq(""), "_status_clean"] = "Unknown"

    return data


if not CSV_PATH.exists():
    st.error(
        "rides_data.csv was not found. Put rides_data.csv in the same "
        "folder as rapido_ride_intelligence.py."
    )
    st.stop()

try:
    df = load_data(str(CSV_PATH))
except Exception as exc:
    st.error(f"Unable to load rides_data.csv: {exc}")
    st.stop()


# ============================================================
# HELPERS
# ============================================================

def format_number(value):
    if value is None or pd.isna(value):
        return "0"
    try:
        value = float(value)
    except Exception:
        return "0"
    return f"{int(value):,}" if value.is_integer() else f"{value:,.2f}"


def format_currency(value):
    if value is None or pd.isna(value):
        return "₹0"
    try:
        value = float(value)
    except Exception:
        return "₹0"
    return f"₹{int(value):,}" if value.is_integer() else f"₹{value:,.2f}"


def safe_pct(num, den):
    if den is None or den == 0 or num is None or pd.isna(num):
        return 0.0
    return float(num) / float(den) * 100


def available_values(series):
    values = series.dropna().astype(str).str.strip()
    values = values[values != ""]
    return sorted(values.unique().tolist(), key=str.lower)


def completed_only(data):
    return data[data["_is_completed"]].copy()


def show_empty():
    st.markdown(
        '<div class="empty-state">No data available for the selected filters.</div>',
        unsafe_allow_html=True,
    )


def page_header(kicker, title, description):
    st.markdown(
        f"""
        <div class="page-kicker">{kicker}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def chart_title(title):
    st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)


def kpi_card(col, label, value, caption="", accent=False):
    with col:
        cls = "kpi-value accent" if accent else "kpi-value"
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="{cls}">{value}</div>
                <div class="kpi-caption">{caption}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def insight_card(col, label, value):
    with col:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">{label}</div>
                <div class="insight-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def apply_theme(fig, height=340):
    fig.update_layout(
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(family="Inter, Arial, sans-serif", color="#D7D7D7", size=12),
        height=height,
        margin=dict(l=45, r=25, t=20, b=45),
        hoverlabel=dict(bgcolor="#181818", bordercolor="#292929", font_color="#F5F5F5"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#BDBDBD")),
    )
    fig.update_xaxes(
        showgrid=True, gridcolor="#242424", zeroline=False, linecolor="#292929",
        tickfont=dict(color="#8A8A8A"), title_font=dict(color="#8A8A8A")
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="#242424", zeroline=False, linecolor="#292929",
        tickfont=dict(color="#8A8A8A"), title_font=dict(color="#8A8A8A")
    )
    return fig


def show_chart(fig, key):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
        key=key,
    )


def hourly_data(data):
    temp = data.dropna(subset=["_hour"]).copy()
    if temp.empty:
        return pd.DataFrame(columns=["hour", "rides"])
    temp["hour"] = pd.to_numeric(temp["_hour"], errors="coerce").round().astype(int).clip(0, 23)
    return temp.groupby("hour", as_index=False).size().rename(columns={"size": "rides"})


def daily_data(data):
    temp = data.dropna(subset=["date"]).copy()
    if temp.empty:
        return pd.DataFrame(columns=["date", "rides"])
    return (
        temp.groupby("date", as_index=False).size()
        .rename(columns={"size": "rides"})
        .sort_values("date")
    )


def daily_revenue(data):
    temp = completed_only(data).dropna(subset=["date", "total_fare"])
    if temp.empty:
        return pd.DataFrame(columns=["date", "revenue"])
    return (
        temp.groupby("date", as_index=False)["total_fare"]
        .sum()
        .rename(columns={"total_fare": "revenue"})
        .sort_values("date")
    )


# ============================================================
# HEADER + NAVIGATION
# ============================================================

brand, nav_col = st.columns([1.5, 5.5], vertical_alignment="center")

with brand:
    st.markdown(
        """
        <div>
            <div class="brand-main"><span class="yellow">Rapido</span> Ride Intelligence</div>
            <div class="brand-subtitle">Mobility Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col:
    nav = st.radio(
        "Navigation",
        [
            "Overview",
            "Demand",
            "Revenue",
            "Operations",
            "Locations",
            "Data Quality",
            "Ride Explorer",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="dashboard_navigation",
    )

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


# ============================================================
# GLOBAL FILTERS
# ============================================================

st.markdown('<div class="filter-label">Global Filters</div>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.2, 1.5], gap="medium")

services = available_values(df["services"])
statuses = available_values(df["ride_status"])
payments = available_values(df["payment_method"])

payment_options = ["All Payment Methods"] + payments

with f1:
    selected_services = st.multiselect(
        "Service", services, default=services, key="services_filter"
    )

with f2:
    selected_statuses = st.multiselect(
        "Ride Status", statuses, default=statuses, key="status_filter"
    )

with f3:
    selected_payments = st.multiselect(
        "Payment Method",
        payment_options,
        default=["All Payment Methods"],
        key="payment_filter",
    )

with f4:
    valid_dates = df["date"].dropna()
    if valid_dates.empty:
        selected_period = None
        st.caption("No valid dates found.")
    else:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        selected_period = st.date_input(
            "Analysis Period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="date_filter",
        )


# ============================================================
# APPLY FILTERS — SINGLE SOURCE OF TRUTH
# ============================================================

filtered = df.copy()

if selected_services:
    filtered = filtered[filtered["services"].astype(str).isin(selected_services)]
else:
    filtered = filtered.iloc[0:0]

if selected_statuses:
    filtered = filtered[filtered["ride_status"].astype(str).isin(selected_statuses)]
else:
    filtered = filtered.iloc[0:0]

# IMPORTANT:
# "All Payment Methods" deliberately means NO payment filter.
# This preserves cancelled rides whose payment method is blank.
if selected_payments and "All Payment Methods" not in selected_payments:
    filtered = filtered[
        filtered["payment_method"].astype(str).isin(selected_payments)
    ]
elif not selected_payments:
    filtered = filtered.iloc[0:0]

if selected_period is not None and not filtered.empty:
    if isinstance(selected_period, tuple) and len(selected_period) == 2:
        start_date, end_date = selected_period
        filtered = filtered[
            filtered["date"].notna()
            & filtered["date"].dt.date.between(start_date, end_date)
        ]
    elif hasattr(selected_period, "year"):
        filtered = filtered[
            filtered["date"].notna()
            & filtered["date"].dt.date.eq(selected_period)
        ]


# ============================================================
# GLOBAL KPIs
# ============================================================

total_rides = len(filtered)
completed = completed_only(filtered)
cancelled = filtered[filtered["_is_cancelled"]]

total_revenue = completed["total_fare"].sum(min_count=1) if not completed.empty else 0
total_revenue = 0 if pd.isna(total_revenue) else total_revenue

completion_rate = safe_pct(len(completed), total_rides)
cancellation_count = len(cancelled)
cancellation_rate = safe_pct(cancellation_count, total_rides)

average_fare = completed["total_fare"].dropna().mean() if not completed.empty else 0
average_fare = 0 if pd.isna(average_fare) else average_fare

kpis = st.columns(5, gap="medium")
kpi_card(kpis[0], "Total Rides", format_number(total_rides), "Filtered rides")
kpi_card(kpis[1], "Total Revenue", format_currency(total_revenue), "Completed rides only", True)
kpi_card(kpis[2], "Completion Rate", f"{completion_rate:.1f}%", "Completed / total rides")
kpi_card(kpis[3], "Cancellations", format_number(cancellation_count), "Filtered cancelled rides")
kpi_card(kpis[4], "Average Fare", format_currency(average_fare), "Completed rides only")

st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)


# ============================================================
# OVERVIEW
# ============================================================

if nav == "Overview":
    page_header(
        "Executive Overview",
        "Ride Intelligence Overview",
        "Demand, revenue, ride outcomes and operating activity.",
    )

    if filtered.empty:
        show_empty()
    else:
        c1, c2 = st.columns([1.5, 1], gap="medium")

        with c1:
            chart_title("Ride Demand by Hour")
            hourly = hourly_data(filtered)
            if hourly.empty:
                show_empty()
            else:
                fig = px.line(hourly, x="hour", y="rides", markers=True)
                fig.update_traces(
                    line=dict(color="#FFD21F", width=3),
                    marker=dict(color="#FFD21F", size=7),
                    hovertemplate="Hour: %{x}:00<br>Rides: %{y}<extra></extra>",
                )
                fig.update_layout(
                    xaxis_title="Hour", yaxis_title="Ride Count",
                    xaxis=dict(tickmode="linear", tick0=0, dtick=2),
                )
                show_chart(apply_theme(fig), "overview_hour")

        with c2:
            chart_title("Ride Outcome Mix")
            outcome = filtered["_status_clean"].value_counts().reset_index()
            outcome.columns = ["status", "rides"]
            colors = []
            for status in outcome["status"]:
                s = str(status).lower()
                colors.append("#FFD21F" if s == "completed" else "#444444" if s == "cancelled" else "#777777")
            fig = go.Figure(data=[go.Pie(
                labels=outcome["status"], values=outcome["rides"], hole=.62,
                marker=dict(colors=colors, line=dict(color="#111111", width=2)),
                textinfo="percent",
                hovertemplate="%{label}<br>Rides: %{value}<br>%{percent}<extra></extra>",
            )])
            fig.update_layout(annotations=[dict(
                text=f"<b>{format_number(total_rides)}</b><br>Rides",
                x=.5, y=.5, showarrow=False,
                font=dict(color="#F5F5F5", size=15)
            )])
            show_chart(apply_theme(fig), "overview_outcome")

        c3, c4 = st.columns([1, 1.5], gap="medium")

        with c3:
            chart_title("Service Volume")
            service_volume = (
                filtered.assign(service=filtered["services"].fillna("Unknown"))
                .groupby("service", as_index=False).size()
                .rename(columns={"size": "rides"})
                .sort_values("rides", ascending=True)
            )
            fig = px.bar(service_volume, x="rides", y="service", orientation="h")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Ride Count", yaxis_title="")
            show_chart(apply_theme(fig), "overview_service")

        with c4:
            chart_title("Daily Ride Trend")
            daily = daily_data(filtered)
            if daily.empty:
                show_empty()
            else:
                fig = px.area(daily, x="date", y="rides")
                fig.update_traces(
                    line=dict(color="#FFD21F", width=2.5),
                    fillcolor="rgba(255,210,31,0.10)",
                    hovertemplate="Date: %{x|%d %b %Y}<br>Rides: %{y}<extra></extra>",
                )
                fig.update_layout(xaxis_title="Date", yaxis_title="Ride Count")
                show_chart(apply_theme(fig), "overview_daily")

        chart_title("Business Insights")
        insights = st.columns(4, gap="medium")
        hourly = hourly_data(filtered)
        peak_hour = "Unavailable"
        if not hourly.empty:
            peak_hour = f"{int(hourly.loc[hourly['rides'].idxmax(), 'hour']):02d}:00"

        service_counts = filtered["services"].dropna().astype(str).str.strip().value_counts()
        leading_service = service_counts.index[0] if not service_counts.empty else "Unavailable"

        insight_card(insights[0], "Peak Demand Hour", peak_hour)
        insight_card(insights[1], "Leading Service", leading_service)
        insight_card(insights[2], "Completion Rate", f"{completion_rate:.1f}%")
        insight_card(insights[3], "Cancellation Rate", f"{cancellation_rate:.1f}%")


# ============================================================
# DEMAND
# ============================================================

elif nav == "Demand":
    page_header(
        "Demand Analytics",
        "When Rides Happen",
        "Explore demand by hour, weekday, service and month.",
    )

    if filtered.empty:
        show_empty()
    else:
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            chart_title("Ride Demand by Hour")
            hourly = hourly_data(filtered)
            fig = px.line(hourly, x="hour", y="rides", markers=True)
            fig.update_traces(line=dict(color="#FFD21F", width=3), marker=dict(color="#FFD21F", size=7))
            fig.update_layout(xaxis_title="Hour", yaxis_title="Ride Count", xaxis=dict(tickmode="linear", tick0=0, dtick=2))
            show_chart(apply_theme(fig, 350), "demand_hour")

        with c2:
            chart_title("Rides by Day of Week")
            weekday = filtered.dropna(subset=["date"]).copy()
            weekday["day_number"] = weekday["date"].dt.dayofweek
            weekday["day"] = weekday["date"].dt.day_name()
            weekday_counts = weekday.groupby(["day_number", "day"], as_index=False).size().rename(columns={"size": "rides"})
            order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            fig = px.bar(weekday_counts, x="day", y="rides")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Day", yaxis_title="Ride Count", xaxis=dict(categoryorder="array", categoryarray=order))
            show_chart(apply_theme(fig, 350), "demand_weekday")

        chart_title("Demand by Service and Hour")
        heat = filtered.dropna(subset=["_hour", "services"]).copy()
        heat["hour"] = pd.to_numeric(heat["_hour"], errors="coerce").round().astype(int).clip(0, 23)
        heat_data = heat.groupby(["services", "hour"], as_index=False).size().rename(columns={"size": "rides"})
        fig = px.density_heatmap(
            heat_data, x="hour", y="services", z="rides",
            color_continuous_scale=["#181818", "#6D5B00", "#FFD21F"]
        )
        fig.update_layout(xaxis_title="Hour", yaxis_title="Service")
        show_chart(apply_theme(fig, 390), "demand_heatmap")

        chart_title("Monthly Ride Volume")
        monthly = filtered.dropna(subset=["date"]).copy()
        monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
        monthly_counts = monthly.groupby("month", as_index=False).size().rename(columns={"size": "rides"})
        fig = px.bar(monthly_counts, x="month", y="rides")
        fig.update_traces(marker_color="#FFD21F")
        fig.update_layout(xaxis_title="Month", yaxis_title="Ride Count")
        show_chart(apply_theme(fig, 350), "demand_monthly")


# ============================================================
# REVENUE
# ============================================================

elif nav == "Revenue":
    page_header(
        "Revenue Analytics",
        "Revenue & Fare Performance",
        "Revenue calculations use completed rides only.",
    )

    if filtered.empty:
        show_empty()
    else:
        done = completed_only(filtered)
        if done.empty:
            show_empty()
        else:
            c1, c2 = st.columns([1.5, 1], gap="medium")

            with c1:
                chart_title("Daily Revenue Trend")
                revenue = daily_revenue(filtered)
                fig = px.area(revenue, x="date", y="revenue")
                fig.update_traces(
                    line=dict(color="#FFD21F", width=2.5),
                    fillcolor="rgba(255,210,31,0.10)",
                    hovertemplate="Date: %{x|%d %b %Y}<br>Revenue: ₹%{y:,.0f}<extra></extra>",
                )
                fig.update_layout(xaxis_title="Date", yaxis_title="Revenue")
                show_chart(apply_theme(fig, 350), "revenue_daily")

            with c2:
                chart_title("Revenue by Payment Method")
                payment = done.dropna(subset=["total_fare"]).copy()
                payment["payment"] = payment["payment_method"].fillna("Unknown")
                payment_revenue = payment.groupby("payment", as_index=False)["total_fare"].sum().rename(columns={"total_fare": "revenue"}).sort_values("revenue", ascending=False)
                fig = px.bar(payment_revenue, x="revenue", y="payment", orientation="h")
                fig.update_traces(marker_color="#FFD21F")
                fig.update_layout(xaxis_title="Revenue", yaxis_title="Payment Method")
                show_chart(apply_theme(fig, 350), "revenue_payment")

            c3, c4 = st.columns(2, gap="medium")

            with c3:
                chart_title("Average Fare by Service")
                fare_service = done.dropna(subset=["total_fare"]).copy()
                fare_service["service"] = fare_service["services"].fillna("Unknown")
                fare_service = fare_service.groupby("service", as_index=False)["total_fare"].mean().rename(columns={"total_fare": "average_fare"}).sort_values("average_fare")
                fig = px.bar(fare_service, x="average_fare", y="service", orientation="h")
                fig.update_traces(marker_color="#FFD21F")
                fig.update_layout(xaxis_title="Average Fare", yaxis_title="Service")
                show_chart(apply_theme(fig, 350), "revenue_average_fare")

            with c4:
                chart_title("Fare Distribution")
                fares = done["total_fare"].dropna()
                fig = go.Figure(go.Histogram(x=fares, nbinsx=30, marker=dict(color="#FFD21F", line=dict(color="#111111", width=.5))))
                fig.update_layout(xaxis_title="Fare", yaxis_title="Ride Count")
                show_chart(apply_theme(fig, 350), "revenue_distribution")


# ============================================================
# OPERATIONS
# ============================================================

elif nav == "Operations":
    page_header(
        "Operations Analytics",
        "Operational Performance",
        "Ride outcomes, duration and service-level operating metrics.",
    )

    if filtered.empty:
        show_empty()
    else:
        c1, c2 = st.columns([1.25, 1], gap="medium")

        with c1:
            chart_title("Ride Status by Service")
            status_service = (
                filtered.assign(
                    service=filtered["services"].fillna("Unknown"),
                    status=filtered["_status_clean"]
                )
                .groupby(["service", "status"], as_index=False).size()
                .rename(columns={"size": "rides"})
            )
            fig = px.bar(
                status_service, x="service", y="rides", color="status",
                barmode="stack",
                color_discrete_map={"Completed": "#FFD21F", "Cancelled": "#444444"}
            )
            fig.update_layout(xaxis_title="Service", yaxis_title="Ride Count")
            show_chart(apply_theme(fig, 370), "operations_status")

        with c2:
            chart_title("Trip Duration Distribution")
            durations = pd.to_numeric(filtered["duration"], errors="coerce").dropna()
            durations = durations[np.isfinite(durations)]
            fig = go.Figure(go.Histogram(x=durations, nbinsx=30, marker=dict(color="#FFD21F", line=dict(color="#111111", width=.5))))
            fig.update_layout(xaxis_title="Duration", yaxis_title="Ride Count")
            show_chart(apply_theme(fig, 370), "operations_duration")

        c3, c4 = st.columns(2, gap="medium")

        with c3:
            chart_title("Completion Rate by Service")
            stats = (
                filtered.assign(service=filtered["services"].fillna("Unknown"))
                .groupby("service")
                .agg(total=("ride_id", "size"), completed=("_is_completed", "sum"))
                .reset_index()
            )
            stats["completion_rate"] = (stats["completed"] / stats["total"].replace(0, np.nan) * 100).fillna(0)
            fig = px.bar(stats.sort_values("completion_rate"), x="completion_rate", y="service", orientation="h")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Completion Rate (%)", yaxis_title="Service", xaxis=dict(range=[0, 100]))
            show_chart(apply_theme(fig, 370), "operations_completion")

        with c4:
            chart_title("Cancellation Rate by Hour")
            hd = filtered.dropna(subset=["_hour"]).copy()
            hd["hour"] = pd.to_numeric(hd["_hour"], errors="coerce").round().astype(int).clip(0, 23)
            stats = hd.groupby("hour").agg(total=("ride_id", "size"), cancelled=("_is_cancelled", "sum")).reset_index()
            stats["cancellation_rate"] = (stats["cancelled"] / stats["total"].replace(0, np.nan) * 100).fillna(0)
            fig = px.line(stats, x="hour", y="cancellation_rate", markers=True)
            fig.update_traces(line=dict(color="#FFD21F", width=3), marker=dict(color="#FFD21F", size=7))
            fig.update_layout(xaxis_title="Hour", yaxis_title="Cancellation Rate (%)", xaxis=dict(tickmode="linear", tick0=0, dtick=2))
            show_chart(apply_theme(fig, 370), "operations_cancellation")


# ============================================================
# LOCATIONS
# ============================================================

elif nav == "Locations":
    page_header(
        "Location Analytics",
        "Pickup, Destination & Route Intelligence",
        "Identify the locations and routes generating the highest ride volumes.",
    )

    if filtered.empty:
        show_empty()
    else:
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            chart_title("Top Pickup Locations")
            pickup = (
                filtered.assign(location=filtered["source"].fillna("Unknown"))
                .groupby("location", as_index=False).size()
                .rename(columns={"size": "rides"})
                .sort_values("rides", ascending=False).head(10)
                .sort_values("rides")
            )
            fig = px.bar(pickup, x="rides", y="location", orientation="h")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Ride Count", yaxis_title="Pickup Location")
            show_chart(apply_theme(fig, 390), "locations_pickup")

        with c2:
            chart_title("Top Destination Locations")
            destination = (
                filtered.assign(location=filtered["destination"].fillna("Unknown"))
                .groupby("location", as_index=False).size()
                .rename(columns={"size": "rides"})
                .sort_values("rides", ascending=False).head(10)
                .sort_values("rides")
            )
            fig = px.bar(destination, x="rides", y="location", orientation="h")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Ride Count", yaxis_title="Destination")
            show_chart(apply_theme(fig, 390), "locations_destination")

        chart_title("Top Routes")
        routes = filtered.copy()
        routes["source_clean"] = routes["source"].fillna("Unknown").astype(str).str.strip()
        routes["destination_clean"] = routes["destination"].fillna("Unknown").astype(str).str.strip()
        routes["route"] = routes["source_clean"] + " → " + routes["destination_clean"]
        route_counts = routes.groupby("route", as_index=False).size().rename(columns={"size": "rides"}).sort_values("rides", ascending=False).head(15).sort_values("rides")
        fig = px.bar(route_counts, x="rides", y="route", orientation="h")
        fig.update_traces(marker_color="#FFD21F")
        fig.update_layout(xaxis_title="Ride Count", yaxis_title="Route")
        show_chart(apply_theme(fig, 470), "locations_routes")


# ============================================================
# DATA QUALITY
# ============================================================

elif nav == "Data Quality":
    page_header(
        "Data Quality Audit",
        "Can This Data Be Trusted?",
        "Validate completeness, fare-distance relationships and operational plausibility.",
    )

    done = completed_only(filtered)
    valid_done = done[(done["distance"] > 0) & (done["duration"] > 0)].copy()

    if valid_done.empty:
        show_empty()
    else:
        corr = valid_done["distance"].corr(valid_done["total_fare"])
        corr_text = "n/a" if pd.isna(corr) else f"{corr:+.3f}"

        speed = valid_done["distance"] / (valid_done["duration"] / 60)
        fast_pct = safe_pct((speed > 80).sum(), len(valid_done))

        missing_fares = int(filtered["total_fare"].isna().sum())
        route_counts = filtered.groupby(["source", "destination"], dropna=False).size()
        repeat_routes = int((route_counts > 1).sum())

        dq = st.columns(4, gap="medium")
        kpi_card(dq[0], "Fare vs Distance", corr_text, "Pearson correlation", True)
        kpi_card(dq[1], "High-Speed Trips", f"{fast_pct:.1f}%", "Completed rides above 80 km/h")
        kpi_card(dq[2], "Missing Fares", format_number(missing_fares), "Records with missing total fare")
        kpi_card(dq[3], "Repeated Routes", format_number(repeat_routes), "Routes observed more than once")

        c1, c2 = st.columns(2, gap="medium")

        with c1:
            chart_title("Fare vs Distance — Completed Rides")
            sample = valid_done.sample(min(3000, len(valid_done)), random_state=1)
            fig = px.scatter(sample, x="distance", y="total_fare", opacity=.35)
            fig.update_traces(marker=dict(color="#FFD21F", size=5))
            fig.update_layout(xaxis_title="Distance (km)", yaxis_title="Total Fare (INR)")
            show_chart(apply_theme(fig), "dq_scatter")

        with c2:
            chart_title("Average Fare by Distance Band")
            bands = (
                valid_done.assign(
                    band=pd.cut(
                        valid_done["distance"],
                        [0, 10, 20, 30, 40, 50, np.inf],
                        labels=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
                    )
                )
                .groupby("band", observed=True, as_index=False)
                .agg(avg_fare=("total_fare", "mean"))
            )
            fig = px.bar(bands, x="band", y="avg_fare")
            fig.update_traces(marker_color="#FFD21F")
            fig.update_layout(xaxis_title="Distance Band (km)", yaxis_title="Average Fare (INR)")
            show_chart(apply_theme(fig), "dq_bands")

        st.info(
            "Quality note: this audit flags unusual fare-distance relationships "
            "and unusually high implied speeds. These checks identify data-quality "
            "signals; they do not by themselves prove that the underlying data is synthetic."
        )


# ============================================================
# RIDE EXPLORER
# ============================================================

elif nav == "Ride Explorer":
    page_header(
        "Ride Explorer",
        "Inspect Individual Rides",
        "Search the filtered dataset at ride level.",
    )

    if filtered.empty:
        show_empty()
    else:
        search = st.text_input(
            "Search Ride ID / Source / Destination",
            placeholder="e.g. RIDE123 or location name",
        )

        explorer = filtered.copy()

        if search.strip():
            term = search.strip().lower()
            mask = (
                explorer["ride_id"].astype(str).str.lower().str.contains(term, na=False)
                | explorer["source"].astype(str).str.lower().str.contains(term, na=False)
                | explorer["destination"].astype(str).str.lower().str.contains(term, na=False)
            )
            explorer = explorer[mask]

        columns = [
            "ride_id", "services", "date", "time", "ride_status",
            "source", "destination", "duration", "distance",
            "total_fare", "payment_method"
        ]
        explorer = explorer[columns].sort_values("date", ascending=False, na_position="last").head(100)
        explorer["date"] = explorer["date"].dt.strftime("%Y-%m-%d").fillna("")

        st.dataframe(
            explorer,
            use_container_width=True,
            hide_index=True,
            height=min(560, 100 + len(explorer) * 35),
            column_config={
                "ride_id": st.column_config.TextColumn("Ride ID"),
                "services": st.column_config.TextColumn("Service"),
                "date": st.column_config.TextColumn("Date"),
                "time": st.column_config.TextColumn("Time"),
                "ride_status": st.column_config.TextColumn("Ride Status"),
                "source": st.column_config.TextColumn("Source"),
                "destination": st.column_config.TextColumn("Destination"),
                "duration": st.column_config.NumberColumn("Duration", format="%.2f"),
                "distance": st.column_config.NumberColumn("Distance", format="%.2f"),
                "total_fare": st.column_config.NumberColumn("Total Fare", format="₹%.2f"),
                "payment_method": st.column_config.TextColumn("Payment Method"),
            },
        )
        st.caption(
            f"Showing up to 100 rides • {format_number(len(explorer))} rows shown."
        )
