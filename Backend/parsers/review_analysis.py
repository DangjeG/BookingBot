import time
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from razdel import sentenize
from transformers import BertModel, BertTokenizer
import umap.umap_ as umap
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


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


def main():
    reviews = parse_review("https://101hotels.com/main/cities/chelyabinsk/gostinitsa_markshtadt.html?adults=2&in=03.08.2023&out=09.08.2023&selected_room_id=2247336&selected_placement_id=544804")
    sentences = list(sentenize(reviews))
    n_clusters = 8

    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model = BertModel.from_pretrained('bert-base-multilingual-cased')
    help_me = dict()
    vectors = np.ndarray
    for sentence in sentences:
        encoded_input = tokenizer.encode(str(sentence.text), return_tensors='pt', truncation=True, padding=True)
        outputs = model(encoded_input)
        vector = outputs[0][0].mean(dim=0).detach().numpy().reshape(-1, 1)
        help_me[sentence.text] = vector
        vectors = np.append(vectors, vector)
    vectors = np.delete(vectors, 0).reshape(-1, 1)

    # silhouette_scores = []  # Список для хранения оценок силуэта для различных чисел кластеров
    # for n_cluster in range(2, 10):
    #     kmeans = KMeans(n_clusters=n_cluster)
    #     try:
    #         kmeans.fit(vectors)
    #     except TypeError:
    #         continue
    #     cluster_labels = kmeans.labels_
    #
    #     # Силуэтный коэффициент
    #     silhouette_avg = silhouette_score(vectors, cluster_labels)
    #     silhouette_scores.append(silhouette_avg)
    #
    # # Найдем оптимальное количество кластеров, которое соответствует максимальному силуэтному коэффициенту
    # optimal_n_clusters = silhouette_scores.index(
    #     max(silhouette_scores)) + 2  # +2 потому что мы начинаем с 2 кластеров

    # Создание экземпляра алгоритма K-средних
    kmeans = KMeans(n_clusters=n_clusters)
    # Процесс кластеризации
    kmeans.fit(vectors)
    # Получение меток кластеров для каждого вектора
    cluster_labels = kmeans.labels_

    # Получение центроидов кластеров
    cluster_centers = kmeans.cluster_centers_
    # cluster_centroid = np.mean(vectors)

    reducer = umap.UMAP(6)
    vectors_reduced = reducer.fit_transform(vectors)

    # Создайте DataFrame для удобства визуализации
    df = pd.DataFrame(vectors_reduced, columns=['UMAP1', 'UMAP2'])
    df['Cluster'] = cluster_labels  # добавьте метки кластеров в DataFrame

    # Визуализируйте результаты с помощью Plotly
    fig = px.scatter(df, x='UMAP1', y='UMAP2', color='Cluster')  # используйте метки кластеров для окрашивания точек
    fig.write_image("plot.png")


if "__name__" == main():
    main()
