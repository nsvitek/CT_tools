# -*- coding: utf-8 -*-
"""
Starting point for the user to convert data to Morphosource batch upload spreadsheet.

As a user, you change any of the variables in ALL CAPS below to suit your needs.
The default values are set here as an example to show working syntax.  
There are sometimes workable alternative settings in the #comments.

If you are not going to use a variable, don't leave it blank. Write 'None' instead.
   Example: If you have no spreadsheet of metadata, then:
       OTHER_METADATA_FILE = None
"""
#%% File Paths ################################################################
#path to folder where all your inputs are stored
INPUT_PATH = 'C:/cygwin/home/N.S/scripts/CT_tools/morphosource_batch_convert/sample_data' 

#The name of the folder containing files to batch upload.
UPLOAD_FOLDER = 'sample_ctscans'
#UPLOAD_FOLDER = None

#The rest of your metadata should come from either a series of CT metadata files
    #or a spreadsheet.
#The name of the folder containing CT metadata files.
CT_METADATA_FOLDER = 'sample_ctscans'
#CT_METADATA_FOLDER = None

#If CT scan metadata is already in a spreadsheet, enter file name. 
    #Don't forget to set CT_METADATA_FOLDER = None in this case.
#CT_METADATA_FILE = 'ctscan_batch_sample1.csv'
CT_METADATA_FILE = None
#If have additional metadata in a separate spreadsheet (.csv or .xlsx), put that file name here
#OTHER_METADATA_FILE = 'input_sample1.csv'
OTHER_METADATA_FILE = None
#Spreadsheet file options:
    #if you have a single spreadsheet with both CT metadata and other data,
    #then use only CT_METADATA_FILE and set OTHER_METADATA_FILE to None.
    
#Name of final output spreadsheet file, assuming same location as input
#note no file ending. Will write to .xlsx
OUTPUT_FILE = 'MSBIW_test'

#%% Media Permissions #########################################################
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
#%% Fundamental setup choices #################################################
#determine oVert now, as will set downstream choices.
#oVert: Is this upload part of the oVert TCN grant? ['y'/'n']
OVERT = True
#Batch: Are there batch scans in the upload? ['y'/'n']
BATCH = False

#Do you want to pull extra information to help try to match collection codes?
#Default is False for sake of simplicity
MATCH_EXTRA = False 
#possible index terms to match by: 
#'genus'
IDIGBIO_MATCH = 'genus'

#%% oVert-specific settings ###################################################
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

#File name parsing: User needs to set how a file name will be parsed into a specimen
    #In oVert, the recommended file naming convention is:
    #MUSEUM-COLLLECTION-NUMBER_notes, where MUSEUM = museum code, COLLECTION = collections code,
    #NUMBER = specimen number, and notes might be "head" or "skull" for close-up
    #or a genus name, or some other note. Notes are optional. 
#Set how a name will be broken into pieces. Default is space, dash, or underscore
    #Note that dash and underscore both need a backslash in front of them (ex: '\_')
DELIMITER = '[\_\- ]' 
#After a name is broken up by the delimiter, set which segment corresponds to which part.
#The count begins at 0, so indicate the first segment with 0, the second segment with 1, etc.
SEGMENT_MUSEUM = 0
SEGMENT_COLLECTION = 1
SEGMENT_NUMBER = 2
SEGMENT_DESCRIPTION = None
SEGMENT_BODYPART = 3

#%% CT metadata ###############################################################
##Are the CT metadata still in a series of raw CT output files, 
#    #or are they already in the input spreadsheet?
#CT_METADATA_SPREADSHEET = False

#Add additional CT settings that aren't always in raw output files:
#Write the name of the scanning technician in quotes
TECHNICIAN = 'Ada Lovelace'

#Write what wedge was use in scanning, if any, in quotes.
WEDGE = None

#If you include shading, flux, or geometric calibrations, respectively, change to True.
CALIBRATION_SHADE = True
CALIBRATION_FLUX = False
CALIBRATION_GEOMETRIC = False

#Write any description of scanner calibrations, if wanted, in quotes.
CALIBRATION_DESCRIPTION = None

#If CT_METADATA_SPREADSHEET = True, then you need to map the column names below.
    #Refer to ctscan_sample1.csv for an example of how each default maps.
NAME_SCAN = 'file_name'
NAME_VOXELX = 'X_voxel_size_mm'
NAME_VOXELY = 'Y_voxel_size_mm'
NAME_VOXELZ = 'Z_voxel_size_mm'
NAME_VOLTAGE = 'voltage_kv'
NAME_AMPERAGE = 'amperage_ua'
NAME_WATTS = 'watts'
NAME_EXPOSURE = 'exposure_time'
NAME_PROJECTIONS = 'projections'
NAME_FRAME = 'frame_averaging'
NAME_FILTER = 'filter'

#%% Spreadsheet mapping #######################################################
#This section is one you will need if INPUT_DF = True and you want to map
    #variables that were not included in the CT metadata section.
    #Refer to input_sample1.csv for an example of how each default maps.
NAME_SPECIMENS = 'Catalog number'

#If you want to use extra information to help match collection codes, 
    #what column in the spreadsheet contains the data to use for matching?
NAME_MATCH = 'Genus'
#%% Batch variables ###########################################################
#if you batch scanned, then you must have a spreadsheet in INPUT_DF.
    #Why? Because you need a key to match specimens to the batches they are a part of
    #Make sure you mapped NAME_SPECIMENS above, too. 
#this is the column name containing the name of which batch a specimen is in.
NAME_BATCH = 'Batch'
#%% If not oVert, you need to set these variables, too ########################
#Enter any grant funding as a string in quotes
FUNDING_SOURCE = 'NSF DEB-#########'
#this is the column name containing element information
NAME_ELEMENT = None
#this is the column name containing which side of the body an element comes from
#Note: when populating this column, text options are:
#Not Applicable [use for 'whole body'], Unknown, Left, Right, Midline
NAME_SIDE = None
#The column name containing the file names to be uploaded. It seems unlikely to see use.
NAME_FILE = None