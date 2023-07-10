class Hotel:
    def __init__(self, name, address, rating, url, photo):
        self.name = name
        self.address = address
        self.rating = rating
        self.url = url
        self.photo_url = photo

    def __str__(self):
        return f"Название: {self.name}\n" \
               f"Адрес: {self.address}\n" \
               f"Рейтинг: {self.rating}\n" \
               f"URL: {self.url}" \

