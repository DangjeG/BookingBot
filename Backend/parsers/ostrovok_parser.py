import re
import time
from bs4 import BeautifulSoup
from geopy.distance import great_circle as gd
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import (ElementClickInterceptedException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Backend.ObjectModels.hotel import Hotel
from Backend.ObjectModels.user_request import UserRequest

from parser import Parser

MAIN_PAGE = "https://ostrovok.ru/"
services_mapping = {
    'wifi': 'has_internet',
    'парковка': 'has_parking',
    'бассейн': 'has_pool',
    'бар/ресторан': 'has_meal',
    'кондиционер': 'conditioning',
    'с животными': 'has_pets',
    'трансфер': 'has_airport_transfer'
}


def get_city_url(country, city):
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
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


def get_filters_url(user_request: UserRequest, url):
    date_in = str(user_request.date_in.replace("-", "."))
    date_out = str(user_request.date_out.replace("-", "."))
    adults = str(user_request.adults)
    childrens = ".".join(map(str, user_request.children_ages))
    stars = ".".join(map(str, user_request.stars))

    meal_types = ""
    for meal_type in user_request.meal_types:
        if meal_type == 'завтрак':
            meal_types += "breakfast."
        elif meal_type == 'завтрак+обед/ужин':
            meal_types += "halfBoard."
        elif meal_type == 'завтрак+обед+ужин':
            meal_types += "fullBoard."
        elif meal_type == 'всё включено':
            meal_types += "allInclusive."
        elif meal_type == 'без питания':
            meal_types += "nomeal."
    if meal_types.endswith('.'):
        meal_types = meal_types[:-1]

    price = user_request.price

    amenities = ""
    for service in user_request.services:
        if service in services_mapping:
            amenities += services_mapping[service] + "."
    if amenities.endswith("."):
        amenities = amenities[:-1]

    return set_filters(url=url, date_in=date_in, date_out=date_out,
                       adults=adults, childrens=childrens, stars=stars,
                       meal_types=meal_types, price=price, amenities=amenities)


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


class OstrovokParser(Parser):
    @staticmethod
    def get_hotels(user_request: UserRequest):
        geolocator = Nominatim(user_agent="user_agent")
        location = geolocator.reverse(user_request.user_point)
        country = location.raw['address'].get('country', '')
        city = location.raw['address'].get('city', '')

        url, driver = get_city_url(country=country, city=city)

        url_with_filters = get_filters_url(user_request=user_request, url=url)

        return find_hotels(driver=driver, hotels_url=url_with_filters,
                           user_point=user_request.user_point, radius=user_request.radius_km)
