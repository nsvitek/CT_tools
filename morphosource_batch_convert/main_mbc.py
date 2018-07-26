#! /bin/env python
""" 
Main point of code execution. Most other files are imported to here. 

Quick Start:
    1. Change the variables in ALL CAPS in the user_configuration script to your particular file names for a job
    2. Open the program Anaconda Prompt
    3. navigate to the location of the code location by typing 'cd C:\Path\to\morphosource_batch_convert'
    4. type 'python main_mbc.py'

Initial build uses Python3.6.5
Dependencies: pandas, idigbio, re, sys, os
To install dependencies: recommend 'conda install pandas' and 'pip install idigbio' in anaconda
re, sys, os should be native

Other Notes:
This code is currently written for samples from a single collection and single institution.
If you have multi-collection uploads and do not want to break into multiple uploads, open an Issue on GitHub
"""
#%% import dependencies 
#import time #for log_data.py
import pandas as pd #for input_specimens.py
import idigbio #for query_idigbio.py
import sys #for exiting if there's a problem
import os #to check if files exist
import re #for stripping file endings, etc.

import user_configuration as uc
import input_specimens as inspec

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

if UPLOAD_FOLDER is not None:
    UserInputRaw = os.listdir(INPUT_PATH + '/' + UPLOAD_FOLDER)
    ZipNames = []
    for file in UserInputRaw:
        file_parts = re.match('(^.*)\.(.*)$',file) #get file ending
        if file_parts.group(2) == "zip":
            ZipNames.append(file_parts.group(1))
    SpecimensRaw = pd.Series(ZipNames)
if UPLOAD_FOLDER is None and INPUT_DF is not None:
    UserInputRaw = inspec.read_user_input(INPUT_PATH, INPUT_DF)
    SpecimensRaw = UserInputRaw[,SpecimenName]
else:
    sys.exit("No file names. Please set either UPLOAD_FOLDER or INPUT_DF.") 

#break up the catalogue number into parts
SpecimensSplit = SpecimensRaw.str.split(DELIMITER + '+',expand=True)
print("File names split as follows:")
print(SpecimensSplit)
#if DELIMITER is not None:
#    SpecimensSplit = SpecimensRaw.str.split('[ \-\_]+',expand=True)
#if DELIMITER is None:
#    ### ! Future: do more than print a note. Actually write a solution

#%% check for multiple collections
#MultipleCollections = input("Does this batch of specimens sample multiple collections? [y/n]")
#if MultipleCollections == 'n':
#    print("Okay, just checking.")
#if MultipleCollections == 'y':
#    print("")
#    sys.exit("")
#    ### ! Future: add in the option of searching for a collection each time via a match
#%% query idigbio
print('Starting iDigBio queries to find occurrence IDs.')
import query_idigbio as qi
PossibleSpecimens = qi.find_options(list(Institutions)[0], SpecimensSplit.iloc[0,SEGMENT_NUMBER])
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
SpecimenDf = qi.make_occurrence_df(CollectionsChoice,SpecimensSplit,SEGMENT_MUSEUM,SEGMENT_NUMBER)
#%% Grant reporting
#oVert was user input earlier.
if oVert == 'y': 
    import grant_reporting as ggr
    GrantText = ggr.generate_grant_report()
if oVert == 'n':
    Granttext = FUNDING_SOURCE
#%% Copyright policy
import media_policies as mp
Provider = input("Please type the name of the copyright holder (often an institution):")
CopyPerm = mp.choose_copyright_permission()
MediaPol = mp.choose_media_policy()
#%% #Element
#in the sample data, this info is in two columns: "body scan" and "close-up scan"
#all oVert scans will at least have whole body

#How to tell what has a close-up and what doesn't? Should be a suffix name. Probably most reliable way.


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
