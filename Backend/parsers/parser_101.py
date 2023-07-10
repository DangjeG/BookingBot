import requests
from geopy import Nominatim
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from geopy.distance import great_circle as gd
from selenium.webdriver.support.wait import WebDriverWait
from Backend.ObjectModels.hotel import Hotel
import re

from Backend.ObjectModels.user_request import UserRequest
from Backend.parsers.parser import Parser

MAIN_PAGE = "https://101hotels.com"
services_mapping = {
    'wifi': '19',
    'парковка': '14',
    'бассейн': '10',
    'бар/ресторан': '2',
    'кондиционер': '5',
    'с животными': '96',
    'трансфер': '183'
}


def get_source_html(url):
    return requests.Session().get(url=url).text


def get_country_url(country, countries_html):
    soup = BeautifulSoup(countries_html, "lxml")
    country_divs = soup.find_all("div", class_="item")

    for country_div in country_divs:
        if country_div.find("div", class_="item-country-inner").find("a").get("title") == country:
            return MAIN_PAGE + country_div.find("div", class_="item-country-inner").find("a").get("href") + "/cities"

    raise Exception("Страна не найдена")


def get_city_url(city, country_url):
    cities_html = get_source_html(country_url)
    soup = BeautifulSoup(cities_html, "lxml")
    letter_containers = soup.find_all("div", class_="letter-container clearfix")

    for container in letter_containers:
        li = container.find_all("li")
        for current_city in li:
            if current_city.find("a").getText() == city:
                return current_city.find("a").get("href")

    raise Exception("Город не найден")


def get_distance(hotel_coords, user_coords):
    return gd((user_coords[0], user_coords[1]), (hotel_coords[0], hotel_coords[1])).km


def find_hotels(hotels_url, user_point, radius):
    hotels = list()
    options = Options()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(hotels_url)
    WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loader-text')))

    while True:
        try:
            soup = BeautifulSoup(driver.page_source, "lxml")
            if not re.search(r'<div class="hotels-not-found" style="display: none;">', str(soup)):
                return hotels

            ul = soup.find("ul", class_="unstyled clearfix hotellist list")
            li = ul.find_all("li", class_=["item", "some-hotels-found"])
            for item in li:
                if 'some-hotels-found' in item.get('class', []):
                    break

                float_values = ((item.find("div", class_="item-meta clearfix").
                                 find("div", class_="pull-left").
                                 find("div", class_="item-address-wrap js-on-map tooltip").
                                 get("data-hotel-coords"))[1:-1]).split(",")

                distance = get_distance(hotel_coords=tuple([float(value) for value in float_values]),
                                        user_coords=user_point)
                if distance <= radius:
                    name = item.find('span', itemprop='name').text
                    address = item.find('span', itemprop='streetAddress').text
                    rating = item.find('span', itemprop='ratingValue').text
                    url = MAIN_PAGE + item.find('a', itemprop='url')['href']
                    photo = item.find('img', itemprop='image')['src']
                    hotels.append(Hotel(name, address, rating, url, photo))
            try:
                next_button = driver.find_element(By.XPATH, '//a[@class="page-link next"]')
                if 'disabled' in next_button.find_element(By.XPATH, './..').get_attribute('class'):
                    break
                next_button.click()
            except KeyboardInterrupt:
                break
        except NoSuchElementException:
            break

        return hotels


def get_filters_url(user_request: UserRequest):
    date_in = str(user_request.date_in.replace("-", "."))
    date_out = str(user_request.date_out.replace("-", "."))
    adults = str(user_request.adults)
    children = ",".join(map(str, user_request.children_ages))
    price = user_request.price
    stars = ",".join(map(str, user_request.stars))
    meal_categories = ""
    for meal_type in user_request.meal_types:
        if meal_type == 'завтрак':
            meal_categories += "1,"
        elif meal_type == 'завтрак+обед/ужин':
            meal_categories += "2,"
        elif meal_type == 'завтрак+обед+ужин':
            meal_categories += "3,"
        elif meal_type == 'всё включено':
            meal_categories += "4,"
    if meal_categories.endswith(","):
        meal_categories = meal_categories[:-1]
    services = ""
    for service in user_request.services:
        if service in services_mapping:
            services += services_mapping[service] + ","
    if services.endswith(","):
        services = services[:-1]

    return ("?in=" + date_in + "&out=" + date_out +
            "&adults=" + adults + "&children=" + children +
            "&price=" + price + "&services=" + services + "&stars=" + stars +
            "&meal_categories=" + meal_categories + "&viewType=list")


class Parser101Hotels(Parser):
    @staticmethod
    def get_hotels(user_request):
        geolocator = Nominatim(user_agent="user_agent")
        location = geolocator.reverse(user_request.user_point)
        country = location.raw['address'].get('country', '')
        if country != "Россия":
            return []
        
        city = location.raw['address'].get('city', '')

        country_url = get_country_url(country=country, countries_html=get_source_html(url=MAIN_PAGE + "/countries"))
        city_url = MAIN_PAGE + get_city_url(city=city, country_url=country_url)
        url_with_filters = city_url + get_filters_url(user_request)

        return find_hotels(hotels_url=url_with_filters, user_point=user_request.user_point,
                           radius=user_request.radius_km)
