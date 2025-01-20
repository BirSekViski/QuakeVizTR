import os
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# TODO
# 1. Do not get the table rows, which include the advertisement.
# 2. Get the data from the next pages.


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
browser = webdriver.Chrome(f"{os.getcwd()}../chromedriver", options=chrome_options)
link = "https://www.canbula.com/dataviz/180315008"
browser.get(link)
time.sleep(2)
table = browser.find_element(by=By.CSS_SELECTOR, value='.table-striped tbody')
rows = table.find_elements(by=By.CSS_SELECTOR, value='tr')
data_list = []

for row in rows:
    date_time = row.find_element(by=By.CSS_SELECTOR, value='.datetime').text
    city = row.find_element(by=By.CSS_SELECTOR, value='.city').text
    magnitude = float(row.find_element(by=By.CSS_SELECTOR, value='.magnitude').text)
    data_list.append({'date_time': date_time, 'city': city, 'magnitude': magnitude})

with open('dataset.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date_time', 'city', 'magnitude'])
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)

print(data_list)
time.sleep(1)
browser.close()