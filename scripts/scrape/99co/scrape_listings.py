import requests
from datetime import datetime
import pyautogui
from time import sleep
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import pandas as pd

from onkeypress import while_not_exit, onkeypress, Key

# options = Options()
# options.debugger_address = "127.0.0.1:9222"
# driver = webdriver.Chrome(options=options)

step = [1]

def scrape_listing(driver, url):
    driver.get(url)
    pyautogui.move(0, step[0])
    step[0] = -step[0]
    sleep(1)

    rowdata = {"url":  url}
    prop_details = driver.find_elements(By.CSS_SELECTOR, "div#propertyDetails")
    if prop_details:
        segment = prop_details[0].find_elements(By.CSS_SELECTOR, "div.mt-4.flex")
        for segment in segment:
            try:
                key, val = segment.find_elements(By.CSS_SELECTOR, "div")
                rowdata[key.text] = val.text
            except: pass

    dev_overview = driver.find_elements(By.CSS_SELECTOR, "div#development")
    if dev_overview:
        segment = dev_overview[0].find_elements(By.CSS_SELECTOR, "div.mt-4.flex")
        for segment in segment:
            try:
                key, val = segment.find_elements(By.CSS_SELECTOR, "div")
                rowdata[key.text] = val.text
            except: pass
    
    desc = driver.find_elements(By.CSS_SELECTOR, "div#description")
    if desc:
        desc = desc[0]
        rowdata["desc"] = desc.text

    return rowdata

driver = webdriver.Chrome()

existing_urls = set()
existing_names = set()
with open("raw/99co/data.txt", "r") as f:
    for line in f:
        rowdata = json.loads(line.strip())
        url = rowdata["url"]
        existing_urls.add(url)
        name = rowdata.get("Name", "").lower()
        existing_names.add(name)

try:    
    urls = []
    with open("raw/99co/urls.txt") as f:
        for line in f:
            urls.append("https://99.co" + line.strip())
    for url_i, url in enumerate(urls):
        if url in existing_urls:
            continue
        print(url_i, end=" ")
        test_name_segments = url.split("/property/")[-1].split("-")
        name_exists = False
        for i in range(len(test_name_segments)):
            temp = test_name_segments[:i+1]
            testname = " ".join(temp)
            if testname in existing_names:
                name_exists = True
                break
        if name_exists:
            print(f"skipping due to existing name {testname!r}")
            continue

        try:
            rowdata = scrape_listing(driver, url)
            with open("raw/99co/data.txt", "a") as f:
                f.write(json.dumps(rowdata) + "\n")
            print(str(rowdata)[:100])
        except Exception as e:
            print("ERROR", e)
        finally:
            sleep(1)

finally:
    driver.close()



r"""

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug"

"""