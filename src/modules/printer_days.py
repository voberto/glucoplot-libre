from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait
from reportlab.platypus import Image
from reportlab.lib import utils
from reportlab.lib.units import inch, cm

import glob
import os
import datetime

def printer_days(month_number, year_number, glucose_month_avg):
    png_filename = []
    patient_data = []    
    # Search png files in /fig folder for desired month
    if month_number < 10:
        png_filedir = 'figs/glucose-' + str(year_number) + '-0' + str(month_number) + '-*.png'
        pdf_filename = 'glucose-' + str(year_number) + '-0' + str(month_number) + '.pdf'
    else:
        png_filedir = 'figs/glucose-' + str(year_number) + '-' + str(month_number) + '-*.png'
        pdf_filename = 'glucose-' + str(year_number) + '-' + str(month_number) + '.pdf'
    # Append PNG file names to list 
    for name in glob.glob(png_filedir):
        png_filename.append(name)
    # Organize elements of list in alphabetical order
    png_filename = sorted(png_filename)
    # Get size of images list
    png_figs_length = int(len(png_filename))
    # Build canvas for pdf file
    cv = canvas.Canvas(pdf_filename, pagesize=portrait(A4))
    # Save current timestamp to generate report ID 
    now = datetime.datetime.now()
    # Calculate equivalent HbA1c value
    hba1c_value = float((round(glucose_month_avg,2) + 46.7)/28.7)
    # Read patient's and doctor's name from "patient_data.txt" file
    try:
        patient_file = open("patient_data.txt", "r")
        for lines in patient_file:
       	    patient_data.append(lines)
        patient_name_str = "Patient: " + str(patient_data[0])
        patient_name_str = patient_name_str.rstrip()
        doctor_name_str = "Doctor: " + str(patient_data[1])
        doctor_name_str = doctor_name_str.rstrip()
        print("Printing " + str(pdf_filename) + " file ...")
        # First page comprises general data for the month report		   
        cv.drawString(100, 730, "Glucose report number " + str(now))
        cv.drawString(100, 710, patient_name_str)
        cv.drawString(100, 690, doctor_name_str)
        cv.drawString(100, 670, "Month: " + str(month_number))
        cv.drawString(100, 650, "Number of days: " + str(png_figs_length))
        cv.drawString(100, 630, "Average glucose of the period: " + str(round(glucose_month_avg,2)) + " mg/dl")
        cv.drawString(100, 610, "Estimated HbA1c value of the period: " + str(round(hba1c_value, 1)) + " %")
        cv.showPage()
        # Print images in pdf file
        for x in range(0, png_figs_length):
            if x % 2 == 0:
                # Even index for odd day, image will be printed in the higher half of the page
                cv.drawImage(png_filename[x], 85, 450, width=15*cm, height=10*cm, preserveAspectRatio=True)
            if x % 2 != 0:
                # Odd index for even day, image will be printed in the lower half of the page, and the page is shown
                cv.drawImage(png_filename[x], 85, 100, width=15*cm, height=10*cm, preserveAspectRatio=True)
                cv.showPage()
        # Save pdf file
        cv.save()
        print("Printing is finished!")
    except FileNotFoundError:
        print("File \'patient_data.txt\' not found! Create such file with patient's and doctor's names in first and second line, respectively.")