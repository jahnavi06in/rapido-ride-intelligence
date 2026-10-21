# 🚖 Rapido Ride Intelligence

**Interactive ride-analytics dashboard + data-validity audit on 50,000 ride-hailing trips.**
Python · SQL · Pandas · Plotly · Streamlit

🔗 **[Live dashboard](https://rapido-ride-intelligence-po3rarnj2dd66w4pzlt94e.streamlit.app/)**

<!-- Add 2-3 screenshots here: Overview, Operations, Locations -->
![Overview](screenshots/overview.png)

## The question
> Where is this ride-hailing business losing revenue, and can its data be trusted to say why?

## Key findings
| # | Finding | Evidence |
|---|---------|----------|
| 1 | **Cancellations cost an estimated ₹2.76M**, about 10% of potential revenue. | 5,036 of 50,000 rides cancelled × ₹547 avg completed fare. Completed-ride revenue is ₹24.6M. |
| 2 | **Cancellation rate is flat (~10%) across every service, hour and weekday.** No segment is a fix-first target. | Chi-square tests: service p=0.31, hour p=0.80, weekday p=0.72, all far above 0.05. |
| 3 | **Pricing does not follow distance.** Fare is unrelated to trip length. | corr(distance, fare) = −0.005. Average fare is ₹544-₹549 in every distance band, so ₹/km falls from ₹140 (0-10 km) to ₹12 (40-50 km). |
| 4 | **~10% of completed trips have impossible speeds.** | 4,415 rides imply >80 km/h, up to 300 km/h. Distance and duration are uncorrelated (r = 0.008). |
| 5 | **Demand is flat once partial months are normalised.** | June (14 days) and August (16 days) are partial. Rides/day: 806 / 824 / 823. |
| 6 | **Route analysis has no signal.** 49,993 unique routes across 50,000 rides. | Only 7 routes repeat, so "top routes" is noise. Aggregate to area level instead. |

**Takeaway:** the data's fares, distances and durations are statistically independent, which suggests it is synthetic or has a broken pricing pipeline. Before acting on any "peak hour" or "best service" insight, the pricing logic must be validated. The one reliable business metric is cancellation leakage.

**Recommendations**
1. Audit the fare and distance pipeline before building pricing or demand models.
2. Treat cancellations as a platform-wide issue (rider and driver side), not a service-specific one.
3. Log cancellation reasons and who cancelled; the current data cannot explain the 10%.

## How I handled the data
- **Missing values:** 5,036 cancelled rides have no fare or payment method. Excluded from revenue and average fare, kept for demand and cancellation analysis (never treated as ₹0).
- **Validation:** checked duplicates (none), nulls, impossible speeds and fare-per-km outliers.
- **Statistics:** chi-square tests to confirm differences between groups were or were not real.

## Project structure
```
rapido_ride_intelligence.py   Streamlit dashboard (6 pages incl. Data Quality audit, global filters)
analysis/findings.py          Reproduces every number above
sql/queries.sql, run_sql.py   Same KPIs and audits in SQL
rides_data.csv                50,000 rides, 17 Jun - 16 Aug 2024
```

## Run it
```bash
pip install -r requirements.txt
python -m streamlit run rapido_ride_intelligence.py   # dashboard
python analysis/findings.py                           # findings
python sql/run_sql.py                                 # SQL queries
```

## Limitations
Two-month window, no cancellation reasons or driver data, and the data-validity issues above. Findings 2-6 should be re-run on production data.
