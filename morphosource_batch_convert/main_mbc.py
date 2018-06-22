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
import pandas as pd #for input_specimens.py

# indicates if batch is part of oVert grant. Affects funding information
OVERT = True 
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
SPECIMEN_NAME = 'Catalog number'
GENUS = 'Genus'
SEPARATOR = ' ' #could also be '_' or '-' ' '.
#start
MyLogger.debug('Starting specimen name input.')
import input_specimens as inspec
UserInputRaw = inspec.read_user_input(INPUT_PATH, INPUT_FILE)
### ! Future: use debug log to check here that file was able to be read properly
### ! Future: turn SpecimensSplit into a dataframe, not a list of lists. 
SpecimensSplit = inspec.read_catalog_numbers(UserInputRaw, SPECIMEN_NAME, SEPARATOR)
### ! Future: use debug log to check to see that column was found, string properly split.
#pull genus to use in making best guess of collection code
### ! Future: make sure code doesn't break if no genus is provided
Genera = UserInputRaw[GENUS]

#%% query idigbio
import idigbio #for query_idigbio.py
api = idigbio.json() #shorten

#for now, using only the first specimen to find correct collection. This is bad long-term practice. 
### ! Future: check the whole batch of specimens for some sort of consistency
#design query to find all collections in an institution that contain the first specimen number
SpecimensSplit[0][0] #the institution name from the catalogue number
query = {"institutioncode": SpecimensSplit[0][0],"catalognumber": SpecimensSplit[0][1]}
#query = {"institutioncode": "MVZ","catalognumber": 111719}

# Search for records containing first institution code and catalog number
MyRecordList = api.search_records(rq= query )

 
# make a list of collections  
PossibleCollections = []
# populate list with options, also take a guess using genus matching
### ! Future: Give user option to let program take best guess or not. 
for i in range(len(MyRecordList['items'])):
    #tell user possible collections
    print(str(i) + " : " + MyRecordList['items'][i]['indexTerms']['collectioncode'])
    #store possible collections
    PossibleCollections.append(MyRecordList['items'][i]['indexTerms']['collectioncode'])
    #avoid error if record has no genus
    if 'genus' not in MyRecordList['items'][i]['indexTerms']:
        print("no genus given")
        MyRecordList['items'][i]['indexTerms']['genus'] = 'no genus given'
    else:
        print(MyRecordList['items'][i]['indexTerms']['genus'])
    #take a guess of correct collection based on which record matches user-provided genus
    if MyRecordList['items'][i]['indexTerms']['genus'] == str.lower(Genera[0]):
        BestGuess = i
        print('Best guess of correct collection: ' + PossibleCollections[i])
    
### ! Future: Here, the user interactively selects the collection, or at least confirms best guess
CollectionsChoice = PossibleCollections[BestGuess]

#for each, pull the Occurrence IDs.
### ! Future: Don't assume that the user put only one institution in the spreadsheet. Check and warn. 
Institutions = [SpecimensSplit[0][0]]*len(SpecimensSplit) #this is terrible. Change SpecimensSplit to dataframe above
Collections = [CollectionsChoice]*len(SpecimensSplit)
OccurrenceIDs = []
for i in range(len(SpecimensSplit)):
    query = {"institutioncode": SpecimensSplit[i][0],
             "catalognumber": SpecimensSplit[i][1],
             "collectioncode": CollectionsChoice}
    TempRecords = api.search_records(rq= query )
    ### ! Future: if this query doesn't return anything, there's something very wrong. Flag.
#    Institutions.append(TempRecords['items'][0]['indexTerms']['institutioncode'])
    OccurrenceIDs.append(TempRecords['items'][0]['indexTerms']['occurrenceid'])

SpecimenDictionary = {'Institution': Institutions,
                  'Collection' : Collections,
                  'OccurrenceID': OccurrenceIDs}
SpecimenDf = pd.DataFrame.from_dict(SpecimenDictionary)

#write results
writer = pd.ExcelWriter(INPUT_PATH + '/OccurrenceID_output.xlsx')
SpecimenDf.to_excel(writer,'Sheet1')
writer.save()

##what do I need?
#print(type(MyRecordList))
#print(MyRecordList)
#MyRecordList.keys() #what are the options?
#MyRecordList['items'][0] #first specimen option, part of a list
#type(MyRecordList['items'][0]) #is a dictionary
#MyRecordList['items'][0].keys()
#MyRecordList['items'][0]['indexTerms']
#type(MyRecordList['items'][0]['indexTerms']) #is a dictionary
#MyRecordList['items'][0]['indexTerms'].keys()
