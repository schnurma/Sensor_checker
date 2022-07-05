#!/usr/bin/env python
# -*- coding: utf-8 -*-


# License Info ...
#
#
# /////////////////////////////////////////////////////////////////////////////

# Loads Adafruit CircuitPython Librarie Bundle

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
import subprocess
import sys
import re


# TEST VARIABLES AND STUFFF
# /////////////////////////////////////////////////////////////////////////////
#subdir_path = '/home/workshopper/Documents/GitHub/Sensor_checker/resources/Adafruit_CircuitPython_Bundle-main/libraries/drivers/'
#search_str = "hts221"




# /////////////////////////////////////////////////////////////////////////////


def download_git_lib(url, search_str):

    #url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git'
    #url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip'
    path_to_dir = 'resources' # fixed path to directory
    #path_to_file = 'Adafruit_CircuitPython_Bundle.zip'
    path_to_file = search_str
    file_path = path_to_dir + '/' + path_to_file

    # Safe as a file
    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)

    # if .zip file unzip
    # Unzip the file
    if path_to_file.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(path_to_dir)
    else :
        print("ERORR: File is not a .zip")


# https://www.techiedelight.com/list-all-subdirectories-in-directory-python/          
# Creates and returns list of all folders in subdir_path
def get_subdir_list(subdir_path):
    list_sensors = []
    for path in Path(subdir_path).iterdir():
        if path.is_dir():
            #print(path)
            list_sensors.append(path.name)

    #print(list_sensors)
    return(list_sensors)

#list_sensors = get_subdir_list(subdir_path)


def find_sensors(list_sensors, search_str):
        if search_str in list_sensors:
            #print("Desired item is in list:", search_str)
            #pip_install(search_str)
            return True
        else:
            #print("Not found, try other search naming")
            return False

#list_sensors = get_subdir_list(subdir_path)

# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
# Installs the Sensors Library with pip
# i. E. pip3 install adafruit-circuitpython-lis3dh
def pip_install(search_str):
    package = 'adafruit-circuitpython-' + search_str
    #subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Installing:", package)
    print("THIS IS A TEST LINE, REMOVE LATER")

# prints the sensor implementation notes
def check_file(search_str):
    START_PATTERN = 'Hardware'
    END_PATTERN = 'Software'

    with open(search_str) as file:
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

def show_sensor_info(dist_packages, search_str):
    # /usr/local/lib/python3.?/dist-packages
    # search in dist-package after sensor lib load Implemantion Notes
    if search_str in dist_packages:
        check_file(search_str)

    else:
        print("ERORR: Sensor not found")
        

#def load_example_code(search_str):
    # open example code into editor so user can check pins and test sensor
 #   pass


#find_sensors(list_sensors, search_str)
