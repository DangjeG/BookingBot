import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def parse_review(hotel_url):
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    driver.get(hotel_url)

    driver.find_element(By.CLASS_NAME, "toggle-reviews").click()
    time.sleep(1)

    reviews = str()
    while True:
        soup = BeautifulSoup(driver.page_source, "lxml")
        review_items = soup.find("ul", class_="hidden unstyled").find_all("li", class_="review-item")
        for item in review_items:
            try:
                reviews += item.find("div", class_="review-pro").text.replace("\n", "")
            except AttributeError:
                try:
                    reviews += item.find("div", class_="review-contra").text.replace("\n", "")
                except AttributeError:
                    continue
            finally:
                try:
                    reviews += item.find("div", class_="review-contra").text.replace("\n", "")
                except AttributeError:
                    continue

        try:
            next_button = driver.find_element(By.CLASS_NAME, "page-link.next")
            try:
                next_button.click()
            except ElementClickInterceptedException:
                break
        except NoSuchElementException:
            break

    return reviews
