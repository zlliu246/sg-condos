# from website, scrape data to raw/condo_csv/*.csv

from time import sleep
from datetime import datetime

import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup

url = "https://eservice.ura.gov.sg/property-market-information/pmiResidentialTransactionSearch#"

with mysql.connector.connect(host="localhost", user="root", password="", database="house_data") as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(sale_date) FROM sales
    """)
    max_date = cursor.fetchall()[0][0]

max_year = str(max_date.year)
max_month = max_date.strftime("%B")[:3]

def click_project_select(driver):
    spans = driver.find_elements(By.CSS_SELECTOR, "span.select-span")
    for span in spans:
        if span.text.lower() == "select project or postal district":
            span.click() ; return

def click_postal_district(driver):
    anchors = driver.find_elements(By.TAG_NAME, "a")
    for anchor in anchors:
        if anchor.text.lower().strip() == "postal district":
            anchor.click() ; return
        
def check_all_checkboxes(driver):
    divs = driver.find_elements(By.CSS_SELECTOR, "div#postalDistrict")
    for div in divs:
        labels = div.find_elements(By.TAG_NAME, "label")[::-1]
        for label in labels:
            text = label.text.strip().lower()
            if not text:
                continue
            if text[0] == "d" and text[1].isnumeric():
                label.click()
                sleep(0.1)

def click_apply(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, "button#apply")
    for button in buttons:
        if button.text.lower().strip() == "apply":
            button.click()
            return

def select_from_year(driver):
    selects = driver.find_elements(By.CSS_SELECTOR, "select#saleYearFrom")
    for select in selects:
        select = Select(select)
        select.select_by_visible_text(max_year)
        return
    
def select_from_month(driver):
    selects = driver.find_elements(By.CSS_SELECTOR, "select#saleMonthFrom")
    for select in selects:
        select = Select(select)
        select.select_by_visible_text(max_month)
        return

def select_prop_type(driver):
    selects = driver.find_elements(By.CSS_SELECTOR, "select#propertyTypeGroupNo")
    for select in selects:
        select = Select(select)
        select.select_by_visible_text("Apartments & Condominiums")
        return

def click_search_button(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-primary[type="submit"]')
    for button in buttons:
        if button.text.strip().lower() == "search":
            button.click()
            return

def click_download_dropdown_button(driver):
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn.btn-default.dropdown-toggle")
    for button in buttons:
        if button.text.lower().strip() == "download":
            button.click()
            return

def click_download_csv_button(driver):
    anchors = driver.find_elements(By.CSS_SELECTOR, "a.downloadCSV")
    for anchor in anchors:
        if "csv" in anchor.text.lower().strip():
            print(anchor)
            anchor.click()

try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": "/Users/lzl/Documents/repos/notes/__PROJECTS/house_data/raw/condo_csvs"
    })
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(0.5)
    click_project_select(driver)
    sleep(0.5)
    click_postal_district(driver)
    sleep(0.5)
    check_all_checkboxes(driver)
    sleep(0.5)
    click_apply(driver)
    sleep(0.5)
    select_from_year(driver)
    sleep(0.5)
    select_from_month(driver)
    sleep(0.5)
    select_prop_type(driver)
    sleep(0.5)
    click_search_button(driver)
    sleep(0.5)
    click_download_dropdown_button(driver)
    sleep(0.5)
    click_download_csv_button(driver)
    sleep(10)
    print("downloaded CSV file")

    # input(">>>")
    # while_not_exit(
    #     onkeypress(Key.ENTER).call(lambda: print("Enter to continue"))
    # )

except Exception as e:
    print("ERROR", e)

finally:
    driver.close()
