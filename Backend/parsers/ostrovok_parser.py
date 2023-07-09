import re
import time

from bs4 import BeautifulSoup
from geopy.distance import great_circle as gd
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.common import (ElementClickInterceptedException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Backend.ObjectModels.hotel import Hotel
from Backend.ObjectModels.user_request import UserRequest

from . import Parser

MAIN_PAGE = "https://ostrovok.ru/"


def get_city_url(country, city):
    driver = webdriver.Chrome()
    driver.get(MAIN_PAGE)
    city_field = driver.find_element(By.CLASS_NAME, "Input-module__control--tqFEn")
    city_field.clear()
    city_field.send_keys(city + ", " + country)
    time.sleep(3)
    city_field.send_keys(Keys.RETURN)
    driver.find_element(By.CLASS_NAME,
                        "Button-module__button--MR2Ly.Button-module__button_size_m--184Hw."
                        "Button-module__button_wide--eV274").click()

    return driver.current_url, driver


def set_filters(url, date_in, date_out, adults, childrens, stars, meal_types, price, amenities):
    url = url.replace("price=one", "price=" + price + ".one")
    url = url.split('dates=')[0] + 'dates=' + date_in + "-" + date_out + '&' + '&'.join(
        url.split('&')[1:])

    if childrens == "":
        url = url.split('guests=')[0] + 'guests=' + adults + '&' + '&'.join(
            url.split('&')[1:])
    else:
        url = url.split('guests=')[0] + 'guests=' + adults + "and" + childrens + '&' + '&'.join(
            url.split('&')[1:])

    url += "&meal_types=" + meal_types + "&stars=" + stars + "&amenities=" + amenities

    return url


def get_distance(hotel_coords, user_coords):
    return gd((user_coords[0], user_coords[1]), (hotel_coords[0], hotel_coords[1])).km


def find_hotels(driver, hotels_url, user_point, radius):
    hotels = list()
    driver.get(hotels_url)
    while True:
        try:
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located(
                (By.CLASS_NAME, 'zenserpresult.zenserpresult-hasfilters.zenserpresult-hasloading')))

            soup = BeautifulSoup(driver.page_source, "lxml")
            if re.search(r'<div class="emptyserpfiltered-title">', str(soup)):
                return hotels

            items = soup.find_all("div", class_="hotel-wrapper")
            for item in items:
                geolocator = Nominatim(user_agent="user_agent")
                try:
                    location = geolocator.geocode(
                        item.find("p", class_="zen-hotelcard-address link").text.replace("ul. ", "").replace(
                            "Street", ""))
                    float_values = (location.latitude, location.longitude)

                    if get_distance(hotel_coords=tuple([float(value) for value in float_values]),
                                    user_coords=user_point) <= radius:
                        name = item.find('a', class_='zen-hotelcard-name-link link').text
                        address = item.find("p", class_="zen-hotelcard-address link").text
                        rating = item.find('a', class_='zen-hotelcard-rating-total').text
                        url = MAIN_PAGE + item.find('a', class_='zen-hotelcard-name-link link')['href']
                        photo = item.find('img', class_="zenimage-content")['src']
                        hotels.append(Hotel(name, address, rating, url, photo))
                except AttributeError:
                    continue

            try:
                driver.find_element(By.CSS_SELECTOR, ".zenpagination-button-next").click()
            except ElementClickInterceptedException:
                break

        except NoSuchElementException:
            break

    return hotels


class OstrovokParser(Parser):
    @staticmethod
    def get_hotels(user_request: UserRequest):
        geolocator = Nominatim(user_agent="user_agent")
        location = geolocator.reverse(user_request.user_point)
        country = location.raw['address'].get('country', '')
        city = location.raw['address'].get('city', '')
        radius_km = user_request.radius_km
        date_in = str(user_request.date_in)
        date_out = str(user_request.date_out)
        adults = str(user_request.adults)
        childrens = ""  # указывается возраст ребёнка,
        # если несколько детей, то возраста через точку

        # 0.1 / 2 / 3 / 4 / 5
        stars = ""  # количество звёзд через точку

        # без питания=nomeal; завтрак=breakfast,
        # завтрак+обед/ужин=halfBoard,
        # завтрак+обед+ужин=fullBoard,
        # всё включено=allInclusive
        meal_types = "nomeal"  # вводится через точку

        # минимальное 100 рублей, максимум 100.000
        price = "100-10000"
        # wifi=has_internet, парковка=has_parking, бассейн=has_pool,
        # кондиционер=air-conditioning, с животными=has_pets,
        # трансфер=has_airport_transfer, бар/ресторан=has_meal
        amenities = "has_internet.air-conditioning"  # вводится через точку

        url, driver = get_city_url(country=country, city=city)
        url_with_filters = set_filters(url, date_in, date_out, adults,
                                       childrens, stars, meal_types, price, amenities)

        return find_hotels(driver=driver, hotels_url=url_with_filters,
                           user_point=user_request.user_point, radius=radius_km)


if __name__ == '__main__':
    OstrovokParser.get_hotels(UserRequest(user_id=0))
