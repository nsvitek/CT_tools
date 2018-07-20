# -*- coding: utf-8 -*-
"""
grant reporting. 
Recommended format: 'oVert TCN, NSF DBI-{id1}, NSF DBI-{id2}' 
Report scanning institute first, then collections institution.
If no institutions, lead TCN institute (UF) used provisionally. 

"""
import json

def generate_grant_report():
    """ uses recommended grant citation format for oVert TCN """
    #open up a static version of the json Kevin looked up. 
    Jfile = open('grant_numbers.json')
    GrantData = json.load(Jfile)['response']['award'] #Thank you Kevin Love. 
    Jfile.close()
    #show user the options, starting with header
    print('### TCN Institutions')
    #start counter
    j = 0
    #print institute options
    for i in GrantData:
        print(str(j) + ": " + i['awardeeName'])
        j = j+1
    #ask user to choose
    GrantScan = input("Which institution were specimens scanned at? If none, type 'none':")
    GrantIn = input("Which institution did specimens come from? If none, type 'none':")
    #make modifications for missing choices
    if GrantIn == GrantScan == 'none': #in case no institution chosen, at least cite lead TCN
        GrantScan = '5'
    if GrantScan == 'none': #if first instituion missing, print only the second
        GrantScan = GrantIn
        GrantIn = 'none'
    if GrantIn == GrantScan: #if same institute, only report once
        GrantIn = 'none'
    #format grant citation text
    if GrantIn == 'none': #use if only one institution reported, as per machinations above
        GrantText = f"oVert TCN, NSF DBI-{GrantData[int(GrantScan)]['id']}"
    else:
        GrantText = f"oVert TCN, NSF DBI-{GrantData[int(GrantScan)]['id']}, NSF DBI-{GrantData[int(GrantIn)]['id']}"
    return GrantText


