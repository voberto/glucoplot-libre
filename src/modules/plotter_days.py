import csv
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
import time
import math
from matplotlib import rc
import numpy as np
import glob

def plotter_days(month_number, year_number):
    try:
        try:
            list_cols = ['line', 'date', 'glucose', 'idk', 'type', 'source']
            index_line = 0
            index_data = 1
            index_glucose = 2
            index_idk = 3
            index_type = 4
            index_source = 5
            day_name_str = []
            day_name_str2 = []
            dataframe_day = []
            dataframe_glucose = []
            list_glucose = []
            dataframe_clock = []
            list_clock = []
            list_clock_hours = []
            list_clock_minutes = []
            list_clock_hourmin_float = []
            val_xmax = []
            val_glucose_max = 110
            val_glucose_min = 70
            file_name_strsize = 29
            list_glucose_length = []
            list_glucose_min = []
            list_glucose_max = []
            rc('text', usetex=False)
            plt.rc('grid', linestyle="-", color='grey')
            plt.rcParams.update({'figure.max_open_warning': 0})
            val_glucose_avg = []
            label_glucose_avg = []
            label_title = []
            fig = []
            ax1 = []
            list_png_title = []
            if month_number > 9:
                filename = "tables/glucose-" + str(year_number) + "-" + str(month_number) + "*.csv"
            if month_number <= 9:
                filename = "tables/glucose-" + str(year_number) + "-0" + str(month_number) + "*.csv"
            filename_list = []
            list_count = []
            # Get and append each non empty daily CSV tables names from desired month
            # to filename list variable
            with open('countfile' , 'w') as out:
                list_of_files = glob.glob(filename)
                for file_name in list_of_files:
                    with open(file_name, 'r') as f:
                        count = sum(1 for line in f)
                        # If there are lines in each daily csv file and
                        # file name string size is correct,
                        # append file name to list 
                        if ((count > 1) and (len(file_name) == file_name_strsize)):
                            filename_list.append(str(file_name))
            # Sorts filenames alphabetically
            filename_list = sorted(filename_list)
            # Select only the datestamp for each png filename 
            list_png_title = [str(str(i[23:25]) + "/" + str(i[20:22]) + "/" + str(i[15:19])) for i in filename_list]
            # Open and read each valid CSV tables
            for file_name in filename_list:
                dataframe_day.append(pd.read_csv(str(file_name), sep=','))
            # Create daily plots from valid dataframes
            for x in range(len(filename_list)):
                dataframe_day[x].columns = list_cols
                # Delete first column of daily dataframe because panda added this column
                # in a struct (csv file) that already inherited this column from 
                # "parser_days.py"
                dataframe_day[x] = dataframe_day[x].drop('line', 1)
                # Extract values from column 'glucose' of 'dataframe_chosendata'
                dataframe_glucose.append(dataframe_day[x].iloc[:,index_glucose-1])
                # Create list with 'dataframe_glucose' values
                list_glucose.append(dataframe_glucose[x].values.T.tolist())
                # Extract hours, minutes and seconds from 'dataframe_day_data'
                # [0] - date
                # [1] - clock
                dataframe_clock.append(dataframe_day[x]['date'].apply(lambda x: x.split(' ')[1]))
                # Create list with 'dataframe_clock' values
                list_clock.append(dataframe_clock[x].values.T.tolist())
                # Extract hours of 'list_clock' and convert each value to integer type
                list_clock_hours.append([datetime.datetime.strptime(x, "%H:%M:%S").strftime("%H") for x in list_clock[x]])
                list_clock_minutes.append([datetime.datetime.strptime(x, "%H:%M:%S").strftime("%M") for x in list_clock[x]])
                # Convert each clock list values to float type
                list_clock_hourmin_float.append([(float(z) + float(y)/60) for z, y in zip(list_clock_hours[x], list_clock_minutes[x])])
                # Calculate maximum x value to limit x axis ticks
                val_xmax.append(24)
                # Create lists of minimum and maximum values for target glucose
                list_glucose_length.append(len(list_clock_hourmin_float[x]))
                list_glucose_min.append([val_glucose_min] * list_glucose_length[x])
                list_glucose_max.append([val_glucose_max] * list_glucose_length[x])
                # Calculate glucose average value of given day
                val_glucose_avg.append(sum(list_glucose[x])/len(list_glucose[x]))
                label_glucose_avg.append('Average = ' + str(round(val_glucose_avg[x],2)) + ' mg/dl')
                #label_title.append('Glucose profile: ' + str(filename_list[x]))
                label_title.append("Glucose daily profile -> " + str(list_png_title[x]))
                # Plot glucose of chosen day
                fig.append(plt.figure(figsize=(15/2.54, 10/2.54)))
                ax1.append(fig[x].add_subplot(111))
                plt.locator_params(axis='x', nbins=val_xmax[x])
                plt.title(label_title[x], fontsize=14)
                plt.xlabel('Hour', fontsize=12)
                plt.ylabel('Glucose [mg/dl]', fontsize=12)
                plt.xlim([0, val_xmax[x]])
                plt.ylim([0, 500])
                plt.plot(list_clock_hourmin_float[x], list_glucose[x], label=label_glucose_avg[x])
                plt.plot(list_clock_hourmin_float[x], list_glucose_max[x], linestyle='--', color='red')
                plt.plot(list_clock_hourmin_float[x], list_glucose_min[x], linestyle='--', color='red')
                plt.grid(which='both', alpha=0.3)
                plt.legend(loc='upper left', fontsize=10)
                plt.tight_layout()
            # Create figure name list elements by removing "tables/" and ".csv" from 
            # CSV filename list corresponding elements
            figname = [x[7:-4] for x in filename_list]
            # Save figure as png
            print("Saving figures (this process can take a while) ...")
            for i in plt.get_fignums():
                plt.figure(i)
                days_figname = "figs/" + str(figname[i-1]) + ".png"
                plt.savefig(days_figname, bbox_inches='tight', dpi=300)
                plt.close(i)
            glucose_month_avg = sum(val_glucose_avg)/len(val_glucose_avg)
            hba1c_value = float((round(glucose_month_avg,2) + 46.7)/28.7)
            print("Number of days with valid glucose data: " + str(len(filename_list)))
            return glucose_month_avg, hba1c_value
        except ZeroDivisionError:
            print("Cannot find glucose images from desired month! Run \'parse <month_index>\' to process collected data from the reader.")
            glucose_month_avg = 0
            hba1c_value = 0
            return glucose_month_avg, hba1c_value
    except FileNotFoundError:
        print("Cannot find daily tables for desired month! Run \'parse <month_index>\' to process collected data from the reader.")