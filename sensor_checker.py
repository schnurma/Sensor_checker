#!/usr/bin/env python
# -*- coding: utf-8 -*-


# License Info ...
#
#
# /////////////////////////////////////////////////////////////////////////////

# Imports
import re
import helper


# Keywords
file_name = 'adafruit_sgp30.py'
search_str = 'I2C'


subdir_path = '/home/workshopper/Documents/GitHub/Sensor_checker/resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/'
search_str = "hts221"
dist_packages = '/usr/local/lib/python3.?/dist-packages'

# User should input Sensor ID to search in Adafruit Library
# Searching in Lib for Sensor ID downloads the file
# Prints out Implementation Notes and Connection Type (I2C, SPi, etc...)
# Develops Core for ROS2 and Dockercontainer with Comments what is needed to implement?
# 


def user_input():
    print('Enter your search string:')
    search_str = input()
   
    return search_str


def check_file():
    START_PATTERN = 'Hardware'
    END_PATTERN = 'Software'

    with open(file_name) as file:
        match = False   
        newfile = None

        for line in file:
            if re.search(START_PATTERN, line):
                match = True
                newfile = open('my_new_file.txt', 'w')
                continue
            elif re.search(END_PATTERN, line):
                match = False
                newfile.close()
                continue
            elif match:
                newfile.write(line)
                newfile.write('\n')
                print(line)


# Downloads/ Reloads Adafruit Library Bundle:
url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip'
search_str = 'Adafruit_CircuitPython_Bundle.zip'
helper.download_git_lib(url, search_str)

# Creates a searchable Sensor Library List:
#helper.download_git_lib()
list_sensors = helper.get_subdir_list(subdir_path)

# Outputs the list for the user to choose from:
print(list_sensors)

# User Input Sensor ID
while True:
    search_str = user_input()
    if helper.find_sensors(list_sensors, search_str):
        break
    else:
        print("Not found, try other search naming")
        continue

# Installing with pip Sensor Lib to IOT2050 Python directory:
# /usr/local/lib/python3.?/dist-packages
helper.pip_install(search_str)
# !! this need Exceptions to handle if the Sensor is not found !!!

# Show the Sensor Library Implementation Notes:
helper.show_sensor_info(search_str, dist_packages)
# And load Example Code for testing the sensors native with the IOT2050!
url = 'https://github.com/adafruit/Adafruit_CircuitPython_' + '/' + search_str + '/archive/refs/heads/main.zip'
helper.download_git_lib(url, search_str)






# Check File for Sensor ID
