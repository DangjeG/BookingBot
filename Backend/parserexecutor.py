from typing import List, Any

from Backend.ObjectModels.user_request import UserRequest
from Backend.ObjectModels.hotel import Hotel
from Backend.parsers.parser import Parser


class ParserExecutor:
    parsers = list[Parser]

    def __init__(self, parsers):
        self.parsers = parsers

    def get_hotels(self, usr_req) -> list[Hotel]:
        hotels = []
        for element in self.parsers:
            hotels.extend(element.get_hotels(user_request=usr_req))
        return hotels
