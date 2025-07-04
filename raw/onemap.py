import requests
from time import sleep
import json
import pandas as pd

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyY2I3MmQ5NjViZjNiMzBlZTI5MmI5YmQzZWVlODc5MyIsImlzcyI6Imh0dHA6Ly9pbnRlcm5hbC1hbGItb20tcHJkZXppdC1pdC1uZXctMTYzMzc5OTU0Mi5hcC1zb3V0aGVhc3QtMS5lbGIuYW1hem9uYXdzLmNvbS9hcGkvdjIvdXNlci9wYXNzd29yZCIsImlhdCI6MTc1MDI1OTMwMCwiZXhwIjoxNzUwNTE4NTAwLCJuYmYiOjE3NTAyNTkzMDAsImp0aSI6Imo5eUJNVzZQRnhZeTlmb04iLCJ1c2VyX2lkIjo3NTY3LCJmb3JldmVyIjpmYWxzZX0.bsq9PSYzVb13RqQfZZmxyvV-bPXu_kbVFW0HzJaoKTg"

def search(val, page_num=1):
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={val}%20road&returnGeom=Y&getAddrDetails=Y&pageNum={page_num}"
    return requests.get(url).json()

def get_condos():
    df = pd.read_csv("static/condos.csv")
    return "condo_latlons.txt", set(df["project_name"].values) | set(df["street_name"].values), [1]

def get_mrts():
    return "mrt_latlons.txt", {"mrt"}, range(1, 201)

def get_primary_schools():
    with open("raw/primary_schools.txt", "r") as f:
        schools = [line.strip().lower() for line in f]
    return "primary_schools_latlons.txt", schools, [1]

def get_malls():
    with open("raw/malls.txt", "r") as f:
        malls = [line.strip().lower() for line in f]
    return "malls_latlons.txt", malls, [1]

filename, search_values, page_nums = get_mrts()

with open(f"raw/{filename}", "w") as f:
    for i, search_val in enumerate(search_values):
        try:
            for page_num in page_nums:
                print(f"{i=} {search_val=!r} {page_num=!r}",flush=True)
                results = search(search_val, page_num)["results"]
                for result in results:
                    result["query"] = search_val
                    f.write(json.dumps(result) + "\n")
                    break
        except Exception as e:
            print("ERROR", e)

