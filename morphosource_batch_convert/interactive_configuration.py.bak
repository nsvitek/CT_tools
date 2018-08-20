# -*- coding: utf-8 -*-
"""
Interactively create a user_configuration file.

@author: N.S
"""

from shutil import copyfile
import sys #for exiting if there's a problem
import os #to check if files exist
import re #for stripping file endings, etc.
import pandas as pd
import json #for grant reporting
import input_specimens as inspec


#for safety, save an original version of the configuration file with all the notes.
copyfile('user_configuration.py','user_configuration_original.py')
File = open('user_configuration.py','w')

#%% Get going.
#path to folder where all your inputs are stored
INPUT_PATH = input('\nType the path to the folder where all your inputs are stored.') 
File.write(f'INPUT_PATH = "{INPUT_PATH}"')

UPLOAD_FOLDER = input('Type the name of the folder containing files to batch upload.')
File.write(f'\nUPLOAD_FOLDER = "{UPLOAD_FOLDER}"')

CtMetaFolder = input("\nDo you have a folder of CT metadata files? [y/n]")
if CtMetaFolder == 'y':
    CT_METADATA_FOLDER = input('Type the name of the folder of CT metadata files.')
    File.write(f'\nCT_METADATA_FOLDER = "{CT_METADATA_FOLDER}"')
if CtMetaFolder == 'n':
    CT_METADATA_FOLDER = None
    File.write(f'\nCT_METADATA_FOLDER = None')

CtMetaFile = input("\nIs CT scan metadata already in a spreadsheet? [y/n]")
if CtMetaFile == 'y':
    CT_METADATA_FILE = input('Type the file name of the CT metadata spreadsheet.')
    File.write(f'\nCT_METADATA_FILE = "{CT_METADATA_FILE}"')
if CtMetaFile == 'n':
    CT_METADATA_FILE = None
    File.write(f'\nCT_METADATA_FILE = None')

OtherMetaFile = input("\nDo you have additional metadata in a separate spreadsheet? [y/n]")
if OtherMetaFile == 'y':
    OTHER_METADATA_FILE = input('Type the file name of that spreadsheet.')
    File.write(f'\nOTHER_METADATA_FILE = "{OTHER_METADATA_FILE}"')
if OtherMetaFile == 'n':
    OTHER_METADATA_FILE = None
    File.write(f'\nOTHER_METADATA_FILE = None')

OUTPUT_FILE = input('\nType the name of the output file (plus path, if different from input).')
File.write(f'\nOUTPUT_FILE = "{OUTPUT_FILE}"')

oVert = input('\nIs this upload part of the oVert TCN grant? [y/n]')
if oVert == 'y':
    OVERT = True
    File.write(f'\nOVERT = True')
if oVert == 'n':
    OVERT = False
    File.write(f'\nOVERT = False')


Batch = input('\nAre there batch scans in the upload? [y/n]')
if Batch == 'y':
    BATCH = True
    File.write(f'\nBATCH = True')
    #this is the column name containing the name of which batch a specimen is in.
    NAME_BATCH = input('What is the name of the column containing the batch name for each specimen?')
    File.write(f'\nNAME_BATCH = "{NAME_BATCH}"')
if Batch == 'n':
    BATCH = False
    File.write(f'\nBATCH = False')
    File.write(f'\nNAME_BATCH = None')

if OtherMetaFile == 'y':
    NAME_SPECIMENS = input('\nType in the name of the column containing specimen names in the spreadsheet of additional data.')
    File.write(f'\nNAME_SPECIMENS = "{NAME_SPECIMENS}"')

if CT_METADATA_FILE is not None:
    NAME_SCAN = input('\nType the name of the column in the CT metadata spreadsheet containing scan names.')
    File.write(f'\nNAME_SCAN = "{NAME_SCAN}"')
    NAME_VOXELX = input('\nType the name of the column containing voxel size information.')
    NAME_VOXELY = NAME_VOXELZ = NAME_VOXELX
    File.write(f'\nNAME_VOXELX = "{NAME_VOXELX}"')
    File.write(f'\nNAME_VOXELY = "{NAME_VOXELY}"')
    File.write(f'\nNAME_VOXELZ = "{NAME_VOXELZ}"')
    NAME_VOLTAGE = input('\nType the name of the column containing voltage information.')
    File.write(f'\nNAME_VOLTAGE = "{NAME_VOLTAGE}"')
    NAME_AMPERAGE = input('\nType the name of the column containing amperage information.')
    File.write(f'\nNAME_AMPERAGE = "{NAME_AMPERAGE}"')
    NameWatt = input("\nIs there a column in a spreadsheet for watts? [y/n]")
    if NameWatt == 'y':
        NAME_WATTS = input('Type the name of that column.')
        File.write(f'\nNAME_WATTS = "{NAME_WATTS}"')
    if NameWatt == 'n':
        File.write(f'\nNAME_WATTS = None')
    NameExpose = input("\nIs there a column in a spreadsheet for exposure time? [y/n]")
    if NameExpose == 'y':
        NAME_EXPOSURE = input('Type the name of that column.')
        File.write(f'\nNAME_EXPOSURE = "{NAME_EXPOSURE}"')
    if NameExpose == 'n':
        File.write(f'\nNAME_EXPOSURE = None')
    NameProj = input("\nIs there a column in a spreadsheet for number of projections? [y/n]")
    if NameProj == 'y':
        NAME_PROJECTIONS = input('Type the name of that column.')
        File.write(f'\nNAME_PROJECTIONS = "{NAME_PROJECTIONS}"')
    if NameProj == 'n':
        File.write(f'\nNAME_PROJECTIONS = None')
    NameFrame = input("\nIs there a column in a spreadsheet for frame averaging? [y/n]")
    if NameFrame == 'y':
        NAME_FRAME = input('Type the name of that column.')
        File.write(f'\nNAME_FRAME = "{NAME_FRAME}"')
    if NameFrame == 'n':
        File.write(f'\nNAME_FRAME = None')
    NameFilter = input("\nIs there a column in a spreadsheet for filter information? [y/n]")
    if NameFilter == 'y':
        NAME_FILTER = input('Type the name of that column.')
        File.write(f'\nNAME_FILTER = "{NAME_FILTER}"')
    if NameFilter == 'n':
        File.write(f'\nNAME_FILTER = None')

#%% If not oVert, you need to set these variables, too ########################
if OVERT == False:
    FUNDING_SOURCE = input('\nEnter any grant funding.')
    File.write(f'\nFUNDING_SOURCE = "{FUNDING_SOURCE}"')
    NameElement = input("\nIs there a column in a spreadsheet for element information? [y/n]")
    if NameElement == 'y':
        NAME_ELEMENT = input('Type the name of that column.')
        File.write(f'\nNAME_ELEMENT = "{NAME_ELEMENT}"')
    if NameElement == 'n':
        File.write(f'\nNAME_ELEMENT = None')
    NameSide = input("\nIs there a column in a spreadsheet for element side information? [y/n]")
    if NameSide == 'y':
        NAME_SIDE = input('Type the name of that column.')
        File.write(f'\nNAME_SIDE = "{NAME_SIDE}"')
    if NameSide == 'n':
        File.write(f'\nNAME_SIDE = None')
    NameFile = input("\nIs there a column in a spreadsheet for the names of files to be uploaded? [y/n]")
    if NameFile == 'y':
        NAME_FILE = input('Type the name of that column.')
        File.write(f'\nNAME_FILE = "{NAME_FILE}"')
    if NameFile == 'n':
        NAME_FILE = None
        File.write(f'\nNAME_FILE = None')

#%% to get  the name parts.    
#delimitations
Del1 = input('\nAre your specimen names delimited \n(ex: Delimited: "MUS 12345", Undelimited: "MUS12345")? [y/n]')
if Del1 == 'n':
    DELIMITER = None #CHECK THIS
    File.write(f'\nDELIMITER = None')
if Del1 == 'y':
    DELIMITER = '[\_\- ]'
    File.write(f'\nDELIMITER = "{DELIMITER}"')
    #currently, users can't customize how names are delimited.
    
if UPLOAD_FOLDER is None and NAME_FILE is None:
    sys.exit("Error: No names of files to upload. Please set either a folder of uploads or the name of a file with upload data.")
if UPLOAD_FOLDER is not None:
    FileNamesRaw = os.listdir(INPUT_PATH + '/' + UPLOAD_FOLDER)
    ZipNames = []
    ZipEnd = []
    for file in FileNamesRaw:
        file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
        if file_parts.group(2) == "zip" or file_parts.group(2) == "dcm" :
            ZipNames.append(file_parts.group(1))
            ZipEnd.append('.' + file_parts.group(2))
            
#File option second.
if CT_METADATA_FOLDER is None and CT_METADATA_FILE is not None:
    #Read in file
    CTdf = inspec.read_user_input(INPUT_PATH, CT_METADATA_FILE)
    CTdf.index = CTdf[NAME_SCAN]

# Merge spreadsheets, if necessary 
if OTHER_METADATA_FILE is not None:
    UserInput = inspec.read_user_input(INPUT_PATH, OTHER_METADATA_FILE)
    UserInputMatch = []
    if BATCH == True:
        #merge on NAME_BATCH and NAME_SCAN. Should be exact match
        for row1 in range(len(UserInput)):
            for row2 in range(len(CTdf)):
                if UserInput[NAME_BATCH][row1] == CTdf[NAME_SCAN][row2]:
                    UserInputMatch.append(list(CTdf.iloc[row2,:]))
    if BATCH == False:
        #merge on NAME_SPECIMENS and NAME_SCAN
        for row1 in range(len(UserInput)):
            for row2 in range(len(CTdf)):
                if UserInput[NAME_SPECIMENS][row1] == CTdf[NAME_SCAN][row2]:
                    UserInputMatch.append(list(CTdf.iloc[row2,:]))
    if len(UserInputMatch) != len(UserInput):
        sys.exit("Error: cannot completely match the two spreadsheets.")
    #then turn UserInputMatch list into dataframe
    CTdfMatch = pd.DataFrame(UserInputMatch, columns = CTdf.columns)
    #merge two spreadsheets into CTdf
    CTdf = pd.concat([UserInput,CTdfMatch],axis = 1)
    CTdf.index = CTdf[NAME_SPECIMENS]

#%% file names in upload batch ################################################
#The names of the files to upload. They're either in a folder or spreadsheet column
if UPLOAD_FOLDER is None and NAME_FILE is None:
    sys.exit("Error: No names of files to upload. Please set either UPLOAD_FOLDER or NAME_FILE.")
#Folder option first
if UPLOAD_FOLDER is not None:
    FileNamesRaw = os.listdir(INPUT_PATH + '/' + UPLOAD_FOLDER)
    ZipNames = []
    ZipEnd = []
    for file in FileNamesRaw:
        file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
        if file_parts.group(2) == "zip" or file_parts.group(2) == "dcm" :
            ZipNames.append(file_parts.group(1))
            ZipEnd.append('.' + file_parts.group(2))
#Spreadsheet option next
if UPLOAD_FOLDER is None and FILE_NAME is not None:
    CTdfReorder = CTdf
    FileNamesRaw = CTdf[FILE_NAME]
    file_name_check = re.match('(^.*)\.(.*)$', FileNamesRaw[0]) #get file ending
    if file_parts is None:
        ZipNames = FileNamesRaw
    if file_parts is not None:
        ZipNames = []
        ZipEnd = []
        for file in FileNamesRaw:
            file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
            if file_parts.group(2) == "zip":
                ZipNames.append(file_parts.group(1))
                ZipEnd.append('.' + file_parts.group(2))

SpecimensRaw = pd.Series(ZipNames)

if DELIMITER is not None:
    SpecimensSplit = SpecimensRaw.str.split(uc.DELIMITER + '+', expand=True)
if DELIMITER is None:
    Entry = []
    for name in SpecimensRaw:
        Answer = re.search('([A-Z\/]*)([0-9].*)',name)
        Entry.append([Answer.group(1),Answer.group(2)])
    SpecimensSplit = pd.DataFrame(Entry,columns = [0,1])

print('\n' + SpecimensSplit)
SegMuseum = input('Type the column number containing museum codes.')
SEGMENT_MUSEUM = int(SegMuseum)
File.write(f'\nSEGMENT_MUSEUM = {SEGMENT_MUSEUM}')
SegNumber = input('Type the column number containing specimen numbers.')
SEGMENT_NUMBER = int(SegNumber)
File.write(f'\nSEGMENT_NUMBER = {SEGMENT_NUMBER}')

SC = input('Do any of these columns contain collection code? [y/n]')
if SC == 'y':
    SegCollection = input('Type the column number containing collection codes.')
    SEGMENT_COLLECTION = int(SegCollection)
    File.write(f'\nSEGMENT_COLLECTION = {SEGMENT_COLLECTION}')
if SC == 'n':
    SEGMENT_COLLECTION = None
    File.write(f'\nSEGMENT_COLLECTION = None')
SB = input('Do any of these columns contain element information? [y/n]')
if SB == 'y':
    SegBody = input('Type the column number containing element information.')
    SEGMENT_BODYPART = int(SegBody)
    File.write(f'\nSEGMENT_BODYPART = {SEGMENT_BODYPART}')
if SB == 'n':
    SEGMENT_BODYPART = None
    File.write(f'\nSEGMENT_BODYPART = None')

#%% oVert grant settings
if OVERT == True:
    Jfile = open('grant_numbers.json') #open up a static version of the json Kevin looked up. 
    GrantData = json.load(Jfile)['response']['award'] #Thank you Kevin Love. 
    Jfile.close()
    #show user the options, starting with header
    print('\n### TCN Institutions')
    #start counter
    j = 0
    #print institute options
    for i in GrantData:
        print(str(j) + ": " + i['awardeeName'])
        j = j+1
    #ask user to choose
    GrantScan = input("Which institution were specimens scanned at? If none, type 'none':")
    GrantIn = input("Which institution did specimens come from? If none, type 'none':")
    if GrantScan != 'none':
        File.write(f'\nGRANT_SCANNING_INSTITUTION = {int(GrantScan)}')
    if GrantScan == 'none':
        File.write(f'\nGRANT_SCANNING_INSTITUTION = None')
    if GrantIn != 'none':
        File.write(f'\nGRANT_SPECIMEN_PROVIDER = {int(GrantIn)}')
    if GrantIn == 'none':
        File.write(f'\nGRANT_SPECIMEN_PROVIDER = None')

#%% Keep on trucking.
        
PROVIDER = input('\nType the name of the copyright holder. This is often an instution, not a person.')
File.write(f'\nPROVIDER = "{PROVIDER}"')

CopyrightPermission = ["Copyright permission not set",
    "Person loading media owns copyright and grants permission for use of media on MorphoSource",
    "Permission to use media on MorphoSource granted by copyright holder",
    "Permission pending",
    "Copyright expired or work otherwise in public domain",
    "Copyright permission not yet requested"]
print("\n### Copyright Permission Options:")
for i in range(len(CopyrightPermission)):
    print(str(i) + ": " + CopyrightPermission[i])
PermissionChoice = input("Select copyright permission (often choice 2):")
File.write(f'\nCOPY_PERMISSION = {int(PermissionChoice)}')

MediaPolicy = ["Media reuse policy not set",
    "CC0 - relinquish copyright",
    "Attribution CC BY - reuse with attribution",
    "Attribution-NonCommercial CC BY-NC - reuse but noncommercial",
    "Attribution-ShareAlike CC BY-SA - reuse here and applied to future uses",
    "Attribution- CC BY-NC-SA - reuse here and applied to future uses but noncommercial",
    "Attribution-NoDerivs CC BY-ND - reuse but no changes",
    "Attribution-NonCommercial-NoDerivs CC BY-NC-ND - reuse noncommerical no changes",
    "Media released for onetime use, no reuse without permission",
    "Unknown - Will set before project publication"]
print("\n### Media Policy Options:")
for i in range(len(MediaPolicy)):
    print(str(i) + ": " + MediaPolicy[i])
PolicyChoice = input("Select media policy (oVert prefers 5, but check with your institution):")
File.write(f'\nMEDIA_POLICY = {int(PolicyChoice)}')

#Add additional CT settings that aren't always in raw output files:
#Write the name of the scanning technician in quotes
TECHNICIAN = input('\nType in the name of the people who assisted in CT scanning and processing.')
File.write(f'\nTECHNICIAN = "{TECHNICIAN}"')

#Write what wedge was use in scanning, if any, in quotes.
Wedge = input('\nDo you have information about the wedge used in scanning? [y/n]')
if Wedge == 'y':
    WEDGE = input('Enter wedge type (ex: "air", "cotton"):')
    File.write(f'\nWEDGE = "{WEDGE}"')
if Wedge == 'n':
    File.write(f'\nWEDGE = None')

#If you include shading, flux, or geometric calibrations, respectively, change to True.
CalShade = input('\nWere shading calibrations included in the scan? [y/n]')
if CalShade == 'y':
    File.write(f'\nCALIBRATION_SHADE = True')
if CalShade == 'n':
    File.write(f'\nCALIBRATION_SHADE = False')

CalFlux = input('\nWere flux calibrations included in the scan? [y/n]')
if CalFlux == 'y':
    File.write(f'\nCALIBRATION_FLUX = True')
if CalFlux == 'n':
    File.write(f'\nCALIBRATION_FLUX = False')


CalGeo = input('\nWere geometric calibrations included in the scan? [y/n]')
if CalGeo == 'y':
    File.write(f'\nCALIBRATION_GEOMETRIC = True')
if CalGeo == 'n':
    File.write(f'\nCALIBRATION_GEOMETRIC = False')

CalDesc = input('\nDo you have additional information about calibrations? [y/n]')
if CalDesc == 'y':
    CALIBRATION_DESCRIPTION = input('Type any description of scanner calibrations, if wanted.')
    File.write(f'\nCALIBRATION_DESCRIPTION = "{CALIBRATION_DESCRIPTION}"')
if CalDesc == 'n':
    File.write(f'\nCALIBRATION_DESCRIPTION = None')

MeshSuf = input('\nDo mesh file names have suffixes (ex: "UF-M-12345_mesh.stl")? [y/n]')
if MeshSuf == 'y':
    File.write(f'\nMESH_SUFFIX = True')
if MeshSuf == 'n':
    File.write(f'\nMESH_SUFFIX = False')
 
File.close() 
