import os
import requests

from dotenv import load_dotenv
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Sheety API Config
sheety_project_name = os.getenv("SHEETY_PROJECT_NAME")
sheety_project_sheet = os.getenv("SHEETY_PROJECT_SHEET")
sheety_app_key = os.getenv("SHEETY_API_KEY")
sheety_endpoint = f"https://api.sheety.co/{sheety_app_key}/{sheety_project_name}/{sheety_project_sheet}"
sheety_headers = {
    "Authorization": os.getenv("SHEETY_AUTH")
}

class SeleniumDriver():

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_property_listing(self):
        property_details = []
        user_input = input("Enter the url from 99acres after selecting a city: ")
        self.driver.get(user_input)
        time.sleep(5)
        property_list = self.driver.find_elements(By.CSS_SELECTOR, ".srpTuple__tupleTitleOverflow")
        property_links = self.driver.find_elements(By.CSS_SELECTOR, ".srpTuple__tdClassPremium a")
        property_prices = []
        property_listings = []
        property_links_list = []
        for l in property_list:
            property_listings.append(l.text)
        for l in range(0, len(property_listings)-2):
            property_links[l].click()
            time.sleep(3)
            url = property_links[l].get_attribute("href")
            property_links_list.append(url)
            self.driver.get(url)
            price = self.driver.find_element(By.ID, "pdPrice")
            property_prices.append(price.text)
            time.sleep(3)
            self.driver.back()
            self.driver.get(user_input)
            time.sleep(3)
            property_links = self.driver.find_elements(By.CSS_SELECTOR, ".srpTuple__tdClassPremium a")
        # for l in property_links:
        #     print(l.get_attribute("href"))
        # for l in property_prices:
        #     print(l)
        for l in range(0, len(property_listings)-2):
            property_details.append({
                "name": property_listings[l],
                "url": property_links_list[l],
                "price": property_prices[l]
            })
            sheety_data = {
                "listing": {
                    "name": property_details[l]["name"],
                    "link": property_details[l]["url"],
                    "price": property_details[l]["price"],
                }
            }
            response = requests.post(url=sheety_endpoint, json=sheety_data, headers=sheety_headers)
            print(response.json())
        print(property_details)




bot = SeleniumDriver()
bot.get_property_listing()
