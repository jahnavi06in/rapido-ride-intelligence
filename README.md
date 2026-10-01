# Rapido Ride Intelligence

A professional **Streamlit-based ride analytics dashboard** for analyzing ride demand, revenue, operations, and location performance using the `rides_data.csv` dataset.

## Dashboard Preview

### Executive Overview

Rapido Ride Intelligence provides an interactive view of ride demand, revenue, operational performance, and location analytics.

The dashboard combines KPI cards, interactive filters, and Plotly visualizations to help explore:

- Ride demand by hour and date
- Completed-ride revenue
- Completion and cancellation rates
- Service performance
- Payment-method revenue
- Trip duration and distance
- Pickup and destination locations
- Frequently used routes

Users can filter the dashboard by service, ride status, payment method, and analysis period.
## Live Dashboard

🚀 **[Open Rapido Ride Intelligence Dashboard](https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/)**

Explore the interactive dashboard for ride demand, revenue, operations, and location analytics.

## Features

### Overview

* Total Rides
* Total Revenue
* Completion Rate
* Cancellations
* Average Fare
* Ride Demand by Hour
* Ride Outcome Mix
* Service Volume
* Daily Ride Trend
* Business Insights

### Demand Analytics

* Ride Demand by Hour
* Rides by Day of Week
* Demand by Service and Hour
* Monthly Ride Volume

### Revenue Analytics

* Daily Revenue Trend
* Revenue by Payment Method
* Average Fare by Service
* Fare Distribution

> Revenue calculations use **completed rides only**. Missing fares from cancelled rides are not treated as revenue.

### Operations Analytics

* Ride Status by Service
* Trip Duration Distribution
* Completion Rate by Service
* Cancellation Rate by Hour

### Location Analytics

* Top Pickup Locations
* Top Destination Locations
* Top Routes
* Route analysis using `Source → Destination`

### Ride Explorer

* Interactive filtered ride table
* Displays up to 100 records
* Sorts rides by date where available

## Interactive Filters

The dashboard includes global filters for:

* Service
* Ride Status
* Payment Method
* Analysis Period

All filters dynamically affect the KPIs, charts, insights, and Ride Explorer.

## Dataset

The application uses:

```text
rides_data.csv
```

Expected columns:

```text
services
date
time
ride_status
source
destination
duration
ride_id
distance
ride_charge
misc_charge
total_fare
payment_method
```

The application safely handles:

* Missing values
* Invalid numeric values
* Invalid dates
* Missing cancelled-ride fares
* Empty filter results

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

## Project Structure

```text
Rapido Ride Intelligence/
│
├── rapido_ride_intelligence.py
├── rides_data.csv
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Start the Streamlit application:

```bash
python -m streamlit run rapido_ride_intelligence.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

## Requirements

The project dependencies are listed in `requirements.txt`:

```text
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
```

## Data Handling

The application converts the following fields into appropriate formats:

* `date` → datetime
* `time` → hour/time information
* `duration` → numeric
* `distance` → numeric
* `ride_charge` → numeric
* `misc_charge` → numeric
* `total_fare` → numeric

Cancelled rides with missing fare values are retained as rides but are **excluded from revenue and average-fare calculations**.

## Dashboard Design

The interface uses:

* Dark black background
* Dark analytics cards
* Rapido-inspired yellow accent
* Interactive Streamlit navigation
* Plotly visualizations
* Responsive column layouts
* No sidebar
* Minimal animations
* Professional analytics-focused design

## Navigation

The dashboard contains five interactive sections:

```text
Overview
Demand
Revenue
Operations
Locations
```

Navigation is implemented using Streamlit controls rather than static HTML navigation.

## Business Use Cases

This dashboard can be used to analyze:

* Ride demand patterns
* Peak operating hours
* Service utilization
* Revenue performance
* Payment-method contribution
* Completion and cancellation rates
* Trip duration
* Pickup and destination concentration
* Frequently used routes

## Notes

For privacy and repository security, avoid committing sensitive or production ride-level data to a public GitHub repository.

The dashboard is designed to work directly with the provided `rides_data.csv` structure without requiring additional geographic or external data sources.

