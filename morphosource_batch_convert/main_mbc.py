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
query = {"institutioncode": "MVZ","catalognumber": 111719}

# PROBLEM: Still searching all records, not just searching the list of collections
MyRecordList = api.search_records(rq= query )
MyRecordList

print(type(MyRecordList))
print(MyRecordList)
MyRecordList.keys() #what are the options?
MyRecordList['items'][0] #first specimen option, part of a list
type(MyRecordList['items'][0]) #is a dictionary
MyRecordList['items'][0].keys()
MyRecordList['items'][0]['indexTerms']
type(MyRecordList['items'][0]['indexTerms']) #is a dictionary
MyRecordList['items'][0]['indexTerms'].keys()

#dict_keys(['startdayofyear', 'continent', 'country', 'earliestepochorlowestseries',
# 'collectioncode', 'dqs', 'countrycode', 'datecollected', 'county', 
#'lowestbiostratigraphiczone', 'flags', 'recordset', 'hasMedia', 'hasImage', 
#'indexData', 'formation', 'uuid', 'catalognumber', 'collector', 'basisofrecord', 
#'earliesteraorlowesterathem', 'datemodified', 'class', 'group', 'order', 
#'individualcount', 'locality', 'geopoint', 'scientificname', 'occurrenceid', 
#'stateprovince', 'kingdom', 'eventdate', 'phylum', 'coordinateuncertainty', 'etag', 
#'institutioncode', 'family', 'earliestperiodorlowestsystem', 'recordids'])
MyRecordList['items'][0]['indexTerms']['occurrenceid']

# test to figure out which value is the correct occurrence ID fro morphosource
# guess collection by genus, if one unique result, print and use.
#or, list possible collections for first specimen [0], and then have the user choose. 
#from either option, get minimal info necessary to link by morphosource


# for each, pull institution code. Are they all the same? Then print and store institution name. low priority.


MyRecordList['items'][0]['uuid'] #is this the occurrence ID? Nope.

#does this one help?
api.top_records(rq = query)

dir(MyRecordList)
len(MyRecordList)
MyRecordList
