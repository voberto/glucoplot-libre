import csv
import pandas as pd 
import datetime
import time
import math
import subprocess
import re

def func_check_cmd():
    # Get glucose.csv filename with full path
    current_path = subprocess.check_output("pwd", shell=True)
    path_decoded = current_path.decode("utf-8").rstrip()
    dataframe_filename = path_decoded + '/tables/glucose.csv' 
    # Get current and last years
    year_current = datetime.datetime.now().year
    year_last = year_current - 1
    month_ocurrence_counter_year_last = [0,0,0,0,0,0,0,0,0,0,0,0]
    month_ocurrence_counter_year_current = [0,0,0,0,0,0,0,0,0,0,0,0]
    month_valid_year_last = []
    month_valid_year_current = []
    month_valid_year_both = []
    try:
        # Read glucose.csv file
        list_cols = ['date', 'glucose', 'idk', 'type', 'source']
        dataframe_main = pd.read_csv(dataframe_filename, sep=',', index_col=None)
        dataframe_main = pd.DataFrame(dataframe_main)
        dataframe_main.columns = list_cols
        # Extract date column as a list
        list_dates_from_dt = dataframe_main['date'].tolist()
        # Assemble strings with months and years
        list_str_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for str_month, pos_month in enumerate(list_str_months, 0):
            # Month lower than 10
            if(str_month < 9):
                str_month_with_year_last = str(year_last) + '-0' + str(str_month+1)
                str_month_with_year_current = str(year_current) + '-0' + str(str_month+1)
            # Month higher than 10
            else:
                str_month_with_year_last = str(year_last) + '-' + str(str_month+1)
                str_month_with_year_current = str(year_current) + '-0' + str(str_month+1)
            # Count number of glucose readings for each month with last and current year in list
            for str_dates in enumerate(list_dates_from_dt):
                # Last year
                if(str_month_with_year_last in str(str_dates)):
                    month_ocurrence_counter_year_last[str_month] += 1
                # Current year
                if(str_month_with_year_current in str(str_dates)):
                    month_ocurrence_counter_year_current[str_month] += 1
            # Assemble list containing months (plus respective year) found in the search performed above
            if(month_ocurrence_counter_year_last[str_month] > 1):
                month_valid_year_last.append(str_month_with_year_last)
            if(month_ocurrence_counter_year_current[str_month] > 1):
                month_valid_year_current.append(str_month_with_year_current)
        month_valid_year_both = month_valid_year_last + month_valid_year_current
        return(month_valid_year_both)
    except FileNotFoundError:
        print("Cannot find \'glucose.csv\' file! Connect the reader to the computer and run \'get\' to collect stored data from the sensor.")