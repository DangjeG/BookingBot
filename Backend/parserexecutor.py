from typing import List, Any

from Backend.ObjectModels import user_request
from Backend.ObjectModels.hotel import Hotel
from parsers.parser import Parser
from parsers import ostrovok_parser
from parsers import parser_101


class ParserExecutor:
    parsers = list[Parser]

    def __init__(self, parsers):
        self.parsers = parsers

    def get_hotels(self, usr_req: user_request) -> list[Hotel]:
        hotels = []
        for element in self.parsers:
            hotels.extend(element.get_hotels(usr_req=usr_req))
        return hotels
