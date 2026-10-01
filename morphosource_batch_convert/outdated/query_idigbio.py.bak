#! /bin/env python
""" get information from iDigBio API """
import idigbio #for query_idigbio.py
import pandas as pd

def find_options(InstitutionCode,CatalogNumber):
    #for now, using only the first specimen to find correct collection. 
    #design query to find all collections in an institution that contain the first specimen number
    Query = {"institutioncode": InstitutionCode,"catalognumber": CatalogNumber}
    api = idigbio.json() #shorten
    # Search for records containing first institution code and catalog number
    MyRecordList = api.search_records(rq= Query )
    return MyRecordList

def collections_options(MyRecordList):
    """ make a list of possible collections matching a catalog number query """
    PossibleCollections = []
    for i in range(len(MyRecordList['items'])):
        PossibleCollections.append(MyRecordList['items'][i]['indexTerms']['collectioncode'])
    return PossibleCollections

def genera_options(MyRecordList):
    """ make a list of genera corresponding the list of possible collections in collections_options()"""
    PossibleGenera = []
    for i in range(len(MyRecordList['items'])):
        if 'genus' not in MyRecordList['items'][i]['indexTerms']:
            PossibleGenera.append("no genus given")
            #MyRecordList['items'][i]['indexTerms']['genus'] = 'no genus given' #no longer returned
        else:
            PossibleGenera.append(MyRecordList['items'][i]['indexTerms']['genus'])
    return PossibleGenera

def choose_genus_column(UserInputRaw):
    """pull genus from user-input dataframe to use in making best guess of collection code."""
    for i in range(len(UserInputRaw.columns)):
        print(str(i) + ": " + UserInputRaw.columns[i])
    print("999: No column for variable of interest")
    Genus = int(input("Select the column number containing genus:")) #make integer
    if Genus == 999:
        Genera = None
    if pd.isna(UserInputRaw.iloc[0,Genus]) == True:
        print("This column is blank.")
        Genera = None
    else:
        Genera = UserInputRaw.iloc[:,Genus]
    return Genera

def user_choose_collection(PossibleCollections):
    """ User manually selects the correct collection code."""
    for i in range(len(PossibleCollections)):
        print(str(i) + ": " + PossibleCollections[i])
    UserChoice = input("Choose the number of the correct collection:")
    CollectionsChoice = PossibleCollections[int(UserChoice)]
    return CollectionsChoice

def guess_collections(PossibleCollections, PossibleGenera, Genus):
    """By comparing user-provided genus and iDigBio-scraped genera, program guesses correct collection"""
    BestGuess = None
    for i in range(len(PossibleGenera)): #take a guess of correct collection based on which record matches user-provided genus
        if PossibleGenera[i] == str.lower(Genus[0]):
            BestGuess = i
            print()
            print('Best guess of correct collection: ' + PossibleCollections[i])
            GoodGuess = input("Is this the correct collection? [y/n]")
            if GoodGuess == 'y':
                CollectionsChoice = PossibleCollections[BestGuess]
    if BestGuess == None: 
        print("No match found. Can't guess. Please choose a collection.")
        CollectionsChoice = user_choose_collection(PossibleCollections)
    return CollectionsChoice

def make_occurrence_df(CollectionsChoice,SpecimensSplit,InstituteCol,CatalogCol):
    Collections = [CollectionsChoice]*len(SpecimensSplit)
    OccurrenceIDs = []
    for i in range(len(SpecimensSplit)):
        Query = {"institutioncode": SpecimensSplit.iloc[i,InstituteCol],
                 "catalognumber": SpecimensSplit.iloc[i,CatalogCol],
                 "collectioncode": CollectionsChoice}
        api = idigbio.json() #shorten
        TempRecords = api.search_records(rq= Query )
        ### ! Future: if this query doesn't return anything, there's something very wrong. Flag.
        OccurrenceIDs.append(TempRecords['items'][0]['indexTerms']['occurrenceid'])
    SpecimenDictionary = {'Institution': list(SpecimensSplit.iloc[:,InstituteCol]),
                      'Collection' : Collections,
                      'CatalogNumber': list(SpecimensSplit.iloc[:,CatalogCol]),
                      'OccurrenceID': OccurrenceIDs}
    SpecimenDf = pd.DataFrame.from_dict(SpecimenDictionary)
    return SpecimenDf