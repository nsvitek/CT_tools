from tkinter import *
from tkinter import filedialog
import os
import shutil
import csv

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        baseDriveText = Label(master, text="Search Drive").grid(row=0, column=0)

        self.baseDrivePath = StringVar()
        self.baseDriveLoc = Entry(master, text=self.baseDrivePath, width=50)
        self.baseDriveLoc.grid(row=0, column=1)

        self.baseDriverBrowse = Button(master, text="Browse", command=self.OnBaseBrowse)
        self.baseDriverBrowse.grid(row=0, column=2)

        copyDriveText = Label(master, text="Copy Drive").grid(row=1, column=0)

        self.copyDrivePath = StringVar()
        self.copyDriveLoc = Entry(master, text=self.copyDrivePath, width=50)
        self.copyDriveLoc.grid(row=1, column=1)

        self.copyDriverBrowse = Button(master, text="Browse", command=self.OnCopyBrowse)
        self.copyDriverBrowse.grid(row=1, column=2)

        csvFileText = Label(master, text="CSV File").grid(row=2, column=0)

        self.csvFilePath = StringVar()
        self.csvFileLoc = Entry(master, text=self.csvFilePath, width=50)
        self.csvFileLoc.grid(row=2, column=1)

        self.csvFileBrowse = Button(master, text="Browse", command=self.OnCSVBrowse)
        self.csvFileBrowse.grid(row=2, column=2)

        tripText = Label(master, text="Trip Filter").grid(row=3, column=0)

        self.tripFilter = StringVar()
        self.tripFilterEntry = Entry(master, text=self.tripFilter, width=50)
        self.tripFilterEntry.grid(row=3, column=1)

        self.submit = Button(master, text="Submit and Run", command=self.OnSubmit)
        self.submit.grid(row=4, column=1)

    def OnBaseBrowse(self):
        filename = filedialog.askdirectory(title="Select Search Data Location")
        self.baseDrivePath.set(filename)

    def OnCopyBrowse(self):
        filename = filedialog.askdirectory(title="Copy to Location")
        self.copyDrivePath.set(filename)

    def OnCSVBrowse(self):
        filename = filedialog.askopenfilename(title="Select CSV", filetypes=(("CSV Files", "*.csv"),))
        self.csvFilePath.set(filename)

    def OnSubmit(self):
        base_drive = self.baseDrivePath.get()
        copy_drive = self.copyDrivePath.get()
        csv_data = self.csvFilePath.get()
        trip_folder_filter = self.tripFilter.get()
        print(base_drive,copy_drive, csv_data, trip_folder_filter )
        errorLog=[]
        if not os.path.exists(copy_drive):
            os.mkdir(copy_drive)
        with open(csv_data) as myCSV:
            readCSV = csv.DictReader(myCSV)
            entries = []
            for rows in readCSV:
                if len(rows["trip_folder"]) < 1 or len(rows["scan_folder"]) < 1 or len(rows["scan_name"]) < 1:
                    continue
                else:
                    tempDict = {"trip_folder": rows["trip_folder"], "scan_folder": rows["scan_folder"],
                                "scan_name": rows["scan_name"], "folder": "", "zip_loc": [], "ply_loc": []}
                    entries.append(tempDict)
            for data in entries:
                if trip_folder_filter != data["trip_folder"]:
                    continue
                currentTripFolder = data["trip_folder"]
                currentScanFolder = data["scan_folder"]
                currentScanName = data["scan_name"]
                lastLoc = base_drive
                foundLoc = False
                for i in os.listdir(base_drive):
                    temp_drive = os.path.join(base_drive, i)
                    if currentTripFolder in i and os.path.isdir(temp_drive):
                        foundLoc = True
                        data["folder"] = temp_drive
                        break
                if foundLoc:
                    foundLoc = False
                    for i in os.listdir(data["folder"]):
                        temp_drive = os.path.join(data["folder"], i)
                        if currentScanFolder in i and os.path.isdir(temp_drive):
                            foundLoc = True
                            data["folder"] = temp_drive
                            break
                # adding final folder location to dictionary entry
                if foundLoc:
                    foundLoc = False
                    for i in os.listdir(data["folder"]):
                        temp_drive = os.path.join(data["folder"], i)
                        if currentScanName in i and os.path.isdir(temp_drive) and "raw" not in i:
                            foundLoc = True
                            data["folder"] = temp_drive
                            break
                errorDict = {"trip_folder": data["trip_folder"], "scan_folder": data["scan_folder"],
                             "scan_name": data["scan_name"], "error": []}
                # if scan_name not in folder location means folder location is not found so skip to next
                if currentScanName not in data["folder"]:
                    print("ERROR: No zip files found for", currentScanName)
                    print("ERROR: No ply files found for", currentScanName)
                    errorDict["error"].append("No zip")
                    errorDict["error"].append("No ply")
                    errorLog.append(errorDict)
                    continue
                # looking for zip and ply files in folder location
                zipFiles = []
                for i in os.listdir(data["folder"]):
                    temp_loc = os.path.join(data["folder"], i)
                    # checks to see if it's a .zip file
                    if i.endswith(".zip"):
                        zipFiles.append(temp_loc)
                data["zip_loc"] = zipFiles

                plyFiles = []
                for i in os.listdir(data["folder"]):
                    temp_loc = os.path.join(data["folder"], i)
                    # checks to see if it's a .ply file and its not a fill type of ply file
                    if i.endswith(".ply") and "fill" not in i:
                        plyFiles.append(temp_loc)
                data["ply_loc"] = plyFiles

                # Attemping to zip and ply files into the copy to location
                if len(data["zip_loc"]) == 0:
                    print("ERROR: No zip files found for", currentScanName)
                    errorDict["error"].append("No zip")
                else:
                    # print("Copying zip files for", currentScanName)
                    for i in data["zip_loc"]:
                        shutil.copy(i, copy_drive)
                if len(data["ply_loc"]) == 0:
                    print("ERROR: No ply files found for", currentScanName)
                    errorDict["error"].append("No ply")
                else:
                    # print("Copying ply files for", currentScanName)
                    for i in data["ply_loc"]:
                        shutil.copy(i, copy_drive)
                # checking to see if error occurred
                    if len(errorDict["error"]) > 0:
                        errorLog.append(errorDict)
        if len(errorLog) > 0:
            print("ERRORS Log:")
            for i in errorLog:
                print(i)
        else:
            print("Copying files completed there are no errors.")
if __name__=="__main__":
    root = Tk()
    root.geometry('430x130')
    root.title("Copy ZIP and PLY Tool")
    root.resizable(False, False)
    app = Window(root)
    root.mainloop()

