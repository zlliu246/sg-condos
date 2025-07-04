import json
import pandas as pd
from fuzzywuzzy.fuzz import token_set_ratio

def get_rows(name, cat):
    data = []
    with open(f"raw/{name}.txt") as f:
        for line in f:
            row = json.loads(line.strip().lower())
            row["category"] = cat
            data.append(row)
    return data

def get_best_row(rows, query):
    bestscore = -1
    bestrow = None
    for row in rows:
        row_val = row["searchval"]
        score = token_set_ratio(row_val, query)
        if score > bestscore:
            bestscore = score
            bestrow = row
    return bestrow

condos_raw = get_rows("condo_latlons", "condo")
d = {}
for row in condos_raw:
    # for each query, use one where searchval is closest to query
    query = row["query"]
    if query not in d:
        d[query] = []
    d[query].append(row)
data = []
for query, rows in d.items():
    best_row = get_best_row(rows, query)
    data.append(best_row)

data.extend(get_rows("malls_latlons", "mall"))
data.extend(get_rows("mrt_latlons", "mrt"))
data.extend(get_rows("primary_schools_latlons", "school"))

df = pd.DataFrame(data)
df.to_csv(f"static/latlon.csv", index=False)