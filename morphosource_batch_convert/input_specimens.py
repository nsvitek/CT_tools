#! /bin/env python
### import list of specimen names

import pandas as pd

#%% log file

### ! Future: Edit log_data.py so that I'm using methods and classes
#logger.debug('Starting specimen name input script.')
#%% set variables
### ! Future: allow user to choose to set all variables intitially or use interactive mode.
#ASSUMPTION: User has data in a .csv (or, eventually, .xlsx) spreadsheet
#ASSUMPTION: Spreadsheet has rows of specimens, columns of specimen attributes
#path to where spreadsheet is located
INPUT_PATH = 'sample_data' 
#name of spreadsheet file. 
INPUT_FILE = 'input_sample1.csv'
#INPUT_FILE = 'input_sample3.xlsx'

#set name of column that contains specimen name
#ASSUMPTION: User put the institution and catalog number together in one column
#NOT ASSUMED: User included collection code or not
### ! Future: include flexibility to handle case where institution, collection, and catalogue number are in separate columns
### ! Future: interactively choose columns. 
SPECIMEN_NAMES = 'Catalog number'
#set character used to separate institution from specimen number
### ! Future: a good opportunity to use regular expressions to make code more flexible
### ! Future: deal with possibility of no separation between institution and specimen number ('UF12345')
SEPARATOR = ' ' #could also be '_' or '-' ' '.
#%% read file
### ! Future: decide if the file is csv or excel, then read either way
UserInputRaw = pd.read_csv(INPUT_PATH + '/' + INPUT_FILE)
#UserInputRaw = pd.read_excel(INPUT_PATH + '/' + INPUT_FILE)

### ! Future: use debug log to check here that file was able to be read properly

#pull out specimen names
SpecimensRaw = UserInputRaw[SPECIMEN_NAMES]

#break up the catalogue number into parts
SpecimensSplit = SpecimensRaw.str.split(SEPARATOR)
#SpecimensRaw.str.split(SEPARATOR)[0][1] #example of how to index

SpecimensSplit