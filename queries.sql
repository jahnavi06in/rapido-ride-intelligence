-- SQLite / standard SQL. Load rides_data.csv into a table named rides.
-- Run all queries:  python sql/run_sql.py

-- Q1. Headline KPIs (revenue counts completed rides only)
SELECT COUNT(*) AS total_rides,
       ROUND(100.0 * SUM(ride_status = 'completed') / COUNT(*), 1) AS completion_pct,
       ROUND(SUM(CASE WHEN ride_status = 'completed' THEN total_fare END), 0) AS revenue,
       ROUND(AVG(total_fare), 0) AS avg_fare
FROM rides;

-- Q2. Estimated revenue lost to cancellations
WITH f AS (SELECT AVG(total_fare) AS avg_fare FROM rides WHERE ride_status = 'completed')
SELECT SUM(ride_status = 'cancelled') AS cancelled_rides,
       ROUND(SUM(ride_status = 'cancelled') * (SELECT avg_fare FROM f), 0) AS est_revenue_lost
FROM rides;

-- Q3. Cancellation rate by service (does any service stand out?)
SELECT services, COUNT(*) AS rides,
       ROUND(100.0 * SUM(ride_status = 'cancelled') / COUNT(*), 1) AS cancel_pct
FROM rides GROUP BY services ORDER BY cancel_pct DESC;

-- Q4. Fare vs distance band: does price follow distance?
SELECT CASE WHEN distance <= 10 THEN '1: 0-10 km'
            WHEN distance <= 20 THEN '2: 10-20 km'
            WHEN distance <= 30 THEN '3: 20-30 km'
            WHEN distance <= 40 THEN '4: 30-40 km'
            ELSE '5: 40-50 km' END AS band,
       COUNT(*) AS rides,
       ROUND(AVG(total_fare), 0) AS avg_fare,
       ROUND(AVG(total_fare / distance), 1) AS avg_fare_per_km
FROM rides WHERE ride_status = 'completed' GROUP BY band ORDER BY band;

-- Q5. Impossible trips: implied speed above 80 km/h
SELECT COUNT(*) AS suspect_rides,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM rides WHERE ride_status = 'completed'), 1) AS pct_of_completed,
       ROUND(MAX(distance / (duration / 60.0)), 0) AS max_kmh
FROM rides
WHERE ride_status = 'completed' AND distance / (duration / 60.0) > 80;

-- Q6. Rides per active day by month (months are partial, so normalise)
SELECT SUBSTR(date, 1, 7) AS month, COUNT(*) AS rides,
       COUNT(DISTINCT date) AS days,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT date), 0) AS rides_per_day
FROM rides GROUP BY month ORDER BY month;
