class Hotel:
    def __init__(self, name, address, rating, url):
        self.name = name
        self.address = address
        self.rating = rating
        self.url = url

    def __str__(self):
        return f"Hotel: {self.name}\nAddress: {self.address}\nRating: {self.rating}\nURL: {self.url}"

