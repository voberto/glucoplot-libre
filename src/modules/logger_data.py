import usb
import usb.core
import usb.util
import usb.backend.libusb1
import subprocess
import re

def logger_data_get():
    # Free Style Libre vendor and product IDs
    fslibre_idvendor = 0x1a61
    fslibre_idproduct = 0x3650
    # USB device path
    dev_path_start = "/dev"
    # Find our device
    dev = usb.core.find(idVendor=fslibre_idvendor, idProduct=fslibre_idproduct)
    # Was it found?
    if dev is None:
        print('Reader not found.')
    else:
        print('Reader is connected.')
        # Check for manufacturer's name in the dmesg log lines and save those lines in a txt file
        print('Searching device directory ...')
        subprocess.check_output("dmesg | grep \"Abbott Diabetes Care\" >> usbdevpath.txt", shell=True)
        # Search and store hidraw+{number} in the last saved line from dmesg log txt file
        print('Creating device path ...')
        dev_name = subprocess.check_output("grep -E -o \"hidraw.{0,1}\" usbdevpath.txt | tail -1", shell=True)
        dev_path_end = dev_name.decode("utf-8").rstrip()
        # Generate full /dev path detected after reader's connection
        dev_path_full = dev_path_start + '/' + dev_path_end
        # Request permissions for the reader
        chmod_cmd = "sudo chmod 0666 " + dev_path_full
        print('Requesting permissions ...')
        subprocess.check_output(chmod_cmd, shell=True)
        # Check current directory (where the app was deployed and initialized)
        # to create /figs and /tables folders
        current_path = subprocess.check_output("pwd", shell=True)
        path_decoded = current_path.decode("utf-8").rstrip()
        tables_dir = "/tables"
        figs_dir = "/figs"
        mkdir_tables_cmd_str = "mkdir -p " + path_decoded + tables_dir
        mkdir_figs_cmd_str = "mkdir -p " + path_decoded + figs_dir
        print("Creating /tables and /figs folders (if not already created) ...")
        subprocess.call(mkdir_tables_cmd_str, shell=True)
        subprocess.call(mkdir_figs_cmd_str, shell=True)
        # Send command for the reader to dump data in the glucose.csv file
        glucose_csv_filename = path_decoded + tables_dir + "/glucose.csv"
        print('Dumping data on tables/glucose.csv ...')
        dump_data_cmd = "glucometer --driver fslibre --device " + dev_path_full + " dump >> " + glucose_csv_filename
        subprocess.call(dump_data_cmd, shell=True)
        print('Data dumping complete!')