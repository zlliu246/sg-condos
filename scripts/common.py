import re
import os
import json
from datetime import datetime
from pathlib import Path
from decimal import Decimal

import pandas as pd

def get_cleaned_condos_as_df():
    df = pd.DataFrame()
    for filename in os.listdir("./raw/condo_csvs"):
        if not filename.endswith(".csv"):
            continue
        filepath = Path("./raw/condo_csvs") / filename
        try:
            new_df = pd.read_csv(filepath, encoding="utf-8", encoding_errors="ignore")
            df = pd.concat([new_df, df], axis=0)
        except Exception as e:
            print("ERROR", filepath)
            print(e)

    # deduplicate rows in raw condo data
    old_num_rows = df.shape[0]
    deduplicated_rows = []
    seen = set()
    for i, row in df.iterrows():
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        deduplicated_rows.append(list(row))
    df = pd.DataFrame(deduplicated_rows, columns=list(df.columns))
    print(f"Num rows before deduplication: {old_num_rows}, After: {df.shape[0]}")

    # clean columns in condo data
    original_colnames = list(df.columns)

    df["project_name"] = [n.lower() for n in df["Project Name"]]
    df["price"] = [int(p.replace(",", "")) for p in df["Transacted Price ($)"]]
    df["area"] = [float(a.replace(",", "")) for a in df["Area (SQFT)"]]
    df["psf"] = [round(price/area) for price, area in zip(df["price"], df["area"])]
    df["sale_date"] = [datetime.strptime(d, "%b-%y") for d in df["Sale Date"]]
    df["street_name"] = [s.lower() for s in df["Street Name"]]
    df["sale_type"] = [s.lower() for s in df["Type of Sale"]]
    df["area_type"] = [a.lower() for a in df["Type of Area"]]
    df["property_type"] = [p.lower() for p in df["Property Type"]]
    df["num_units"] = [n for n in df["Number of Units"]]
    def get_tenure(string):
        if re.match("freehold", string.lower()):
            return "freehold"
        try: return re.findall(r"(\d+) yrs", string.lower())[0]
        except: return string
    df["tenure"] = [get_tenure(t) for t in df["Tenure"]]
    def get_tenure_start(string):
        try: return int(re.findall(r".*from (\d\d\d\d)", string)[0])
        except: return None
    df["tenure_start"] = [get_tenure_start(t) for t in df["Tenure"]]
    df["postal_district"] = [p for p in df["Postal District"]]
    df["market_segment"] = [m.lower() for m in df["Market Segment"]]
    df["floor_level"] = [l.lower() for l in df["Floor Level"]]

    for colname in original_colnames:
        del df[colname]

    print("Finished cleaning columns")

    return df

def get_99co_maps(df):
    # fetch 99.co data (num_units, top, developer)
    _existing_project_names = set(df["project_name"].values)
    def mode(ls):
        if not ls: return None
        ls = sorted([(ls.count(v), v) for v in ls if v is not None])
        return ls[-1][-1]
    out = {}
    with open("raw/99co/data.txt", "r") as f:
        for line in f:
            row = json.loads(line.strip().lower())
            name = row.get("name", "").lower().strip()
            num_units = row.get("total units")
            top = row.get("built year")
            dev = row.get("developer")
            if name not in out:
                out[name] = {"num_units": [], "top": [], "developer": []}
            if num_units: out[name]["num_units"].append(int(num_units))
            if top: out[name]["top"].append(int(top))
            if dev: out[name]["developer"].append(dev)
    for name, info in out.items():
        info["num_units"] = mode(info["num_units"])
        info["top"] = mode(info["top"]) 
        info["developer"] = mode(info["developer"])
    _unmatched_names = set(out) - _existing_project_names
    return out, _unmatched_names

def get_latlon_maps():
    # fetch (latitude, longitude) info from static/latlon.csv
    latlon_df = pd.read_csv("static/latlon.csv", dtype={"latitude": "object", "longitude": "object"})

    out = {}
    for i, row in latlon_df.iterrows():
        category, name, lat, lon = row.category, row.query, row.latitude, row.longitude
        if row.category not in out:
            out[category] = {}
        if category == "mrt":
            matches = re.findall("(.* mrt) station.*", str(row.searchval))
            if not matches:
                continue
            name = matches[0]
            if name not in out[category]:
                out[category][name] = [lat, lon]
            continue
        if name not in out[category]:
            out[category][name] = [lat, lon]

    # some data not accurate, so hardcode
    out["condo"]["the orie"] = ["1.3398566678680583", "103.85014225029732"]
    out["mrt"]["punggol mrt"] = ["1.40532764450158", "103.90239489927282"]

    print(f"Found {len(out['condo'])} condos, {len(out['mrt'])} mrts, {len(out['school'])} schools, {len(out['mall'])} malls")

    return out

def delete_and_recreate_tables(conn, cursor):
    cursor.execute("DROP TABLE IF EXISTS sales")
    cursor.execute("DROP TABLE IF EXISTS projects_facilities_assoc")
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute("""
        CREATE TABLE projects (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            project_name VARCHAR(255) UNIQUE,
            street_name VARCHAR(255),
            area_type VARCHAR(255),
            property_type VARCHAR(255),
            tenure VARCHAR(255),
            tenure_start INT,
            postal_district TINYINT,
            market_segment VARCHAR(255),
            latitude DECIMAL(18, 15),
            longitude DECIMAL(18, 15),
            num_units INT,
            top INT,
            developer VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE sales (
            `id` INT PRIMARY KEY AUTO_INCREMENT,
            price INT,
            area FLOAT,
            psf FLOAT,
            sale_date DATETIME,
            sale_type VARCHAR(255),
            floor_level VARCHAR(255),
            project_id INT,
            FOREIGN KEY (project_id) REFERENCES projects (`id`)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects_facilities_assoc (
            project_id INT,
            facility_name VARCHAR(255),
            facility_type VARCHAR(255),
            dist_meters INT,
            FOREIGN KEY (project_id) REFERENCES projects(`id`),
            PRIMARY KEY (project_id, facility_name, facility_type)
        )
    """)
    conn.commit()

def get_new_condo_sales_df(df, cursor):
    # PK: (project_name, price, area, year, month, sale_type, floor_level)
    cursor.execute("""
        SELECT
            project_name,
            price,
            area,
            YEAR(sale_date) AS `year`,
            MONTH(sale_date) AS `month`,
            sale_type,
            floor_level
        FROM
            sales LEFT JOIN projects ON sales.project_id = projects.id
    """)
    existing_sales = set(cursor.fetchall())
    new_rows = []
    for i, row in df.iterrows():
        key = (
            row.project_name, 
            row.price, 
            row.area, 
            row.sale_date.year,
            row.sale_date.month,
            row.sale_type,
            row.floor_level,
        )
        if key not in existing_sales:
            new_rows.append(row)
    return pd.DataFrame(new_rows, columns=df.columns)