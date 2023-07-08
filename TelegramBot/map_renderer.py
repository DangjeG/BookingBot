import plotly.graph_objects as go

# Координаты центра карты
center_lat = 51.5074
center_lon = -0.1278

# Зум карты
zoom = 15

# Создание объекта карты
fig = go.Figure(go.Scattermapbox(
    mode="markers",
    lon=[center_lon],
    lat=[center_lat],
    marker={'size': 15, 'color': 'red'}
))

# Настройка параметров карты
fig.update_layout(
    mapbox={
        'center': {'lon': center_lon, 'lat': center_lat},
        'style': "open-street-map",
        'zoom': zoom
    },
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0}
)

# Отображение карты
# fig.show()
fig.write_image("map.png")

