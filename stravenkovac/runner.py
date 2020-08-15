import os
import re
import tabula
from Exceptions_stravenkovac import FolderNotFound
from common_data import csv_path_month_hour, pdf_path_travel_costs, csv_path_travel_costs
from monthly_hours_parser import MonthlyHoursParser
from travel_costs_parser import TravelCostsParser


class Runner:
    def __init__(self, directory, month, year=2020):
        self.directory_path = directory
        self.month = month
        self.year = year

    def __check_existence(self):
        month_folder = ''
        month_name = ''
        list_of_pdfs = []
        for (rootDir, subDirs, files) in os.walk(self.directory_path):
            for subDir in subDirs:
                if str(self.month) in subDir:
                    try:
                        month_name = str(re.split('_', subDir)[1])
                    except IndexError:
                        break
                    month_folder = os.path.join(self.directory_path, subDir)
                    for filename in os.listdir(month_folder):
                        if filename.startswith(month_name) or not filename.endswith(".pdf"):
                            continue
                        else:
                            path_to_source_pdf = os.path.join(month_folder, filename)
                            list_of_pdfs.append(path_to_source_pdf)
                            # print(path_to_source_pdf, len(list_of_pdfs))
        if month_folder == '':
            raise FolderNotFound("Folder for month " + str(self.month) + " was not found")

        return list_of_pdfs  # path_to_source_pdf

    def __parse_name_travel(self, folder_by_name):
        path_to_year_folder = ''
        p = os.listdir(folder_by_name)
        for item in p:
            item_path = os.path.join(folder_by_name, item)
            if os.path.isdir(item_path) and item.startswith(str(self.year)):
                path_to_year_folder = item_path
            else:
                continue
        return path_to_year_folder

    def __create_travel_object(self, folder_path):
        for file in os.listdir(folder_path):
            pdf = os.path.join(folder_path, file)
            if os.path.isfile(pdf) and pdf.endswith(".pdf"):
                print(pdf)
                travelCosts = TravelCostsParser(pdf, csv_path_travel_costs)
                travelCosts.load_data_source()
                travelCosts.extract_data()

    def __check_existence_travel(self):
        month_folder = ''
        for item in os.listdir(self.directory_path):
            if os.path.isdir(os.path.join(self.directory_path, item)) and not item.startswith('_'):
                print(item)
                year_folder = self.__parse_name_travel(os.path.join(self.directory_path, item))
                print(year_folder)
                for month in os.listdir(year_folder):
                    if str(self.month) in month:
                        month_folder = os.path.join(year_folder, month)
                        print(month_folder)
                        self.__create_travel_object(month_folder)
            else:
                print("File directory is empty or file format is wrong")
                return None
        # if month_folder:
        #     return month_folder
        # else:
        #     return 0

        # month_folder = ''
        # month_name = ''
        # list_of_pdfs = []
        # for (rootDir, subDirs, files) in os.walk(self.directory_path):
        #     for subDir in subDirs:
        #         if subDir.startswith('_'):
        #             continue
        #         if self.year in subDir:
        #             year_folder = self.directory_path + '/' + subDir
        #         else:
        #             print(subDir)

        # print(self.year)

    def start(self):
        """Choosing the file to parse"""
        if "20_Bericht" in self.directory_path:
            result = self.__check_existence()
            print(result, len(result))
            # monthly = MonthlyHoursParser("S:/20_Bericht/2020/07_July\\Month hour registration_07_2020_Ales_Cepelak_2.pdf", "month_hour.csv")
            # monthly.load_data_source()
            # print(help(tabula.io.build_options))
            # if result:
            #     for pdf in result:
            #         print(pdf)
            #         monthly = MonthlyHoursParser(pdf, "month_hour.csv")
            #         monthly.load_data_source()
            #         monthly.extract_data()
        elif "30_Reisekosten" in self.directory_path:
            print("To be continue")
            self.__check_existence_travel()

        else:
            print("Unknown path")
            self.__check_existence_travel()

        # self.__open_month_hour(path_to_source_pdf)




