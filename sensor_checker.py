#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2022 Martin Schnur for Siemens AG
#
# SPDX-License-Identifier: MIT

# Imports
import re
import sys
from unittest import case
import helper


# Keywords

# Path for all downloads
path_to_dir = "resources"
# Lib Bundel url:
url = "https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip"
# Lib Bundel, subdir for all librarys:
subdir_path = "resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/"

#
# User should input Sensor ID to search in Adafruit Sensor Library
# Searching in Lib for Sensor ID, downloads the file
# Prints out Implementation Notes and Connection Type (I2C, SPI, etc...)
# Develops Core for ROS2 and Dockercontainer with Comments what is needed to implement?

# ERROR HANDLING !!!???!!!


# Downloads/ Reloads Adafruit Library Bundle:
# check if file exists, check time of last update, if file is older than 24h, download new file
search_str = "Adafruit_CircuitPython_Bundle.zip"
helper.download_git_lib(url, search_str, path_to_dir)

# Creates a searchable Sensor Library List:
# helper.download_git_lib()
# Outputs the list for the user to choose from:
# Formatting ???
list_sensors = helper.get_subdir_list(subdir_path)
print(list_sensors)


# User Input Sensor ID out of list_sensors:
while True:
    print("Which sensor do you want to use:")
    search_str = input()
    # i.e. search_str = "sgp30"
    if helper.find_sensors(list_sensors, search_str):
        break
    else:
        print("Unfortunately, the sensor was not found. Try another notation")
        continue

# Installing with pip Sensor Lib to IOT2050 Python directory:
# /usr/local/lib/python3.?/dist-packages
# how to address the right python folder?
helper.pip_install(search_str)
# !! this need Exceptions to handle if the Sensor is not found !!!

# Load Example Code in subdir for testing the sensors native with the IOT2050:
url = (
    "https://github.com/adafruit/Adafruit_CircuitPython_"
    + search_str
    + "/archive/refs/heads/main.zip"
)
helper.download_git_lib(url, search_str, path_to_dir)


# Show the Sensor Library Implementation Notes:
# search_dir = path_to_dir + "/Adafruit_CircuitPython_" + search_str.upper() + "-main/"
# helper.show_sensor_info(search_str, search_dir)
# Doestn work because of case sensitivity:
# approach find search_str in dir and set search_dir to the right path
# search_dir = helper.show_sensor_info(search_str, path_to_dir)
search_type = "main"
search_list = helper.get_subdir_list2(search_str, path_to_dir, search_type)
# Should be only one entry, create string from list:
search_dir = "".join(search_list)
print("Library loaded, path: ", search_dir)

# Open Example Code in Textprogram for user to edit Pins and other settings:
# helper.load_example_code(search_str):

# extra function for path generation ??? Not a good place to set this variable...
search_dir = path_to_dir + "/" + search_dir + "/"
# search type = "example", "library"

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
        # TODO: user can choose file to open
        # open file in texteditor
        search_type = "examples"
        list_subfile = helper.get_subfile_list(search_str, search_dir, search_type)
        file_path = helper.list_menue(search_type, search_dir, list_subfile)
        helper.open_nano(file_path)
        continue

    elif answer == "2":
        # runs the example code
        # TODO: user can choose which file to run
        search_type = "examples"
        list_subfile = helper.get_subfile_list(search_str, search_dir, search_type)
        file_path = helper.list_menue(search_type, search_dir, list_subfile)
        helper.run_code(file_path)
        continue

    elif answer == "3":
        # opens the Sensor Library in nano
        # TODO: user can choose file to open
        # open file in texteditor
        search_type = "library"
        list_subfile = helper.get_subfile_list(search_str, search_dir, search_type)
        file_path = helper.list_menue(search_type, search_dir, list_subfile)
        helper.open_nano(file_path)
        continue

    elif answer == "5":
        # continues to next step
        break

    elif answer == "6":
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
#
# change node stuff to class
# node_name = "py_" + search_str
# node_type = 1
# node_type_str = helper.get_note_type(node_type)
node = helper.Sensors_node(search_str)

while True:
    print("////////////////////////////////////////////////////")
    print(f"Docker Image (ROS2 Node) Name will be: {node.name} ")
    print(f"Image Type will be: {node.type_str} ")
    print(f"This {node.files} will be copied to the Docker Image")
    print("Do you want to change the name of Docker Image? Press '1'")
    print("Do you want to change the Settings for the Docker Image? Press '2'")
    print(f"Change which {node.sensor} python file will be used? Press '3'")
    print("Do you want to continue? Press '5'")
    print("Press '6' to exit")
    print("////////////////////////////////////////////////////")
    answer = input()

    if answer == "5":
        # proceed to next step
        break

    elif answer == "1":
        # Changes the name of the node
        print("How do you want to name this Node? (i.e. py_sgp30):")
        node.node_name(input())
        # node_name = input()
        continue

    if answer == "2":
        # Change the Settings for the Docker Image:
        print(f"Image Type will be: {node.type_str} ")
        print(" Press '1' to change to 'without ROS 2 Node'")
        print(" Press '2' to change to 'with ROS2 Node'")
        node.node_type(input())
        continue

    if answer == "3":
        # Change which *.py file will be copied to the Docker Image:
        # IS THIS USEFULL ???
        print(f"{node.sensor} python file will be used: {node.files}")
        print(" THIS IS NOT THOUGHT THROUGH....")

        # node.node_type(input())
        continue

    elif answer == "6":
        # Exit program
        # clean directorys!
        sys.exit("User aborted the Program")

    else:
        # Loop till user enters valid input
        print("\n \n \n")
        print("Please enter a valid input")
        continue


# Creates Docker / ROS2 Directory Structure:
# why not copy complete installer folder and create folder with node_name???
# copy .py code into Docker Image source directory:
helper.create_new_dir(node.sensor, node.name, node.dir)
# name of the .py file has to be the same in CMakeLists.txt for the ROS2 Node!!!
file_path = search_dir + "examples"
helper.copy_src(node.sensor, node.name, file_path)
helper.create_dirs(node.name)
# helper.copy_dirs(node_name)
# helper.copy_files(node_name)


# updates Files, changes Placerholder with Sensor Name and Node Name:
# search_str = Sensor Name = e.g. sgp30
# node_name = ROS2 Node Name = e.g. py_sgp30
placeholder = "${SENSOR_VAR}"
file_path = node.name + "/README.md"
try:
    helper.replace_string(file_path, placeholder, node.sensor)
except:
    print("Error: File not found")


placeholder = "${SENSOR_NODE}"
file_path = node.name + "/CMakeLists.txt"
helper.replace_string(file_path, placeholder, node.name)

placeholder = "${SENSOR_VAR}"
file_path = node.name + "/CMakeLists.txt"
helper.replace_string(file_path, placeholder, node.sensor)

placeholder = "${SENSOR_NODE}"
file_path = node.name + "/package.xml"
helper.replace_string(file_path, placeholder, node.name)

placeholder = "${SENSOR_NODE}"
file_path = node.name + "/Dockerfile"
helper.replace_string(file_path, placeholder, node.name)

placeholder = "${SENSOR_VAR}"
file_path = node.name + "/Dockerfile"
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
