#! /bin/env python
# -*- coding: utf-8 -*-
"""
These are the functions to support CT metadata extraction
They are written to both (1) allow use in the morphosource batch code and
(2) work as a standalone script. Let's see how this goes.
### FUTURE NOTE: Is "[AutoScO] \n Active=1" the part where it specifies auto scan optimization?

"""
import os, re, csv
import pandas as pd

def pull_ct_files(INPUT_PATH):
    # check to make sure paths exist, that files are there.
    if os.path.isdir(INPUT_PATH): #check to make sure the folder exists
    	print('Path to raw CT metadata files found.')
    	FileNames = [] #make a list of the pca files in the folder
    	for root, dirs, files in os.walk(INPUT_PATH):
    		for file in files:
    			if file.endswith(".pca") or file.endswith(".xtekct") or file.endswith(".log"):
    				FileNames.append(os.path.join(root, file))
    	print('CT metadata files found in this directory:')
    	for file in FileNames: #list those files so the user can check to see if these are the files they're looking for
    		print(file)
    else:
    	print('Path to raw CT metadata files not found.')
    return(FileNames)    

def read_log(Text2,Filename): #a string object split into list of lines.
    for Line in range(len(Text2)): #search through lines for relevant values
        SearchVox = re.search('^Image Pixel Size \(um\)=([0-9\.]*)',Text2[Line])
        if SearchVox:
            VoxelSizeUM = SearchVox.group(1)  
        SearchImageNumber = re.search('Number of Files=[ ]*([0-9\.]*)', Text2[Line])
        if SearchImageNumber:
            NumberImages = SearchImageNumber.group(1)            
        SearchTiming = re.search('^Exposure \(ms\)=[ ]*([0-9\.]*)',Text2[Line])
        if SearchTiming:
            TimingVal = SearchTiming.group(1)   
        SearchAvg = re.search('^Frame Averaging=ON \((5)\)$',Text2[Line])
        if SearchAvg:
            Avg = SearchAvg.group(1)
        SearchVoltage = re.search('^Source Voltage \(kV\)=[ ]*([0-9\.]*)',Text2[Line])
        if SearchVoltage:
            Voltage = SearchVoltage.group(1)
        SearchCurrent = re.search('^Source Current \(uA\)=[ ]*([0-9\.]*)',Text2[Line])
        if SearchCurrent:
            Current = SearchCurrent.group(1)
        SearchFilter = re.search('^Filter=(.*)$',Text2[Line])
        if SearchFilter:
            Filter = SearchFilter.group(1)
    Skip = "unknown"
    print("\n Reminder: SkyScan log files do not record number of skipped frames.")
    Sensitivity = "unknown"
    print("Reminder: SkyScan log files do not record sensitivity settings.")
    Watts = float(Current)*float(Voltage)/1000 # calculate watts
    VoxelSizeMM = float(VoxelSizeUM)/1000
    ExposureTime = float(TimingVal)/1000
    FileID = re.search('([^\\\/]*)\.log',Filename).group(1) # pull out file name
    RowEntry = [FileID, VoxelSizeMM, VoxelSizeMM, VoxelSizeMM, Voltage, Current, Watts, ExposureTime, Filter, NumberImages, Avg]
    return(RowEntry)

def read_pca(Text2,Filename): #a string object split into list of lines.
    for Line in range(len(Text2)): #search through lines for relevant values
        SearchVox = re.search('^Voxel[sS]ize.*=([0-9\.]*)',Text2[Line])
        if SearchVox:
            VoxelSize = SearchVox.group(1)
        SearchImages = re.search('^\[CT\]',Text2[Line])
        if SearchImages:
            Line2 = Text2[Line+2]
            SearchImageNumber = re.search('NumberImages=([0-9\.]*)', Line2)
            NumberImages = SearchImageNumber.group(1)
        SearchTiming = re.search('^TimingVal=([0-9\.]*)',Text2[Line])
        if SearchTiming:
            TimingVal = SearchTiming.group(1)
        SearchAvg = re.search('^Avg=([0-9\.]*)',Text2[Line])
        if SearchAvg:
            Avg = SearchAvg.group(1)
        if not SearchAvg: #try an alternative search term in PCA if first doesn't work
            SearchAvg = re.search('^Averaging=([0-9\.]*)',Text2[Line])
            if SearchAvg:
                Avg = SearchAvg.group(1)
        SearchSkip = re.search('^Skip=([0-9\.]*)',Text2[Line])
        if SearchSkip:
            Skip = SearchSkip.group(1)
        SearchVoltage = re.search('^Voltage=([0-9\.]*)',Text2[Line])
        if SearchVoltage:
            Voltage = SearchVoltage.group(1)
        SearchCurrent = re.search('^Current=([0-9\.]*)',Text2[Line])
        if SearchCurrent:
            Current = SearchCurrent.group(1)
        SearchFilter = re.search('^Filter=(.*)$',Text2[Line])
        if SearchFilter:
            Filter = SearchFilter.group(1)
        if not SearchFilter: #try an alternative search term in PCA if first doesn't work
            SearchFilter = re.search('^XRayFilter=(.*)$',Text2[Line])
            if SearchFilter:
                Line2 = Text2[Line+1]
                SearchFilter2 = re.search('XRayFilterThickness=([0-9\.]*)', Line2)
                Filter = SearchFilter2.group(1) + SearchFilter.group(1)
        SearchSensitivity = re.search('^CameraGain=(.*)$',Text2[Line])
        if SearchSensitivity:
            Sensitivity = SearchSensitivity.group(1)
        if not SearchImages: #if the first search term for number of images didn't work, try an alternative
            for Line in range(len(Text2)): #search through lines for relevant values
                SearchImages = re.search('^\[ACQUISITION\]',Text2[Line])
                if SearchImages:
                    Line2 = Text2[Line+1]
                    SearchImageNumber = re.search('NumberImages=([0-9\.]*)', Line2)
                    NumberImages = SearchImageNumber.group(1)
    Watts = float(Current)*float(Voltage)/1000 # calculate watts
    VoxelSizeUM = float(VoxelSize)*1000
    ExposureTime = float(TimingVal)/1000
    FileID = re.search('([^\\\/]*)\.pca',Filename).group(1) # pull out file name
    RowEntry = [FileID, VoxelSize, VoxelSize, VoxelSize, Voltage, Current, Watts, ExposureTime, Filter, NumberImages, Avg]
    return(RowEntry)

def read_xtekct(Text2,Filename): #a string object split into list of lines.
    for Line in range(len(Text2)): #search through lines for relevant values
        SearchVox = re.search('^Voxel[sS]ize.*=([0-9\.]*)',Text2[Line])
        if SearchVox:
            VoxelSize = SearchVox.group(1)
        SearchImageNumber = re.search('^Projections=([0-9\.]*)', Text2[Line])
        if SearchImageNumber:
            NumberImages = SearchImageNumber.group(1)
        SearchVoltage = re.search('^XraykV=([0-9\.]*)',Text2[Line])
        if SearchVoltage:
            Voltage = SearchVoltage.group(1)
        SearchCurrent = re.search('^XrayuA=([0-9\.]*)',Text2[Line])
        if SearchCurrent:
            Current = SearchCurrent.group(1)
        SearchFilter = re.search('^Filter_ThicknessMM=(.*)$',Text2[Line])
        if SearchFilter:
            if SearchFilter.group(1) == '0.000':
                Filter = "none"
            if SearchFilter.group(1) != '0.000':
                Filter1 = SearchFilter.group(1)
                SearchFilter2 = re.search('^Filter_Material=(.*)$',Text2[Line+1])
                Filter = Filter1 + " mm" + SearchFilter2.group(1)
    #xtekct files don't record exposure time as of 08-2018
    ExposureTime = "unknown"
    print("\n Reminder: xtekct files do not record exposure time.")
    Avg = "unknown"
    print("Reminder: xtekct files do not record frame averaging.")
    Skip = "unknown"
    print("Reminder: xtekct files do not record number of skipped frames.")
    Sensitivity = "unknown"
    print("Reminder: xtekct files do not record sensitivity settings.")
    Watts = float(Current)*float(Voltage)/1000 # calculate watts
    VoxelSizeUM = float(VoxelSize)*1000
    FileID = re.search('([^\\\/]*)\.xtekct',Filename).group(1) # pull out file name
    RowEntry = [FileID, VoxelSize, VoxelSize, VoxelSize, Voltage, Current, Watts, ExposureTime, Filter, NumberImages, Avg]
    return(RowEntry)

def ct_table(FileNames):
    # write the header for values
    ColumnNames = ['file_name','X_voxel_size_mm','Y_voxel_size_mm','Z_voxel_size_mm','voltage_kv','amperage_ua','watts','exposure_time','filter','projections','frame_averaging']
    #set up holder list for information
    Results = [[]]*(len(FileNames)+1)
    Results[0] = ColumnNames
    i = 1
    # extract relevant information from each file
    for filename in FileNames:
        InFile = open(filename,'r') #open file
        Text1 = InFile.read()
        InFile.close() #close file, leaving behind the text object
        Text2 = str.splitlines(Text1) #split text object into lines
        Line2 = None
        if filename.endswith(".pca"): 
            RowEntry = read_pca(Text2,filename)
        if filename.endswith(".xtekct"): 
            RowEntry = read_xtekct(Text2,filename)
        if filename.endswith(".log"):
            RowEntry = read_log(Text2,filename)
        Results[i] = RowEntry
        i = i+1
    return(Results)

def ctmeta_from_raw_files(CTInputPath,IndexColumn):
    CTfiles = pull_ct_files(CTInputPath)
    Results = ct_table(CTfiles)
    CTdf = pd.DataFrame(Results[1:], columns = Results[0])
    CTdf.index = CTdf[IndexColumn]
    return(CTdf)