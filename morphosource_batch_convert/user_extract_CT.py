# -*- coding: utf-8 -*-
"""
This is a new verison of the CT_extract-settings script.

@author: N.S
"""

#from __future__ import print_function
from builtins import range
import os, re, csv
#import logging, time #for logging
import ct_metadata as ctmd
# start log for troubleshooting 
# logging.basicConfig(level=logging.INFO,filename='CT_extract-settings'+time.strftime('%Y-%m-%d')+'.log',filemode='a')
#%% User Configuration. ######################################################
#User sets each of these variables in ALL CAPS

# user enters path of folder containing files, or individual file
INPUT_PATH = "F:/Miocene_CSBR"
#INPUT_PATH = "C:/path/to/files"

# ask the user for an output file name
OUTPUT_NAME = "ctscan_metadata"

#%% End User Configuration. ##################################################
#%% Start running script. ####################################################

FileNames = ctmd.pull_ct_files(INPUT_PATH)
Results = ctmd.ct_table(FileNames)

# write a csv with results
with open(INPUT_PATH + '/' + OUTPUT_NAME + '.csv','w') as CSVFile:
	DataWriter = csv.writer(CSVFile,lineterminator = '\n')
	for i in range(0,len(Results)):
		DataWriter.writerow(Results[i])

CSVFile.close()
