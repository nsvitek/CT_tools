#! /bin/env python
# -*- coding: utf-8 -*-
"""
This is a temporary copy of the CT_extract-settings script used to make the morphosource batch code work until I figure out a better configuration.

In future, hope to refactor and allow extraction from other CT file types.

### FUTURE NOTE: Is "[AutoScO] \n Active=1" the part where it specifies auto scan optimization?

"""
import os, re, csv
import pandas as pd

def pull_pca(INPUT_PATH):
    # check to make sure paths exist, that files are there.
    if os.path.isdir(INPUT_PATH): #check to make sure the folder exists
    	print('Path to raw CT metadata files found.')
    	FileNames = [] #make a list of the pca files in the folder
    	for root, dirs, files in os.walk(INPUT_PATH):
    		for file in files:
    			if file.endswith(".pca"):
    				FileNames.append(os.path.join(root, file))
    	print('CT metadata files found in this directory:')
    	for file in FileNames: #list those files so the user can check to see if these are the files they're looking for
    		print(file)
    else:
    	print('Path to raw CT metadata files not found.')
    # write the header for values
    ColumnNames = ['file_name','X_voxel_size_mm','Y_voxel_size_mm','Z_voxel_size_mm','voltage_kv','amperage_ua','watts','exposure_time','filter','projections','frame_averaging']
    #set up holder list for information
    Results = [[]]*(len(FileNames)+1)
    Results[0] = ColumnNames
    i = 1
    # extract relevant information from each pca file
    for filename in FileNames:
    	InFile = open(filename,'r') #open file
    	Text1 = InFile.read()
    	InFile.close() #close file, leaving behind the text object
    	Text2 = str.splitlines(Text1) #split text object into lines
    	Line2 = None
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
    	FileID = re.search('([^\\\/]*)\.pca',filename).group(1) # pull out file name
    	RowEntry = [FileID, VoxelSize, VoxelSize, VoxelSize, Voltage, Current, Watts, ExposureTime, Filter, NumberImages, Avg]
    	Results[i] = RowEntry
    	i = i+1
    return Results

def ctmeta_from_raw_files(CTInputPath,IndexColumn):
     Results = pull_pca(CTInputPath)
     CTdf = pd.DataFrame(Results[1:], columns = Results[0])
     CTdf.index = CTdf[IndexColumn]
     return CTdf