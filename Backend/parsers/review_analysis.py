import time
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import umap.umap_ as umap
from bs4 import BeautifulSoup
from matplotlib.colors import ListedColormap
from razdel import sentenize
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from transformers import BertModel, BertTokenizer
import matplotlib.pyplot as plt


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
    vectors = []
    for sentence in sentences:
        encoded_input = tokenizer.encode(str(sentence.text), return_tensors='pt', truncation=True, padding=True)
        outputs = model(encoded_input)
        vector = outputs[0][0].mean(dim=0).detach().numpy()
        help_me[sentence.text] = vector
        vectors.append(vector)

    # Создание экземпляра алгоритма K-средних
    kmeans = KMeans(n_clusters=n_clusters)
    # Процесс кластеризации
    kmeans.fit(vectors)
    # Получение меток кластеров для каждого вектора
    cluster_labels = kmeans.labels_

    reducer = umap.UMAP(7)
    vectors_reduced = reducer.fit_transform(vectors)

    # Создайте DataFrame с данными
    df = pd.DataFrame(vectors_reduced, columns=['UMAP1', 'UMAP2'])
    df['Cluster'] = cluster_labels

    colors = cm.get_cmap('tab10', n_clusters)
    cmap = ListedColormap(colors(np.linspace(0, 1, n_clusters)))

    # Создайте график с помощью Matplotlib
    plt.scatter(df['UMAP1'], df['UMAP2'], c=df['Cluster'], cmap=cmap)
    plt.colorbar()

    # Сохраните график в файл
    plt.savefig("plot.png")

    # Получение центроидов кластеров
    cluster_centers = kmeans.cluster_centers_

    # Создание экземпляра NearestNeighbors
    nbrs = NearestNeighbors(n_neighbors=5, metric='euclidean').fit(vectors)

    # Находим индексы ближайших соседей для каждого вектора из cluster_centers
    distances, indices = nbrs.kneighbors(cluster_centers)

    # Выводим результаты
    for i in range(len(cluster_centers)):
        print(f"Номер группы: {i}")
        print("Предложения из этой группы:")
        for j in range(len(indices[i])):
            sentence = list(help_me.keys())[indices[i][j]]
            print(f"Предложение: {sentence}")
        print()

    print()


if "__name__" == main():
    main()
