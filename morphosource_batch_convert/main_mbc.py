#! /bin/env python
""" 
Starting point for the user to convert data to Morphosource batch upload spreadsheet 
ALL_CAPS = variables the user should set. 
note: Assumptions and options for future code expansion are hidden in the imported files. Check 'em out.

Initial build uses Python3.6.5
Dependencies: pandas, idigbio, re
To install dependencies: recommend 'conda install pandas' and 'pip install idigbio' in anaconda 
"""
#import modules to make everything work. Note additional modules in imported files.  
import time #for log_data.py
import pandas as pd #for input_specimens.py
import re
import idigbio #for query_idigbio.py


#%% USER SETS THESE VARIABLES
# indicates if batch is part of oVert grant. Affects funding information.
OVERT = True 
#ASSUMPTION: Specimens have occurrence IDs in iDigBio. If not, also change OVERT to False
#path to where spreadsheet is located
INPUT_PATH = 'sample_data' 
#name of spreadsheet file. 
INPUT_FILE = 'input_sample1.csv'
#INPUT_FILE = 'input_sample3.xlsx'
#indicates that parts of specimen names [instituteion, number] are delimited.
SEPARATOR = True 
#%% log file
#Name puts log file in "logs" folder labelled with the date. 
LOG_FILENAME = 'logs/log-'+time.strftime('%Y-%m-%d')+'.log' #-%H-%M for hour and minute
from log_data import log_debug 
MyLogger = log_debug(LOG_FILENAME)
ErrorMessage = None
#%% #Start. Get specimen numbers. 
MyLogger.debug('Starting specimen name input.')
import input_specimens as inspec
UserInputRaw = inspec.read_user_input(INPUT_PATH, INPUT_FILE)
if (ErrorMessage != None): #write error if wrong file ending.
    MyLogger.error(ErrorMessage)
    ErrorMessage = None

### ! Future: use debug log to check here that file was able to be read properly
#choose specimen name column
print("### Column Options")
for i in range(len(UserInputRaw.columns)):
    print(str(i) + ": " + UserInputRaw.columns[i])
SPECIMEN_NAME = input("Select the column number containing catalog numbers:")
#pull out specimen names
SpecimensRaw = UserInputRaw.iloc[:,int(SPECIMEN_NAME)]
#break up the catalogue number into parts
if SEPARATOR == True:
    SpecimensSplit = SpecimensRaw.str.split('[ \-\_]+',expand=True)
if SEPARATOR == False:
    ### ! Future: do more than print a note. Actually write a solution
    #re.split('(\d+)',specimens_raw[2])
    print('No delimiter provides between collection code and catalog number.')
### ! Future: use debug log to check to see that column was found, string properly split.
    
print(SpecimensSplit)
InstituteCol = input("Select the column number containing institution codes:")
CatalogCol = input("Select the column number containing catalog numbers:")

#check the whole batch of specimens for some sort of consistency
#more than one collection?
Institutions = set(SpecimensSplit.iloc[:,int(InstituteCol)])
if len(Institutions) > 1:
    print('More than one institution or collection in this spreadsheet!')
    MyLogger.debug(f'Multiple institution codes found: {Institutions}')
    ### ! Future: actually do something, don't just print a note. 
#%% #pull genus to use in making best guess of collection code
print("### Column Options")
for i in range(len(UserInputRaw.columns)):
    print(str(i) + ": " + UserInputRaw.columns[i])
print("999: No column for variable of interest")

GENUS = input("Select the column number containing genus:")

if int(GENUS) == 999:
    Genera = None
else:
    Genera = UserInputRaw.iloc[:,int(GENUS)]

#%% query idigbio
api = idigbio.json() #shorten

#for now, using only the first specimen to find correct collection. This is bad long-term practice. 
#design query to find all collections in an institution that contain the first specimen number
Query = {"institutioncode": list(Institutions)[0],"catalognumber": SpecimensSplit.iloc[0,int(CatalogCol)]}
#Query = {"institutioncode": "MVZ","catalognumber": 111719}

# Search for records containing first institution code and catalog number
MyRecordList = api.search_records(rq= Query )

# make a list of collections  
PossibleCollections = []
PossibleGenera = []
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
        PossibleGenera.append("no genus given")
        MyRecordList['items'][i]['indexTerms']['genus'] = 'no genus given'
    else:
        print("   Genus of matching catalog number: " + MyRecordList['items'][i]['indexTerms']['genus'])
        PossibleGenera.append(MyRecordList['items'][i]['indexTerms']['genus'])

#%% guess collection?
Guess = input("Do you want the program to guess the correct collection based on genus provided? [y/n]")
   
if Guess == 'y':
    for i in range(len(PossibleGenera)): #take a guess of correct collection based on which record matches user-provided genus
        if PossibleGenera[i] == str.lower(Genera[0]):
            BestGuess = i
            print('Best guess of correct collection: ' + PossibleCollections[i])
            GoodGuess = input("Is this the correct collection? [y/n]")
            if GoodGuess == 'y':
                CollectionsChoice = PossibleCollections[BestGuess]
            else:
                for i in range(len(PossibleCollections)):
                    print(str(i) + ": " + PossibleCollections[i])
                UserChoice = input("Choose the number of the correct collection:")
                CollectionsChoice = PossibleCollections[int(UserChoice)]
if Guess == 'n':
    for i in range(len(PossibleCollections)):
        print(str(i) + ": " + PossibleCollections[i])
    UserChoice = input("Choose the number of the correct collection:")
    CollectionsChoice = PossibleCollections[int(UserChoice)]
    
MultipleCollections = input("Does this batch of specimens sample multiple collections? [y/n]")
if MultipleCollections == 'n':
    print("Okay, just checking.")
if MultipleCollections == 'y':
    print("This code is currently written for samples from a single collection and single institution.")
    print("Until stated otherwise, please subdivide your sample into single-collection, single-institution sets.")
    ### ! Future: add in this feature.

#%% #for each, pull the Occurrence IDs.
Collections = [CollectionsChoice]*len(SpecimensSplit)
OccurrenceIDs = []
for i in range(len(SpecimensSplit)):
    Query = {"institutioncode": SpecimensSplit.iloc[i,int(InstituteCol)],
             "catalognumber": SpecimensSplit.iloc[i,int(CatalogCol)],
             "collectioncode": CollectionsChoice}
    TempRecords = api.search_records(rq= Query )
    ### ! Future: if this query doesn't return anything, there's something very wrong. Flag.
    OccurrenceIDs.append(TempRecords['items'][0]['indexTerms']['occurrenceid'])

SpecimenDictionary = {'Institution': list(SpecimensSplit.iloc[:,int(InstituteCol)]),
                  'Collection' : Collections,
                  'CatalogNumber': list(SpecimensSplit.iloc[:,int(CatalogCol)]),
                  'OccurrenceID': OccurrenceIDs}
SpecimenDf = pd.DataFrame.from_dict(SpecimenDictionary)

#%% #Element
#in the sample data, this info is in two columns: "body scan" and "close-up scan"
#one option: ask the user if all specimens are represented by whole body scans only (no additional scans), then let them choose:
#0: yes, 1: no, 2: this information is in the input spreadsheet. check it.
#if 0: element = whole body
#if 1: ask: are all specimens the same element? [y/n]
    # if y: type anatomical element
    #if n: choose column containing element description
#if 2: Is there a column for whether or not a specimen has a whole-body scan?:
    #if y, choose column:
    #Is there a column for other elements scanned (ex: close-ups, head-only, individual element descriptions)
    #if y, choose column
    #if n, 'you have run out of options. Go back and try again, or skip element'

#how to link up scan settings in this way?
#%% #put it all together
#read in blank worksheet
WorksheetRaw = pd.read_excel('MorphoSourceBatchImportWorksheet.xlsx',header = None)
Rows = list(range(3,(len(SpecimensRaw)+3))) #which rows need to be filled

WorksheetBlank = pd.DataFrame(index=range(0, Rows[-1]+1), columns=WorksheetRaw.columns)
WorksheetBlank.iloc[0:3,:] = WorksheetRaw.iloc[0:3,:]
WorksheetFilled = WorksheetBlank

#%% Fill in inital description column, as well as media description column. Same text.
#0th column is "Description", should read: 'microCT volume and derivatives of ###'
Description = 'microCT volume and derivatives of ' + SpecimensRaw
WorksheetFilled.iloc[Rows,0] = Description.values
WorksheetFilled.iloc[Rows,46] = Description.values #46 = Media group description

#%% Fill in IDs, knowing that the occurrence ID trumps all.
WorksheetFilled.iloc[Rows,2] = SpecimenDf.iloc[:,3].values #2= OccurrenceID
WorksheetFilled.iloc[Rows,3] = SpecimenDf.iloc[:,0].values #3= Institution Code
WorksheetFilled.iloc[Rows,4] = SpecimenDf.iloc[:,1].values #4= Collections Code
WorksheetFilled.iloc[Rows,5] = SpecimenDf.iloc[:,2].values #5= Specimen Number

#%% write
writer = pd.ExcelWriter(INPUT_PATH + '/MSBIW_test.xlsx')
WorksheetFilled.to_excel(writer,'Sheet1',index=False, header=False)
writer.save()