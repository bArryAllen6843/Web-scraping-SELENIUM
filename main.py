from selenium import webdriver
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

with open("data.json", "w") as f:
    json.dump([], f)


def write_json(new_data, filename="data.json"):
    with open(filename, 'r+') as file:
        # first we load existing data into a dict
        file_data = json.load(file)
        file_data.append(new_data)
        # sets file's current position to offset
        file.seek(0)
        # convert back to json
        json.dump(file_data, file, indent=4)


os.environ['PATH'] += r"C:/SeleniumDrivers"
browser = webdriver.Chrome()
browser.get("https://www.amazon.in/s?k=clothes&crid=1QYYJQL7GTAW1&sprefix=clothes%2Caps%2C359&ref=nb_sb_noss_1")

isNextDisabled = False

while not isNextDisabled:
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '//div[@data-component-type="s-search-result"]')))

        elem_list = browser.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")

        items = elem_list.find_elements(
            By.XPATH, '//div[@data-component-type="s-search-result"]')

        for item in items:
            title = item.find_element(By.TAG_NAME, 'h2').text
            price = item.find_element(By.CLASS_NAME, 'a-price').text
            img = item.find_element(By.CLASS_NAME, 's-image').get_attribute("src")
            link = item.find_element(By.CLASS_NAME, 'a-link-normal.s-no-outline').get_attribute("href")
            print("Title: " + title)
            print("Price: " + price)
            print("Image: " + img)
            print("Link: " + link)
            print("")

            write_json({
                "title": title,
                "price": price,
                "image": img,
                "link": link
            })

        next_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, 's-pagination-next')))

        next_class = next_btn.get_attribute('class')

        if 's-pagination-disabled' in next_class:
            isNextDisabled = True
            break

        browser.find_element(By.CLASS_NAME, 's-pagination-next').click()

    except Exception as e:
        print(e, "Main Error")
        isNextDisabled = True
