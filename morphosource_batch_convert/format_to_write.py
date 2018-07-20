#! /bin/env python
# -*- coding: utf-8 -*-
"""
Module is for reading and writing data in the Morphosource Batch Import Worksheet format.
"""
import pandas as pd

#read in blank worksheet
WorksheetRaw = pd.read_excel('MorphoSourceBatchImportWorksheet.xlsx',header = None)
Rows = list(range(3,(len(SpecimensRaw)+3))) #which rows need to be filled

WorksheetBlank = pd.DataFrame(index=range(0, Rows[-1]+1), columns=WorksheetRaw.columns)
WorksheetBlank.iloc[0:3,:] = WorksheetRaw.iloc[0:3,:]
WorksheetFilled = WorksheetBlank

#%% Fill in inital description column, as well as media description column. Same text.
#0th column is "Description", should read: 'microCT volume and derivatives of ###'
Description = 'microCT volume and derivatives of ' + SpecimensRaw
WorksheetFilled.iloc[Rows,0] = Description.values
WorksheetFilled.iloc[Rows,46] = Description.values #46 = Media group description

#%% Fill in IDs, knowing that the occurrence ID trumps all.
WorksheetFilled.iloc[Rows,2] = SpecimenDf.iloc[:,3].values #2= OccurrenceID
WorksheetFilled.iloc[Rows,3] = SpecimenDf.iloc[:,0].values #3= Institution Code
WorksheetFilled.iloc[Rows,4] = SpecimenDf.iloc[:,1].values #4= Collections Code
WorksheetFilled.iloc[Rows,5] = SpecimenDf.iloc[:,2].values #5= Specimen Number

#%% Fill in
WorksheetFilled.iloc[1,60:]
#48 element: whole body or not?
#49 side [column with info? y/n/skip]
#51 grant support
#55 is copyrighted?
#56 copyright permission
#57 copyright license
#58 copyright info
#59-74: scan settings
#75-83: files for first media object
#84-93: second media object
#94-101: third media object

#%% write
writer = pd.ExcelWriter(INPUT_PATH + '/MSBIW_test.xlsx')
WorksheetFilled.to_excel(writer,'Sheet1',index=False, header=False)
writer.save()