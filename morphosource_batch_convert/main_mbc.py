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
#%% import dependencies #######################################################
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
import format_to_write as ftw
#%% #Start. Get specimen numbers. #############################################
print('\nStarting specimen name input.')
if uc.UPLOAD_FOLDER is not None:
    FileNamesRaw = os.listdir(uc.INPUT_PATH + '/' + uc.UPLOAD_FOLDER)
    ZipNames = []
    for file in FileNamesRaw:
        file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
        if file_parts.group(2) == "zip":
            ZipNames.append(file_parts.group(1))
    SpecimensRaw = pd.Series(ZipNames)
if uc.INPUT_DF is not None:
    UserInputRaw = inspec.read_user_input(uc.INPUT_PATH, uc.INPUT_DF)
    SpecimensRawD = UserInputRaw[uc.NAME_SPECIMENS]
    #If this is the only place with file names, give it it the standard object name [SpecimensRaw]
    if uc.UPLOAD_FOLDER is None: 
        SpecimensRaw = SpecimensRawD
        
if uc.UPLOAD_FOLDER is None and uc.INPUT_DF is None:
    sys.exit("Error: No file names. Please set either UPLOAD_FOLDER.")
#%% break up the catalogue number into parts ##################################
#if DELIMITER is not None:
SpecimensSplit = SpecimensRaw.str.split(uc.DELIMITER + '+', expand=True)
print("\nFile names split as follows:")
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

#%% query idigbio #############################################################
print('\nStarting iDigBio queries to find occurrence IDs.')
PossibleSpecimens = qi.find_options(list(Institutions)[0], list(SpecimenNumbers)[0])
PossibleCollections = qi.collections_options(PossibleSpecimens)
print('\nHere are possible collection codes based on the first specimen number:')
#%% guess collection? #########################################################
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
#%% check for multiple collections ############################################
#MultipleCollections = input("Does this batch of specimens sample multiple collections? [y/n]")
#if MultipleCollections == 'n':
#    print("Okay, just checking.")
#if MultipleCollections == 'y':
#    print("")
#    sys.exit("")
#    ### ! Future: add in the option of searching for a collection each time via a match
#%% #Element ##################################################################
#in the sample data, this info is in two columns: "body scan" and "close-up scan"
#all oVert scans will at least have "whole body", and "not applicable" for "whole body" in side
if uc.OVERT == 'y':
    SideText = "not applicable"
    if uc.SEGMENT_CLOSEUP is not None:
        ElementText = []
        for i in Closeup:
            if i is None:
                ElementText.append("whole body")
            else:
                ElementText.append(i.lower())
    else:
        ElementText = None
if uc.OVERT == 'n':
    ElementText = UserInputRaw[uc.NAME_ELEMENT]
    SideText = UserInputRaw[uc.NAME_SIDE]
#%% Grant reporting ###########################################################
print('\nStarting policy input.')
#oVert was user input earlier.
if uc.OVERT == 'y': 
    import grant_reporting as ggr
    GrantText = ggr.generate_grant_report(uc.GRANT_SCANNING_INSTITUTION,uc.GRANT_SPECIMEN_PROVIDER)
if uc.OVERT == 'n':
    Granttext = uc.FUNDING_SOURCE
#%% Copyright policy ##########################################################
CopyPerm = mp.choose_copyright_permission(uc.COPY_PERMISSION)
MediaPol = mp.choose_media_policy(uc.MEDIA_POLICY)
#%% Scan metadata #############################################################
print('\nStarting scan metadata input.')
#first, get the metadata in one of two ways:
if uc.CT_METADATA_FOLDER is not None:
    #run the extract settings script, modified temporarily
    import temp_ct_pca as tcp
    CTInputPath = uc.INPUT_PATH + '/' + uc.CT_METADATA_FOLDER
    Results = tcp.pull_pca(CTInputPath)
    CTdf = pd.DataFrame(Results[1:], columns = Results[0])
    CTdf.index = CTdf[uc.NAME_SCAN]
if uc.CT_METADATA_FOLDER is None and uc.INPUT_DF is not None:
    CTdf = UserInputRaw
if uc.CT_METADATA_FOLDER is None and uc.INPUT_DF is None:
    sys.exit("Error: No CT metadata. Please set either CT_METADATA_FOLDER or INPUT_DF.")

#read the file names and match with the specimen names
#if there are closeups [i.e., multiple scans of same specimen], exact match:
if uc.SEGMENT_CLOSEUP is not None:
   #re-sort CT metadata to match files for upload
    CTdfReorder = CTdf.reindex(SpecimensRaw)               
#if there are no closeups, then probably not multiple scans of one specimen so partial matching is okay
#create a string concatenating matching elements of file names, with or without collections code:
if uc.SEGMENT_CLOSEUP is None:
    CTSplit = CTdf[uc.NAME_SCAN].str.split(uc.DELIMITER + '+', expand=True)
    if uc.SEGMENT_COLLECTION is None:
        NamePartsSpec = Institutions + SpecimenNumbers
        NamePartsCT = CTSplit.iloc[:,uc.SEGMENT_MUSEUM]  + CTSplit.iloc[:,uc.SEGMENT_NUMBER]
    if uc.SEGMENT_COLLECTION is not None:
        NamePartsSpec = Institutions + UserCollections + SpecimenNumbers
        NamePartsCT = CTSplit.iloc[:,uc.SEGMENT_MUSEUM] + CTSplit.iloc[:,uc.SEGMENT_COLLECTION] + CTSplit.iloc[:,uc.SEGMENT_NUMBER]
    #will need to change index of CT metadata for sorting
    CTdfReorder.index = NamePartsCT
    #re-sort CT metadata to match files for upload
    CTdfReorder = CTdfReorder.reindex(NamePartsSpec)
#change index back so that there aren't index duplicates downstream
CTdfReorder = CTdfReorder.reindex(SpecimensRaw) 

#add in additional info not necessarily included in CT metadata files
if uc.TECHNICIAN is not None:
    CTdfReorder['technician'] = uc.TECHNICIAN
else:
    CTdfReorder['technician'] = None
if uc.WEDGE is not None:
    CTdfReorder['wedge'] = uc.WEDGE
else:
    CTdfReorder['wedge'] = None
CTdfReorder['shade_calib'] = uc.CALIBRATION_SHADE
CTdfReorder['flux_calib'] = uc.CALIBRATION_FLUX
CTdfReorder['geom_calib'] = uc.CALIBRATION_GEOMETRIC
if uc.CALIBRATION_DESCRIPTION is not None:
    CTdfReorder['calib_descrip'] = uc.CALIBRATION_DESCRIPTION
else:
    CTdfReorder['calib_descrip'] = None       
       
#Standardize variable names
if uc.CT_METADATA_FOLDER is None and uc.INPUT_DF is not None:
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_VOXELX: 'X_voxel_size_mm'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_VOXELY: 'Y_voxel_size_mm'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_VOXELZ: 'Z_voxel_size_mm'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_VOLTAGE: 'voltage_kv'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_AMPERAGE: 'amperage_ua'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_WATTS: 'watts'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_EXPOSURE: 'exposure_time'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_FILTER: 'filter'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_PROJECTIONS: 'projections'})
    CTdfReorder = CTdfReorder.rename(columns={uc.NAME_FRAME: 'frame_averaging'})
#%% get file names for first media object: zipped files of raw data ###########
print('\nStarting file name input.')
#ZipNames already has file names minus the '.zip', so add it back in
ZipFileNames = [s + '.zip' for s in ZipNames] 
#given that these are zipped tiff stacks or similar, no preview file
PreviewNames1 = None
#%% fill information into formatted dataframe #################################
print('\nOrganizing batch worksheet.')
Rows = list(range(3,(len(SpecimensRaw)+3))) #which rows need to be filled
Worksheet = ftw.read_mbs_worksheet(Rows)
Worksheet = ftw.fill_description(Worksheet, SpecimensRaw)
Worksheet = ftw.fill_ids(Worksheet,SpecimenDf)
Worksheet = ftw.fill_permissions(Worksheet,GrantText,uc.PROVIDER,CopyPerm,MediaPol)
Worksheet = ftw.fill_ctmetadata(Worksheet,CTdfReorder)
if ElementText is not None:
    Worksheet = ftw.fill_element(Worksheet,ElementText,SideText)
Worksheet = ftw.fill_media1(Worksheet,ZipFileNames,PreviewNames1)

# check first before writing dataframe to spreadsheet
print('\nWorksheet assembly complete.')
print('\n'*3)
print('Here are the data gathered for the first specimen entry.')
print('\n'*3)
for i in Worksheet.columns:
    if pd.isna(Worksheet.iloc[3,i]) == False:
        print(Worksheet.iloc[[1,3],i].values)
Finished = input("Does everything look correct based on the first entry? [y/n]")
if Finished == 'y':
    #if everything looks good, write to file.
    writer = pd.ExcelWriter(uc.INPUT_PATH + '/' + uc.OUTPUT_FILE + '.xlsx')
    Worksheet.to_excel(writer,'Sheet1',index=False, header=False)
    writer.save()
    print('Okay. File written.')
    sys.exit('Program finished. Goodbye!')
if Finished == 'n':
    ### ! Future: allow the code to go back to the beginning? Can you do this?
    sys.exit("Sorry. Check user_configuration.py and try again.")
