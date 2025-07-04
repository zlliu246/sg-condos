# from website, scrape data to raw/condo_csv/*.csv

import requests
from datetime import datetime
import pyautogui
from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import pandas as pd

from onkeypress import while_not_exit, onkeypress, Key



# https://www.99.co/singapore/sale/condos-apartments?page_num=1
# https://www.99.co/singapore/condos-apartments/bloomsbury-residences

# def download(driver):
#     print("downloading")
#     html = driver.page_source
#     with open("raw/99co/urls.txt", "a") as f:
#         soup = BeautifulSoup(html, "html.parser")
#         anchors = soup.find_all("a")
#         for anchor in anchors:
#             href = anchor.get("href")
#             if "/sale"
#             print(href)

options = Options()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()

for page_num in range(300, 1001):
    url = f"https://www.99.co/singapore/sale/condos-apartments?page_num={page_num}"

    try:
        with open("raw/99co/urls.txt", "a") as f:
            driver.get(url)
            sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            anchors = soup.find_all("a")
            for anchor in anchors:
                href = anchor.get("href")
                f.write(str(href) + "\n")
        sleep(2)

    except Exception as e:
        print(f"ERROR {page_num=} error: {e}")

# try:
#     options = Options()
#     options.debugger_address = "127.0.0.1:9222"
#     driver = webdriver.Chrome(options=options)
#     with open("raw/pg_listings.txt", "a") as f:
#         i = 0
#         while True:
#             for handle in driver.window_handles:
#                 driver.switch_to.window(handle)
#                 if "property" in driver.title.lower():
#                     break            
#             print("##### DRIVER TITLE #####", driver.title)

#             while_not_exit(
#                 onkeypress("d").call(download).args(driver)
#             )

# finally:
#     # driver.close()
#     pass

r"""

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug"

"""