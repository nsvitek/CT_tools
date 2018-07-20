#! /bin/env python
"""This modules reads and parses a list of specimen names"""
import pandas as pd #for input_specimens.py
import re

#%% set variables
### ! Future: allow user to choose to set all variables intitially or use interactive mode.
#ASSUMPTION: User has data in a .csv (or, eventually, .xlsx) spreadsheet
#ASSUMPTION: Spreadsheet has rows of specimens, columns of specimen attributes
#%% set name of column that contains specimen name
#ASSUMPTION: User put the institution and catalog number together in one column
#NOT ASSUMED: User included collection code or not
### ! Future: flexibility to handle case where institution, catalogue number are in separate columns
### ! Future: interactively choose columns.
#%% read file
def read_user_input(input_path, input_file):
    """ reads in user-provided specimen data """
    file_suffix = re.match('.*\.(.*)',input_file).group(1) #get file ending
    if (file_suffix == "csv"): #if file is csv
        user_input_raw = pd.read_csv(input_path + '/' + input_file)
    if (file_suffix == "xlsx"): #if file is excel spreadsheet
        user_input_raw = pd.read_excel(input_path + '/' + input_file)
    if (file_suffix not in ('csv', 'xlsx')):
        ErrorMessage = f'File ending {file_suffix} is not csv or xlsx.'
        print(ErrorMessage)
    return user_input_raw

#def read_catalog_numbers(user_input_raw, specimen_names):
#    """ pulls out a list of catalog numbers, broken into segments """
#    #pull out specimen names
#    specimens_raw = user_input_raw[specimen_names]
#    #break up the catalogue number into parts
#    specimens_split = specimens_raw.str.split('[ \-\_]+',expand=True)
#    return specimens_split
