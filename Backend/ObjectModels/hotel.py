class Hotel:
    def __init__(self, name, address, rating, url, photo):
        self.name = name
        self.address = address
        self.rating = rating
        self.url = url
        self.photo_url = photo

    def __str__(self):
        return f"Hotel: {self.name}\nAddress: {self.address}\nRating: {self.rating}\nURL: {self.url}\nPhoto URL: {self.photo_url}"
