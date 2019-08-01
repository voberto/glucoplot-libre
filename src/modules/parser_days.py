import csv
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import time
import math
from matplotlib import rc

def parser_days(month_number, year_number):
    list_cols = ['line', 'data', 'glucose', 'idk', 'type', 'source']
    index_line = 0
    index_data = 1
    index_glucose = 2
    index_idk = 3
    index_type = 4
    index_source = 5
    # Read csv file created by month parser
    # and create month dataframe
    if(month_number <= 9):
        dataframe_month_filename = 'tables/glucose-' + str(year_number) + '-0' + str(month_number) + '.csv'
    if(month_number > 9):
        dataframe_month_filename = 'tables/glucose-' + str(year_number) + '-' + str(month_number) + '.csv'
    dataframe_month = pd.read_csv(dataframe_month_filename, sep=',')
    dataframe_month = pd.DataFrame(dataframe_month)
    dataframe_month.columns = list_cols
    dataframe_month_data = dataframe_month['data']
    # Extract date from month dataframe
    dataframe_date = dataframe_month_data.apply(lambda x: x.split(' ')[0])
    # Convert dataframes into list
    list_date = dataframe_date.values.T.tolist()
    # Isolate days from date dataframe into separate list
    list_date_days = [datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%d') for x in list_date]
    list_date_days = list(map(int, list_date_days))
    # If list is not empty, it means the user chose a valid month
    if list_date_days:
        # Calculate number of days
        days_number = max(list_date_days)
        # Create CSV file for each day
        list_days_str = []
        dataframe_days = []
        list_days_filename = []
        for x in range(0, days_number):
            if int(month_number) <= 9:
                if x < 9:
                    list_days_str.append(str(year_number) + "-0" + str(month_number) + "-0" + str(x+1))
                else:
                    list_days_str.append(str(year_number) + "-0" + str(month_number) + "-" + str(x+1))
            if int(month_number) > 9:
                if x < 9:
                    list_days_str.append(str(year_number) + "-" + str(month_number) + "-0" + str(x+1))
                else:
                    list_days_str.append(str(year_number) + "-" + str(month_number) + "-" + str(x+1))
            dataframe_days.append(dataframe_month[dataframe_month['data'].str.contains(list_days_str[x])])
            # Delete first column of dataframe because dataframe module adds an index column for rows
            dataframe_days[x] = dataframe_days[x].drop('line', 1)
            list_days_filename.append("tables/glucose-" + list_days_str[x] + ".csv")
            dataframe_days[x].to_csv(list_days_filename[x])
        print("Glucose data from desired month was processed successfully!")
        return days_number
    else:
        print("Desired month not found! Choose a valid month or collect data from the reader again!")