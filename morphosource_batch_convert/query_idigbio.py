#! /bin/env python
### get information from iDigBio API

import idigbio
api = idigbio.json() #shorten

#%%
#starting information from input_specimens.py 
#Eventually will be methods & classes
SpecimensRaw[0] 

#get the institution name from the catalogue number
SpecimensSplit[0][0]


#get list of collections in that institution that contain the specimen number
api.search_records(rsq={"institutioncode": SpecimensSplit[0][0]})



### ! Future: What to do if user already input collections code (inpus_sample3.xslx, 'MVZ-H-12345')
#       First, check to see if that's actually the collections ID ('amphibian and reptile specimens' not 'H')
#       If yes, use it to help narrow down the collections
#check to see if it exists, then also save that object for grant numbers later
#list the collections, then choose one, and view the specimen information
#need to get the darwin core triplet? Need to get the collections code

#%% ###### EXAMPLES FROM INTERNET
##View record by UUID
#api = idigbio.json()
#record = api.view("records","1db58713-1c7f-4838-802d-be784e444c4a")
#record
#api.search_records(rq={"catalognumber": SpecimensRaw[0]}) #does not work
#record_list = api.search_records(rq={"scientificname": "puma concolor"})
#record_list
#
##Get list of collections in an instution
#api.search_records(rq={"institutioncode": SpecimensSplit[0][0]})
#api.search_records(rq={"institutioncode": SpecimensSplit[0][0],"catalognumber": SpecimensSplit[0][1]})
#dir(api.search_records(rq={"institutioncode": SpecimensSplit[0][0],"catalognumber": SpecimensSplit[0][3]}))
##%%
#api.search_records(rq={"institutioncode": SpecimensSplit[0][0],"catalognumber": SpecimensSplit[0][1]}).aslist()
##%%
##note: not all UF collections have collections codes. Lots of other institutions don't either
##'data':{...,...,'dwc:occurrenceID':'#####',...'dwc:institutionCode'...,'dwc:catalogNumber'...,}
#api.search_records(rq={"institutioncode": 'MVZ'})
#api.search_records(rq={'uuid': 'b3976394-a174-4ceb-8d64-3a435d66bde6'})
#%% ####### BABY API EXAMPLE
##without using the python idigbio module
#import requests
## Make a get request to get the MVZ Herpetology collection from iDigBio.
#response = requests.get("https://search.idigbio.org/v2/view/b3976394-a174-4ceb-8d64-3a435d66bde6")
#
## Print the status code of the response.
#print(response.status_code) #did you get 200?
#print(response.content) #should have gotten MVZ herpetology