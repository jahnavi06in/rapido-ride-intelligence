"""Reproduces every number quoted in the README 'Key Findings' section.
Run from the project root:  python analysis/findings.py
"""
import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv("rides_data.csv")
df["date"] = pd.to_datetime(df["date"])
df["hour"] = pd.to_datetime(df["time"], format="mixed").dt.hour
df["cancelled"] = df["ride_status"].eq("cancelled")
done = df[~df["cancelled"]].copy()

# ---- 1. Baseline KPIs -------------------------------------------------
n_rides = len(df)
revenue = done["total_fare"].sum()
avg_fare = done["total_fare"].mean()
cancel_rate = df["cancelled"].mean()
leakage = df["cancelled"].sum() * avg_fare
print(f"Rides {n_rides:,} | {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Revenue (completed) Rs {revenue:,.0f} | avg fare Rs {avg_fare:,.0f}")
print(f"Cancel rate {cancel_rate:.1%} | est. revenue leakage Rs {leakage:,.0f} "
      f"({leakage / (revenue + leakage):.1%} of potential revenue)")

# ---- 2. Is cancellation driven by anything? (chi-square tests) --------
print("\nCancellation vs. driver (chi-square, p > 0.05 = no relationship)")
for col in ["services", "hour"]:
    p = chi2_contingency(pd.crosstab(df[col], df["cancelled"]))[1]
    print(f"  {col:<10} p = {p:.3f}")
df["dow"] = df["date"].dt.dayofweek
p = chi2_contingency(pd.crosstab(df["dow"], df["cancelled"]))[1]
print(f"  {'weekday':<10} p = {p:.3f}")
by_svc = df.groupby("services")["cancelled"].mean()
print("  cancel rate by service:", by_svc.round(3).to_dict())

# ---- 3. Pricing logic audit -------------------------------------------
print("\nPricing / data-validity audit (completed rides)")
print(f"  corr(distance, fare)     = {done['distance'].corr(done['total_fare']):+.3f}")
print(f"  corr(distance, duration) = {done['distance'].corr(done['duration']):+.3f}")
done["kmh"] = done["distance"] / (done["duration"] / 60)
done["fare_per_km"] = done["total_fare"] / done["distance"]
print(f"  rides with implied speed > 80 km/h: {(done['kmh'] > 80).mean():.1%} "
      f"(max {done['kmh'].max():.0f} km/h)")
print(f"  fare per km: min Rs {done['fare_per_km'].min():.1f}, "
      f"max Rs {done['fare_per_km'].max():.0f}")
print("  avg fare by service:", done.groupby("services")["total_fare"].mean().round(0).to_dict())

# ---- 4. Volume is flat once partial months are normalised -------------
daily = df.groupby(df["date"].dt.to_period("M")).agg(
    rides=("ride_id", "count"), days=("date", "nunique"))
daily["rides_per_day"] = (daily["rides"] / daily["days"]).round(0)
print("\nRides per day by month:\n", daily)

# ---- 5. Location granularity ------------------------------------------
routes = df.groupby(["source", "destination"]).size()
print(f"\nUnique pickups {df['source'].nunique():,} | unique routes {len(routes):,} "
      f"| routes seen more than once: {(routes > 1).sum()}")
