# from raw/condo_csvs/*.csv, collect and put into MySQL DB.

import sys
from pathlib import Path

import pandas as pd
import mysql.connector
from geopy.distance import distance as get_distance

# if nuke, delete everything in house_data, and start from scratch
# else, add incremental data into table
nuke = "nuke" in sys.argv

from scripts.common import (
    get_cleaned_condos_as_df,
    get_99co_maps,
    get_latlon_maps,
    delete_and_recreate_tables,
    get_new_condo_sales_df,
)

# from raw/condo_csvs/*.csv, fetch, deduplicate, clean and return as dataframe
df = get_cleaned_condos_as_df()

# from raw/99co/data.txt, get name to (num_units, top, developer) maps + unmatched_names
_99name_to_info, unmatched_99co_names = get_99co_maps(df)

# from raw/latlon.csv, get category to {name: [lat, lon]}
cat_to_name_to_latlon_map = get_latlon_maps()
facilities = []
for cat, name_to_latlon_map in cat_to_name_to_latlon_map.items():
    if cat == "condo": continue
    for name, (lat, lon) in name_to_latlon_map.items():
        facilities.append([name, lat, lon, cat])

with mysql.connector.connect(host="localhost", user="root", password="", database="house_data") as conn:
    cursor = conn.cursor()

    if nuke:
        delete_and_recreate_tables(conn, cursor)
        print("Nuking all existing tables")
    else:
        df = get_new_condo_sales_df(df, cursor)
        print(f"Found {df.shape[0]} new sales to insert")

    # get existing projects names
    cursor.execute("SELECT project_name FROM projects")
    existing_project_names = {row[0] for row in cursor.fetchall()}

    # from df, get projects to insert
    project_data, seen = [], set()
    for _, row in df.iterrows():
        if row.project_name in seen or row.project_name in existing_project_names:
            continue
        seen.add(row.project_name)
        lat, lon = cat_to_name_to_latlon_map["condo"].get(row.project_name, [None, None])

        num_units = top = developer = None
        if row.project_name in _99name_to_info:
            num_units = _99name_to_info.get(row.project_name, {}).get("num_units")
            top = _99name_to_info.get(row.project_name, {}).get("top")
            developer = _99name_to_info.get(row.project_name, {}).get("developer")
        else:
            for unmatched_name in unmatched_99co_names:
                if row.project_name in unmatched_name:
                    num_units = _99name_to_info.get(unmatched_name, {}).get("num_unit")
                    top = _99name_to_info.get(unmatched_name, {}).get("top")
                    developer = _99name_to_info.get(unmatched_name, {}).get("developer")
                    break

        project_data.append(
            [
                row.project_name,
                row.street_name,
                row.area_type,
                row.property_type, 
                row.tenure,
                row.tenure_start if not pd.isnull(row.tenure_start) else None,
                row.postal_district,
                row.market_segment, 
                lat,
                lon,
                num_units,
                top,
                developer
            ]
        )

    cursor.executemany("""
        INSERT IGNORE INTO projects(
            project_name,
            street_name,
            area_type,
            property_type,
            tenure,
            tenure_start,
            postal_district,
            market_segment,
            latitude,
            longitude,
            num_units,
            top,
            developer
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, project_data)
    conn.commit()
    print("Finished writing to projects")

    # get project id map
    cursor.execute("""SELECT `id`, project_name FROM projects""")
    project_name_to_id_map = {project_name: id_ for id_, project_name in cursor.fetchall()}

    # insert sales data
    sales_data = []
    for _, row in df.iterrows():
        sales_data.append(
            [row.price, row.area, row.psf, row.sale_date, row.sale_type, row.floor_level, project_name_to_id_map.get(row.project_name)]
        )
    cursor.executemany("""
        INSERT INTO sales(
            price, area, psf, sale_date, sale_type, floor_level, project_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, sales_data)
    conn.commit()
    print("Finished writing to sales")

    # insert projects_facilities_assoc data
    cursor.execute("""
        SELECT `id`, project_name, latitude, longitude
        FROM projects
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)
    DISTANCE_THRESHOLD = 1500

    seen = set()
    add_values = []
    condo_projects = cursor.fetchall()
    for i, (project_id, condo_name, latitude, longitude) in enumerate(condo_projects):
        if condo_name in existing_project_names:
            continue
        print(f"Searching {i} out of {len(condo_projects)} projects")
        condo_latlon = (latitude, longitude)

        for faci_name, faci_lat, faci_lon, faci_type in facilities:
            faci_latlon = (faci_lat, faci_lon)
            dist = get_distance(condo_latlon, faci_latlon).meters * 1.45
            if dist > DISTANCE_THRESHOLD:
                continue
            key = (project_id, faci_name, faci_type)
            if key in seen:
                continue
            seen.add(key)
            add_values.append([project_id, faci_name, faci_type, int(dist)])

    print(f"Found {len(add_values)} to add into table")
    
    # add values into table
    cursor.executemany("""
        INSERT INTO projects_facilities_assoc
        (project_id, facility_name, facility_type, dist_meters)
        VALUES (%s, %s, %s, %s)
    """, add_values)

    conn.commit()
    print("Finished writing to condo_projects_facilities_association")

    # dumping tables into CSV files
    def run(query):
        cursor.execute(query)
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=[i[0] for i in cursor.description])

    run("SELECT * FROM projects").to_csv("public/projects.csv", index=False)
    run("SELECT * FROM sales").to_csv("public/sales.csv", index=False)
    run("SELECT * FROM projects_facilities_assoc").to_csv("public/projects_facilities_assoc.csv", index=False)
