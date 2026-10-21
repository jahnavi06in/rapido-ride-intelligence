import sqlite3, pandas as pd
con = sqlite3.connect(":memory:")
pd.read_csv("rides_data.csv").to_sql("rides", con, index=False)
for q in open("sql/queries.sql").read().split(";"):
    body = "\n".join(l for l in q.splitlines() if not l.strip().startswith("--")).strip()
    if body:
        print(pd.read_sql(body, con).to_string(index=False), "\n")
