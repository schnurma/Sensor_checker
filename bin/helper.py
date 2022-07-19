#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2022 Martin Schnur for Siemens AG
#
# SPDX-License-Identifier: MIT

"""
`helper.py`
================================================================================

Containts the outsourced classes and fucntions for the main script.

* Author(s): Martin Schnur

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

"""

# Imports
from asyncio import subprocess
from logging import NOTSET
from venv import create
from xml.dom.minidom import Element
from pathlib import Path
from distutils.dir_util import copy_tree

import sys
import re
import os
import pathlib
import shutil
import datetime
import zipfile
import requests
import subprocess


# ??? from msilib.schema import Class

def exit_program() -> None:
    """Exit programm, clear folders (resources, )"""
    # TODO: clear resources folder
    # TODO: ???
    sys.exit("User aborted the Program")


class SensorLibrary:
    """Class for the Adafruit Library:"""
    def __init__(
        self, path_to_dir: str, url: str, search_str: str, subdir_path: str
    ) -> None:
        self.path_to_dir = path_to_dir  # local path for all downloads
        self.url = url  # url for the file
        self.search_str = search_str  # search string for the file
        self.subdir_path = subdir_path  # subdir to all librarys:
        self.list_sensors = []  # list of all sensors
        self.file_path = None
        self.check_git_lib()
        self.get_subdir_list()

    # Checks if file exists, check time of last update,
    # if file is older than 24h, download new file
    # https://stackoverflow.com/questions/5799070/how-to-see-if-file-is-older-than-3-months-in-python
    def check_git_lib(self) -> None:
        lib_stat = True
        try:
            file_time = os.path.getmtime(self.subdir_path)
            modified_last_24h = datetime.datetime.fromtimestamp(file_time)
            now = datetime.datetime.today()
            diff = now - modified_last_24h
            if diff.total_seconds() > 86400:
                print(" File is older than 24h, downloading new file")
                lib_stat = False
        except FileNotFoundError:
            print("ERROR: File not found, downloading new file")
            lib_stat = False

        if lib_stat is False:
            self.download_git_lib(self.url, self.search_str, self.path_to_dir)

    # Downloads and unzips the requested file
    def download_git_lib(self, url: str, search_str: str, path_to_dir: str) -> None:
        self.file_path = path_to_dir + "/" + search_str

        # Safe as a file
        req = requests.get(url, allow_redirects=True)
        with open(self.file_path, "wb").write(req.content):
            print("File downloaded")

        # If .zip file unzip
        try:
            if url.endswith(".zip"):
                with zipfile.ZipFile(self.file_path, "r") as zip_ref:
                    zip_ref.extractall(path_to_dir)
        except TypeError:
            print("ERROR: File is not a .zip")

    # https://www.techiedelight.com/list-all-subdirectories-in-directory-python/
    # https://realpython.com/working-with-files-in-python/
    # Creates and returns list of all folders in subdir_path
    def get_subdir_list(self) -> list:
        search_dir = self.subdir_path
        self.list_sensors = []
        for path in Path(search_dir).iterdir():
            if path.is_dir():
                # print(path)
                self.list_sensors.append(path.name)
        return self.list_sensors


# Class for Sensor Node:
class SensorNode:

    # Installation Type Statement (node.type_str)
    MODE_1 = "without ROS2 node"
    MODE_2 = "with ROS2 node"

    def __init__(self, sensor: str, path_to_dir: str) -> None:
        self.sensor = sensor
        self.name = "py_" + self.sensor  # Node Name
        self.path_to_dir = path_to_dir  # local path for all downloads
        self.folder_name = ""  # local path for the file
        self.file_path = self.path_to_dir + "/" + self.folder_name
        self.package_name = "Adafruit_CircuitPython_" + self.sensor
        self.url = (
            "https://github.com/adafruit/Adafruit_CircuitPython_"
            + self.sensor
            + "/archive/refs/heads/main.zip"
        )
        self.type = 1  # Installation Type
        self.dir = ""  # installer dir (Docker Image and ROS2 node)
        self.list_subfile_1 = []
        self.list_subfile_2 = []
        self.node_type(self.type)
        self.download_git_lib()
        self.pip_install()
        self.find_folder()

    # Set note type:
    def node_type(self, node_type: int) -> None:
        self.type = int(node_type)
        while True:
            if self.type == 1:
                self.type_str = self.MODE_1
                self.dir = "installer_" + str(self.type)
                break
            if self.type == 2:
                self.type_str = self.MODE_2
                self.dir = "installer_" + str(self.type)
                break
            # loop till user enters valid input
            print("Wrong input, try again")
            self.type = int(input("Enter 1 or 2: "))
            continue

    # Change name of node:
    def node_name(self, node_name: str) -> None:
        self.name = node_name

    # Downloads and unzips the requested file:
    def download_git_lib(self) -> None:
        file_path = self.path_to_dir + "/" + self.sensor
        # download and safe as a file
        req = requests.get(self.url, allow_redirects=True)
        open(file_path, "wb").write(req.content)
          

        # if *.zip file, unzip
        try:
            if self.url.endswith(".zip"):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(self.path_to_dir)
        except TypeError:
            print("ERROR: File is not a .zip")

    # Installs the Sensors Library with pip:
    # i.e. pip3 install adafruit-circuitpython-lis3dh
    # https://stackoverflow.com/questions/12332975/installing-python-module-within-code
    def pip_install(self) -> None:
        try:
            # package = "adafruit-circuitpython-" + self.sensor
            # subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("Installing:", self.package_name)
            print("THIS IS A TEST LINE, REMOVE LATER and uncomment subprocess...")
        except subprocess.CalledProcessError as err:
            print("Error:", err)

    # Find the sensor-main folder:
    def find_folder(self) -> None:
        file_name = self.sensor + "-main"
        for path in Path(self.path_to_dir).iterdir():
            # search, case-insensitive = re.I
            if re.search(file_name, path.name, re.I):
                self.folder_name = path.name
                self.file_path = self.path_to_dir + "/" + self.folder_name
                print(f"Found this folder {self.file_path}")

    # Creates specific filepath for subfolder and adds files to list:
    def get_subfile_list(self) -> None:
        ar_types = ["examples", "library"]
        for search_type in ar_types:
            if search_type == "examples":
                self.list_subfile_1 = []
                self.search_dir[0] = self.file_path + self.EXAMPLES
                file_name = ".py"
                self.fill_subfile_list(
                    self.search_dir[0], file_name, self.list_subfile_1
                )
            elif search_type == "library":
                self.list_subfile_2 = []
                self.search_dir[1] = self.file_path + self.LIBRARY
                file_name = self.sensor + ".py"
                self.fill_subfile_list(
                    self.search_dir[1], file_name, self.list_subfile_2
                )

    # Inner Class for filepaths:
    class Filepath:
        """Creating a subclass for the needed filepaths to the Library *.py file
        and the examples *.py files for the user menue and to copy these files
        when choosen for the Docker Image.
        """

        # list_types = ["examples", "library"]:
        EXAMPLES = "/examples"
        LIBRARY = "/"

        def __init__(self, sensor: str, code_type: str, file_path: str) -> None:
            self.sensor = sensor
            self.code_type = code_type  # examples or library *.py
            self.file_path = file_path
            self.code_path = None
            self.list = []
            self.list_path = []
            self.list_py = 0
            self.init(code_type)

        # Set filepaths:
        def init(self, mode="library") -> None:
            if mode == "library":
                self.code_path = self.file_path + self.LIBRARY
                self.file_name = self.sensor + ".py"
            elif mode == "examples":
                self.code_path = self.file_path + self.EXAMPLES
                self.file_name = ".py"
            else:
                print("ERROR: Wrong mode")        
            self.fill_list()

        # Creates a list of all *.py files in the directory:
        # Problem no Lib file -> there should be a Lib Folder! With other *.py files
        def fill_list(self) -> None:
            for f_name in Path(self.code_path).iterdir():
                # if f_name.is_file():
                if f_name.name.endswith(self.file_name):
                    # print(f_name)
                    self.list.append(f_name.name)
                    list_path = self.code_path + "/" + f_name.name
                    self.list_path.append(list_path)
                    print("Found this file", f_name.name)

        # Creates a list of all *.py files in the directory:
        # User can select file
        def list_menue(self) -> str:
            print("List of files:")
            for i in range(len(self.list)):
                print(i, self.list[i])
            print("")
            print("Enter the number of file:")
            filenum = int(input())
            return filenum

        # Sets and returns the filepath of the selected file:
        def set_py(self, filenum: str) -> None:
            self.list_py = filenum
            print(
                f"Set this file: {self.list[int(filenum)]}",
            )
            print(
                f"Set this file: {self.list_path[int(filenum)]}",
            )

        # End of Subclass Filepath:
        # /////////////////////////////////////////////////////////////////////////

    # creats a list of all files in subdir_path:
    def fill_subfile_list(
        self, search_dir: str, file_name: str, list_subfile: list
    ) -> None:
        for f_name in Path(search_dir).iterdir():
            if f_name.name.endswith(file_name):
                list_subfile.append(f_name.name)
                print("Found this file", f_name.name)

    def list_menue(self, list_subfile: list) -> str:

        print("List of files:")
        for i in range(len(list_subfile)):
            print(i, list_subfile[i])
        print("")
        print("Enter number of file to open:")
        file_num = input()
        file_path = self.search_dir[0] + "/" + list_subfile[int(file_num)]
        return file_path


# End of Class Sensor:
# /////////////////////////////////////////////////////////////////////////////


# Open example code in nano editor:
def open_nano(file_path: str) -> None:
    print("Opening nano editor for:", file_path)
    # subprocess.call(['nano', 'resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py'])
    subprocess.call(["nano", file_path])


# Runs example code with python3:
def run_code(file_path: str) -> None:
    print("Running code:", file_path)
    subprocess.call(["python3", file_path])


# Creates and returns list of all folders in subdir_path:
# https://www.techiedelight.com/list-all-subdirectories-in-directory-python/
# https://realpython.com/working-with-files-in-python/
def get_subdir_list(search_dir: str) -> list:
    list_sensors = []
    for path in Path(search_dir).iterdir():
        if path.is_dir():
            list_sensors.append(path.name)

    return list_sensors


# Creates and returns list of all files in subdir_path:
# with search_str in file name
# case insensitive !
# https://www.tutorialspoint.com/python/python_reg_expressions.htm
def get_subdir_list2(search_str: str, search_dir: str, search_type: str) -> list:
    list_sensors = []
    if search_type == "main":
        file_name = search_str + "-main"
    for path in Path(search_dir).iterdir():
        if re.search(file_name, path.name, re.I):
            list_sensors.append(path.name)
            print("Found this file", path.name)

    return list_sensors


# Creates and returns list of all files in subdir_path:
# list_sensors = get_subdir_list(subdir_path) ???
def get_subfile_list(search_str: str, search_dir: str, search_type: str) -> list:
    list_subfile = []
    if search_type == "examples":
        search_dir = search_dir + "examples/"
        file_name = ".py"
    elif search_type == "library":
        file_name = search_str + ".py"

    for f_name in Path(search_dir).iterdir():
        if f_name.name.endswith(file_name):
            list_subfile.append(f_name.name)
            print("Found this file", f_name.name)

    return list_subfile


# Creates menue with list elements and returns user input:
def list_menue(search_type: str, search_dir: str, list_subfile: list) -> str:
    if search_type == "examples":
        search_dir = search_dir + "examples/"

    print("List of files:")
    for i in range(len(list_subfile)):
        print(i, list_subfile[i])
    print("")
    print("Enter number of file to open:")
    file_num = input()
    file_path = search_dir + list_subfile[int(file_num)]
    return file_path


# Find file in subdir_path:
def find_file(search_str: str, search_type: str, search_dir: str) -> str:
    # /resources/*Sensor/examples/
    # Adafruit_CircuitPython_SGP30-main
    if search_type == "examples":
        search_dir = search_dir + "examples/"
        file_name = ".py"
    elif search_type == "library":
        file_name = search_str + ".py"

    # dist_packages = "/resources/Adafruit_CircuitPython_" + search_str + "-main" + "/examples/"
    # i.e. : "resources/Adafruit_CircuitPython_SGP30-main/examples/"
    # carefull "in" is case sensitive  !
    for f_name in os.listdir(search_dir):
        if f_name.endswith(file_name):
            print("Found this file", f_name)
            file_path = search_dir + f_name
            print(file_path)
            return file_path
    print("ERROR: File not found")
    return False


# Search and open the Library file:
# search_str = "hts221"
# dist_packages IOT2050 = '/usr/local/lib/python3.8/dist-packages'
def show_sensor_info(search_str: str, dist_packages: str) -> None:
    file_name = search_str + ".py"
    # print(path)
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            # check_file(f_name)
            print("Found this file", f_name)   
    print("ERROR: Sensor Library not found")
    return False


# Prints the sensor implementation notes:
def check_file(search_str: str) -> None:
    start_pattern = "==="
    end_pattern = "Software"

    with open(search_str, encoding="utf-8") as file:
        match = False
        newfile = None

        for line in file:
            if re.search(start_pattern, line):
                match = True
                newfile = open("resources/sensor_info.txt", "w", encoding="utf-8")
                continue
            if re.search(end_pattern, line):
                match = False
                newfile.close()
                continue
            if match:
                newfile.write(line)
                newfile.write("\n")
                print(line)


# Finds example code for sensor:
def find_example_code(search_str: str, dist_packages: str) -> str:
    # /resources/*Sensor/examples/
    # Adafruit_CircuitPython_SGP30-main
    # search in dist-package after sensor lib load Implemantion Notes

    file_name = ".py"
    # dist_packages = "/resources/Adafruit_CircuitPython_" + search_str + "-main" + "/examples/"
    # i.e. = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
    # carefull "in" is case sensitive  !
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            print("Found this file", f_name)
            file_path = dist_packages + f_name
            print(file_path)
            return file_path

    print("ERROR: Example Code not found")
    return False


# Creates new directory for sensor node:
def create_new_dir(search_str: str, node_name: str, source_dir: str) -> None:
    # source_dir = "installer/"
    copy_tree(source_dir, node_name)


# Creates needed directories for Docker Image / ROS2 Node:
def create_dirs(node_name: str) -> None:
    dir_name = node_name
    node_include = "include/" + node_name
    node_name_init = node_name + "/" + "__init__.py"
    # List of folders to create:
    subdir_list = [node_name_init, node_include, "resource", "src"]

    for line in subdir_list:
        try:
            dir_name_sub = dir_name + "/" + line
            os.umask(0)
            print("Creating directory:", dir_name_sub)
            os.makedirs(dir_name_sub, mode=0o777, exist_ok=True)
        except FileExistsError:
            print("Directory ", dir_name_sub, " already exists")


# Copys all *.py into node_name/src
def copy_src_2(sensor: str, dir_name: str, file_path: str, file: list) -> None:
    try:
        for i in range(len(file_path)):

            target_list = dir_name + "/src/" + file[i]
            shutil.copyfile(file_path[i], target_list)
            print("Copying:", file_path[i], "to:", target_list)
    except FileNotFoundError:
        print("ERROR: File not found or already exists")


# Copys .py into node_name/src:
def copy_src(search_str: str, dir_name: str, file_path: str) -> None:
    source_list = file_path
    target_list = dir_name + "/src/" + search_str
    try:
        shutil.copyfile(source_list, target_list)
        # Path(line).rename(target_list[i])
        print("Copying:", source_list, "to:", target_list)
    except FileNotFoundError:
        print("ERROR: File not found or already exists")


# Moves all needed files to the new directory:
# Permissions problems....!!!
def copy_files(node_name: str) -> None:
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
        except FileNotFoundError:
            print("ERROR: File not found or already exists")


# Copy files from resources to node_name:
# blinka: files for the blinka platform till offical release
# platformdetect: files for the platformdetect platform till offical release
# usr: files for mraa !
def copy_dirs(node_name: str) -> None:
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
        except FileNotFoundError:
            print("ERROR: File not found or already exists")


# Finds Placeholder in the file and replaces it with the Variable:
def replace_string(file_path: str, search_str: str, replace_str: str) -> None:
    try:
        with open(file_path, encoding="utf-8") as file:
            source = file.read()
            source = source.replace(search_str, replace_str)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(source)
    except:
        print("ERROR: File not found or already exists")


# Create Dockerfile:
def create_dockerfile(sensor_1, filepath_1, filepath_2) -> None:

    # Creates Docker / ROS2 Directory Structure:
    create_new_dir(sensor_1, sensor_1.name, sensor_1.dir)
    # name of the .py file has to be the same in CMakeLists.txt for the ROS2 Node!!!
    copy_src_2(sensor_1.sensor, sensor_1.name, filepath_1.list_path, filepath_1.list)
    create_dirs(sensor_1.name)

    # updates Files, changes Placerholder with Sensor Name and Node Name:
    # search_str = Sensor Name = i.e. sgp30
    # node_name = ROS2 Node Name = i.e. py_sgp30
    placeholder = "${SENSOR_VAR}"
    file_path = sensor_1.name + "/README.md"
    replace_string(file_path, placeholder, sensor_1.sensor)

    placeholder = "${SENSOR_NODE}"
    file_path = sensor_1.name + "/CMakeLists.txt"
    replace_string(file_path, placeholder, sensor_1.name)

    placeholder = "${SENSOR_VAR}"
    file_path = sensor_1.name + "/CMakeLists.txt"
    replace_string(file_path, placeholder, filepath_1.list_py)

    placeholder = "${SENSOR_NODE}"
    file_path = sensor_1.name + "/package.xml"
    replace_string(file_path, placeholder, sensor_1.name)

    placeholder = "${SENSOR_NODE}"
    file_path = sensor_1.name + "/Dockerfile"
    replace_string(file_path, placeholder, sensor_1.name)

    placeholder = "${SENSOR_VAR}"
    file_path = sensor_1.name + "/Dockerfile"
    replace_string(file_path, placeholder, sensor_1.sensor)

    placeholder = "${SENSOR_PY}"
    file_path = sensor_1.name + "/Dockerfile"
    replace_string(file_path, placeholder, filepath_1.list[int(filepath_1.list_py)])


def run_docker_image(node_name: str) -> None:
    docker_command = "docker build .-t " + node_name
    # subprocess.check_output(docker_command, stderr=subprocess.STDOUT, shell=True)
    # subprocess.run(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open("/tmp/output.log", "a") as output:
        subprocess.call(docker_command, shell=True, stdout=output, stderr=output)
    """
    try:
        with open("/tmp/output.log", "a", encoding="utf-8") as output:
            subprocess.call(docker_command, shell=True, stdout=output, stderr=output)
    except:
        print("Docker not found")
    """
