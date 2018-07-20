#! /bin/env python
# -*- coding: utf-8 -*-
"""
Module is for reading and writing data in the Morphosource Batch Import Worksheet format.
"""
import pandas as pd

#read in blank worksheet
def read_mbs_worksheet(Rows):
    WorksheetRaw = pd.read_excel('MorphoSourceBatchImportWorksheet.xlsx',header = None)
    WorksheetBlank = pd.DataFrame(index=range(0, Rows[-1]+1), columns=WorksheetRaw.columns)
    WorksheetBlank.iloc[0:3,:] = WorksheetRaw.iloc[0:3,:]
    return WorksheetBlank
#%% Fill in inital description column, as well as media description column. Same text.
#0th column is "Description", should read: 'microCT volume and derivatives of ###'
#Worksheet is the output of read_mbs_worksheet() or some partially-filled derivative
#SpecimensRaw is an object, a column of specimen numbers (ex: UF 12345, UF 23456): 
def fill_description(Worksheet, SpecimensRaw):
    Description = 'microCT volume and derivatives of ' + SpecimensRaw
    Worksheet.iloc[3:,0] = Description.values
    Worksheet.iloc[3:,46] = Description.values #46 = Media group description
    return Worksheet
#%% Fill in IDs, knowing that the occurrence ID trumps all.
#Worksheet is the output of read_mbs_worksheet() or some partially-filled derivative
#SpecimenDf is a dataframe derived from code to pull Occurrence IDs
def fill_ids(Worksheet,SpecimenDf):
    Worksheet.iloc[3:,2] = SpecimenDf.iloc[:,3].values #2= OccurrenceID
    Worksheet.iloc[3:,3] = SpecimenDf.iloc[:,0].values #3= Institution Code
    Worksheet.iloc[3:,4] = SpecimenDf.iloc[:,1].values #4= Collections Code
    Worksheet.iloc[3:,5] = SpecimenDf.iloc[:,2].values #5= Specimen Number
    return Worksheet
#%% Fill in element
#Worksheet.iloc[1,60:] #shows column names
#48 element: whole body or not?
#49 side [column with info? y/n/skip]
#%% Fill in grant, copyright info
def fill_permissions(Worksheet,GrantText,Provider,CopyPerm,MediaPol):
    Worksheet.iloc[3:,51] = GrantText #51= Funding information
    Worksheet.iloc[3:,52] = f"{Provider} provided access to these data"
    Worksheet.iloc[3:,54] = f", the collection of which was funded by {GrantText}."
    Worksheet.iloc[3:,55] = True #55= Is it copyrighted?
    Worksheet.iloc[3:,56] = CopyPerm #56= Who gave permission?
    Worksheet.iloc[3:,57] = MediaPol #57= Media license
    Worksheet.iloc[3:,57] = Provider #58= Copyright holder
    return Worksheet
#%% Scan settings
#59-74: scan settings
#75-83: files for first media object
#84-93: second media object
#94-101: third media object