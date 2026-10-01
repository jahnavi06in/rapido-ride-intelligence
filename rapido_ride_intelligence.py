# rapido_ride_intelligence.py

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Rapido Ride Intelligence",
    page_icon="🟡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. CONSTANTS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "rides_data.csv"

EXPECTED_COLUMNS = [
    "services",
    "date",
    "time",
    "ride_status",
    "source",
    "destination",
    "duration",
    "ride_id",
    "distance",
    "ride_charge",
    "misc_charge",
    "total_fare",
    "payment_method",
]

NUMERIC_COLUMNS = [
    "duration",
    "distance",
    "ride_charge",
    "misc_charge",
    "total_fare",
]


# ============================================================
# 3. CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background: #080808;
        color: #F5F5F5;
    }

    [data-testid="stAppViewContainer"] {
        background: #080808;
    }

    [data-testid="stHeader"] {
        background: #080808;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }


    /* ======================================================
       BRAND HEADER
       ====================================================== */

    
     .brand-block {
    padding-top: 0.15rem;
    padding-right: 1.2rem;
    white-space: nowrap;

    }

    .brand-main {
    color: #F5F5F5;
    font-size: 1.35rem;
    line-height: 1.05;
    font-weight: 750;
    letter-spacing: -0.04em;
    white-space: nowrap;
}

    .brand-main .yellow {
        color: #FFD21F;
    }

    .brand-subtitle {
        color: #777777;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 0.38rem;
        white-space: nowrap;
    }


    /* ======================================================
       NAVIGATION
       ====================================================== */

    .nav-wrapper {
        padding-top: 0.05rem;
    }

    /* Keep the actual Streamlit radio interactive */
    div[role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.35rem !important;
        justify-content: center !important;
        align-items: center !important;
        background: transparent !important;
    }

    div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        background: #111111 !important;
        border: 1px solid #292929 !important;
        border-radius: 8px !important;
        padding: 0.38rem 0.82rem !important;
        min-height: 34px !important;
        cursor: pointer !important;
        transition: none !important;
    }

    div[role="radiogroup"] > label:hover {
        border-color: #FFD21F !important;
        background: #171717 !important;
    }

    /*
       Hide only the radio circle, NOT the clickable label.
       The label itself remains the interactive control.
    */
    div[role="radiogroup"] > label input[type="radio"] {
        position: absolute !important;
        opacity: 0 !important;
        width: 1px !important;
        height: 1px !important;
        pointer-events: none !important;
    }

    div[role="radiogroup"] > label:has(input[type="radio"]:checked) {
        background: #FFD21F !important;
        border-color: #FFD21F !important;
    }

    div[role="radiogroup"] > label:has(input[type="radio"]:checked) p {
        color: #080808 !important;
        font-weight: 750 !important;
    }

    div[role="radiogroup"] > label p {
        color: #BDBDBD !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        white-space: nowrap !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    .section-divider {
        height: 1px;
        background: #292929;
        margin: 1rem 0 1.25rem 0;
    }


    /* ======================================================
       PAGE HEADINGS
       ====================================================== */

    .page-kicker {
        color: #FFD21F;
        font-size: 0.69rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.18rem;
    }

    .page-title {
        color: #F5F5F5;
        font-size: 1.5rem;
        font-weight: 750;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
    }

    .page-description {
        color: #858585;
        font-size: 0.84rem;
        margin-bottom: 1rem;
    }


    /* ======================================================
       FILTERS
       ====================================================== */

    .filter-label {
        color: #858585;
        font-size: 0.69rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    div[data-baseweb="select"] > div {
        background-color: #111111 !important;
        border-color: #292929 !important;
    }

    div[data-baseweb="select"] span {
        color: #F5F5F5 !important;
    }

    div[data-baseweb="select"] svg {
        fill: #888888 !important;
    }

    [data-testid="stDateInput"] input {
        color: #F5F5F5 !important;
        background-color: #111111 !important;
        border-color: #292929 !important;
    }


    /* ======================================================
       KPI CARDS
       ====================================================== */

    .kpi-card {
        background: #111111;
        border: 1px solid #292929;
        border-radius: 10px;
        padding: 1rem;
        min-height: 108px;
    }

    .kpi-label {
        color: #858585;
        font-size: 0.69rem;
        font-weight: 650;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #F5F5F5;
        font-size: 1.5rem;
        font-weight: 750;
        letter-spacing: -0.035em;
        margin-top: 0.35rem;
    }

    .kpi-value.accent {
        color: #FFD21F;
    }

    .kpi-caption {
        color: #666666;
        font-size: 0.7rem;
        margin-top: 0.25rem;
    }


    /* ======================================================
       INSIGHTS
       ====================================================== */

    .insight-card {
        background: #111111;
        border: 1px solid #292929;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        min-height: 85px;
    }

    .insight-label {
        color: #858585;
        font-size: 0.68rem;
        font-weight: 650;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }

    .insight-value {
        color: #F5F5F5;
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }


    /* ======================================================
       CHARTS
       ====================================================== */

    .chart-title {
        color: #F5F5F5;
        font-size: 0.94rem;
        font-weight: 680;
        margin-bottom: 0.2rem;
    }

    .stPlotlyChart {
        background: #111111;
        border-radius: 8px;
    }


    /* ======================================================
       EMPTY STATE
       ====================================================== */

    .empty-state {
        background: #111111;
        border: 1px solid #292929;
        border-radius: 10px;
        padding: 1.35rem;
        color: #858585;
        text-align: center;
        margin: 0.4rem 0 1rem 0;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #292929;
        border-radius: 8px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. DATA LOADING
# ============================================================

@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA

    df = df[EXPECTED_COLUMNS].copy()

    # Date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    # Time
    time_text = (
        df["time"]
        .astype("string")
        .str.strip()
    )

    parsed_time = pd.to_datetime(
        time_text,
        errors="coerce",
    )

    numeric_time = pd.to_numeric(
        time_text,
        errors="coerce",
    )

    df["_hour"] = parsed_time.dt.hour

    df["_hour"] = df["_hour"].fillna(
        numeric_time.where(
            numeric_time.between(0, 23),
            np.nan,
        )
    )

    extracted_hour = pd.to_numeric(
        time_text.str.extract(
            r"^(\d{1,2})(?::\d{1,2})?",
            expand=False,
        ),
        errors="coerce",
    )

    df["_hour"] = df["_hour"].fillna(extracted_hour)

    df["_hour"] = pd.to_numeric(
        df["_hour"],
        errors="coerce",
    )

    # Numeric fields
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Text fields
    text_columns = [
        "services",
        "ride_status",
        "source",
        "destination",
        "ride_id",
        "payment_method",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Status helpers
    status = (
        df["ride_status"]
        .fillna("")
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df["_is_completed"] = status.eq("completed")
    df["_is_cancelled"] = status.eq("cancelled")

    df["_status_clean"] = (
        df["ride_status"]
        .fillna("Unknown")
        .astype("string")
        .str.strip()
    )

    df.loc[
        df["_status_clean"].eq(""),
        "_status_clean",
    ] = "Unknown"

    return df


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def format_number(value) -> str:
    if value is None or pd.isna(value):
        return "0"

    try:
        value = float(value)
    except Exception:
        return "0"

    if value.is_integer():
        return f"{int(value):,}"

    return f"{value:,.2f}"


def format_currency(value) -> str:
    if value is None or pd.isna(value):
        return "₹0"

    try:
        value = float(value)
    except Exception:
        return "₹0"

    if value.is_integer():
        return f"₹{int(value):,}"

    return f"₹{value:,.2f}"


def safe_pct(numerator, denominator) -> float:
    if denominator is None or denominator == 0:
        return 0.0

    if numerator is None or pd.isna(numerator):
        return 0.0

    return float(numerator) / float(denominator) * 100


def available_values(series) -> list:
    values = (
        series
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[values != ""]

    return sorted(
        values.unique().tolist(),
        key=str.lower,
    )


def completed_only(data):
    if data.empty:
        return data.copy()

    return data[data["_is_completed"]].copy()


def show_empty():
    st.markdown(
        """
        <div class="empty-state">
            No data available for the selected filters.
        </div>
        """,
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
    st.markdown(
        f'<div class="chart-title">{title}</div>',
        unsafe_allow_html=True,
    )


def apply_theme(fig, height=340):
    fig.update_layout(
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#D7D7D7",
            size=12,
        ),
        height=height,
        margin=dict(
            l=45,
            r=25,
            t=20,
            b=45,
        ),
        hoverlabel=dict(
            bgcolor="#181818",
            bordercolor="#292929",
            font_color="#F5F5F5",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#BDBDBD",
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#242424",
        zeroline=False,
        linecolor="#292929",
        tickfont=dict(
            color="#8A8A8A",
        ),
        title_font=dict(
            color="#8A8A8A",
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#242424",
        zeroline=False,
        linecolor="#292929",
        tickfont=dict(
            color="#8A8A8A",
        ),
        title_font=dict(
            color="#8A8A8A",
        ),
    )

    return fig


def show_chart(fig, key):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
        key=key,
    )


def kpi_card(column, label, value, caption="", accent=False):
    with column:
        css_class = (
            "kpi-value accent"
            if accent
            else "kpi-value"
        )

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="{css_class}">{value}</div>
                <div class="kpi-caption">{caption}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def insight_card(column, label, value):
    with column:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-label">{label}</div>
                <div class="insight-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def hourly_data(data):
    if data.empty:
        return pd.DataFrame(
            columns=["hour", "rides"]
        )

    temp = data.dropna(
        subset=["_hour"]
    ).copy()

    if temp.empty:
        return pd.DataFrame(
            columns=["hour", "rides"]
        )

    temp["hour"] = (
        pd.to_numeric(
            temp["_hour"],
            errors="coerce",
        )
        .round()
        .astype(int)
        .clip(0, 23)
    )

    return (
        temp.groupby(
            "hour",
            as_index=False,
        )
        .size()
        .rename(
            columns={"size": "rides"}
        )
    )


def daily_data(data):
    if data.empty:
        return pd.DataFrame(
            columns=["date", "rides"]
        )

    temp = data.dropna(
        subset=["date"]
    ).copy()

    if temp.empty:
        return pd.DataFrame(
            columns=["date", "rides"]
        )

    return (
        temp.groupby(
            "date",
            as_index=False,
        )
        .size()
        .rename(
            columns={"size": "rides"}
        )
        .sort_values("date")
    )


def daily_revenue(data):
    temp = completed_only(data)

    if temp.empty:
        return pd.DataFrame(
            columns=["date", "revenue"]
        )

    temp = temp.dropna(
        subset=["date", "total_fare"]
    )

    if temp.empty:
        return pd.DataFrame(
            columns=["date", "revenue"]
        )

    return (
        temp.groupby(
            "date",
            as_index=False,
        )["total_fare"]
        .sum()
        .rename(
            columns={
                "total_fare": "revenue"
            }
        )
        .sort_values("date")
    )


# ============================================================
# 6. LOAD DATA
# ============================================================

if not CSV_PATH.exists():
    st.error(
        "rides_data.csv was not found. "
        "Place rides_data.csv in the same folder as "
        "rapido_ride_intelligence.py."
    )
    st.stop()

try:
    df = load_data(str(CSV_PATH))
except Exception as exc:
    st.error(f"Unable to load rides_data.csv: {exc}")
    st.stop()


# ============================================================
# 7. HEADER
# ============================================================

# IMPORTANT:
# JJ Analyst / Analytics has been completely removed.
# The header now has only branding + navigation.

header_brand, header_nav = st.columns(
    [1.5, 4.5],
    vertical_alignment="center",
)


with header_brand:
    st.markdown(
        """
        <div class="brand-block">
            <div class="brand-main">
                <span class="yellow">Rapido</span>
                Ride Intelligence
            </div>
            <div class="brand-subtitle">
                Mobility Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_nav:
    # Real Streamlit navigation.
    # No static HTML navigation is used.
    nav = st.radio(
        "Navigation",
        [
            "Overview",
            "Demand",
            "Revenue",
            "Operations",
            "Locations",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="dashboard_navigation",
    )


st.markdown(
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)


# ============================================================
# 8. GLOBAL FILTERS
# ============================================================

st.markdown(
    '<div class="filter-label">Global Filters</div>',
    unsafe_allow_html=True,
)

filter1, filter2, filter3, filter4 = st.columns(
    [1.2, 1.2, 1.2, 1.5],
    gap="medium",
)

services = available_values(
    df["services"]
)

statuses = available_values(
    df["ride_status"]
)

payments = available_values(
    df["payment_method"]
)

with filter1:
    selected_services = st.multiselect(
        "Service",
        services,
        default=services,
        key="services_filter",
    )

with filter2:
    selected_statuses = st.multiselect(
        "Ride Status",
        statuses,
        default=statuses,
        key="status_filter",
    )

with filter3:
    selected_payments = st.multiselect(
        "Payment Method",
        payments,
        default=payments,
        key="payment_filter",
    )

with filter4:
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
# 9. APPLY FILTERS
# ============================================================

filtered = df.copy()

if selected_services:
    filtered = filtered[
        filtered["services"]
        .astype(str)
        .isin(selected_services)
    ]
else:
    filtered = filtered.iloc[0:0]

if selected_statuses:
    filtered = filtered[
        filtered["ride_status"]
        .astype(str)
        .isin(selected_statuses)
    ]
else:
    filtered = filtered.iloc[0:0]

if selected_payments:
    filtered = filtered[
        filtered["payment_method"]
        .astype(str)
        .isin(selected_payments)
    ]
else:
    filtered = filtered.iloc[0:0]

if selected_period is not None and not filtered.empty:

    if (
        isinstance(selected_period, tuple)
        and len(selected_period) == 2
    ):
        start_date, end_date = selected_period

        filtered = filtered[
            filtered["date"].notna()
            & filtered["date"].dt.date.between(
                start_date,
                end_date,
            )
        ]

    elif hasattr(selected_period, "year"):
        filtered = filtered[
            filtered["date"].notna()
            & filtered["date"].dt.date.eq(
                selected_period
            )
        ]


# ============================================================
# 10. KPI CALCULATIONS
# ============================================================

total_rides = len(filtered)

completed = completed_only(filtered)

cancelled = filtered[
    filtered["_is_cancelled"]
].copy()

total_revenue = (
    completed["total_fare"]
    .sum(min_count=1)
    if not completed.empty
    else 0
)

if pd.isna(total_revenue):
    total_revenue = 0

completion_rate = safe_pct(
    len(completed),
    total_rides,
)

cancellation_count = len(cancelled)

average_fare = (
    completed["total_fare"]
    .dropna()
    .mean()
    if not completed.empty
    else 0
)

if pd.isna(average_fare):
    average_fare = 0


# ============================================================
# 11. KPI CARDS
# ============================================================

kpis = st.columns(
    5,
    gap="medium",
)

kpi_card(
    kpis[0],
    "Total Rides",
    format_number(total_rides),
    "Filtered rides",
)

kpi_card(
    kpis[1],
    "Total Revenue",
    format_currency(total_revenue),
    "Completed rides only",
    accent=True,
)

kpi_card(
    kpis[2],
    "Completion Rate",
    f"{completion_rate:.1f}%",
    "Completed / total rides",
)

kpi_card(
    kpis[3],
    "Cancellations",
    format_number(cancellation_count),
    "Filtered cancelled rides",
)

kpi_card(
    kpis[4],
    "Average Fare",
    format_currency(average_fare),
    "Completed rides only",
)


st.markdown(
    "<div style='height:0.8rem'></div>",
    unsafe_allow_html=True,
)


# ============================================================
# 12. OVERVIEW
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

        # ------------------------------
        # Demand by Hour
        # ------------------------------

        col1, col2 = st.columns(
            [1.5, 1],
            gap="medium",
        )

        with col1:

            chart_title(
                "Ride Demand by Hour"
            )

            hourly = hourly_data(
                filtered
            )

            if hourly.empty:
                show_empty()

            else:

                fig = px.line(
                    hourly,
                    x="hour",
                    y="rides",
                    markers=True,
                )

                fig.update_traces(
                    line=dict(
                        color="#FFD21F",
                        width=3,
                    ),
                    marker=dict(
                        color="#FFD21F",
                        size=7,
                    ),
                    hovertemplate=(
                        "Hour: %{x}:00"
                        "<br>Rides: %{y}"
                        "<extra></extra>"
                    ),
                )

                fig.update_layout(
                    xaxis_title="Hour",
                    yaxis_title="Ride Count",
                    xaxis=dict(
                        tickmode="linear",
                        tick0=0,
                        dtick=2,
                    ),
                )

                show_chart(
                    apply_theme(fig),
                    "overview_hour",
                )

        # ------------------------------
        # Outcome Mix
        # ------------------------------

        with col2:

            chart_title(
                "Ride Outcome Mix"
            )

            outcome = (
                filtered["_status_clean"]
                .value_counts()
                .reset_index()
            )

            outcome.columns = [
                "status",
                "rides",
            ]

            if outcome.empty:
                show_empty()

            else:

                colors = []

                for status in outcome["status"]:
                    if str(status).lower() == "completed":
                        colors.append("#FFD21F")
                    elif str(status).lower() == "cancelled":
                        colors.append("#444444")
                    else:
                        colors.append("#777777")

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=outcome["status"],
                            values=outcome["rides"],
                            hole=0.62,
                            marker=dict(
                                colors=colors,
                                line=dict(
                                    color="#111111",
                                    width=2,
                                ),
                            ),
                            textinfo="percent",
                            hovertemplate=(
                                "%{label}"
                                "<br>Rides: %{value}"
                                "<br>%{percent}"
                                "<extra></extra>"
                            ),
                        )
                    ]
                )

                fig.update_layout(
                    annotations=[
                        dict(
                            text=(
                                f"<b>{format_number(total_rides)}</b>"
                                "<br>Rides"
                            ),
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(
                                color="#F5F5F5",
                                size=15,
                            ),
                        )
                    ]
                )

                show_chart(
                    apply_theme(fig),
                    "overview_outcome",
                )


        # ------------------------------
        # Service Volume
        # ------------------------------

        col3, col4 = st.columns(
            [1, 1.5],
            gap="medium",
        )

        with col3:

            chart_title(
                "Service Volume"
            )

            service_volume = (
                filtered.assign(
                    service=filtered[
                        "services"
                    ].fillna("Unknown")
                )
                .groupby(
                    "service",
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
                .sort_values(
                    "rides",
                    ascending=True,
                )
            )

            if service_volume.empty:
                show_empty()

            else:

                fig = px.bar(
                    service_volume,
                    x="rides",
                    y="service",
                    orientation="h",
                )

                fig.update_traces(
                    marker_color="#FFD21F",
                    hovertemplate=(
                        "Service: %{y}"
                        "<br>Rides: %{x}"
                        "<extra></extra>"
                    ),
                )

                fig.update_layout(
                    xaxis_title="Ride Count",
                    yaxis_title="",
                )

                show_chart(
                    apply_theme(fig),
                    "overview_service",
                )

        # ------------------------------
        # Daily Trend
        # ------------------------------

        with col4:

            chart_title(
                "Daily Ride Trend"
            )

            daily = daily_data(
                filtered
            )

            if daily.empty:
                show_empty()

            else:

                fig = px.area(
                    daily,
                    x="date",
                    y="rides",
                )

                fig.update_traces(
                    line=dict(
                        color="#FFD21F",
                        width=2.5,
                    ),
                    fillcolor=(
                        "rgba(255,210,31,0.10)"
                    ),
                    hovertemplate=(
                        "Date: %{x|%d %b %Y}"
                        "<br>Rides: %{y}"
                        "<extra></extra>"
                    ),
                )

                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Ride Count",
                )

                show_chart(
                    apply_theme(fig),
                    "overview_daily",
                )


        # ------------------------------
        # Insights
        # ------------------------------

        chart_title(
            "Business Insights"
        )

        insights = st.columns(
            4,
            gap="medium",
        )

        hourly = hourly_data(
            filtered
        )

        if hourly.empty:
            peak_hour = "Unavailable"
        else:
            row = hourly.loc[
                hourly["rides"].idxmax()
            ]
            peak_hour = (
                f"{int(row['hour']):02d}:00"
            )

        service_counts = (
            filtered["services"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
        )

        leading_service = (
            service_counts.index[0]
            if not service_counts.empty
            else "Unavailable"
        )

        cancellation_rate = safe_pct(
            cancellation_count,
            total_rides,
        )

        insight_card(
            insights[0],
            "Peak Demand Hour",
            peak_hour,
        )

        insight_card(
            insights[1],
            "Leading Service",
            leading_service,
        )

        insight_card(
            insights[2],
            "Completion Rate",
            f"{completion_rate:.1f}%",
        )

        insight_card(
            insights[3],
            "Cancellation Rate",
            f"{cancellation_rate:.1f}%",
        )


# ============================================================
# 13. DEMAND
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

        col1, col2 = st.columns(
            2,
            gap="medium",
        )

        # ------------------------------
        # Hour
        # ------------------------------

        with col1:

            chart_title(
                "Ride Demand by Hour"
            )

            hourly = hourly_data(
                filtered
            )

            if hourly.empty:
                show_empty()

            else:

                fig = px.line(
                    hourly,
                    x="hour",
                    y="rides",
                    markers=True,
                )

                fig.update_traces(
                    line=dict(
                        color="#FFD21F",
                        width=3,
                    ),
                    marker=dict(
                        color="#FFD21F",
                        size=7,
                    ),
                )

                fig.update_layout(
                    xaxis_title="Hour",
                    yaxis_title="Ride Count",
                    xaxis=dict(
                        tickmode="linear",
                        tick0=0,
                        dtick=2,
                    ),
                )

                show_chart(
                    apply_theme(fig, 350),
                    "demand_hour",
                )

        # ------------------------------
        # Weekday
        # ------------------------------

        with col2:

            chart_title(
                "Rides by Day of Week"
            )

            weekday = filtered.dropna(
                subset=["date"]
            ).copy()

            if weekday.empty:
                show_empty()

            else:

                weekday["day_number"] = (
                    weekday["date"]
                    .dt.dayofweek
                )

                weekday["day"] = (
                    weekday["date"]
                    .dt.day_name()
                )

                weekday_counts = (
                    weekday.groupby(
                        [
                            "day_number",
                            "day",
                        ],
                        as_index=False,
                    )
                    .size()
                    .rename(
                        columns={
                            "size": "rides"
                        }
                    )
                    .sort_values(
                        "day_number"
                    )
                )

                order = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]

                fig = px.bar(
                    weekday_counts,
                    x="day",
                    y="rides",
                )

                fig.update_traces(
                    marker_color="#FFD21F"
                )

                fig.update_layout(
                    xaxis_title="Day",
                    yaxis_title="Ride Count",
                    xaxis=dict(
                        categoryorder="array",
                        categoryarray=order,
                    ),
                )

                show_chart(
                    apply_theme(fig, 350),
                    "demand_weekday",
                )


        # ------------------------------
        # Service / Hour
        # ------------------------------

        chart_title(
            "Demand by Service and Hour"
        )

        heat = filtered.dropna(
            subset=[
                "_hour",
                "services",
            ]
        ).copy()

        if heat.empty:
            show_empty()

        else:

            heat["hour"] = (
                pd.to_numeric(
                    heat["_hour"],
                    errors="coerce",
                )
                .round()
                .astype(int)
                .clip(0, 23)
            )

            heat_data = (
                heat.groupby(
                    [
                        "services",
                        "hour",
                    ],
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
            )

            fig = px.density_heatmap(
                heat_data,
                x="hour",
                y="services",
                z="rides",
                color_continuous_scale=[
                    "#181818",
                    "#6D5B00",
                    "#FFD21F",
                ],
            )

            fig.update_layout(
                xaxis_title="Hour",
                yaxis_title="Service",
            )

            show_chart(
                apply_theme(fig, 390),
                "demand_heatmap",
            )


        # ------------------------------
        # Monthly Volume
        # ------------------------------

        chart_title(
            "Monthly Ride Volume"
        )

        monthly = filtered.dropna(
            subset=["date"]
        ).copy()

        if monthly.empty:
            show_empty()

        else:

            monthly["month"] = (
                monthly["date"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_counts = (
                monthly.groupby(
                    "month",
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
            )

            fig = px.bar(
                monthly_counts,
                x="month",
                y="rides",
            )

            fig.update_traces(
                marker_color="#FFD21F"
            )

            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Ride Count",
            )

            show_chart(
                apply_theme(fig, 350),
                "demand_monthly",
            )


# ============================================================
# 14. REVENUE
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

        completed = completed_only(
            filtered
        )

        if completed.empty:
            st.markdown(
                """
                <div class="empty-state">
                    No completed rides available for revenue analysis
                    under the selected filters.
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            col1, col2 = st.columns(
                [1.5, 1],
                gap="medium",
            )

            # --------------------------
            # Daily Revenue
            # --------------------------

            with col1:

                chart_title(
                    "Daily Revenue Trend"
                )

                revenue = daily_revenue(
                    filtered
                )

                if revenue.empty:
                    show_empty()

                else:

                    fig = px.area(
                        revenue,
                        x="date",
                        y="revenue",
                    )

                    fig.update_traces(
                        line=dict(
                            color="#FFD21F",
                            width=2.5,
                        ),
                        fillcolor=(
                            "rgba(255,210,31,0.10)"
                        ),
                        hovertemplate=(
                            "Date: %{x|%d %b %Y}"
                            "<br>Revenue: ₹%{y:,.0f}"
                            "<extra></extra>"
                        ),
                    )

                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Revenue",
                    )

                    show_chart(
                        apply_theme(fig, 350),
                        "revenue_daily",
                    )

            # --------------------------
            # Payment Method
            # --------------------------

            with col2:

                chart_title(
                    "Revenue by Payment Method"
                )

                payment = (
                    completed
                    .dropna(
                        subset=["total_fare"]
                    )
                    .copy()
                )

                payment["payment"] = (
                    payment[
                        "payment_method"
                    ].fillna("Unknown")
                )

                payment_revenue = (
                    payment.groupby(
                        "payment",
                        as_index=False,
                    )["total_fare"]
                    .sum()
                    .rename(
                        columns={
                            "total_fare":
                            "revenue"
                        }
                    )
                    .sort_values(
                        "revenue",
                        ascending=False,
                    )
                )

                if payment_revenue.empty:
                    show_empty()

                else:

                    fig = px.bar(
                        payment_revenue,
                        x="revenue",
                        y="payment",
                        orientation="h",
                    )

                    fig.update_traces(
                        marker_color="#FFD21F"
                    )

                    fig.update_layout(
                        xaxis_title="Revenue",
                        yaxis_title="Payment Method",
                    )

                    show_chart(
                        apply_theme(fig, 350),
                        "revenue_payment",
                    )


            col3, col4 = st.columns(
                2,
                gap="medium",
            )

            # --------------------------
            # Average Fare
            # --------------------------

            with col3:

                chart_title(
                    "Average Fare by Service"
                )

                fare_service = (
                    completed
                    .dropna(
                        subset=["total_fare"]
                    )
                    .copy()
                )

                fare_service["service"] = (
                    fare_service[
                        "services"
                    ].fillna("Unknown")
                )

                fare_service = (
                    fare_service.groupby(
                        "service",
                        as_index=False,
                    )["total_fare"]
                    .mean()
                    .rename(
                        columns={
                            "total_fare":
                            "average_fare"
                        }
                    )
                    .sort_values(
                        "average_fare",
                        ascending=True,
                    )
                )

                if fare_service.empty:
                    show_empty()

                else:

                    fig = px.bar(
                        fare_service,
                        x="average_fare",
                        y="service",
                        orientation="h",
                    )

                    fig.update_traces(
                        marker_color="#FFD21F"
                    )

                    fig.update_layout(
                        xaxis_title="Average Fare",
                        yaxis_title="Service",
                    )

                    show_chart(
                        apply_theme(fig, 350),
                        "revenue_average_fare",
                    )

            # --------------------------
            # Fare Distribution
            # --------------------------

            with col4:

                chart_title(
                    "Fare Distribution"
                )

                fares = (
                    completed[
                        "total_fare"
                    ]
                    .dropna()
                )

                if fares.empty:
                    show_empty()

                else:

                    fig = go.Figure()

                    fig.add_trace(
                        go.Histogram(
                            x=fares,
                            nbinsx=30,
                            marker=dict(
                                color="#FFD21F",
                                line=dict(
                                    color="#111111",
                                    width=0.5,
                                ),
                            ),
                        )
                    )

                    fig.update_layout(
                        xaxis_title="Fare",
                        yaxis_title="Ride Count",
                    )

                    show_chart(
                        apply_theme(fig, 350),
                        "revenue_distribution",
                    )


# ============================================================
# 15. OPERATIONS
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

        col1, col2 = st.columns(
            [1.25, 1],
            gap="medium",
        )

        # ------------------------------
        # Status by Service
        # ------------------------------

        with col1:

            chart_title(
                "Ride Status by Service"
            )

            status_service = (
                filtered.assign(
                    service=filtered[
                        "services"
                    ].fillna("Unknown"),
                    status=filtered[
                        "_status_clean"
                    ],
                )
                .groupby(
                    [
                        "service",
                        "status",
                    ],
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
            )

            if status_service.empty:
                show_empty()

            else:

                fig = px.bar(
                    status_service,
                    x="service",
                    y="rides",
                    color="status",
                    barmode="stack",
                    color_discrete_map={
                        "Completed": "#FFD21F",
                        "Cancelled": "#444444",
                    },
                )

                for trace in fig.data:
                    if trace.name not in {
                        "Completed",
                        "Cancelled",
                    }:
                        trace.marker.color = "#777777"

                fig.update_layout(
                    xaxis_title="Service",
                    yaxis_title="Ride Count",
                )

                show_chart(
                    apply_theme(fig, 370),
                    "operations_status",
                )


        # ------------------------------
        # Duration
        # ------------------------------

        with col2:

            chart_title(
                "Trip Duration Distribution"
            )

            durations = pd.to_numeric(
                filtered["duration"],
                errors="coerce",
            ).dropna()

            durations = durations[
                np.isfinite(durations)
            ]

            if durations.empty:
                show_empty()

            else:

                fig = go.Figure()

                fig.add_trace(
                    go.Histogram(
                        x=durations,
                        nbinsx=30,
                        marker=dict(
                            color="#FFD21F",
                            line=dict(
                                color="#111111",
                                width=0.5,
                            ),
                        ),
                    )
                )

                fig.update_layout(
                    xaxis_title="Duration",
                    yaxis_title="Ride Count",
                )

                show_chart(
                    apply_theme(fig, 370),
                    "operations_duration",
                )


        col3, col4 = st.columns(
            2,
            gap="medium",
        )

        # ------------------------------
        # Completion by Service
        # ------------------------------

        with col3:

            chart_title(
                "Completion Rate by Service"
            )

            service_stats = (
                filtered.assign(
                    service=filtered[
                        "services"
                    ].fillna("Unknown")
                )
                .groupby("service")
                .agg(
                    total=(
                        "ride_id",
                        "size",
                    ),
                    completed=(
                        "_is_completed",
                        "sum",
                    ),
                )
                .reset_index()
            )

            if service_stats.empty:
                show_empty()

            else:

                service_stats[
                    "completion_rate"
                ] = (
                    service_stats["completed"]
                    / service_stats["total"]
                    .replace(0, np.nan)
                    * 100
                ).fillna(0)

                service_stats = (
                    service_stats
                    .sort_values(
                        "completion_rate"
                    )
                )

                fig = px.bar(
                    service_stats,
                    x="completion_rate",
                    y="service",
                    orientation="h",
                )

                fig.update_traces(
                    marker_color="#FFD21F"
                )

                fig.update_layout(
                    xaxis_title="Completion Rate (%)",
                    yaxis_title="Service",
                    xaxis=dict(
                        range=[0, 100]
                    ),
                )

                show_chart(
                    apply_theme(fig, 370),
                    "operations_completion",
                )


        # ------------------------------
        # Cancellation by Hour
        # ------------------------------

        with col4:

            chart_title(
                "Cancellation Rate by Hour"
            )

            hour_data = filtered.dropna(
                subset=["_hour"]
            ).copy()

            if hour_data.empty:
                show_empty()

            else:

                hour_data["hour"] = (
                    pd.to_numeric(
                        hour_data["_hour"],
                        errors="coerce",
                    )
                    .round()
                    .astype(int)
                    .clip(0, 23)
                )

                stats = (
                    hour_data.groupby("hour")
                    .agg(
                        total=(
                            "ride_id",
                            "size",
                        ),
                        cancelled=(
                            "_is_cancelled",
                            "sum",
                        ),
                    )
                    .reset_index()
                )

                stats[
                    "cancellation_rate"
                ] = (
                    stats["cancelled"]
                    / stats["total"]
                    .replace(0, np.nan)
                    * 100
                ).fillna(0)

                fig = px.line(
                    stats,
                    x="hour",
                    y="cancellation_rate",
                    markers=True,
                )

                fig.update_traces(
                    line=dict(
                        color="#FFD21F",
                        width=3,
                    ),
                    marker=dict(
                        color="#FFD21F",
                        size=7,
                    ),
                )

                fig.update_layout(
                    xaxis_title="Hour",
                    yaxis_title="Cancellation Rate (%)",
                    xaxis=dict(
                        tickmode="linear",
                        tick0=0,
                        dtick=2,
                    ),
                )

                show_chart(
                    apply_theme(fig, 370),
                    "operations_cancellation",
                )


# ============================================================
# 16. LOCATIONS
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

        col1, col2 = st.columns(
            2,
            gap="medium",
        )

        # ------------------------------
        # Pickup
        # ------------------------------

        with col1:

            chart_title(
                "Top Pickup Locations"
            )

            pickup = (
                filtered.assign(
                    location=filtered[
                        "source"
                    ].fillna("Unknown")
                )
                .groupby(
                    "location",
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
                .sort_values(
                    "rides",
                    ascending=False,
                )
                .head(10)
                .sort_values(
                    "rides",
                    ascending=True,
                )
            )

            if pickup.empty:
                show_empty()

            else:

                fig = px.bar(
                    pickup,
                    x="rides",
                    y="location",
                    orientation="h",
                )

                fig.update_traces(
                    marker_color="#FFD21F"
                )

                fig.update_layout(
                    xaxis_title="Ride Count",
                    yaxis_title="Pickup Location",
                )

                show_chart(
                    apply_theme(fig, 390),
                    "locations_pickup",
                )


        # ------------------------------
        # Destination
        # ------------------------------

        with col2:

            chart_title(
                "Top Destination Locations"
            )

            destination = (
                filtered.assign(
                    location=filtered[
                        "destination"
                    ].fillna("Unknown")
                )
                .groupby(
                    "location",
                    as_index=False,
                )
                .size()
                .rename(
                    columns={
                        "size": "rides"
                    }
                )
                .sort_values(
                    "rides",
                    ascending=False,
                )
                .head(10)
                .sort_values(
                    "rides",
                    ascending=True,
                )
            )

            if destination.empty:
                show_empty()

            else:

                fig = px.bar(
                    destination,
                    x="rides",
                    y="location",
                    orientation="h",
                )

                fig.update_traces(
                    marker_color="#FFD21F"
                )

                fig.update_layout(
                    xaxis_title="Ride Count",
                    yaxis_title="Destination",
                )

                show_chart(
                    apply_theme(fig, 390),
                    "locations_destination",
                )


        # ------------------------------
        # Routes
        # ------------------------------

        chart_title(
            "Top Routes"
        )

        routes = filtered.copy()

        routes["source_clean"] = (
            routes["source"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        routes["destination_clean"] = (
            routes["destination"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        routes["route"] = (
            routes["source_clean"]
            + " → "
            + routes["destination_clean"]
        )

        route_counts = (
            routes.groupby(
                "route",
                as_index=False,
            )
            .size()
            .rename(
                columns={
                    "size": "rides"
                }
            )
            .sort_values(
                "rides",
                ascending=False,
            )
            .head(15)
            .sort_values(
                "rides",
                ascending=True,
            )
        )

        if route_counts.empty:
            show_empty()

        else:

            fig = px.bar(
                route_counts,
                x="rides",
                y="route",
                orientation="h",
            )

            fig.update_traces(
                marker_color="#FFD21F"
            )

            fig.update_layout(
                xaxis_title="Ride Count",
                yaxis_title="Route",
            )

            show_chart(
                apply_theme(fig, 470),
                "locations_routes",
            )


# ============================================================
# 17. RIDE EXPLORER
# ============================================================

st.markdown(
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

chart_title(
    "Ride Explorer"
)

if filtered.empty:

    show_empty()

else:

    explorer_columns = [
        "ride_id",
        "services",
        "date",
        "time",
        "ride_status",
        "source",
        "destination",
        "duration",
        "distance",
        "total_fare",
        "payment_method",
    ]

    explorer = filtered[
        explorer_columns
    ].copy()

    explorer = explorer.sort_values(
        "date",
        ascending=False,
        na_position="last",
    ).head(100)

    explorer["date"] = (
        explorer["date"]
        .dt.strftime("%Y-%m-%d")
        .fillna("")
    )

    st.dataframe(
        explorer,
        use_container_width=True,
        hide_index=True,
        height=min(
            520,
            80 + len(explorer) * 35,
        ),
        column_config={
            "ride_id": st.column_config.TextColumn(
                "Ride ID"
            ),
            "services": st.column_config.TextColumn(
                "Service"
            ),
            "date": st.column_config.TextColumn(
                "Date"
            ),
            "time": st.column_config.TextColumn(
                "Time"
            ),
            "ride_status": st.column_config.TextColumn(
                "Ride Status"
            ),
            "source": st.column_config.TextColumn(
                "Source"
            ),
            "destination": st.column_config.TextColumn(
                "Destination"
            ),
            "duration": st.column_config.NumberColumn(
                "Duration",
                format="%.2f",
            ),
            "distance": st.column_config.NumberColumn(
                "Distance",
                format="%.2f",
            ),
            "total_fare": st.column_config.NumberColumn(
                "Total Fare",
                format="₹%.2f",
            ),
            "payment_method": st.column_config.TextColumn(
                "Payment Method"
            ),
        },
    )

    st.caption(
        f"Showing up to 100 filtered rides • "
        f"{format_number(len(filtered))} rides match the current filters."
    )
