import plotly.graph_objects as go

class map_renderer:
    def generate_map():
        # Координаты центра карты
        center_lat = 51.5074
        center_lon = -0.1278

        # Зум карты
        zoom = 10

        marker_lats = [51.5074, 51.5033, 51.5098]
        marker_lons = [-0.1278, -0.1195, -0.1180]

        # Создание объекта карты
        fig = go.Figure(go.Scattermapbox(
            mode="markers",
            lon=[marker_lons],
            lat=[marker_lats],
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
        fig.show()


if __name__ == '__main__':
    map_renderer.generate_map()

# Отображение карты

#fig.write_image("map.png")

