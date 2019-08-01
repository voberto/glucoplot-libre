from cmd import Cmd
import sys
import subprocess

import modules.logger_data as logger_data
import modules.parser_month as parser_month
import modules.parser_days as parser_days
import modules.plotter_days as plotter_days
import modules.printer_days as printer_days
import modules.check_cmd as check_cmd

days_number = 0
glucose_month_avg = 0
hba1c_value = 0
list_months_valid = []

class GlucoPlot_REPL(Cmd):
    def do_get(self, args):
        """
Check if reader is connected. If positive, send request to dump data on .csv file.
Usage: get
        """
        if len(args) == 0:
            logger_data.logger_data_get()
        else:
            print("Incorrect usage of command \'get\'! Execute \'help get\' to see available options.")

    def do_check(self, args):
        """
Check existing months with associated year in the glucose.csv file
Usage: check
        """
        global list_months_valid
        if(list_months_valid is not None):
            del list_months_valid[:]
        if len(args) == 0:
            list_months_valid = check_cmd.func_check_cmd()
            if(list_months_valid is not None):
                print('\nFollowing months with respective year are available in the glucose table:')
                for i in range(len(list_months_valid)):
                    print('[',i+1,'] -> ', list_months_valid[i])
                str_process_user = '\nType \'process\' + desired month index (1 to ' + str(len(list_months_valid)) + ') and press \'Enter\' to print daily glucose curves ...'
                print(str_process_user)
        else:
            print("Incorrect usage of command \'check\'! Execute \'help check\' to see available options.")

    def do_process(self, args):
        """
Parse, plot and print daily glucose curves
in a PDF file for desired month
Usage: process <month_index>
<month_index> = integer representing a valid
month found in the glucose table
        """
        global glucose_month_avg
        global hba1c_value
        global list_months_valid
        args = args.split()
        current_path = subprocess.check_output("pwd", shell=True)
        path_decoded = current_path.decode("utf-8").rstrip()
        dataframe_filename = path_decoded + '/tables/glucose.csv'
        if len(args) == 1:
            # If valid months list is not empty
            if(list_months_valid):
                # If desired month index is out of range
                if(int(args[0]) < 1 or int(args[0]) > len(list_months_valid)):
                    print('Desired month index is not valid!')
                    print('\nFollowing months with respective year are available in the glucose table:')
                    for i in range(len(list_months_valid)):
                        print('[',i+1,'] -> ', list_months_valid[i])
                # If month index is valid
                else:
                    ## PARSE
                    # Get month and year from the selected month index
                    print("\n### 1 - PARSE ###")
                    month_value = int(list_months_valid[int(args[0])-1][5:])
                    year_value = int(list_months_valid[int(args[0])-1][:4])
                    parser_month.parser_month(month_value, year_value, dataframe_filename)
                    # Create daily dataframes for desired month
                    days_number = parser_days.parser_days(month_value, year_value)
                    ## PLOT
                    # Plot and save daily glucose graphics for desired month
                    print("\n### 2 - PLOT ###")
                    glucose_month_avg, hba1c_value = plotter_days.plotter_days(month_value, year_value)
                    print("Average glucose of the month: " + str(round(glucose_month_avg,2)) + " mg/dl.")
                    print("Equivalent HbA1c value of the month: " + str(round(hba1c_value, 1)) + " %.")
                    ## PRINT
                    # Print daily glucose curves for desired month index in a PDF file
                    print("\n### 3 - PRINT ###")
                    printer_days.printer_days(month_value, year_value, glucose_month_avg)
                    print()
            else:
                print('Cannot find any valid month! Run \'check\' command to get available months from the glucose table.') 
        else:
            print("Incorrect usage of command \'process\'! Execute \'help process\' to see available options.")

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        print()
        raise SystemExit

# Startup routine
def func_glucoplot_startup():
    global list_months_valid
    if(list_months_valid is not None):
        del list_months_valid[:]
    print()
    print('Welcome to the glucoplot-libre command line interface!')
    print('\nSearching for existing \'glucose.csv\' file ...') 
    list_months_valid = check_cmd.func_check_cmd()
    if(list_months_valid is not None):
        if(len(list_months_valid) > 0):
            print('\nFollowing months with respective year are available in the existing glucose table:')
            for i in range(len(list_months_valid)):
                print('[',i+1,'] -> ', list_months_valid[i])
    print('Type \'help\' to see available commands.')

# Main loop    
if __name__ == '__main__':
    glucoplot_REPL = GlucoPlot_REPL()
    glucoplot_REPL.prompt = '> '
    func_glucoplot_startup()
    glucoplot_REPL.cmdloop()