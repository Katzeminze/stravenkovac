import csv
import tabula


import pandas as pd
import re
from datetime import datetime
import copy
import os

from stravenkovac.common_data import required_WH, dictionary_TH
from stravenkovac.exceptions_stravenkovac import DateIsInappropriate
from stravenkovac.parser_interface import ParserInterface


class TravelCostsParser(ParserInterface):
    """Initialize data for TravelCostParsel and create a csv file if it does not exist"""
    def __init__(self, path, path_to, employee_name):
        self.initial_path = path
        if not os.path.exists(path_to):
            with open(path_to, 'a'):
                pass
        self.path_to_csv = path_to
        self.employee_name = employee_name

    def __parse_date(self, list_of_journeys, str_to_process):
        """Parse dates of the appropriate format"""
        date_entity = []
        date = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", str_to_process)
        # date = re.findall(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", str_to_process)
        time = re.findall(r"[\d]{1,2}:[\d]{1,2}", str_to_process)
        if date and time:
            for (date_particular, time_particular) in zip(date, time):
                resulted_date = date_particular + ' ' + time_particular
                try:
                    date_entity.append(datetime.strptime(resulted_date, '%m/%d/%Y %H:%M'))
                #     date_entity.append(datetime.strptime(resulted_date, '%d-%m-%y %H:%M'))
                except ValueError:
                    raise ValueError(
                        "Error: Incorrect date format. It must be like 'dd-mm-yy' (ex: '01-07-20 12:00').")
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
                        print("Employee ", emploee_name)
                    except IndexError:
                        print("Employee name was not found")
                if date_str in line:
                    list_of_journeys = self.__parse_date(list_of_journeys, line)

        print("List ", list_of_journeys)
        if list_of_journeys:
            stravenky_counter = 0
            for date_list in list_of_journeys:
                if date_list[0] > date_list[1]:
                    raise DateIsInappropriate("The time of starting the journey is smaller than the time of its end")
                overall_travel_time_in_hours = (date_list[1] - date_list[0]).total_seconds()/3600
                print(overall_travel_time_in_hours)
                if overall_travel_time_in_hours > required_WH:
                    stravenky_counter += 1
            if stravenky_counter > 0:
                dictionary_TH[self.employee_name] = stravenky_counter
            else:
                dictionary_TH[self.employee_name] = 0

        for k, v in dictionary_TH.items():
            print(k, v)



