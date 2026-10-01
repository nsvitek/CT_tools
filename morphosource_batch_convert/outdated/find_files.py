# -*- coding: utf-8 -*-
"""
Create a .csv of file names from a list of files in a folder
"""
import os, csv

#set path to folder containing files
INPUT_PATH = 'C:/Users/N.S/Desktop/sample_data/input_sample_files' 
#can rename output path, but here is an auto-configured exmaple
OUTPUT_FILE = INPUT_PATH + '_filenames.csv' 
#list file names
FileNames = os.listdir(INPUT_PATH)
#write list to .csv spreadsheet
with open(OUTPUT_FILE, 'w', newline = '') as OutputFile:
    #'w' = write, newline = '' keeps writer from skipping lines between entries
    wr = csv.writer(OutputFile)
    for file in FileNames:
        wr.writerow([file])
OutputFile.close()