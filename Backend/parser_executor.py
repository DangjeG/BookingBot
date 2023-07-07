from typing import List, Any

from Backend.ObjectModels import user_request
from Backend.ObjectModels.hotel import Hotel
from parsers.parser import parser


class parser_executor:
    parser = list[parser]

    def __init__(self, parsers):
        self.parsers = parsers

    def get_hotels(self, usr_req: user_request) -> list[Hotel]:
        hotels = []
        for element in self.parsers:
            hotels.extend(element.get_hotels(usr_req=usr_req))
        return hotels
