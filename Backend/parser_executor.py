class parser_executor:
    parsers = []

    def __init__(self, parsers):
        self.parsers = parsers

    def get_hotels(self):
        hotels = []
        for parser in self.parsers:
            hotels.extend(parser.get_hotels)
        return hotels
