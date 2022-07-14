#!/usr/bin/env python
# -*- coding: utf-8 -*-


# License Info ...
#
#
# /////////////////////////////////////////////////////////////////////////////

# Imports
import re
import sys
from unittest import case
import helper


# Keywords

#subdir_path = '/home/workshopper/Documents/GitHub/Sensor_checker/resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/'
subdir_path = 'resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/'
path_to_dir = 'resources' # fixed path to directory

# User should input Sensor ID to search in Adafruit Sensor Library
# Searching in Lib for Sensor ID, downloads the file
# Prints out Implementation Notes and Connection Type (I2C, SPI, etc...)
# Develops Core for ROS2 and Dockercontainer with Comments what is needed to implement?

# ERROR HANDLING !!!???!!!


def user_input() -> None:
    # Input Sensor ID for search
    print("Enter your search string:")
    search_str = input()
   
    return search_str


def check_file() -> None:
    # Exports Search String to File
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
helper.download_git_lib(url, search_str, path_to_dir)

# Creates a searchable Sensor Library List:
#helper.download_git_lib()
list_sensors = helper.get_subdir_list(subdir_path)

# Outputs the list for the user to choose from:
print(list_sensors)

# User Input Sensor ID
while True:
    #search_str = user_input()
    print("Enter your search string:")
    search_str = input()
    #search_str = "sgp30"
    if helper.find_sensors(list_sensors, search_str):
        break
    else:
        print("Not found, try other naming or other sensor")
        continue 

# Installing with pip Sensor Lib to IOT2050 Python directory:
# /usr/local/lib/python3.?/dist-packages
# how to address the right python folder?
helper.pip_install(search_str)
# !! this need Exceptions to handle if the Sensor is not found !!!

# Show the Sensor Library Implementation Notes:
search_dir = path_to_dir + "/Adafruit_CircuitPython_" + search_str.upper() + "-main/"
helper.show_sensor_info(search_str, search_dir)
# And load Example Code for testing the sensors native with the IOT2050!
url = 'https://github.com/adafruit/Adafruit_CircuitPython_' + search_str + '/archive/refs/heads/main.zip'
helper.download_git_lib(url, search_str, path_to_dir)


# Open Example Code in Textprogram for user to edit Pins and other settings:
#helper.load_example_code(search_str):

 # extra function for path generation ??? Not a good place to set this variable...
search_dir = search_dir + "examples/"
# file_path = "resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py"
# file_path = "resources/Adafruit_CircuitPython_HTS221-main/examples/hts221_simpletest.py"
file_path = (helper.find_example_code(search_str, search_dir))

while True:
    print("////////////////////////////////////////////////////")
    print("Do you want to open the example code? Press '1'")
    print("Do you want to run the example code? Press '2' ")
    print("Do you want to continue? Press '5'")
    print("Do you want to exit? Press '6'")
    answer = input()

    # switch case better but only supported in Python 3.10
    if answer == '1':
        # open file in text editor
        # TODO: user can choose file to open
        # open file in texteditor
        helper.open_nano(file_path)
        continue

    elif answer == '2':        
        # runs the example code
        # TODO: user can choose which file to run       
        helper.run_code(file_path)
        continue

    elif answer == '5':
        # continues to next step
        break

    elif answer == '6':
        # exit program
        sys.exit("User aborted the Program")

    else:
        # loop till user enters valid input
        print("\n \n \n")
        print("Wrong input, try again")
        continue
                
# Exports the example code to Docker Image source directory:
# ASK user for sensor type?
# check for sensor type in example code?
# or check the type of sensors type with mraa?
node_name = "py_" + search_str
while True:
    print(f"\nDocker Image (ROS2 Node) Name will be: {node_name} ")
    print("Do you want to create the Docker Image with this name? (y/n)")
    print("Press '6' to exit")
    answer = input()
    if answer == 'y':
        # proceed to next step
        break

    elif answer == 'n':
        # Changes the name of the node
        print("How do you want to name this Node? (e.g. py_sgp30):")
        node_name = input()
        continue

    elif answer == '6':
        # Exit program
        sys.exit("User aborted the Program")

    else:
        # Loop till user enters valid input
        print("\n \n \n")
        print("Wrong input, try again")
        continue


# Creates Docker / ROS2 Directory Structure:
# why not copy complete installer folder and create folder with node_name???
# copy .py code into Docker Image source directory:
helper.create_new_dir(search_str, node_name)
# name of the .py file has to be the same in CMakeLists.txt for the ROS2 Node!!!
helper.copy_src(search_str, node_name, file_path)
helper.create_dirs(node_name)
# helper.copy_dirs(node_name)
# helper.copy_files(node_name)


# updates Files, changes Placerholder with Sensor Name and Node Name:
# search_str = Sensor Name = e.g. sgp30
# node_name = ROS2 Node Name = e.g. py_sgp30
placeholder = "${SENSOR_VAR}"
file_path = node_name + "/README.md"
helper.replace_string(file_path, placeholder, search_str)

placeholder = "${SENSOR_NODE}"
file_path = node_name + "/CMakeLists.txt"
helper.replace_string(file_path, placeholder, node_name)

placeholder = "${SENSOR_VAR}"
file_path = node_name + "/CMakeLists.txt"
helper.replace_string(file_path, placeholder, search_str)

placeholder = "${SENSOR_NODE}"
file_path = node_name + "/package.xml"
helper.replace_string(file_path, placeholder, node_name)

placeholder = "${SENSOR_NODE}"
file_path = node_name + "/Dockerfile"
helper.replace_string(file_path, placeholder, node_name)

placeholder = "${SENSOR_VAR}"
file_path = node_name + "/Dockerfile"
helper.replace_string(file_path, placeholder, search_str)

# Dockerfile for Docker Image:
# How to run Docker commands?




# #############################################################################
print("Done Done Done")
print("/////////////////////////////////////////////////////////////////////////////")


# (Choose Connectivity Type)

# Edited Code is saved to a new file for Export to Docker Container
# Create Dockerfile for the Sensor
# Create Docker Container for the Sensor
# Run the Sensor in the Container
