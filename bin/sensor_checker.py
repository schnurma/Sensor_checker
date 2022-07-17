#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2022 Martin Schnur for Siemens AG
#
# SPDX-License-Identifier: MIT

"""
’sensor_checker.py’ 
================================================================================

Script for creating a Docker Image / ROS2 Node on a Siemens IOT2050 Gateway
with the integration of a Adafruit Sensor and Circuit Python.

* Author(s): Martin Schnur

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

"""

# Imports
import re
import sys
from unittest import case
import helper
import helper_fn

#
# User should input Sensor ID to search in Adafruit Sensor Library
# Searching in Lib for Sensor ID, downloads the file
# Prints out Implementation Notes and Connection Type (I2C, SPI, etc...)
# Develops Core for ROS2 and Dockercontainer with Comments what is needed to implement?
# implement GUI?

# ERROR HANDLING !!!???!!!

# Adafruit Library Bundle Values:
# Library Bundle url:
# GitHub: 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git'
url = "https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip"
search_str = "Adafruit_CircuitPython_Bundle.zip"

# local Datastructure:
# Path for all downloads
path_to_dir = "resources"
# subdir to all librarys:
subdir_path =  path_to_dir + "/Adafruit_CircuitPython_Bundle-main/libraries/drivers/"

# Downloads/ Reloads Adafruit Library Bundle:
# check if file exists, check time of last update, if file is older than 24h, download new file
#helper.download_git_lib(url, search_str, path_to_dir)
# Creates Class for Library:
# correct way???
sensors_lib = helper.Sensor_Library(path_to_dir, url, search_str, subdir_path)

# Creates a searchable Sensor Library List:
#helper.download_git_lib()
# Outputs the list for the user to choose from:
#list_sensors = helper.get_subdir_list(subdir_path)
#print(list_sensors)
print(sorted(sensors_lib.list_sensors))

# User Input Sensor ID out of list_sensors:
while True:
    try:
        #print("Which sensor do you want to use:")
        search_str = input("Which sensor do you want to use: ")
        # i.e. search_str = "sgp30"
        if search_str in sensors_lib.list_sensors:
            sensor_1 = helper.Sensors_node(search_str, path_to_dir)
            break
        else:
            print("Sensor not found in list, please try again")

# not working...
    except ValueError:
        print("Unfortunately, the sensor was not found. Try another notation")
    except FileNotFoundError:
        print("Unfortunately, the sensor was not found. Try another notation")
        continue

# Inits Subclass for example code:
filepath_1 = sensor_1.Filepath(sensor_1.sensor, "examples", sensor_1.file_path)
filepath_2 = sensor_1.Filepath(sensor_1.sensor, "library", sensor_1.file_path)

# Menue for the user, open and test example code, view library:
while True:
    print("////////////////////////////////////////////////////")
    print("Do you want to open the example code? Press '1'")
    print("Do you want to run the example code? Press '2' ")
    print("Do you want to open the Sensor Library? Press '3' ")
    print("Do you want to continue? Press '5'")
    print("Do you want to exit? Press '6'")
    print("////////////////////////////////////////////////////")
    answer = input()

    # switch case better but only supported in Python 3.10
    if answer == "1":
        # opens example code in nano
        # user can choose file to open
        # open file in texteditor
       
        # prints the files in the dir examples:
        filenum = filepath_1.list_menue()
        # user input file to open:
        helper.open_nano(filepath_1.list_path[int(filenum)])

        continue

    elif answer == "2":
        # runs the example code
        # user can choose which file to run
        #search_type = "examples"
        filenum = filepath_1.list_menue()
        # user input file to open:
        helper.run_code(filepath_1.list_path[int(filenum)])

        continue

    elif answer == "3":
        # opens the Sensor Library in nano
        # user can choose file to open
        # open file in texteditor
        #search_type = "library"
        filenum = filepath_2.list_menue()
        # user input file to open:
        helper.open_nano(filepath_2.list_path[int(filenum)])
        continue

    elif answer == "5":
        # proceed to next step
        break

    elif answer == "6":
        # Exit program
        # clean directorys!
        sys.exit("User aborted the Program")

    else:
        # Loop till user enters valid input
        print("\n \n \n")
        print("Please enter a valid input")
        continue

# Exports the example code to Docker Image source directory:
# ASK user for sensor type?
# check for sensor type in example code?
# Other ROS2 / Docker Settings ?


# Menue for the user, edit settings for Docker / ROS2 Node creation:
while True:
    print("////////////////////////////////////////////////////")
    print(f"Docker Image (ROS2 Node) Name will be: {sensor_1.name} ")
    print(f"Image Type will be: {sensor_1.type_str} ")
    print(f"This files {filepath_1.list} will be copied to the Docker Image")
    print("Do you want to change the name of Docker Image? Press '1'")
    print("Do you want to change the Settings for the Docker Image? Press '2'")
    print(f"Change which python file will be used {filepath_1.list[filepath_1.list_py]}? Press '3'")
    print("Do you want to create the Dockerfile? Press '5'")
    print("Do you want to create the Docker Image? Press '6'")
    print("Press '0' to exit")
    print("////////////////////////////////////////////////////")
    answer = input()

    if answer == "1":
        # Changes the name of the sensor_1
        print("How do you want to name this Node? (i.e. py_sgp30):")
        sensor_1.node_name(input())
        # node_name = input()
        continue

    elif answer == "2":
        # Change the Settings for the Docker Image:
        print(f"Image Type will be: {sensor_1.type_str} ")
        print(" Press '1' to change to 'without ROS 2 Node'")
        print(" Press '2' to change to 'with ROS2 Node'")
        sensor_1.node_type(int(input()))
        continue

    elif answer == "3":
        # Change which *.py file will be copied to the Docker Image:
        print(f"For Sensor {sensor_1.sensor} following python file will be used: {filepath_1.list}")
        # prints the files in the dir examples:
        filenum = filepath_1.list_menue()
        # user input choose the mainfile for the Docker Image:
        filepath_1.set_py(filenum)
        continue

    elif answer == "5":
        helper.create_dockerfile(sensor_1, filepath_1, filepath_2)
        continue

    elif answer == "6":
        helper.run_docker_image(sensor_1.name)
        continue

    elif answer == "0":
        # Exit program
        # clean directorys!
        sys.exit("User aborted the Program")

    else:
        # Loop till user enters valid input
        print("\n \n \n")
        print("Please enter a valid input")
        continue



# #############################################################################
print("Done Done Done")
print("////////////////////////////////////////////////////")


# (Choose Connectivity Type)

# Edited Code is saved to a new file for Export to Docker Container
# Create Dockerfile for the Sensor
# Create Docker Container for the Sensor
# Run the Sensor in the Container
