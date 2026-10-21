
# 🟡 Rapido Ride Intelligence

**A business-focused mobility analytics dashboard that transforms ride-level data into interactive demand, revenue, operational and location insights.**



![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)




![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)




![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)




![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)




![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-FFD21F?style=flat&logo=streamlit&logoColor=black)

](https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/)

## 🚀 Live Dashboard

**[Open Rapido Ride Intelligence →](https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/)**

```
https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/
```

No installation is needed. The dashboard runs in the browser.

---

## Quick Facts

| | |
|---|---|
| **Data** | 50,000 ride records · 13 columns · 17 Jun 2024 – 16 Aug 2024 |
| **Services covered** | bike, auto, cab economy, parcel, bike lite |
| **Dashboard pages** | Overview · Demand · Revenue · Operations · Locations · Data Quality · Ride Explorer |
| **Global filters** | Service · Ride Status · Payment Method · Analysis Period |
| **Stack** | Python · Pandas · NumPy · Plotly · Streamlit |
| **Deployment** | Streamlit Community Cloud |

---

## Project Overview

Rapido Ride Intelligence is an interactive Streamlit application that analyzes a ride-level CSV dataset (`rides_data.csv`). Each row is a single ride with its service type, date, time, status, pickup, destination, duration, distance, fare components and payment method.

The app turns those records into a seven-page dashboard covering demand, revenue, operations, locations, data quality and individual ride lookup. All pages share one set of global filters, so every KPI and chart reflects the same filtered dataset.

Interactive analytics fits this kind of data well. A static report gives one view, while a ride-hailing dataset raises many follow-up questions, such as how demand differs by service, how cancellations vary by hour, or how a payment method contributes to revenue. The filters and charts let a user answer these without rewriting any code.

## Business Objective

The dashboard is built to answer questions such as:

- When is ride demand highest?
- Which services generate the most rides?
- What is the completion rate?
- Where are cancellations concentrated (by service and by hour)?
- How does revenue change over time?
- Which payment methods contribute the most revenue?
- Which services perform better operationally?
- Which pickup and destination locations are busiest?
- Which routes occur most frequently?
- Are there potential data-quality issues?
- Can individual rides be investigated?

---

## Dashboard Overview

Navigation is a horizontal radio control at the top of the page (the Streamlit sidebar is hidden). Five KPI cards sit below the filters on every page.

### Overview
**Purpose:** An executive summary of ride performance.

- **KPIs:** Total Rides, Total Revenue, Completion Rate, Cancellations, Average Fare
- **Charts:** Ride Demand by Hour (line), Ride Outcome Mix (donut), Service Volume (bar), Daily Ride Trend (area)
- **Business Insights:** Peak Demand Hour, Leading Service, Completion Rate, Cancellation Rate

**Why it matters:** It gives a quick read on overall health before drilling into a specific area.

### Demand
**Purpose:** Show when and where demand occurs.

- Ride Demand by Hour
- Rides by Day of Week
- Demand by Service and Hour (heatmap)
- Monthly Ride Volume

**Why it matters:** Peak hours, busy weekdays and service-specific demand patterns support staffing and capacity decisions.

### Revenue
**Purpose:** Fare and revenue analysis. **Revenue pages use completed rides only.**

- Daily Revenue Trend
- Revenue by Payment Method
- Average Fare by Service
- Fare Distribution (histogram)

**Why it matters:** It shows where money comes from and how fares differ across services and payment methods.

### Operations
**Purpose:** Ride outcomes and service-level performance.

- Ride Status by Service (stacked bar)
- Trip Duration Distribution
- Completion Rate by Service
- Cancellation Rate by Hour

**Why it matters:** It shows which services complete more rides and which hours see more cancellations.

### Locations
**Purpose:** Where rides start, end and repeat.

- Top Pickup Locations (top 10)
- Top Destination Locations (top 10)
- Top Routes (top 15, shown as `Source → Destination`)

**Why it matters:** Concentrated pickup areas and recurring routes show where demand clusters. No external mapping data is used.

### Data Quality
**Purpose:** A set of audit checks on the filtered data (see [Data Quality Methodology](#data-quality-methodology)).

- **KPIs:** Fare vs Distance, High-Speed Trips, Missing Fares, Repeated Routes
- **Charts:** Fare vs Distance scatter plot, Average Fare by Distance Band

### Ride Explorer
**Purpose:** Move from aggregates to individual records.

- One search box that matches against **Ride ID, Source or Destination** (case-insensitive, partial match)
- Ride-level table with ride ID, service, date, time, status, source, destination, duration, distance, total fare and payment method
- Respects all global filters
- Sorted by date (newest first) and capped at **100 rows**

---

## Key Metrics & Calculations

```
Total Rides       = number of rows remaining after the global filters

Completion Rate   = Completed Rides / Total Rides × 100

Cancellation Rate = Cancelled Rides / Total Rides × 100

Total Revenue     = sum of total_fare for completed rides

Average Fare      = mean of total_fare for completed rides with a valid total_fare

Implied Speed     = distance / (duration / 60)        # duration treated as minutes

Fare-Distance Correlation = Pearson correlation between distance and total_fare
                            (completed rides with distance > 0 and duration > 0)
```

If a denominator is zero, rates are returned as 0 instead of raising an error.

---

## Global Filtering

Four filters sit at the top of every page. They are applied once, and every KPI and chart is built from the resulting filtered DataFrame.

| Filter | Behavior |
|---|---|
| **Service** | Multi-select, all services selected by default |
| **Ride Status** | Multi-select, all statuses selected by default |
| **Payment Method** | Multi-select with an **All Payment Methods** option (default) |
| **Analysis Period** | Date range between the earliest and latest valid dates in the data |

**Payment method handling:** Cancelled rides have a blank payment method. When *All Payment Methods* is selected, the payment filter is skipped entirely, so those rides stay in the dataset. Choosing a specific payment method excludes rides with no payment value.

If a filter leaves no records, pages show an empty-state message instead of failing.

---

## Data Preprocessing

All cleaning happens in a single cached loader (`load_data`, decorated with `st.cache_data`).

- **CSV loading** from `rides_data.csv`, located relative to the script file
- **Expected-column handling:** any of the 13 expected columns missing from the CSV is created as empty, and columns are reordered to a fixed schema
- **Date conversion** with `pd.to_datetime(errors="coerce")`
- **Hour extraction** from `time` (stored as timestamp-style text such as `08:30:40.542646`), using three fallbacks: parsed time, a numeric hour (0–23), then a regex for `HH` or `HH:MM`
- **Numeric conversion** of `duration`, `distance`, `ride_charge`, `misc_charge`, `total_fare` (invalid values become `NaN`)
- **Text cleaning:** whitespace stripped from `services`, `ride_status`, `source`, `destination`, `ride_id`, `payment_method`
- **Status flags:** case-insensitive `_is_completed` and `_is_cancelled`, plus a cleaned status label where blank values become `Unknown`
- **Missing values:** missing text labels are shown as `Unknown` in charts; missing numeric values are excluded from the relevant calculation rather than treated as zero

---

## Dataset

The app reads `rides_data.csv`: **50,000 ride records across 13 columns**, covering **17 June 2024 to 16 August 2024**.

| Column | Description |
|---|---|
| `services` | Service type: bike, auto, cab economy, parcel, bike lite |
| `date` | Ride date |
| `time` | Ride time (used to derive the hour) |
| `ride_status` | Ride outcome: `completed` or `cancelled` |
| `source` | Pickup location |
| `destination` | Drop location |
| `duration` | Trip duration, numeric (10 to 119 in this dataset) |
| `ride_id` | Ride identifier |
| `distance` | Trip distance, numeric (1 to 50 in this dataset) |
| `ride_charge` | Base ride charge |
| `misc_charge` | Additional charges |
| `total_fare` | Total fare, shown in ₹ by the dashboard |
| `payment_method` | Paytm, GPay, Amazon Pay or QR scan |

**Composition**

| Field | Breakdown |
|---|---|
| Ride status | 44,964 completed · 5,036 cancelled |
| Services | bike 15,128 · auto 12,327 · cab economy 10,202 · parcel 7,459 · bike lite 4,884 |
| Payment method | Paytm 11,315 · GPay 11,268 · Amazon Pay 11,225 · QR scan 11,156 · blank 5,036 |

`ride_charge`, `misc_charge`, `total_fare` and `payment_method` are blank for 5,036 rides, the same number as cancelled rides. This is why revenue and average fare use completed rides only, and why the Payment Method filter has an *All Payment Methods* option. With default filters, the Missing Fares check on the Data Quality page shows 5,036 for the same reason.

---

## Data Quality Methodology

The Data Quality page helps a reviewer judge how reliable the data is before drawing conclusions. The Fare vs Distance, High-Speed Trips and distance-band checks run on **completed rides with distance > 0 and duration > 0**. Missing Fares and Repeated Routes use the full filtered dataset.

| Check | How it works | Why it is useful |
|---|---|---|
| **Fare vs Distance** | Pearson correlation of `distance` and `total_fare`, plus a scatter plot (random sample of up to 3,000 rides) | Fares in a ride-hailing dataset are normally expected to rise with distance. A weak relationship is worth a closer look. |
| **High-Speed Trips** | Share of rides whose implied speed (`distance / (duration / 60)`) exceeds **80 km/h** | Very high implied speeds can point to distance or duration values that need checking. |
| **Missing Fares** | Count of filtered records with no `total_fare` | Missing fares reduce revenue coverage and affect fare averages. In this dataset they coincide with cancelled rides. |
| **Repeated Routes** | Count of distinct source–destination pairs that appear more than once | Shows recurring ride patterns in the data. |
| **Average Fare by Distance Band** | Mean fare across bands: 0–10, 10–20, 20–30, 30–40, 40–50, 50+ | Shows whether average fare increases steadily with distance. |

> **Important:** These are analytical signals. They do not prove that any individual record is incorrect, fraudulent or synthetic, and the dashboard presents them that way.

---

## Technical Architecture

```
CSV Dataset (rides_data.csv)
        ↓
Data Loading (cached)
        ↓
Data Cleaning / Transformation
        ↓
Global Filters (service, status, payment, period)
        ↓
KPI Calculations
        ↓
Analytical Modules (Demand, Revenue, Operations, Locations, Data Quality, Explorer)
        ↓
Plotly Visualizations
        ↓
Streamlit Interface
```

The whole app lives in one Python file. Shared helpers handle formatting, KPI cards, chart theming and empty states, so the pages stay consistent.

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and analytics logic |
| **Pandas** | Data loading, cleaning, filtering, grouping and aggregation |
| **NumPy** | Numerical operations (NaN handling, distance bins) |
| **Plotly** (Express and Graph Objects) | Interactive charts |
| **Streamlit** | Dashboard UI, filters, navigation, caching and deployment |

## Project Structure

```
rapido-ride-intelligence/
├── .devcontainer/                 # Dev container configuration
├── rapido_ride_intelligence.py    # Streamlit application (all pages and logic)
├── rides_data.csv                 # Ride-level dataset (50,000 rows)
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Local Setup

```bash
git clone https://github.com/jahnavi06in/rapido-ride-intelligence.git
cd rapido-ride-intelligence
pip install -r requirements.txt
streamlit run rapido_ride_intelligence.py
```

Streamlit will open the app in your browser, usually at `http://localhost:8501`.

## Live Deployment

- **Live Dashboard:** https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/
- **GitHub:** https://github.com/jahnavi06in/rapido-ride-intelligence

The dashboard is hosted on Streamlit Community Cloud.

---

## Business Value

The same structure could support the following in a ride-hailing context:

- **Demand planning:** peak hours, busy weekdays and monthly volume
- **Revenue monitoring:** daily revenue, payment-method contribution and fare distribution
- **Service performance:** completion rates and average fares across services
- **Cancellation monitoring:** cancellations by service and by hour
- **Location and route analysis:** busiest pickups, destinations and repeated routes
- **Operational investigation:** ride-level search to inspect individual records
- **Data-quality monitoring:** checks on fare, distance, speed and missing values

## Skills Demonstrated

**Data Analytics**
- Data cleaning and type conversion
- Exploratory data analysis
- KPI development
- Aggregation and segmentation (by service, status, hour, location, payment method)
- Trend analysis
- Correlation analysis
- Data-quality analysis

**Python**
- Pandas (`groupby`, `agg`, `pd.cut`, datetime and string handling)
- NumPy
- Reusable helper functions
- Cached data loading and defensive handling of empty or invalid data

**Visualization**
- Plotly interactive charts
- Time-series charts
- Heatmaps
- Distribution analysis (histograms)
- Scatter plots
- KPI card design and a custom dark theme

**Business Intelligence**
- KPI design
- Revenue and demand analysis
- Operational reporting
- Service comparison
- Business-focused dashboard design

**Application Development**
- Streamlit
- Global interactive filters
- Search functionality
- Multi-page dashboard navigation
- Cloud deployment

## Key Project Highlights

- End-to-end ride-level analytics dashboard on a 50,000-record dataset
- Seven-page interactive Streamlit application
- Centralized filtering shared by every KPI and chart
- Executive KPI layer with computed business insights
- Demand, revenue, operations and location analysis
- Data-quality audit with explicit, documented thresholds
- Ride-level search and exploration
- Live cloud deployment

---

## Project Limitations / Scope

- This is a **portfolio and analytical project**. The dataset should not be read as Rapido's internal or production data, and the project is not affiliated with Rapido.
- The data-quality checks identify **signals**, not confirmed errors. The 80 km/h speed threshold is a fixed heuristic, and it assumes `duration` is in minutes.
- The dashboard is **analytical and descriptive**. It does not forecast, use machine learning, or process live data, and it is not a ride-dispatch system.
- Analysis is limited to what the CSV contains: a two-month window, with no map visualization and no driver or customer information.

---

## Author

**Jahnavi J**
BCA Student | Data Analytics | Business Intelligence

Skills: Python · SQL · Power BI · Tableau · Excel · Data Analytics

## Links

- **GitHub Repository:** https://github.com/jahnavi06in/rapido-ride-intelligence
- **Live Dashboard:** https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/
```` Ride Intelligence

A production-style Streamlit mobility analytics dashboard for ride demand, revenue, operations, locations and data-quality investigation.

## Business Questions

- When is ride demand highest?
- Which services and locations drive volume?
- How much revenue comes from completed rides?
- Where are cancellations concentrated?
- What does the fare and distance relationship look like?
- Can the dataset be trusted for business decisions?
- Which individual rides require investigation?

## Dashboard

1. Overview
2. Demand
3. Revenue
4. Operations
5. Locations
6. Data Quality
7. Ride Explorer

## Tech Stack

Python • Pandas • NumPy • Plotly • Streamlit

## Data

The dashboard expects `rides_data.csv` in the same directory as `rapido_ride_intelligence.py`.

The application validates the expected schema and converts dates, times and numeric fields before analysis.

## Important Metric Definitions

- Total Rides: rides remaining after the selected filters.
- Completion Rate: completed rides / total filtered rides.
- Cancellation Rate: cancelled rides / total filtered rides.
- Revenue: sum of `total_fare` for completed rides only.
- Average Fare: mean `total_fare` for completed rides only.

## Data Quality

The Data Quality page is an audit layer, not a claim that the source is invalid. It flags unusual relationships and implausible operational values that should be investigated before using the dataset for pricing or forecasting decisions.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run rapido_ride_intelligence.py
```

## Project Structure

```text
rapido-ride-intelligence/
├── rapido_ride_intelligence.py
├── rides_data.csv
├── requirements.txt
├── findings.py
├── queries.sql
├── run_sql.py
└── README.md
```
