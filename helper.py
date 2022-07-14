#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2022 Martin Schnur for Siemens AG
#
# SPDX-License-Identifier: MIT


# Imports
from asyncio import subprocess
from logging import NOTSET
from venv import create
from xml.dom.minidom import Element
from pathlib import Path

import requests
import zipfile
import os
import pathlib
import shutil
import subprocess
import sys
import re
import subprocess


# TEST VARIABLES AND STUFFF
# /////////////////////////////////////////////////////////////////////////////
# subdir_path = '/home/workshopper/Documents/GitHub/Sensor_checker/resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/'
# search_str = "hts221"

# /////////////////////////////////////////////////////////////////////////////


def user_input() -> None:
    # Get and return user input
    print("Enter your search string:")
    search_str = input()

    return search_str


# downloads and unzips the requested file
def download_git_lib(url, search_str, path_to_dir):
    # url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git'
    # url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip'
    # path_to_dir = 'resources' # fixed path to directory
    # path_to_file = 'Adafruit_CircuitPython_Bundle.zip'
    path_to_file = search_str
    file_path = path_to_dir + "/" + path_to_file

    # Safe as a file
    r = requests.get(url, allow_redirects=True)
    open(file_path, "wb").write(r.content)

    # if .zip file unzip
    # Unzip the file
    if url.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(path_to_dir)
    else:
        print("ERROR: File is not a .zip")


# https://www.techiedelight.com/list-all-subdirectories-in-directory-python/
# https://realpython.com/working-with-files-in-python/
# Creates and returns list of all folders in subdir_path
def get_subdir_list(search_dir):
    list_sensors = []

    for path in Path(search_dir).iterdir():
        if path.is_dir():
            # print(path)
            list_sensors.append(path.name)

    # print(list_sensors)
    return list_sensors


# Creates and returns list of all files in subdir_path
# with search_str in file name
# case insensitive !
# https://www.tutorialspoint.com/python/python_reg_expressions.htm
def get_subdir_list2(search_str, search_dir, search_type):
    list_sensors = []
    if search_type == "main":
        file_name = search_str + "-main"

    for path in Path(search_dir).iterdir():
        """if path.name.endswith(file_name):"""
        if re.search(file_name, path.name, re.I):
            # print(path)
            list_sensors.append(path.name)

            print("Found this file", path.name)

    # print(list_sensors)
    return list_sensors


# list_sensors = get_subdir_list(subdir_path) ???
# Creates and returns list of all files in subdir_path
def get_subfile_list(search_str, search_dir, search_type):
    list_subfile = []
    if search_type == "examples":
        search_dir = search_dir + "examples/"
        file_name = ".py"
    elif search_type == "library":
        file_name = search_str + ".py"

    for f_name in Path(search_dir).iterdir():
        # if f_name.is_file():
        if f_name.name.endswith(file_name):
            # print(f_name)
            list_subfile.append(f_name.name)
            print("Found this file", f_name.name)

    return list_subfile


# creates menue with list elements and returns user input
def list_menue(search_type, search_dir, list_subfile):
    if search_type == "examples":
        search_dir = search_dir + "examples/"
        file_name = ".py"

    print("List of files:")
    for i in range(len(list_subfile)):
        print(i, list_subfile[i])
    print("")
    print("Enter number of file to open:")
    file_num = input()
    file_path = search_dir + list_subfile[int(file_num)]
    return file_path


# finde file in subdir_path
def find_file(search_str, search_type, search_dir):
    # /resources/*Sensor/examples/
    # Adafruit_CircuitPython_SGP30-main
    if search_type == "examples":
        search_dir = search_dir + "examples/"
        file_name = ".py"
    elif search_type == "library":
        file_name = search_str + ".py"

    # dist_packages = "/resources/Adafruit_CircuitPython_" + search_str + "-main" + "/examples/"
    # dist_packages  = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
    # carefull "in" is case sensitive  !
    for f_name in os.listdir(search_dir):
        if f_name.endswith(file_name):
            print("Found this file", f_name)
            file_path = search_dir + f_name
            print(file_path)
            return file_path
            # open_nano(file_path)
    else:
        print("ERROR: File not found")
        return False


# Compares search_str with list_sensors and returns True if found
def find_sensors(list_sensors, search_str):
    if search_str in list_sensors:
        # print("Desired item is in list:", search_str)
        # pip_install(search_str)
        return True
    else:
        # print("Not found, try other search naming")
        return False


# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
# Installs the Sensors Library with pip
# i.e. pip3 install adafruit-circuitpython-lis3dh
def pip_install(search_str):
    package = "adafruit-circuitpython-" + search_str
    # subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Installing:", package)
    print("THIS IS A TEST LINE, REMOVE LATER and uncomment subprocess...")


#
# search_str = "hts221"
# dist_packages = '/usr/local/lib/python3.8/dist-packages'
#
# search and open the Library file:
def show_sensor_info(search_str, dist_packages):
    file_name = search_str + ".py"
    # print(path)
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            # check_file(f_name)
            print("Found this file", f_name)
    else:
        print("ERROR: Sensor Library not found")
        return False


# prints the sensor implementation notes
def check_file(search_str):
    START_PATTERN = "==="
    END_PATTERN = "Software"

    with open(search_str) as file:
        match = False
        newfile = None

        for line in file:
            if re.search(START_PATTERN, line):
                match = True
                newfile = open("resources/sensor_info.txt", "w")
                continue
            elif re.search(END_PATTERN, line):
                match = False
                newfile.close()
                continue
            elif match:
                newfile.write(line)
                newfile.write("\n")
                print(line)


# find example code for sensor
def find_example_code(search_str, dist_packages):
    # /resources/*Sensor/examples/
    # Adafruit_CircuitPython_SGP30-main
    # search in dist-package after sensor lib load Implemantion Notes

    file_name = ".py"
    # dist_packages = "/resources/Adafruit_CircuitPython_" + search_str + "-main" + "/examples/"
    # dist_packages  = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
    # carefull "in" is case sensitive  !
    # file_path =
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            print("Found this file", f_name)
            file_path = dist_packages + f_name
            print(file_path)
            return file_path
            # open_nano(file_path)
    else:
        print("ERROR: Example Code not found")
        return False


# open example code in nano editor
def open_nano(file_path):
    print("Opening nano editor for:", file_path)
    # subprocess.call(['nano', 'resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py'])
    subprocess.call(["nano", file_path])


# runs example code with python3
def run_code(file_path):
    print("Running code:", file_path)
    subprocess.call(["python3", file_path])


from distutils.dir_util import copy_tree

# creates new directory for sensor node
def create_new_dir(search_str, node_name, source_dir):
    # source_dir = "installer/"
    copy_tree(source_dir, node_name)


# creates needed directories for Docker Image / ROS2 Node
# also possible to create a bash.sh for less code in this file...
def create_dirs(node_name):
    dir_name = node_name
    node_include = "include/" + node_name
    node_name_init = node_name + "/" + "__init__.py"
    subdir_list = [node_name_init, node_include, "resource", "src"]

    for line in subdir_list:
        try:
            dir_name_sub = dir_name + "/" + line
            os.umask(0)
            # pathlib.Path(dir_name_sub).mkdir(mode=0o777, parents=True, exist_ok=True)
            print("Creating directory:", dir_name_sub)
            os.makedirs(dir_name_sub, mode=0o777, exist_ok=True)
        except FileExistsError:
            print("Directory ", dir_name_sub, " already exists")


# copys .py into node_name/src
def copy_src(search_str, dir_name, file_path):
    source_list = file_path
    target_list = dir_name + "/src/" + search_str + ".py"
    i = 0
    try:
        shutil.copyfile(source_list, target_list)
        # Path(line).rename(target_list[i])
        print("Copying:", source_list, "to:", target_list)
    except:
        print("ERROR: File not found or already exists")


# moves all needed files to the new directory
# Permissions problems....!!!
def copy_files(node_name):
    dir_name = node_name
    source_list = [
        "installer/README.md",
        "installer/Dockerfile",
        "installer/CMakeList.txt",
        "installer/package.xml",
    ]
    target_list = [
        dir_name + "/README.md",
        dir_name + "/Dockerfile",
        dir_name + "/CMakeList.txt",
        dir_name + "/package.xml",
    ]
    i = 0
    for line in source_list:
        try:
            shutil.copyfile(line, target_list[i])
            # Path(line).rename(target_list[i])
            print("Copying:", line, "to:", target_list[i])
            i += 1
        except:
            print("ERROR: File not found or already exists")


# copy files from resources to node_name
# blinka = files for the blinka platform till offical release
# platformdetect = files for the platformdetect platform till offical release
# usr = files for mraa !
def copy_dirs(node_name):
    dir_name = node_name
    source_list = ["installer/blinka", "installer/platformdetect", "installer/usr"]
    target_list = [
        dir_name + "/blinka",
        dir_name + "/platformdetect",
        dir_name + "/usr",
    ]

    i = 0
    for line in source_list:
        try:
            os.umask(0)
            shutil.copytree(line, target_list[i])
            print("Copying:", line, "to:", target_list[i])
            i += 1
        except:
            print("ERROR: File not found or already exists")


# finds Placeholder in the file and replaces it with the node_name
def replace_string(file_path, search_str, replace_str):
    try:
        with open(file_path) as f:
            s = f.read()
            s = s.replace(search_str, replace_str)
        with open(file_path, "w") as f:
            f.write(s)
    except:
        print("ERROR: File not found or already exists")


def run_docker_image(node_name):
    docker_command = "docker build . -t " + node_name
    with open("/tmp/output.log", "a") as output:
        subprocess.call(docker_command, shell=True, stdout=output, stderr=output)


# Class for Sensor Node
# This is first try to create a usefull Class...
class Sensors_node:
    def __init__(self, sensor):
        self.sensor = sensor
        self.name = "py_" + self.sensor
        self.type = 1
        self.node_type(self.type)
        self.files = "test.py"

    # set note type:
    def node_type(self, node_type):
        self.type = int(node_type)
        while True:
            if self.type == 1:
                self.type_str = "without ROS2 node"
                self.dir = "installer_" + str(self.type)
                break
            elif self.type == 2:
                self.type_str = "with ROS2 node"
                self.dir = "installer_" + str(self.type)
                break
            else:
                # loop till user enters valid input
                print("Wrong input, try again")
                self.type = int(input("Enter 1 or 2: "))
                continue

    # change name of node:
    def node_name(self, node_name):
        self.name = node_name


# search_str = "hts221"
# path_to_dir = 'resources' # fixed path to directory
# subdir_path = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
# file_path = "resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py"
# list_sensor = get_subfile_list(subdir_path)
# print(list_sensor)
# search_dir = path_to_dir + "/Adafruit_CircuitPython_" + search_str.upper() + "-main/examples/"
# search_dir = "resources/Adafruit_CircuitPython_HTS221-main/examples/"
# print(search_dir)
# find_example_code(search_str, search_dir)
# node_name = "py_test_XXX"
##create_new_dir(search_str, node_name)
# create_dirs(node_name)
# mov_files(node_name)
# copy_files2(node_name)
# run_code(file_path)

# node_name = "py_hts221"
# placeholder = "SENSOR_PLACEHOLDER"
# file_path = node_name + "/Dockerfile"
# replace_string(file_path, placeholder, search_str)
# print(" Helper Done")

# subprocess.call(['nano', 'resources/Adafruit_CircuitPython_HTS221-main/examples/hts221_simpletest.py'])
