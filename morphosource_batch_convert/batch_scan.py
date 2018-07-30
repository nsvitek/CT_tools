# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 18:39:07 2018

@author: N.S
"""
#first, take care of getting CT metadata into a dataframe
    #either through temp_ct_pca if uc.CT_METADATA_FOLDER has a path
    #or through reading uc.CT_METADATA_FILE
    
#then, match that spreadsheet (CTSpreadsheet) to UserInputRaw
#def match_batch(UserSpreadsheet,CTSpreadsheet):

#then, once you've gone through and created a bright and shiny CTdf,
    #match up to the file names [some combo of SpecimensRaw, SpecimensSplit, Institutions,
    #SpecimenNumbers,UserCollections], to reorder CTdf into CTdfReorder
    #Remember that if batch, then you're matching on NAME_SPECIMENS not NAME_SCAN