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
    file_suffix = re.match('.*\.(.*)$',input_file).group(1) #get file ending
    if (file_suffix == "csv"): #if file is csv
        user_input_raw = pd.read_csv(input_path + '/' + input_file)
    if (file_suffix == "xlsx"): #if file is excel spreadsheet
        user_input_raw = pd.read_excel(input_path + '/' + input_file)
    if (file_suffix not in ('csv', 'xlsx')):
        ErrorMessage = f'File ending {file_suffix} is not csv or xlsx.'
        print(ErrorMessage)
    return user_input_raw

#%% choose specimen name column
#UserInputRaw is the data frame resulting from read_user_input()
def read_catalog_numbers(UserInputRaw):
    print() #providing separation between choices for the eye. 
    print()
    print()
    print("### Column Options")
    for i in range(len(UserInputRaw.columns)):
        print(str(i) + ": " + UserInputRaw.columns[i])
    SpecimenName = input("Select the column number containing catalog numbers:")
    SpecimensRaw = UserInputRaw.iloc[:,int(SpecimenName)]
    return SpecimensRaw

#%%
def parse_catalog_numbers(UserInputRaw,SpecimenName):
    print() #providing separation between choices for the eye. 
    print()
    print()
    print("### Institution, Number Options")
    #pull out specimen names
    return SpecimensRaw

