#!/usr/bin/env python
# -*- coding: utf-8 -*-


# License Info ...
#
#
# /////////////////////////////////////////////////////////////////////////////


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

# downloads and unzips the requested file
def download_git_lib(url, search_str, path_to_dir):
    #url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git'
    #url = 'https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/refs/heads/main.zip'
    #path_to_dir = 'resources' # fixed path to directory
    #path_to_file = 'Adafruit_CircuitPython_Bundle.zip'
    path_to_file = search_str
    file_path = path_to_dir + '/' + path_to_file

    # Safe as a file
    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)

    # if .zip file unzip
    # Unzip the file
    if url.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(path_to_dir)
    else :
        print("ERROR: File is not a .zip")


# https://www.techiedelight.com/list-all-subdirectories-in-directory-python/ 
# https://realpython.com/working-with-files-in-python/         
# Creates and returns list of all folders in subdir_path
def get_subdir_list(subdir_path):
    list_sensors = []
    for path in Path(subdir_path).iterdir():
        if path.is_dir():
            #print(path)
            list_sensors.append(path.name)

    #print(list_sensors)
    return(list_sensors)

def get_subdir_list2(subdir_path):
    list_sensors = []
    for path in os.scandir(subdir_path):
        if path.is_dir():
            #print(path)
            list_sensors.append(path.name)

    #print(list_sensors)
    return(list_sensors)

#list_sensors = get_subdir_list(subdir_path) ???
# Creates and returns list of all files in subdir_path
def get_subfile_list(subdir_path):
    list_sensors = []
    for path in Path(subdir_path).iterdir():
        if path.is_file():
            print(path.name)
            list_sensors.append(path.name)

    #print(list_sensors)
    return(list_sensors)



def find_sensors(list_sensors, search_str):
        if search_str in list_sensors:
            #print("Desired item is in list:", search_str)
            #pip_install(search_str)
            return True
        else:
            #print("Not found, try other search naming")
            return False



# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
# Installs the Sensors Library with pip
# i. E. pip3 install adafruit-circuitpython-lis3dh
def pip_install(search_str):
    package = 'adafruit-circuitpython-' + search_str
    #subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Installing:", package)
    print("THIS IS A TEST LINE, REMOVE LATER and uncomment subprocess...")

# prints the sensor implementation notes
def check_file(search_str):
    START_PATTERN = '==='
    END_PATTERN = 'Software'

    with open(search_str) as file:
        match = False   
        newfile = None

        for line in file:
            if re.search(START_PATTERN, line):
                match = True
                newfile = open('resources/sensor_info.txt', 'w')
                continue
            elif re.search(END_PATTERN, line):
                match = False
                newfile.close()
                continue
            elif match:
                newfile.write(line)
                newfile.write('\n')
                print(line)

#    
#search_str = "hts221"
#dist_packages = '/usr/local/lib/python3.8/dist-packages'
# 
def show_sensor_info(search_str, dist_packages):
    # /usr/local/lib/python3.?/dist-packages
    # search in dist-package after sensor lib load Implemantion Notes
    #print(dist_packages)
    #print(search_str)
    file_name = search_str + '.py'
    #print(path)
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            #print(f_name)
            check_file(f_name)
            break
    else:
        print("ERROR: Sensor Library not found in dist-packages")
        return False

# open example code into editor so user can check pins and test sensor      
def load_example_code(search_str):
    # /resources/*Sensor/examples/
    #Adafruit_CircuitPython_SGP30-main
    # search in dist-package after sensor lib load Implemantion Notes
    
    file_name = ".py"
    #dist_packages = "/resources/Adafruit_CircuitPython_" + search_str + "-main" + "/examples/"
    dist_packages  = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
    #print(path)
    for f_name in os.listdir(dist_packages):
        if f_name.endswith(file_name):
            print("Found this file", f_name)
            file_path = dist_packages + f_name
            print(file_path)
            open_nano(file_path)
            break
    else:
        print("ERROR: Example Code not found")
        return False

# opens nano for showing the example code
def open_nano(file_path):
    print("Opening nano editor for:", file_path)
    #subprocess.call(['nano', 'resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py'])
    subprocess.call(['nano', file_path])

# runs example code with python3
def run_code(file_path):
    print("Running code:", file_path)
    subprocess.call(['python3', file_path])




search_str = "sgp30"
subdir_path = "resources/Adafruit_CircuitPython_SGP30-main/examples/"
file_path = "resources/Adafruit_CircuitPython_SGP30-main/examples/sgp30_simpletest.py"
#list_sensor = get_subfile_list(subdir_path)
#print(list_sensor)

#load_example_code(search_str)
run_code(file_path)

print("Done")

