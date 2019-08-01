# glucoplot-libre
Glucose report generator for FreeStyle Libre device.

This project provides a linux-compatible command line interface capable of generating PDF reports with glucose data dumped from the FreeStyle Libre CGM system.

## 1 - For non-developers

1 - Download the '/app' folder;

2 - Open a terminal window;

3 - Change permissions for the executable file;

4 - Run it!
```
$ cd app
$ sudo chmod 666 glucoplot-libre
$ ./glucoplot-libre
```

### 1.1 - Commands

After starting the program, following commands are available:

1.1.1 - **check** 

Check existing months with associated year in the glucose.csv file.

Usage: ```> check```

1.1.2 - **get**

Check if reader is connected. If positive, send request to dump data on .csv file.

Usage: ```> get```

1.1.3 - **help**

Provides general and specific command documentation.

Usage: ```> help``` or ```> help <command>``` 

1.1.4 - **process**

Parse, plot and print daily glucose curves in a PDF file for desired month.

Usage: ```> process <month_index>```

<month_index> = integer representing a valid month found in the glucose table.

1.1.5 - **quit**

Quits the program.

Usage: ```> quit```

### 1.2 - Example usage

