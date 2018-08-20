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
import copy
from numpy import nan

#import log_data as ld #someday, when logging starts happening, turn this on and make it work.
import user_configuration as uc
import input_specimens as inspec
import query_idigbio as qi
import media_policies as mp
import format_to_write as ftw
import ct_metadata as ctmd
#%% #Start. Get the files in. #################################################
print('\nStarting file input.')
#%% Scan metadata files########################################################
#Users must have one input or the other, but not both. 
if uc.CT_METADATA_FILE is not None and uc.CT_METADATA_FOLDER is not None:
    sys.exit("Error: Cannot have both CT metadata folder and file. Edit user_configuration.")
if uc.CT_METADATA_FILE is None and uc.CT_METADATA_FOLDER is None:
    sys.exit("Error: No CT metadata. Please set either CT_METADATA_FOLDER or CT_METADATA_FILE.")
#Folder option first.
if uc.CT_METADATA_FOLDER is not None: #works for either batch or not
    #run the extract settings script, modified temporarily
    CTInputPath = uc.INPUT_PATH + '/' + uc.CT_METADATA_FOLDER
    CTdf = ctmd.ctmeta_from_raw_files(CTInputPath,uc.NAME_SCAN)
    #set UserInputCT to none, in contrast to file option
    UserInputCT = None
#File option second.
if uc.CT_METADATA_FOLDER is None and uc.CT_METADATA_FILE is not None:
    #Read in file
    CTdf = inspec.read_user_input(uc.INPUT_PATH, uc.CT_METADATA_FILE)
    CTdf.index = CTdf[uc.NAME_SCAN]
    #Standardize variable names
    CTdf = CTdf.rename(columns={uc.NAME_VOXELX: 'X_voxel_size_mm'})
    CTdf = CTdf.rename(columns={uc.NAME_VOXELY: 'Y_voxel_size_mm'})
    CTdf = CTdf.rename(columns={uc.NAME_VOXELZ: 'Z_voxel_size_mm'})
    CTdf = CTdf.rename(columns={uc.NAME_VOLTAGE: 'voltage_kv'})
    CTdf = CTdf.rename(columns={uc.NAME_AMPERAGE: 'amperage_ua'})
    CTdf = CTdf.rename(columns={uc.NAME_WATTS: 'watts'})
    CTdf = CTdf.rename(columns={uc.NAME_EXPOSURE: 'exposure_time'})
    CTdf = CTdf.rename(columns={uc.NAME_FILTER: 'filter'})
    CTdf = CTdf.rename(columns={uc.NAME_PROJECTIONS: 'projections'})
    CTdf = CTdf.rename(columns={uc.NAME_FRAME: 'frame_averaging'})
   
#%% Merge spreadsheets, if necessary #########################################
if uc.OTHER_METADATA_FILE is not None:
    UserInput = inspec.read_user_input(uc.INPUT_PATH, uc.OTHER_METADATA_FILE)
    UserInputMatch = []
    if uc.BATCH == True:
        #merge on uc.NAME_BATCH and uc.NAME_SCAN. Should be exact match
        for row1 in range(len(UserInput)):
            for row2 in range(len(CTdf)):
                if UserInput[uc.NAME_BATCH][row1] == CTdf[uc.NAME_SCAN][row2]:
                    UserInputMatch.append(list(CTdf.iloc[row2,:]))
    if uc.BATCH == False:
        #merge on uc.NAME_SPECIMENS and uc.NAME_SCAN
        for row1 in range(len(UserInput)):
            for row2 in range(len(CTdf)):
                if UserInput[uc.NAME_SPECIMENS][row1] == CTdf[uc.NAME_SCAN][row2]:
                    UserInputMatch.append(list(CTdf.iloc[row2,:]))
    if len(UserInputMatch) != len(UserInput):
        sys.exit("Error: cannot completely match the two spreadsheets.")
    #then turn UserInputMatch list into dataframe
    CTdfMatch = pd.DataFrame(UserInputMatch, columns = CTdf.columns)
    #merge two spreadsheets into CTdf
    CTdf = pd.concat([UserInput,CTdfMatch],axis = 1)
    CTdf.index = CTdf[uc.NAME_SPECIMENS]

#%% file names in upload batch ################################################
#The names of the files to upload. They're either in a folder or spreadsheet column
if uc.UPLOAD_FOLDER is None and uc.NAME_FILE is None:
    sys.exit("Error: No names of files to upload. Please set either UPLOAD_FOLDER or NAME_FILE.")
#Folder option first
if uc.UPLOAD_FOLDER is not None:
    FileNamesRaw = os.listdir(uc.INPUT_PATH + '/' + uc.UPLOAD_FOLDER)
    ZipNames = []
    ZipEnd = []
    for file in FileNamesRaw:
        file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
        if file_parts.group(2) == "zip" or file_parts.group(2) == "dcm" :
            ZipNames.append(file_parts.group(1))
            ZipEnd.append('.' + file_parts.group(2))
#Spreadsheet option next
if uc.UPLOAD_FOLDER is None and uc.FILE_NAME is not None:
    CTdfReorder = CTdf
    FileNamesRaw = CTdf[uc.FILE_NAME]
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

#Either way, get column of specimen names
SpecimensRaw = pd.Series(ZipNames)
print("All files in. Starting processing.")
#%% break up the catalogue number into parts ##################################
print("Linking input by specimen name.")
#split the specimen name so that individual pieces can be compared across input
if DELIMITER is not None:
    SpecimensSplit = SpecimensRaw.str.split(uc.DELIMITER + '+', expand=True)
if DELIMITER is None:
    Entry = []
    for name in SpecimensRaw:
        Answer = re.search('([A-Z\/]*)([0-9].*)',name)
        Entry.append([Answer.group(1),Answer.group(2)])
    SpecimensSplit = pd.DataFrame(Entry,columns = [0,1])

print("\nFile names split as follows:")
print(SpecimensSplit)
if uc.SEGMENT_MUSEUM is None or uc.SEGMENT_NUMBER is None:
    sys.exit('Institution code or specimen number missing. Check SEGMENT_MUSEUM, SEGMENT_NUMBER, or the specimen split pattern above.')
Institutions = SpecimensSplit.iloc[:, uc.SEGMENT_MUSEUM]
if len(set(Institutions)) > 1:
    Continue = input('Warning: Multiple institution codes found: {Institutions}\nDo you want to continue? [y/n]')
    if Continue == 'n':
        sys.exit()
SpecimenNumbers = SpecimensSplit.iloc[:, uc.SEGMENT_NUMBER]
#look for optional collection designation
if uc.SEGMENT_COLLECTION is not None:
    UserCollections = SpecimensSplit.iloc[:, uc.SEGMENT_COLLECTION]
else:
    UserCollections = None
#look for optional close-up scan designation
if uc.SEGMENT_BODYPART is not None:
    Closeup = SpecimensSplit.iloc[:, uc.SEGMENT_BODYPART]
else:
    Closeup = None
#%% standardize entry order between file names and metadata ###################
#create a string concatenating matching elements of file names, with or without collections code:
if uc.BATCH == True:
    CTSplit = CTdf[uc.NAME_SPECIMENS].str.split(uc.DELIMITER + '+', expand=True)
if uc.BATCH == False:
    CTSplit = CTdf[uc.NAME_SCAN].str.split(uc.DELIMITER + '+', expand=True)
if uc.SEGMENT_COLLECTION is None:
    NamePartsSpec = Institutions + SpecimenNumbers
    NamePartsCT = CTSplit.iloc[:,uc.SEGMENT_MUSEUM]  + CTSplit.iloc[:,uc.SEGMENT_NUMBER]
if uc.SEGMENT_COLLECTION is not None:
    NamePartsSpec = Institutions + UserCollections + SpecimenNumbers
    NamePartsCT = CTSplit.iloc[:,uc.SEGMENT_MUSEUM] + CTSplit.iloc[:,uc.SEGMENT_COLLECTION] + CTSplit.iloc[:,uc.SEGMENT_NUMBER]

#if there are close-ups [i.e., multiple scans of same specimen], require exact match:
if uc.SEGMENT_BODYPART is not None:
   #re-sort CT metadata to match files for upload
    CTdfReorder = CTdf.reindex(SpecimensRaw)               
#if there are no closeups, then probably not multiple scans of one specimen so partial matching is okay
if uc.SEGMENT_BODYPART is None:
    #will need to change index of CT metadata for sorting
    CTdf.index = NamePartsCT
    #re-sort CT metadata to match files for upload
    CTdfReorder = CTdf.reindex(NamePartsSpec)
#change index back so that there aren't index duplicates downstream
CTdfReorder.index = SpecimensRaw 
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
if uc.OVERT == True:
    SideText = "not applicable"
    if uc.SEGMENT_BODYPART is not None:
        ElementText = []
        for i in Closeup:
            if i is None:
                ElementText.append("whole body")
            else:
                ElementText.append(i.lower())
    else:
        ElementText = None
if uc.OVERT == False:
    ElementText = UserInputRaw[uc.NAME_ELEMENT]
    SideText = UserInputRaw[uc.NAME_SIDE]
#%% additional CT metadata ####################################################
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
    
# for each in filter, if 'Unknown' set to 'none'
for line in CTdfReorder['filter']:
    if line == 'Unknown':
        line = 'none'
#%% Grant reporting ###########################################################
print('\nStarting policy input.')
#oVert was user input earlier.
if uc.OVERT == True: 
    import grant_reporting as ggr
    GrantText = ggr.generate_grant_report(uc.GRANT_SCANNING_INSTITUTION,uc.GRANT_SPECIMEN_PROVIDER)
if uc.OVERT == False:
    Granttext = uc.FUNDING_SOURCE
#%% Copyright policy ##########################################################
CopyPerm = mp.choose_copyright_permission(uc.COPY_PERMISSION)
MediaPol = mp.choose_media_policy(uc.MEDIA_POLICY)
#%% get file names for first media object: zipped files of raw data ###########
print('\nStarting file name input.')
#ZipNames already has file names minus the '.zip', so add it back in
ZipFileNames = ZipNames + ZipEnd
ZipTitle = []
#make the titles depending on type
for ending in ZipEnd:
    if ending == '.zip':
        ZipTitle.append('zipped tiff stack')
    if ending == '.dcm':
        ZipTitle.append('dicom stack')
ZipFileNames = ['{}{}'.format(a_, b_) for a_, b_ in zip(ZipNames,ZipEnd)]
#%% get file names for other media object(s): mesh files ###########
#Meshes have both their own files and preview image files. Make holder for each
MeshNames = [[] for _ in range(2)] #list of 2 lists
PreviewNames = [[] for _ in range(2)] #list of 2 lists
for file in FileNamesRaw:
    file_parts = re.match('(^.*)\.(.*)$', file) #get file ending
    #find surface files
    if file_parts.group(2) == "stl" or file_parts.group(2) == "ply":
        MeshNames[0].append(file_parts.group(1))
        MeshNames[1].append(file_parts.group(2))
    #find preview files
    if file_parts.group(2) == "jpg" or file_parts.group(2) == "jpeg" or file_parts.group(2) == "png" or file_parts.group(2) == "tiff" or file_parts.group(2) == "psd":
        PreviewNames[0].append(file_parts.group(1))
        PreviewNames[1].append(file_parts.group(2))
#if there are any mesh files, split file name strings for matching
if MeshNames[0] != []:
    MeshSplit = pd.Series(MeshNames[0]).str.split(uc.DELIMITER + '+', expand=True)
    if uc.SEGMENT_COLLECTION is None:
        NamePartsMesh = MeshSplit.iloc[:,uc.SEGMENT_MUSEUM] + MeshSplit.iloc[:,uc.SEGMENT_NUMBER]
    if uc.SEGMENT_COLLECTION is not None:
        NamePartsMesh = MeshSplit.iloc[:,uc.SEGMENT_MUSEUM] + MeshSplit.iloc[:,uc.SEGMENT_COLLECTION] + MeshSplit.iloc[:,uc.SEGMENT_NUMBER]
    #get a list of specimens with meshes for comparisons
    MeshNamesUnique = set(NamePartsMesh)
    #Start by assuming no need for suffixes
    NeedSuffix = False
    #If the user says you need a suffix, then it must be true.
    if uc.MESH_SUFFIX == True:
        NeedSuffix = True
    for name in MeshNamesUnique:
        #Check to make sure each mesh matches a file name
        if name not in list(NamePartsSpec):
            print(f"Mesh ID {name} cannot be matched to raw file.")
        if list(NamePartsMesh).count(name) > 1: #Check for multiple meshes per name:
            NeedSuffix = True
    if NeedSuffix == True:
        #If suffix needed, look at last delimited column
        SuffixColumn = len(MeshSplit.columns)-1
        #make a column of suffixes
        Suffixes = MeshSplit.iloc[:,SuffixColumn]
    if NeedSuffix == False:
        Suffixes = ['']*len(MeshNames[0])
    #make a set of suffixes in that column
    SuffixSet = set(Suffixes)
    #strip names of suffixes, if present, for later matching
    MeshZip = []
    for index in range(len(MeshNames[0])):
        if NeedSuffix == True:
            RegexTerm = '(.*)' + uc.DELIMITER + Suffixes[index]
        if NeedSuffix == False:
            RegexTerm = '(.*)'
        MinusSuffix = re.match(RegexTerm, MeshNames[0][index]).group(1)
        MeshZip.append(MinusSuffix)
    #if there are preview names, match mesh names exactly for now.
    #if there are meshes but no previews, ask if the user still wants to continue.
    if PreviewNames[0] == [] and MeshNames[0] != []:
        Continue = input("No preview files for meshes found. Do you want to continue? [y/n]")
        if Continue == 'n':
            sys.exit()
        if Continue == 'y':
            PreviewNames2 = None
    #if there are previews, get matching
    if PreviewNames[0] != []:
        PreviewMatch = copy.deepcopy(MeshNames)
        for index in range(len(PreviewMatch[0])):
            if PreviewMatch[0][index] not in PreviewNames[0]:
                PreviewMatch[0][index] = None
                PreviewMatch[1][index] = None
            if PreviewMatch[0][index] in PreviewNames[0]:
                index2 = PreviewNames[0].index(PreviewMatch[0][index])
                PreviewMatch[1][index] = PreviewNames[1][index2]
    MeshData = [[[[None] for _ in range(4)] for z in range(len(SuffixSet))] for _ in range(len(ZipNames))]
    #for each file in ZipFile
    for index1 in range(len(MeshData)):
        #find any mesh files that match that ZipNames[index1]
        ZipMatches = [i for i, x in enumerate(MeshZip) if x==(ZipNames[index1])]
                    #look for a match of specimen and suffix
        #if no match, then move on
        if ZipMatches == []:
            next
        #if 1 or more matches, start filling in dictionaries
        else:
            #subset to only the information you need for these matches
            SubNames1 = [MeshNames[0][i] for i in ZipMatches]
            SubNames2 = [MeshNames[1][i] for i in ZipMatches]
            SubNamesP = [PreviewMatch[1][i] for i in ZipMatches]
            SubNames = ['{}.{}'.format(a, b) for a, b in zip(SubNames1,SubNames2)]
            SubPreview = ['{}.{}'.format(a, b) for a, b in zip(SubNames1,SubNamesP)]
            SubSuffix = [Suffixes[i] for i in ZipMatches]
            #then iterate to fill in dictionaries for the matched zip file
            for index2 in range(len(ZipMatches)):
                #file name
                MeshData[index1][index2][0] = [SubNames[index2]]
                #preview name
                if SubNamesP == [None]:
                    MeshData[index1][index2][1] = [None]
                else:
                    MeshData[index1][index2][1] = [SubPreview[index2]]
                #title
                MeshData[index1][index2][2] = [SubSuffix[index2] + " mesh file"]
                if SubNames[index2] == None:
                    MeshData[index1][index2][3] = [None]
                else:
                    MeshData[index1][index2][3] = ["derivative"]
#if there are no mesh files, set whatever variables you need to None
if MeshNames[0] == []:
    MeshData = None

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
Worksheet = ftw.fill_zip(Worksheet,ZipFileNames, ZipTitle)
if MeshData is not None:
    Worksheet = ftw.fill_meshes(Worksheet, MeshData)
#fix those None vs. NaN values
Worksheet.fillna(value=nan, inplace=True)
#    Worksheet.iloc[3,:]
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