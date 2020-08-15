import csv
import tabula

from Exceptions_stravenkovac import FormatIsInappropriate
from parser_interface import ParserInterface
import os
import re
import pandas as pd


class MonthlyHoursParser(ParserInterface):
    def __init__(self, path, path_to):
        self.initial_path = path
        with open(path_to, 'a'):
            pass
        self.path_to_csv = path_to
        self.filename = os.path.basename(self.initial_path)

    def __is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def load_data_source(self):
        # tabula.convert_into(self.initial_path, self.path_to_csv, output_format="csv", pages=[1], stream=True)
        data_to_csv = pd.DataFrame()
        name_and_date = tabula.read_pdf(self.initial_path, area=[0, 0, 150, 800], pages='all', stream=True)  #, java_options ="-Dfile.encoding=UTF16"
        # print(name_and_date)
        # print(type(name_and_date[0]))
        for dataframe in name_and_date:
            data_to_csv = data_to_csv.append(dataframe)
        print(data_to_csv)
        data_to_csv.to_csv(self.path_to_csv)

    def extract_data(self):
        list_of_days = []
        list_of_working_hours = []
        name_str = None
        counter = 0
        time_str = "TIME"
        hours_str = "Hours worked"
        with open(self.path_to_csv, 'r') as read_obj:
            while True:
                line = read_obj.readline()
                if len(line) == 0:
                    break
                if time_str in line:
                    list_of_days = [s for s in re.split(",| ", line) if (self.__is_float(s) or s.isdigit())]
                    print(list_of_days, len(list_of_days))
                if hours_str in line:
                    try:
                        list_of_working_hours = [s for s in re.split(",| ", line.split(')')[1]) if (self.__is_float(s) or s.isdigit())]
                        print(list_of_working_hours, len(list_of_working_hours))
                    except IndexError:
                        print("Could not parse the file {} correctly. Try to obtain/calculate the data by your own.".format(self.filename))
                    # for int_character in hours_str:
                    #     if self.__is_float(int_character) or int_character.isdigit():
                    #         counter += 1
                    # if counter != 0:
                    #     list_of_working_hours = [s for s in re.split(",| ", line.split(')')[1]) if (self.__is_float(s) or s.isdigit())]
                    #     print(list_of_working_hours, len(list_of_working_hours))
                    # else:
                    #     error_format = "Could not parse the file {} correctly. Try to obtain/calculate the data by your own.".format(
                    #         self.filename)

                        # raise Exception(error_format)
                        # line = read_obj.readline()
                        # matches = re.findall(r'\"(.+?)\"', line)  #new_line = line.split("\"")
                        # print(matches)
                        # list_of_working_hours = [s for s in re.split(",| ", line) if (self.__is_float(s) or s.isdigit())]
                        # print(list_of_working_hours, len(list_of_working_hours))