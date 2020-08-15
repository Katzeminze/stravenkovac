# from monthly_hours_parser import MonthlyHoursParser
# from common_data import csv_path_travel_costs
# from runner import Runner
# from travel_costs_parser import TravelCostsParser
import os

from stravenkovac.common_data import csv_path_travel_costs
from stravenkovac.runner import Runner

initial_month_directory = r"S:/20_Bericht/2020"
initial_travel_directory = r"S:/30_Reisekosten"
example = r"D:/Python/stravenkovac/Reise"
example_mh = r"D:/Python/stravenkovac"

if __name__ == "__main__":
    # starting the program by providing path to pdf and the month in case of month-hour
    # path = Runner(example_mh, 7)
    # path_to_source_pdfs = path.start()

    path = Runner(example, 7)
    path_to_source_pdfs2 = path.start()

    # print(path_to_source_pdfs)
    # # Parse all month-hour pdfs
    # if path_to_source_pdfs:
    #     for pdf in path_to_source_pdfs:
    #         print(pdf)
    #         Monthly = MonthlyHoursParser(pdf, csv_path_month_hour)
    #         Monthly.load_data_source()
    #         Monthly.extract_data()
    #
    # TravelCosts = TravelCostsParser(pdf_path_travel_costs, csv_path_travel_costs)
    # TravelCosts.load_data_source()
    # TravelCosts.extract_data()

if os.path.exists(csv_path_travel_costs):
    os.remove(csv_path_travel_costs)
# if os.path.exists(csv_path_month_hour):
#     os.remove(csv_path_month_hour)

