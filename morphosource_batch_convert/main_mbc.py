#! /bin/env python
""" 
Starting point for the user to convert data to Morphosource batch upload spreadsheet.

Quick Start:
    1. Change the variables in ALL CAPS to your particular file names for a job
    2. Open the program Anaconda Prompt
    3. navigate to the location of the code location by typing 'cd C:\Path\to\morphosource_batch_convert'
    4. type 'python main_mbc.py'

Initial build uses Python3.6.5
Dependencies: pandas, idigbio, re, sys, os
To install dependencies: recommend 'conda install pandas' and 'pip install idigbio' in anaconda
re, sys, os should be native

note: Assumptions and options for future code expansion are hidden in the imported files. Check 'em out.
"""
INPUT_PATH = 'C:/Users/N.S/Desktop/sample_data' 
INPUT_FILE = 'input_sample1.csv'
'

#%% import published dependencies 
#import modules to make everything work. 
#import time #for log_data.py
import pandas as pd #for input_specimens.py
import idigbio #for query_idigbio.py
import sys #for exiting if there's a problem
import os #to check if files exist
#import re #for later, if need to split undelimited specimen number strings
#%% log file. Shut off for now. 
##Name puts log file in "logs" folder labelled with the date. 
#LOG_FILENAME = 'logs/log-'+time.strftime('%Y-%m-%d')+'.log' #-%H-%M for hour and minute
#from log_data import log_debug 
#MyLogger = log_debug(LOG_FILENAME)
#ErrorMessage = None
##%% check proposed files
#print('Checking to make sure paths are set.')
#ProposedIn1 = INPUT_PATH + '/' + INPUT_FILE
#print('File with specimen numbers: ' + ProposedIn1)
#if os.path.exists(ProposedIn1) == True:
#    print("Check 1 passed. Specimen number input file exists.")
#else:
#    sys.exit("No specimen number input file found. Change INPUT_FILE in main_mbc.py")
#ProposedOut = INPUT_PATH + '/' + OUTPUT_FILE + '.xlsx'
#print('Proposed Output File: ' + ProposedOut)
#if os.path.exists(ProposedOut) == True: #check to make sure the folder exists
#	Continue = ('File already exists. Do you want to overwrite it? [y/n]')
#if Continue == 'y':
#    print("Okay. Onward.")
#if Continue == 'n':
#    sys.exit("Please change OUTPUT_FILE in main_mbc.py to a new file name.")
#%% #Start. Get specimen numbers. 
#MyLogger.debug('Starting specimen name input.')
print('Starting specimen name input.')
import input_specimens as inspec

UserInputRaw = inspec.read_user_input(INPUT_PATH, INPUT_FILE)
### ! Future: use debug log to check here that file was able to be read properly
#if (ErrorMessage != None): #write error if wrong file ending.
#    MyLogger.error(ErrorMessage)
#    ErrorMessage = None

# pull raw specimen numbers
SpecimensRaw = inspec.read_catalog_numbers(UserInputRaw)

#break up the catalogue number into parts
SpecimensSplit = SpecimensRaw.str.split('[ \-\_]+',expand=True)
print(SpecimensSplit)
### ! Future: Figure out a solution for what to do if institution and number not delimited
#if SEPARATOR == True:
#    SpecimensSplit = SpecimensRaw.str.split('[ \-\_]+',expand=True)
#if SEPARATOR == False:
#    ### ! Future: do more than print a note. Actually write a solution
#    #re.split('(\d+)',specimens_raw[2])
#    sys.exit('No delimiter provided between collection code and catalog number. Stop now.')
### ! Future: use debug log to check to see that column was found, string properly split.
    
InstituteCol = int(input("Select the column number containing institution codes:")) #make integer
CatalogCol = int(input("Select the column number containing catalog numbers:")) #make integer

#check the whole batch of specimens for some sort of consistency. More than one collection?
Institutions = set(SpecimensSplit.iloc[:,InstituteCol])
if len(Institutions) > 1:
     #MyLogger.debug(f'Multiple institution codes found: {Institutions}')
     sys.exit('Warning: More than one institution or collection in this spreadsheet!')
     ### ! Future: actually do something, don't just print a note. 
#%% check for multiple collections
MultipleCollections = input("Does this batch of specimens sample multiple collections? [y/n]")
if MultipleCollections == 'n':
    print("Okay, just checking.")
if MultipleCollections == 'y':
    print("This code is currently written for samples from a single collection and single institution.")
    sys.exit("Please subdivide your sample into single-collection, single-institution sets, then try again.")
    ### ! Future: add in this feature
#%% query idigbio
print('Starting iDigBio queries to find correct collection code.')
import query_idigbio as qi
PossibleSpecimens = qi.find_options(list(Institutions)[0], SpecimensSplit.iloc[0,CatalogCol])
PossibleCollections = qi.collections_options(PossibleSpecimens)
print('Here are possible collection codes based on the first specimen number:')
for i in PossibleCollections:
    print(i)
#%% guess collection?
Guess = input("Do you want the program to guess the correct collection based on genus provided? [y/n]")
if Guess == 'y':
    Genus = qi.choose_genus_column(UserInputRaw)
    if pd.isna(Genus[0]) == True:
        print("No genus provided for guessing. You choose.")
        CollectionsChoice = qi.user_choose_collection(PossibleCollections)
    else:
        PossibleGenera = qi.genera_options(PossibleSpecimens)
        CollectionsChoice = qi.guess_collections(PossibleCollections, PossibleGenera, Genus)
if Guess == 'n':
    CollectionsChoice = qi.user_choose_collection(PossibleCollections)
  
#for each, pull the Occurrence IDs.
SpecimenDf = qi.make_occurrence_df(CollectionsChoice,SpecimensSplit,InstituteCol,CatalogCol)
#%% Grant reporting
#oVert was user input earlier.
if oVert == 'y': 
    import grant_reporting as ggr
    GrantText = ggr.generate_grant_report()
if oVert == 'n':
    Granttext = input("Please type in funding sources:")
#%% Copyright policy
import media_policies as mp
Provider = input("Please type the name of the copyright holder (often an institution):")
CopyPerm = mp.choose_copyright_permission()
MediaPol = mp.choose_media_policy()
#%% #Element
#in the sample data, this info is in two columns: "body scan" and "close-up scan"
#all oVert scans will at least have whole body
if oVert = 'y':
    WholeBody = input("Are any of the scans close-ups (of the head)? [y/n]")
    if WholeBody = 'y':
        #figure out how to delimit which scans are close-ups
#if 1: ask: are all specimens the same element? [y/n]
    # if y: type anatomical element
    #if n: choose column containing element description
#if 2: Is there a column for whether or not a specimen has a whole-body scan?:
    #if y, choose column:
    #Is there a column for other elements scanned (ex: close-ups, head-only, individual element descriptions)
    #if y, choose column
    #if n, 'you have run out of options. Go back and try again, or skip element'

#%%how to optimally link up scan settings?

#%% fill information into formatted dataframe
import format_to_write as ftw
Rows = list(range(3,(len(SpecimensRaw)+3))) #which rows need to be filled
Worksheet = ftw.read_mbs_worksheet(Rows)
Worksheet = ftw.fill_description(Worksheet, SpecimensRaw)
Worksheet = ftw.fill_ids(Worksheet,SpecimenDf)
Worksheet = ftw.fill_permissions(Worksheet,GrantText,Provider,CopyPerm,MediaPol)

# check first before writing dataframe to spreadsheet
print()
print()
print()
print('Here are the data gathered for the first specimen entry.')
print()
print()
print()
for i in Worksheet.columns:
    if pd.isna(Worksheet.iloc[3,i]) == False:
        print(Worksheet.iloc[[1,3],i].values)
Finished = input("Does everything look correct based on the first entry? [y/n]")
if Finished == 'y':
    #if everything looks good, write to file.
    writer = pd.ExcelWriter(INPUT_PATH + '/' + OUTPUT_FILE + '.xlsx')
    Worksheet.to_excel(writer,'Sheet1',index=False, header=False)
    writer.save()
    print('Okay. File written.')
    sys.exit('Program finished. Goodbye!')
if Finished == 'n':
    ### ! Future: allow the code to go back to the beginning? Can you do this?
    sys.exit("Unfortunately, you'll have to start again. We don't yet have a way to skip to specific modules for correction.")
