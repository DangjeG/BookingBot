from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


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
                        "Button-module__button--MR2Ly."
                        "Button-module__button_size_m--184Hw."
                        "Button-module__button_wide--eV274").click()
    url = driver.current_url

    return url


def main():
    country = "Чехия"
    city = "Прага"
    user_point = (55.160797, 61.402509)
    radius_km = 5
    date_in = "14.08.2023"
    date_out = "31.08.2023"
    adults = "2"
    childrens = "10.15.3"  # указывается возраст ребёнка,
    # если несколько детей то возраста через точку
    # минимальное 100 рублей, максимум 100.000
    price = "0-10000"
    # звёзды 1-5 через точку
    stars = "1.2.3"

    url = get_city_url(country, city, date_in, date_out, adults, childrens)

    url = url.split('dates=')[0] + 'dates=' + date_in + "-" + date_out + '&' + '&'.join(
        url.split('&')[1:])

    if childrens is None:
        url = url.split('guests=')[0] + 'guests=' + adults + '&' + '&'.join(
            url.split('&')[1:])
    else:
        url = url.split('guests=')[0] + 'guests=' + adults + "and" + childrens + '&' + '&'.join(
            url.split('&')[1:])

    city_url = url.replace("price=one", "price=" + price + ".one")

    if stars != "":
        city_url = city_url + "&stars=" + stars
    print(city_url)


if __name__ == "__main__":
    main()
