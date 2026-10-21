# Rapido Ride Intelligence

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
