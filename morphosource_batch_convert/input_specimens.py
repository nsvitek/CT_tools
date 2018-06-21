#! /bin/env python
"""This modules reads and parses a list of specimen names"""

import pandas as pd #for input_specimens.py
#%% set variables
### ! Future: allow user to choose to set all variables intitially or use interactive mode.
#ASSUMPTION: User has data in a .csv (or, eventually, .xlsx) spreadsheet
#ASSUMPTION: Spreadsheet has rows of specimens, columns of specimen attributes
#%% set name of column that contains specimen name
#ASSUMPTION: User put the institution and catalog number together in one column
#NOT ASSUMED: User included collection code or not
### ! Future: flexibility to handle case where institution, catalogue number are in separate columns
### ! Future: interactively choose columns.
#%% set character used to separate institution from specimen number
### ! Future: a good opportunity to use regular expressions to make code more flexible
### ! Future: possibility of no separation between institution and specimen number ('UF12345')
#%% read file
def read_user_input(input_path, input_file):
    """ reads in user-provided specimen data """
    ### ! Future: decide if the file is csv or excel, then read either way
    user_input_raw = pd.read_csv(input_path + '/' + input_file)
    #UserInputRaw = pd.read_excel(INPUT_PATH + '/' + INPUT_FILE)
    return user_input_raw

def read_catalog_numbers(user_input_raw, specimen_names, my_separator):
    """ pulls out a list of catalog numbers, broken into segments """
    #pull out specimen names
    specimens_raw = user_input_raw[specimen_names]
    #break up the catalogue number into parts
    specimens_split = specimens_raw.str.split(my_separator)
    #SpecimensRaw.str.split(SEPARATOR)[0][1] #example of how to index
    return specimens_split
