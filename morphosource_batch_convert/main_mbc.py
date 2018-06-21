#! /bin/env python
""" 
Starting point for the user to convert data to Morphosource batch upload spreadsheet 
ALL_CAPS = variables the user should set. 
note: Assumptions and options for future code expansion are hidden in the imported files. Check 'em out.

Initial build uses Python3.6.5
Dependencies: pandas
"""
#import modules to make everything work. Note additional modules in imported files.  
import time #for log_data.py

#%% log file
#Name puts log file in "logs" folder labelled with the date. 
LOG_FILENAME = 'logs/log-'+time.strftime('%Y-%m-%d')+'.log' #-%H-%M for hour and minute
from log_data import log_debug 
MyLogger = log_debug(LOG_FILENAME)
#%% input catalogue numbers
#path to where spreadsheet is located
INPUT_PATH = 'sample_data' 
#name of spreadsheet file. 
INPUT_FILE = 'input_sample1.csv'
#INPUT_FILE = 'input_sample3.xlsx'
SPECIMEN_NAMES = 'Catalog number'
SEPARATOR = ' ' #could also be '_' or '-' ' '.

#start
MyLogger.debug('Starting specimen name input.')
import input_specimens as inspec
UserInputRaw = inspec.read_user_input(INPUT_PATH, INPUT_FILE)
### ! Future: use debug log to check here that file was able to be read properly
SpecimensSplit = inspec.read_catalog_numbers(UserInputRaw, SPECIMEN_NAMES, SEPARATOR)
### ! Future: use debug log to check to see that column was found, string properly split.

#%% query idigbio
import idigbio #for query_idigbio.py
api = idigbio.json() #shorten

#get the institution name from the catalogue number
SpecimensSplit[0][0]

#get list of collections in that institution that contain the specimen number
query = {"institutioncode": SpecimensSplit[0][0],"catalognumber": SpecimensSplit[0][1]}

# PROBLEM: Still searching all records, not just searching the list of collections
MyRecordList = api.search_records(rq= query )
MyRecordList

