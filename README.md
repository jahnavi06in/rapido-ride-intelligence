🚖 Rapido Ride Intelligence

End-to-end ride-hailing analytics: interactive dashboard, revenue-leakage estimation, statistical testing, SQL analysis, and data-quality auditing across 50,000 rides.

"Python" "SQL" "Pandas" "NumPy" "SciPy" "Plotly" "Streamlit"

🔗 "Live Dashboard" (https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/)

---

📸 Dashboard Preview

Overview

"Overview" (overview.png)

Operations

"Operations" (operations.png)

---

📌 1. Business Problem

A ride-hailing operator earns revenue when a booked ride is completed. Cancellations can create revenue leakage, operational inefficiency, and a poorer rider experience.

This project answers:

1. How much revenue could cancellations represent as an estimated leakage opportunity?
2. Is cancellation concentrated in a service, hour, or weekday?
3. Are pricing and trip measurements internally consistent?
4. Can the dataset be trusted for business analysis?
5. What operational decisions can be supported by the available data?

---

🎯 2. Project Objectives

- Analyse ride-demand patterns by hour, day, and month
- Measure revenue from completed rides
- Evaluate completion and cancellation performance
- Compare service-level performance
- Analyse payment-method contribution
- Understand trip duration and distance patterns
- Identify high-demand pickup, destination, and route patterns
- Estimate revenue leakage associated with cancellations
- Perform data-quality and validity checks
- Validate analytical results using SQL
- Deliver the analysis through an interactive business-intelligence dashboard

---

🧩 3. Solution Overview

Layer| What I built| Business purpose
KPI Layer| Revenue, completion rate, average fare, cancellations, with filters| Provides a consistent performance view
Leakage Model| Cancelled rides × average completed fare| Estimates the revenue opportunity associated with cancellations
Driver Analysis| Chi-square tests across service, hour, and weekday| Tests whether cancellation patterns differ meaningfully
Data-Quality Audit| Fare-distance correlation, speed checks, route uniqueness| Identifies potential data or measurement issues
SQL Layer| Six analytical queries| Cross-checks key Python calculations
Dashboard| Six-page Streamlit application with global filters| Enables interactive business exploration

---

🔎 4. Key Findings

#| Finding| Evidence
1| Cancellations represent an estimated ₹2.76M revenue opportunity.| 5,036 cancelled rides × ₹547 average completed fare
2| Cancellation rates do not show statistically significant differences across service, hour, or weekday.| Chi-square p-values: service 0.31, hour 0.80, weekday 0.72
3| Fare has almost no linear relationship with distance in this dataset.| Pearson correlation = −0.005
4| 4,415 completed rides imply speeds above 80 km/h.| Maximum implied speed = 300 km/h
5| Daily demand is relatively stable after normalising partial months.| Jun: 806/day, Jul: 824/day, Aug: 823/day
6| Route repetition is extremely low.| 49,993 unique routes across 50,000 rides

Headline Metrics

- 50,000 total rides
- 44,964 completed rides
- 5,036 cancelled rides
- 89.9% completion rate
- 10.1% cancellation rate
- ₹24.6M completed-ride revenue
- ₹547 average completed fare
- Dataset period: 17 Jun – 16 Aug 2024
- Five services: Bike, Auto, Cab Economy, Parcel, Bike Lite

---

💡 5. Business Decisions Supported

1. Prioritise cancellation reduction

A 1-percentage-point reduction in cancellations corresponds to approximately ₹274K of estimated revenue opportunity over this dataset window, based on 500 rides × ₹547 average completed fare.

This is a sensitivity estimate, not a forecast.

2. Use platform-wide interventions

The statistical tests do not show meaningful cancellation differences by service, hour, or weekday. Therefore, the available data does not justify targeting only one segment.

3. Validate pricing data before modelling

The near-zero fare-distance correlation suggests that pricing relationships should be investigated before using this dataset for pricing or demand modelling.

4. Capture cancellation reasons

The current dataset does not contain cancellation reason, cancelling party, or driver-side information. Adding these fields would make cancellation diagnosis much stronger.

---

📊 6. Dashboard Pages

Overview

Executive KPIs including:

- Total rides
- Completed rides
- Cancellation rate
- Completion rate
- Revenue
- Average fare
- Hourly demand
- Ride outcome mix
- Service volume
- Daily ride trend
- Business insights

Demand

- Hourly demand
- Rides by weekday
- Demand by service and hour
- Monthly volume
- Daily ride trends

Revenue

- Daily revenue trend
- Revenue by payment method
- Average fare by service
- Fare distribution

Revenue metrics are based on completed rides.

Operations

- Ride status by service
- Completion rate by service
- Cancellation rate by hour
- Trip-duration distribution

Locations

- Top pickup locations
- Top destinations
- Popular source → destination routes

Data Quality

- Fare-distance relationship
- Distance-duration relationship
- Implied-speed validation
- Speed outlier detection
- Fare-per-kilometre checks
- Route uniqueness
- Missing-value checks

---

🎛️ 7. Interactive Filters

Filter| Description
Service| Filter by service type
Ride Status| Completed, cancelled, and other outcomes
Payment Method| Filter by payment type when required
Analysis Period| Select a date range

Important: The default payment-method selection does not remove cancelled rides with missing payment information. This preserves the complete ride population for cancellation and operational analysis.

Filters update the relevant dashboard KPIs, charts, and analytical views.

---

🗂️ 8. Dataset

"rides_data.csv" contains 50,000 rides covering:

17 Jun 2024 – 16 Aug 2024

Columns

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

---

🧹 9. Data Processing & Validation

Field| Processing
date| Converted to datetime
time| Parsed into hour
duration| Converted to numeric
distance| Converted to numeric
ride_charge| Converted to numeric
misc_charge| Converted to numeric
total_fare| Converted to numeric

Data-quality checks

The analysis checks:

- Duplicate records
- Missing values
- Invalid numeric values
- Invalid dates
- Missing cancelled-ride fares
- Fare-per-kilometre extremes
- Implied speed outliers
- Distance-duration relationship
- Route uniqueness

---

💰 10. Revenue Methodology

Revenue calculations use completed rides only.

The 5,036 cancelled rides do not contain fare/payment information. They remain part of the overall ride population and are included in demand, cancellation, operational, and ride-status analysis.

Metric Definitions

Metric| Definition
Revenue| Sum of "total_fare" for completed rides
Completion Rate| Completed rides ÷ total rides
Cancellation Rate| Cancelled rides ÷ total rides
Average Fare| Completed revenue ÷ completed rides
Estimated Revenue Leakage| Cancelled rides × average completed fare
Implied Speed| Distance ÷ (Duration ÷ 60)

Revenue leakage is an estimate, not recorded lost revenue.

It assumes the average completed fare is a reasonable proxy for what a cancelled ride could have generated.

---

🧪 11. Statistical Approach

Chi-Square Tests

Cancellation outcomes are tested against:

- Service
- Hour
- Weekday

Significance level:

α = 0.05

Correlation Analysis

Pearson correlation is used to investigate:

- Distance vs fare
- Distance vs duration

Monthly Normalisation

June and August are partial months, so monthly demand is compared using rides per active day rather than raw monthly totals.

---

🗃️ 12. SQL Analysis

"queries.sql" contains six analytical queries:

1. Headline KPIs
2. Estimated cancellation revenue leakage
3. Cancellation rate by service
4. Fare by distance band
5. Impossible trips using implied speed
6. Rides per day by month

SQL is used as a cross-check against the Python analysis.

---

🛠️ 13. Tech Stack

Technology| Purpose
Python| Core analytics
Pandas| Data manipulation
NumPy| Numerical operations
SciPy| Statistical testing
Plotly| Interactive visualisation
Streamlit| Dashboard application
SQL / SQLite| Analytical queries

---

🎨 14. Dashboard Design

The dashboard uses:

- Rapido-inspired visual styling
- KPI cards
- Responsive layouts
- Interactive Plotly charts
- Global filters
- Multi-page Streamlit navigation
- Business-focused insight cards

The goal is to make analytical results understandable to both technical and non-technical stakeholders.

---

📁 15. Project Structure

rapido-ride-intelligence/
│
├── rapido_ride_intelligence.py
├── rides_data.csv
├── findings.py
├── queries.sql
├── run_sql.py
├── requirements.txt
├── README.md
│
├── overview.png
├── operations.png
├── demand.png
├── revenue.png
└── performance.png

---

🚀 16. Run Locally

1. Clone the repository

git clone https://github.com/jahnavi06in/rapido-ride-intelligence.git
cd rapido-ride-intelligence

2. Install dependencies

pip install -r requirements.txt

3. Run the dashboard

python -m streamlit run rapido_ride_intelligence.py

4. Run the Python analysis

python findings.py

5. Run the SQL analysis

python run_sql.py

The dashboard opens at:

http://localhost:8501

---

☁️ 17. Deployment

The dashboard is deployed using Streamlit Community Cloud and can be accessed through the live dashboard link at the top of this README.

---

🏢 18. Business Use Cases

Demand Planning

Identify:

- Peak hours
- High-demand days
- Service-level demand
- Monthly demand patterns

Revenue Management

Analyse:

- Completed revenue
- Average fare
- Revenue trends
- Payment-method contribution
- Potential cancellation leakage

Operational Performance

Monitor:

- Completion rate
- Cancellation rate
- Ride duration
- Service performance

Location Intelligence

Explore:

- High-volume pickup locations
- Popular destinations
- Frequent routes

---

🔐 19. Data Privacy

The published dataset should contain no personally identifiable information.

Before publishing any real-world ride data, remove personal identifiers and use anonymised or appropriately shareable data.

---

⚠️ 20. Limitations

- The dataset covers approximately two months and cannot establish long-term seasonality.
- Cancellation reason is unavailable.
- Cancelling party is unavailable.
- Driver-level information is unavailable.
- City/geographic metadata is limited.
- The fare-distance relationship appears inconsistent with a typical distance-based pricing model.
- High implied speeds suggest potential data-quality or measurement issues.
- Findings should therefore be validated against verified production data before operational deployment.

---

🔮 21. Next Steps

- Re-run the analysis on verified production data.
- Add cancellation reason and driver-side fields.
- Build a cancellation-probability model.
- Forecast daily rides and revenue using longer historical data.
- Add geographic visualisation.
- Add downloadable analytical reports.
- Add automated data-quality monitoring.

---

👩‍💻 Author

Jahnavi J

BCA Student | Data Analytics | Python | SQL | Power BI | Streamlit

GitHub:
https://github.com/jahnavi06in
