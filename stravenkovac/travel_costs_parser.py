import csv
import tabula
from parser_interface import ParserInterface

class TravelCostsParser(ParserInterface):
    def __init__(self):
        self.travel_info = {}

    def load_data_sourse(self, input_path):
        pass