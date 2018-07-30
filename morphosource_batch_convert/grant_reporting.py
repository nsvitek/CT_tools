# -*- coding: utf-8 -*-
"""
grant reporting. 
Recommended format: 'oVert TCN, NSF DBI-{id1}, NSF DBI-{id2}' 
Report scanning institute first, then collections institution.
If no institutions, lead TCN institute (UF) used provisionally. 

"""
import json

def generate_grant_report(GrantScan, GrantIn):
    """ uses recommended grant citation format for oVert TCN """
    #open up a static version of the json Kevin looked up. 
    Jfile = open('grant_numbers.json')
    GrantData = json.load(Jfile)['response']['award'] #Thank you Kevin Love. 
    Jfile.close()
    #make modifications for missing choices
    if GrantScan == 5 or GrantScan == '5': #UF will always be cited as lead TCN, no need to cite twice
        GrantScan = None
    if GrantIn == 5 or GrantScan =='5': #UF will always be cited as lead TCN, no need to cite twice
        GrantIn = None
    if GrantScan is None: #if first instituion missing, print only the second
        GrantScan = GrantIn
        GrantIn = None
    if GrantIn == GrantScan: #if same institute, only report once
        GrantIn = None
    #format grant citation text
    if GrantIn is None and GrantScan is None: #in case no institution chosen, at least cite lead TCN
        GrantText = f"oVert TCN; NSF DBI-1701714"
    if GrantIn is None and GrantScan is not None: #use if only one institution reported, as per machinations above
        GrantText = f"oVert TCN; NSF DBI-1701714; NSF DBI-{GrantData[int(GrantScan)]['id']}"
    if GrantIn is not None and GrantScan is not None:
        GrantText = f"oVert TCN; NSF DBI-1701714; NSF DBI-{GrantData[int(GrantScan)]['id']}; NSF DBI-{GrantData[int(GrantIn)]['id']}"
    return GrantText
