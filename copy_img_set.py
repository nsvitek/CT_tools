# -*- coding: utf-8 -*-
"""
Script to use a dataframe to copy a specified range of images from a tiffstack
into a specified folder.

Assumes that folder structure is:
INPUT_FOLDER
    - folder named specimen 1
    - folder named specimen 2
    ...
    - tiffstack_001.tif
    - tiffstack_002.tif
    ...
    - tiffstack_999.tif
"""
#from __future__ import print_function
from builtins import input
import os, sys, re, pandas, shutil

#%% User sets these variables #################################################
#path to folder where all your tiffs and folders are stored
INPUT_FOLDER = "E:/erethizontidae_mandibles" 

# input path to spreadsheet with file names
METADATA_FILE = "E:/stack1.xlsx"

#Enter the column name that contains desired folder names.
FOLDER_NAME = "folder_names"

#Enter the column name that contains starting image number.
START_NAME = "start"
#Enter the column name that contains ending image number.
END_NAME = "end"

#%% End variables. User leaves the rest of the code alone. ####################

#get list of tif images and their index values
#list all files in the folder with the tiffs
FileOptions = os.listdir(INPUT_FOLDER)
#get the file names only of the tiffs in the tiffstack
Pictures = list(filter(lambda x: x.endswith('.tif'), FileOptions))

#then get just the index numbers of the tiffs
RegexIndex = re.compile(r'.*([0-9]{4}).tif')
PictureIndex0 = list(map(RegexIndex.findall,Pictures))
PictureIndex = [val for sublist in PictureIndex0 for val in sublist]

#function to read spreadsheet METADATA_FILE)
def read_user_input(METADATA_FILE):
    """ reads in user-provided specimen data """
    file_suffix = re.match('.*\.(.*)$',METADATA_FILE).group(1) #get file ending
    if (file_suffix == "csv"): #if file is csv
        user_input_raw = pandas.read_csv(METADATA_FILE)
    if (file_suffix == "xlsx"): #if file is excel spreadsheet
        user_input_raw = pandas.read_excel(METADATA_FILE)
    if (file_suffix not in ('csv', 'xlsx')):
        ErrorMessage = f'File ending {file_suffix} is not csv or xlsx.'
        print(ErrorMessage)
    return user_input_raws

#apply function, read METADATA_FILE
Decider = read_user_input(METADATA_FILE)

#will temporary column renaming make things easier? There's probably a better way.
Decider = Decider.rename(columns={FOLDER_NAME: 'folder_names'})
Decider = Decider.rename(columns={START_NAME: 'start'})
Decider = Decider.rename(columns={END_NAME: 'end'})

#Loop through specimens
for i in range(0,len(Decider.folder_names)):
    SpecimenFolder = INPUT_FOLDER + "/" + Decider.folder_names[i]
    #match starting number to the right index number
    SearchStringStart = str(Decider.start[i]-1).zfill(4)
    SearchStringEnd = str(Decider.end[i]-1).zfill(4)
    for ind in range(1,len(PictureIndex)):
        if re.match(SearchStringStart,PictureIndex[ind]):
            MatchStartIndex = ind
        if re.match(SearchStringEnd,PictureIndex[ind]):
            MatchEndIndex = ind
    for num in range(MatchStartIndex,MatchEndIndex):
        shutil.copy2(INPUT_FOLDER + "/" + Pictures[num],SpecimenFolder)
        print(SpecimenFolder + ": " + Pictures[num])
    
    