from datetime import datetime

import pandas as pd

df = pd.read_csv("hdb_csvs/hdb.csv")

df["price"] = df["resale_price"]
del df["resale_price"]
df["datetime"] = [datetime.strptime(m, "%Y-%m") for m in df["month"]]
del df["month"]
df["town"] = [t.lower() for t in df["town"]]
df["flat_type"] = [f.lower() for f in df["flat_type"]]
df["street_name"] = [s.lower() for s in df["street_name"]]
df["floor_level"] = [s.lower() for s in df["storey_range"]]
del df["storey_range"]
df["area"] = [a * 10.76 for a in df["floor_area_sqm"]]
del df["floor_area_sqm"]
df["flat_model"] = [x.lower() for x in df["flat_model"]]
df["top"] = [x for x in df["lease_commence_date"]]
del df["lease_commence_date"]
del df["remaining_lease"]

cols = ["town", "street_name", "price", "area", "floor_level", "top", "flat_type", "block", "flat_model", "datetime"]
df = df.loc[:, cols]

print(df)
df.to_csv("hdb.csv", index=False)

from csv_to_sql_dump import csv_to_sql_dump

csv_to_sql_dump(df, table_name="hdbs", database_name="house_data", output_filepath="hdb.sql", parse_dates=["datetime"])