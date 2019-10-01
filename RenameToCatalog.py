import csv
import os

csv_file = "scan_file.csv"
rename_drive = "E://ms"
with open(csv_file) as myCSV:
    myDict = {}
    readCSV = csv.DictReader(myCSV)
    for rows in readCSV:
        if len(rows["catalog_number"].strip()) == 0 or len(rows["scan_name"].strip()) == 0:
            continue
        else:
            myDict[rows["scan_name"].strip()] = rows["catalog_number"].strip()
    # for i in myDict:
    #     if i != myDict[i]:
    #         print(i,"::",myDict[i])
    os.chdir(rename_drive)
    for i in os.listdir(rename_drive):
        if "CAB" in i:
            renameTo = myDict[i[:10]]+i[10:]
            os.rename(i, renameTo)
            print(i, "->",renameTo)
