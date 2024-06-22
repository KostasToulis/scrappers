import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

headers_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'},
]


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={random.choice(headers_list)['User-Agent']}")
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def scrape_real_estate(url):

    driver = get_driver()
    driver.get(url)

    driver.implicitly_wait(10)

    images = driver.find_elements(By.CLASS_NAME, 'property__gallery__item')
    price = driver.find_element(By.CLASS_NAME, 'property__price__text').text.strip()
    price = fix_price(price)
    location = driver.find_element(By.CLASS_NAME, 'property__address').text.strip()
    description = driver.find_element(By.CLASS_NAME, 'property__description').text.strip()

    image_urls = []

    for image in images:
        try:
            image_urls.append(image.find_element(By.TAG_NAME, 'img').get_attribute('src'))
            time.sleep(random.uniform(1, 5))
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue

    return image_urls, price, location, description


def fix_price(price):
    price_fixed = price[1:]
    price_fixed = price_fixed.replace(',', '')
    price_fixed = float(price_fixed)
    return price_fixed

image_urls, price, location, description = scrape_real_estate("https://www.spitogatos.gr/en/property/1114561946")
print(image_urls)
print(price)
print(location)
print(description)