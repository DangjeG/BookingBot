import time
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from bs4 import BeautifulSoup
from matplotlib.colors import ListedColormap
from razdel import sentenize
import umap.umap_ as umap
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


def analyze(hotel_url):
    reviews = parse_review(hotel_url)
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

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(vectors)
    cluster_labels = kmeans.labels_
    reducer = umap.UMAP(7)
    vectors_reduced = reducer.fit_transform(vectors)
    df = pd.DataFrame(vectors_reduced, columns=['UMAP1', 'UMAP2'])
    df['Cluster'] = cluster_labels
    colors = cm.get_cmap('tab10', n_clusters)
    cmap = ListedColormap(colors(np.linspace(0, 1, n_clusters)))
    plt.scatter(df['UMAP1'], df['UMAP2'], c=df['Cluster'], cmap=cmap)
    plt.colorbar()
    plt.savefig("plot.png")
    cluster_centers = kmeans.cluster_centers_
    nbrs = NearestNeighbors(n_neighbors=5, metric='euclidean').fit(vectors)
    distances, indices = nbrs.kneighbors(cluster_centers)

    results = []
    for i in range(len(cluster_centers)):
        results.append(f"Номер группы: {i}")
        results.append("Предложения из этой группы:")
        for j in range(len(indices[i])):
            sentence = list(help_me.keys())[indices[i][j]]
            results.append(sentence)
        results.append("\n")

    return results
