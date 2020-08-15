import csv
import tabula

import Exceptions_stravenkovac
from parser_interface import ParserInterface
import pandas as pd
import re
from datetime import datetime
import copy
import os

class TravelCostsParser(ParserInterface):
    def __init__(self, path, path_to):
        self.initial_path = path
        if not os.path.exists(path_to):
            with open(path_to, 'a'):
                pass
        self.path_to_csv = path_to

    def __parse_date(self, list_of_journeys, str_to_process):
        date_entity = []
        date = re.findall(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", str_to_process)
        print(date)
        time = re.findall(r"[\d]{1,2}:[\d]{1,2}", str_to_process)
        for (date_particular, time_particular) in zip(date, time):
            resulted_date = date_particular + ' ' + time_particular
            date_entity.append(datetime.strptime(resulted_date, '%d-%m-%y %H:%M'))
        list_of_journeys.append(copy.deepcopy(date_entity))
        date_entity.clear()
        return list_of_journeys

    def load_data_source(self):
        # tmp = tabula.read_pdf_with_template(self.initial_path, "json2.json.txt")
        # print(tmp)
        # tabula.convert_into(self.initial_path, self.path_to_csv, output_format="csv", pages='all', stream=True, multiple_tables=True)
        data_to_csv = pd.DataFrame()
        name_and_date = tabula.read_pdf(self.initial_path, area=[0, 0, 200, 600], pages='all')
        # print(name_and_date)
        # print(type(name_and_date[0]))
        for dataframe in name_and_date:
            data_to_csv = data_to_csv.append(dataframe)
        print(data_to_csv)
        data_to_csv.to_csv(self.path_to_csv)

    def extract_data(self):
        list_of_journeys = []
        name_str = "Name and Address:"
        date_str = "Start of Journey:"
        with open(self.path_to_csv, 'r') as read_obj:
            while True:
                line = read_obj.readline()
                if len(line) == 0:
                    break
                if name_str in line:
                    try:
                        emploee_name = line.split(",,,")[1]
                    except IndexError:
                        print("Employee name was not found")
                if date_str in line:
                    list_of_journeys = self.__parse_date(list_of_journeys, line)

        print(list_of_journeys)
        for date_list in list_of_journeys:
            if date_list[0] > date_list[1]:
                raise Exceptions_stravenkovac.DateIsInappropriate("The time of starting the journey is smaller than the time of its end")
            print(date_list[1] - date_list[0])
    # def __init__(self):
    #     self.travel_info = {}
    #
    # def load_data_sourse(self, input_path):
    #     pass
