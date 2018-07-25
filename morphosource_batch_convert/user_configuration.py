# -*- coding: utf-8 -*-
"""
Configuration file. User sets their choices here. 

If you are not going to use a variable, don't leave it blank. Write 'None' instead.
   Example: If you have no spreadsheet of metadata, then:
       INPUT_DF = None
"""
#%% File Paths ###############################################################
#path to folder where all your inputs are stored
INPUT_PATH = 'C:/Users/N.S/Desktop/sample_data' 

#The name of the folder containing files to batch upload.
UPLOAD_FOLDER = 'sample_ctscans' #if input path is the folder you want

#The rest of your metadata should come from either a series of CT metadata files
#or a spreadsheet, but not both. If you have both, then integrate them into 
#a single spreadsheet. See [integration code file name here. Future work.]
#The name of the folder containing CT metadata files.
CT_METADATA_FOLDER = 'sample_ctscans'
#CT_METADATA_FOLDER = None
#If your metadata are in a spreadsheet (.csv or .xlsx), put that file name here
#INPUT_DF = 'input_sample1.csv'
INPUT_DF = None

#name of final output spreadsheet file, assuming same location as input
#note no file ending. Will write to .xlsx
OUTPUT_FILE = 'MSBIW_test'

#%% Media Permissions ########################################################
#Name of the copyright holder. Also used as the entity granting permission.
PROVIDER = "Florida Museum of Natural History"

#### Copyright Permission Options:
#0: Copyright permission not set
#1: Person loading media owns copyright and grants permission for use of media on MorphoSource
#2: Permission to use media on MorphoSource granted by copyright holder
#3: Permission pending
#4: Copyright expired or work otherwise in public domain
#5: Copyright permission not yet requested
#Choose either number corresponding to institute or type 'None'.
COPY_PERMISSION = 2

#### Media Policy Options: oVert prefers 5, but check with your institution
#0: Media reuse policy not set
#1: CC0 - relinquish copyright
#2: Attribution CC BY - reuse with attribution
#3: Attribution-NonCommercial CC BY-NC - reuse but noncommercial
#4: Attribution-ShareAlike CC BY-SA - reuse here and applied to future uses
#5: Attribution- CC BY-NC-SA - reuse here and applied to future uses but noncommercial
#6: Attribution-NoDerivs CC BY-ND - reuse but no changes
#7: Attribution-NonCommercial-NoDerivs CC BY-NC-ND - reuse noncommerical no changes
#8: Media released for onetime use, no reuse without permission
#9: Unknown - Will set before project publication
MEDIA_POLICY = 3
#%% Fundamental setup choices ################################################
#determine oVert now, as will set downstream choices.
#oVert: Is this upload part of the oVert TCN grant? ['y'/'n']
OVERT = 'y'
#Batch: Are there batch scans in the upload? ['y'/'n']
BATCH = 'n'

#%% oVert-specific settings ##################################################

INSTITUTE_SEGMENT = 0
NUMBER_SEGMENT = 2
CLOSEUP_SEGMENT = 3 #for determining element

#### TCN Institutions
#0: University of Washington
#1: Field Museum of Natural History
#2: Harvard University
#3: University of California-Berkeley
#4: Louisiana State University & Agricultural and Mechanical College
#5: University of Florida
#6: University of Texas at Austin
#7: University of Kansas Center for Research Inc
#8: California Academy of Sciences
#9: Cornell University
#10: University of Michigan Ann Arbor
#11: Texas A&M AgriLife Research
#12: College of William & Mary Virginia Institute of Marine Science
#13: Academy of Natural Sciences Philadelphia
#14: Yale University
#15: University of California-San Diego Scripps Inst of Oceanography
#Choose either number corresponding to institute or type 'None'.
GRANT_SCANNING_INSTITUTION = 5
GRANT_SPECIMEN_PROVIDER = None





