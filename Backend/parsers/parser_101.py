import requests
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


MAIN_PAGE = "https://101hotels.com"


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

                distance = get_distance(hotel_coords=tuple([float(value) for value in float_values]), user_coords=user_point)
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


def get_hotels():
    country = "Россия"
    city = "Челябинск"
    user_point = (55.160797, 61.402509)  # проспект Ленина, 54, Челябинск
    radius_km = 5
    date_in = "03.08.2023"
    date_out = "09.08.2023"
    adults = "2"
    children = ""  # указывается возраст ребёнка,
    # если несколько детей то возраста через запятую
    price = "0-Infinity"
    # без звёзд-0
    stars = "4"
    # завтрак-1, полупансион-2, полныйпансион-3, всёвключено-4
    meal_categories = "1"
    # wifi-19, парковка-14, бассейн-10, бар/ресторан-2
    # кондиционер-5, с животными-96, трансфер-183
    services = "19,7,5"

    country_url = get_country_url(country=country, countries_html=get_source_html(url=MAIN_PAGE + "/countries"))
    city_url = MAIN_PAGE + get_city_url(city=city, country_url=country_url)
    url_with_filters = (city_url + "?in=" + date_in + "&out=" + date_out +
                        "&adults=" + adults + "&children=" + children +
                        "&price=" + price + "&services=" + services + "&stars=" + stars +
                        "&meal_categories=" + meal_categories + "&viewType=list")
    print(url_with_filters)
    print()
    return find_hotels(hotels_url=url_with_filters, user_point=user_point, radius=radius_km)


if __name__ == "__main__":
    hotels = get_hotels()
    for hotel in hotels:
        print(hotel)

# штука для нечёткого поиска города/страны
# нужен список городов/стран
# def get_current_city(user_city):
#     city = re.findall('\w+', all_countries)
#     score = list(map(lambda x: fuzz.QRatio(x.lower(), user_city), city))
#     max_score = max(score)
#     if max_score > 80:
#         print('cool')
#         return [c for (c, s) in zip(city, score) if s == max_score]
#     else:
#         print('fuck')
