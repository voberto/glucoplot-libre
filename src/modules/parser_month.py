import csv
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import time
import math
from matplotlib import rc

def parser_month(month_number, year_number, datafile_str):
    list_cols = ['date', 'glucose', 'idk', 'type', 'source']
    index_data = 0
    index_glucose = 1
    index_idk = 2
    index_type = 3
    index_source = 4
    # Read csv file created with data dumped by the reader
    # and create main dataframe
    dataframe_main = pd.read_csv(datafile_str, sep=',')
    dataframe_main = pd.DataFrame(dataframe_main)
    dataframe_main.columns = list_cols
    # Creates date string
    if(int(month_number) <= 9):
        str_month = str(year_number) + '-0' + str(month_number)
    if(int(month_number) > 9):
        str_month = str(year_number) +'-' + str(month_number)    
    # Extract and save last month glucose measurements from main dataframe
    dataframe_month = dataframe_main[dataframe_main['date'].str.contains(str_month)]
    dataframe_month_filename = "tables/glucose-" + str_month + ".csv"
    dataframe_month = pd.DataFrame(dataframe_month)
    # Delete duplicates
    dataframe_month.drop_duplicates(inplace=True)
    dataframe_month.to_csv(dataframe_month_filename)