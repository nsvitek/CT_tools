#! /bin/env python
"""
Main point of code execution. Most other files are imported to here.

Quick Start:
1. Set the variables in ALL CAPS in the user_configuration script
2. Open the program Anaconda Prompt
3. Go to the code location by typing 'cd Path\to\morphosource_batch_convert'
4. type 'python main_mbc.py'

Initial build uses Python3.6.5
Dependencies: pandas, idigbio, re, sys, os
To install dependencies: recommend 'conda install pandas' and 'pip install idigbio' in anaconda
re, sys, os should be native

Other Notes:
This code is currently written for samples from a single collection
and single institution. If you have multi-collection uploads and do not
want to break into multiple uploads, open an Issue on GitHub
"""
#%% import dependencies
#import time #for log_data.py
import pandas as pd #for input_specimens.py
import idigbio #for query_idigbio.py
import sys #for exiting if there's a problem
import os #to check if files exist
import re #for stripping file endings, etc.

#import log_data as ld #someday, when logging starts happening, turn this on and make it work.
import user_configuration as uc
import input_specimens as inspec
import query_idigbio as qi
import media_policies as mp
#%% #Start. Get specimen numbers.
print('Starting specimen name input.')
if uc.UPLOAD_FOLDER is not None:
    UserInputRaw = os.listdir(uc.INPUT_PATH + '/' + uc.UPLOAD_FOLDER)
    ZipNames = []
    for file in UserInputRaw:
        file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
        if file_parts.group(2) == "zip":
            ZipNames.append(file_parts.group(1))
    SpecimensRaw = pd.Series(ZipNames)
if uc.UPLOAD_FOLDER is None and uc.INPUT_DF is not None:
    UserInputRaw = inspec.read_user_input(uc.INPUT_PATH, uc.INPUT_DF)
    SpecimensRaw = UserInputRaw[uc.NAME_SPECIMENS]
if uc.UPLOAD_FOLDER is None and uc.INPUT_DF is None:
    sys.exit("No file names. Please set either UPLOAD_FOLDER or INPUT_DF.")
#%% break up the catalogue number into parts
#if DELIMITER is not None:
SpecimensSplit = SpecimensRaw.str.split(uc.DELIMITER + '+', expand=True)
print("File names split as follows:")
print(SpecimensSplit)
#if DELIMITER is None:
#    ### ! Future: do more than print a note. Actually write a solution
if uc.SEGMENT_MUSEUM is None or uc.SEGMENT_NUMBER is None:
    sys.exit('Institution code or specimen number missing. Check SEGMENT_MUSEUM, SEGMENT_NUMBER, or the specimen split pattern above.')
Institutions = SpecimensSplit.iloc[:, uc.SEGMENT_MUSEUM]
if len(set(Institutions)) > 1:
    Continue = input('Warning: Multiple institution codes found: {Institutions}\nDo you want to continue? [y/n]')
    if Continue == 'n':
        sys.exit()
SpecimenNumbers = SpecimensSplit.iloc[:, uc.SEGMENT_NUMBER]

if uc.SEGMENT_COLLECTION is not None:
    UserCollections = SpecimensSplit.iloc[:, uc.SEGMENT_COLLECTION]
if uc.SEGMENT_DESCRIPTION is not None:
    UserDescription = SpecimensSplit.iloc[:, uc.SEGMENT_DESCRIPTION]
if uc.SEGMENT_CLOSEUP is not None:
    Closeup = SpecimensSplit.iloc[:, uc.SEGMENT_CLOSEUP]

#%% query idigbio
print('Starting iDigBio queries to find occurrence IDs.')
PossibleSpecimens = qi.find_options(list(Institutions)[0], list(SpecimenNumbers)[0])
PossibleCollections = qi.collections_options(PossibleSpecimens)
print('Here are possible collection codes based on the first specimen number:')
for i in PossibleCollections:
    print(i)
#%% guess collection?
#Guess = input("Do you want the program to guess the correct collection based on genus provided? [y/n]")
#if Guess == 'y':
#    Genus = qi.choose_genus_column(UserInputRaw)
#    if pd.isna(Genus[0]) == True:
#        print("No genus provided for guessing. You choose.")
#        CollectionsChoice = qi.user_choose_collection(PossibleCollections)
#    else:
#        PossibleGenera = qi.genera_options(PossibleSpecimens)
#        CollectionsChoice = qi.guess_collections(PossibleCollections, PossibleGenera, Genus)
#if Guess == 'n':
CollectionsChoice = qi.user_choose_collection(PossibleCollections)
#for each, pull the Occurrence IDs.
SpecimenDf = qi.make_occurrence_df(CollectionsChoice, SpecimensSplit, uc.SEGMENT_MUSEUM, uc.SEGMENT_NUMBER)
#SpecimenDf.iloc[:,3]
#%% check for multiple collections
#MultipleCollections = input("Does this batch of specimens sample multiple collections? [y/n]")
#if MultipleCollections == 'n':
#    print("Okay, just checking.")
#if MultipleCollections == 'y':
#    print("")
#    sys.exit("")
#    ### ! Future: add in the option of searching for a collection each time via a match
#%% Grant reporting
#oVert was user input earlier.
if uc.OVERT == 'y': 
    import grant_reporting as ggr
    GrantText = ggr.generate_grant_report(uc.GRANT_SCANNING_INSTITUTION,uc.GRANT_SPECIMEN_PROVIDER)
if uc.OVERT == 'n':
    Granttext = FUNDING_SOURCE
#%% Copyright policy
CopyPerm = mp.choose_copyright_permission(COPY_PERMISSION)
MediaPol = mp.choose_media_policy(MEDIA_POLICY)
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
Worksheet = ftw.fill_permissions(Worksheet,GrantText,PROVIDER,CopyPerm,MediaPol)

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
