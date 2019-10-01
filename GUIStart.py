from tkinter import *
from tkinter import filedialog
import os
import shutil
import csv
import GUIConfig as configure

class Window(Frame):
    config = configure.userConfig
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        yPos=5
        self.INPUT_PATH_TEXT = Label(master, text="INPUT PATH:", anchor='w').place(x=0, y=yPos)
        self.INPUT_PATH = StringVar(master, value='E:/ms')
        self.INPUT_PATH_LOC = Entry(master, text=self.INPUT_PATH, width=50)
        self.INPUT_PATH_LOC.place(x=135, y=yPos)
        self.INPUT_PATH_BROWSE = Button(master, text="Browse", command=self.OnInputPathBrowse)
        self.INPUT_PATH_BROWSE.place(x=400, y=yPos)
        yPos+=35
        self.UPLOAD_FOLDER_TEXT = Label(master, text="UPLOAD FOLDER:", anchor='w').place(x=0, y=yPos)
        self.UPLOAD_FOLDER = StringVar(master, value='FILES')
        self.UPLOAD_FOLDER_LOC = Entry(master, text=self.UPLOAD_FOLDER, width=50)
        self.UPLOAD_FOLDER_LOC.place(x=135, y=yPos)
        self.UPLOAD_FOLDER_BROWSE = Button(master, text="Browse", command=self.OnUploadFolderBrowse)
        self.UPLOAD_FOLDER_BROWSE.place(x=400, y=yPos)
        yPos += 35
        self.CT_METADATA_FOLDER_TEXT = Label(master, text="CT METADATA FOLDER:", anchor='w').place(x=0, y=yPos)
        self.CT_METADATA_FOLDER = StringVar(master, value='')
        self.CT_METADATA_FOLDER_LOC = Entry(master, text=self.CT_METADATA_FOLDER, width=50)
        self.CT_METADATA_FOLDER_LOC.bind('<Leave>', self.CheckCTMetadataFolder)
        self.CT_METADATA_FOLDER_LOC.place(x=135, y=yPos)
        self.CT_METADATA_FOLDER_BROWSE = Button(master, text="Browse", command=self.OnCTMetadataFolderBrowse)
        self.CT_METADATA_FOLDER_BROWSE.place(x=400, y=yPos)

        yPos += 35
        self.CT_METADATA_FILE_TEXT = Label(master, text="CT METADATA FILE:", anchor='w').place(x=0, y=yPos)
        self.CT_METADATA_FILE = StringVar(master, value='CT_database_scans.xlsx')
        self.CT_METADATA_FILE_LOC = Entry(master, text=self.CT_METADATA_FILE, width=50)
        self.CT_METADATA_FILE_LOC.bind('<Leave>', self.CheckCTMetadataFile)
        self.CT_METADATA_FILE_LOC.place(x=135, y=yPos)
        self.CT_METADATA_FILE_BROWSE = Button(master, text="Browse", command=self.OnCTMetadataFileBrowse)
        self.CT_METADATA_FILE_BROWSE.place(x=400, y=yPos)
        yPos += 35
        self.OTHER_METADATA_FILE_TEXT = Label(master, text="OTHER METADATA FILE:", anchor='w').place(x=0, y=yPos)
        self.OTHER_METADATA_FILE = StringVar(master, value="scan_file.csv")
        self.OTHER_METADATA_FILE_LOC = Entry(master, text=self.OTHER_METADATA_FILE, width=50)
        self.OTHER_METADATA_FILE_LOC.place(x=135, y=yPos)
        self.OTHER_METADATA_FILE_BROWSE = Button(master, text="Browse", command=self.OnOtherMetadataFileBrowse)
        self.OTHER_METADATA_FILE_BROWSE.place(x=400, y=yPos)
        yPos += 35
        self.OUTPUT_FILE_TEXT = Label(master, text="OUTPUT FILE:", anchor='w').place(x=0, y=yPos)
        self.OUTPUT_FILE = StringVar(master, value='ToUpload_2019-09-25')
        self.OUTPUT_FILE_LOC = Entry(master, text=self.OUTPUT_FILE, width=50)
        self.OUTPUT_FILE_LOC.place(x=135, y=yPos)
        self.OUTPUT_FILE_BROWSE = Button(master, text="Browse", command=self.OnOutputFileBrowse)
        self.OUTPUT_FILE_BROWSE.place(x=400, y=yPos)
        yPos += 35
        # Determine oVert now, as will set downstream choices.
        # oVert: Is this upload part of the oVert TCN grant?
        self.OVERT_TEXT = Label(master, text='OVERT:', anchor='w').place(x=0, y=yPos)
        self.OVERT = BooleanVar(master, value=False)
        self.OVERT_CHECK = Checkbutton(master, text="TRUE", variable=self.OVERT)
        self.OVERT_CHECK.place(x=50, y=yPos-2)
        # Batch: Are there batch scans in the upload?
        self.BATCH_TEXT = Label(master, text='BATCH:', anchor='w').place(x=150, y=yPos)
        self.BATCH = BooleanVar(master, value=True)
        self.BATCH_CHECK = Checkbutton(master, text="TRUE", variable=self.BATCH)
        self.BATCH_CHECK.place(x=200, y=yPos-2)
        # Query iDigBio: Do you want to search the iDigBio database to fill in Collection and Occurrence ID?
        self.QUERY_IDIGBIO_TEXT = Label(master, text='QUERY IDIGBIO:', anchor='w').place(x=300, y=yPos)
        self.QUERY_IDIGBIO = BooleanVar(master, value=True)
        self.QUERY_IDIGBIO_CHECK = Checkbutton(master, text="TRUE", variable=self.QUERY_IDIGBIO)
        self.QUERY_IDIGBIO_CHECK.place(x=400, y=yPos-2)

        yPos += 35
        # Set how a name will be broken into pieces. Default is space, dash, or underscore
        # Note that dash and underscore both need a backslash in front of them (ex: '\_')
        self.DELIMITER_TEXT = Label(master, text="DELIMITER:", anchor='w').place(x=0, y=yPos)
        self.DELIMITER = StringVar(master, value='[\-]')
        self.DELIMITER_INPUT = Entry(master, text=self.DELIMITER, width=10)
        self.DELIMITER_INPUT.place(x=135, y=yPos)
        yPos += 35
        # After a name is broken up by the delimiter, set which segment corresponds to which part.
        # The count begins at 0, so indicate the first segment with 0, the second segment with 1, etc.
        self.SEGMENT_MUSEUM_TEXT = Label(master, text='SEGMENT MUSEUM:').place(x=0, y=yPos)
        self.SEGMENT_MUSEUM = IntVar(master, value=0)
        self.SEGMENT_MUSEUM_INPUT = Entry(master, text=self.SEGMENT_MUSEUM, width=5)
        self.SEGMENT_MUSEUM_INPUT.place(x=135, y=yPos)

        self.SEGMENT_COLLECTION_TEXT = Label(master, text='SEGMENT COLLECTION:').place(x=270, y=yPos)
        self.SEGMENT_COLLECTION = IntVar(master, value=-1)
        self.SEGMENT_COLLECTION_INPUT = Entry(master, text=self.SEGMENT_COLLECTION, width=5)
        self.SEGMENT_COLLECTION_INPUT.place(x=410, y=yPos)
        yPos += 35
        self.SEGMENT_NUMBER_TEXT = Label(master, text='SEGMENT NUMBER:').place(x=0, y=yPos)
        self.SEGMENT_NUMBER = IntVar(master, value=1)
        self.SEGMENT_NUMBER_INPUT = Entry(master, text=self.SEGMENT_NUMBER, width=5)
        self.SEGMENT_NUMBER_INPUT.place(x=135, y=yPos)

        self.SEGMENT_BODYPART_TEXT = Label(master, text='SEGMENT BODYPART:').place(x=270, y=yPos)
        self.SEGMENT_BODYPART = IntVar(master, value=-1)
        self.SEGMENT_BODYPART_INPUT = Entry(master, text=self.SEGMENT_BODYPART, width=5)
        self.SEGMENT_BODYPART_INPUT.place(x=410, y=yPos)

        yPos += 35
        self.GRANT_SCANNING_INSTITUTION_TEXT = Label(master, text='GRANT SCANNING INSTITUTION:').place(x=0, y=yPos)
        self.GRANT_SCANNING_INSTITUTION_OPTIONS = ["#0: University of Washington",
            "#1: Field Museum of Natural History","#2: Harvard University", "#3: University of California-Berkeley",
            "#4: Louisiana State University & Agricultural \nand Mechanical College",
            "#5: University of Florida", "#6: University of Texas at Austin",
            "#7: University of Kansas Center \nfor Research Inc", "#8: California Academy of Sciences",
            "#9: Cornell University", "#10: University of Michigan Ann Arbor", "#11: Texas A&M AgriLife Research",
            "#12: College of William & Mary Virginia \nInstitute of Marine Science",
            "#13: Academy of Natural Sciences \nPhiladelphia", "#14: Yale University",
            "#15: University of California-San Diego \nScripps Inst of Oceanography",
            "NONE"]
        self.GRANT_SCANNING_INSTITUTION = StringVar(master, self.GRANT_SCANNING_INSTITUTION_OPTIONS[5])
        self.GRANT_SCANNING_INSTITUTION_MENU = OptionMenu(master, self.GRANT_SCANNING_INSTITUTION,
                                                          *self.GRANT_SCANNING_INSTITUTION_OPTIONS)
        self.GRANT_SCANNING_INSTITUTION_MENU.place(x=191, y=yPos-5)
        self.GRANT_SCANNING_INSTITUTION_MENU.config(height=1, width=38)

        yPos += 35
        self.GRANT_SPECIMEN_PROVIDER_TEXT = Label(master, text='GRANT SPECIMEN PROVIDER:').place(x=0, y=yPos)
        self.GRANT_SPECIMEN_PROVIDER = StringVar(master, value='None')
        self.GRANT_SPECIMEN_PROVIDER_INPUT = Entry(master, text=self.GRANT_SPECIMEN_PROVIDER, width=45)
        self.GRANT_SPECIMEN_PROVIDER_INPUT.place(x=175, y=yPos)

        yPos += 35
        # Name of the copyright holder. Also used as the entity granting permission.
        self.PROVIDER_TEXT = Label(master, text='PROVIDER:').place(x=0, y=yPos)
        self.PROVIDER = StringVar(master, value="Florida Museum of Natural History")
        self.PROVIDER_INPUT = Entry(master, text=self.PROVIDER, width=45)
        self.PROVIDER_INPUT.place(x=175, y=yPos)

        yPos += 35
        self.COPY_PERMISSION_TEXT = Label(master, text='COPY PERMISSION:').place(x=0, y=yPos)
        self.COPY_PERMISSION_OPTIONS = ["#0: Copyright permission not set",
            "#1: Person loading media owns copyright and \ngrants permission for use of media on MorphoSource",
            "#2: Permission to use media on MorphoSource \ngranted by copyright holder",
            "#3: Permission pending", "#4: Copyright expired or work otherwise in public domain",
            "#5: Copyright permission not yet requested",
            "NONE"]
        self.COPY_PERMISSION = StringVar(master, value=self.COPY_PERMISSION_OPTIONS[2])
        self.COPY_PERMISSION_MENU = OptionMenu(master, self.COPY_PERMISSION, *self.COPY_PERMISSION_OPTIONS)
        self.COPY_PERMISSION_MENU.place(x=120, y=yPos-5)
        self.COPY_PERMISSION_MENU.config(height=1, width=50)

        yPos += 35
        # Media Policy Options: oVert prefers 5, but check with your institution
        self.MEDIA_POLICY_TEXT = Label(master, text='MEDIA POLICY:').place(x=0, y=yPos)

        self.MEDIA_POLICY_OPTIONS = ["#0: Media reuse policy not set", "#1: CC0 - relinquish copyright",
            "#2: Attribution CC BY - reuse with attribution",
            "#3: Attribution-NonCommercial CC BY-NC - \nreuse but noncommercial",
            "#4: Attribution-ShareAlike CC BY-SA - \nreuse here and applied to future uses",
            "#5: Attribution- CC BY-NC-SA - reuse here and \napplied to future uses but noncommercial",
            "#6: Attribution-NoDerivs CC BY-ND - \nreuse but no changes",
            "#7: Attribution-NonCommercial-NoDerivs CC BY-NC-ND - \nreuse noncommerical no changes",
            "#8: Media released for onetime use, \nno reuse without permission",
            "#9: Unknown - Will set before project publication"]
        self.MEDIA_POLICY = StringVar(master, value=self.MEDIA_POLICY_OPTIONS[5])
        self.MEDIA_POLICY_MENU = OptionMenu(master, self.MEDIA_POLICY, *self.MEDIA_POLICY_OPTIONS)
        self.MEDIA_POLICY_MENU.place(x=120, y=yPos-5)
        self.MEDIA_POLICY_MENU.config(height=1, width=50)

        yPos += 35
        # Publication status: oVert prefers 2, but check with your institution
        self.DOWNLOAD_POLICY_TEXT = Label(master, text='MEDIA POLICY:').place(x=0, y=yPos)
        self.DOWNLOAD_POLICY_OPTIONS = ["#0: unpublished", "#1: published, with unrestricted download",
            "#2: published, with request to download necessary"]
        self.DOWNLOAD_POLICY = StringVar(master, value=self.DOWNLOAD_POLICY_OPTIONS[0])
        self.DOWNLOAD_POLICY_MENU = OptionMenu(master, self.DOWNLOAD_POLICY, *self.DOWNLOAD_POLICY_OPTIONS)
        self.DOWNLOAD_POLICY_MENU.place(x=120, y=yPos - 5)
        self.DOWNLOAD_POLICY_MENU.config(width=50)

        yPos += 35
        # Write the name of the scanning technician in quotes
        self.TECHNICIAN_TEXT = Label(master, text='TECHNICIAN:').place(x=0, y=yPos)
        self.TECHNICIAN = StringVar(master, value='Natasha Vitek, Jason Chen')
        self.TECHNICIAN_INPUT = Entry(master, text=self.TECHNICIAN, width=45)
        self.TECHNICIAN_INPUT.place(x=120, y=yPos)

        yPos += 35
        # Write what wedge was use in scanning, if any, in quotes.
        self.WEDGE_TEXT = Label(master, text='WEDGE:').place(x=0, y=yPos)
        self.WEDGE = StringVar(master, value="air")
        self.WEDGE_INPUT = Entry(master, text=self.WEDGE, width=45)
        self.WEDGE_INPUT.place(x=120, y=yPos)

        yPos += 35
        # If you include shading, flux, or geometric calibrations, respectively, change to True.
        self.CALIBRATION_SHADE_TEXT = Label(master, text='CALIBRATION\nSHADE:', anchor='w').place(x=0, y=yPos)
        self.CALIBRATION_SHADE = BooleanVar(master, value=True)
        self.CALIBRATION_SHADE_CHECK = Checkbutton(master, text="TRUE", variable=self.CALIBRATION_SHADE)
        self.CALIBRATION_SHADE_CHECK.place(x=85, y=yPos+2)

        self.CALIBRATION_FLUX_TEXT = Label(master, text='CALIBRATION\nFLUX:', anchor='w').place(x=150, y=yPos)
        self.CALIBRATION_FLUX = BooleanVar(master, value=False)
        self.CALIBRATION_FLUX_CHECK = Checkbutton(master, text="TRUE", variable=self.CALIBRATION_FLUX)
        self.CALIBRATION_FLUX_CHECK.place(x=230, y=yPos+2)

        self.CALIBRATION_GEOMETRIC_TEXT = Label(master, text='CALIBRATION\nGEOMETRIC:', anchor='w')\
            .place(x=300, y=yPos)
        self.CALIBRATION_GEOMETRIC = BooleanVar(master, value=False)
        self.CALIBRATION_GEOMETRIC_CHECK = Checkbutton(master, text="TRUE", variable=self.CALIBRATION_GEOMETRIC)
        self.CALIBRATION_GEOMETRIC_CHECK.place(x=400, y=yPos+2)

        yPos += 35
        # Write any description of scanner calibrations, if wanted, in quotes.
        self.CALIBRATION_DESCRIPTION_TEXT = Label(master, text='CALIBRATION\nDESCRIPTION:').place(x=0, y=yPos)
        self.CALIBRATION_DESCRIPTION = StringVar(master, value='None')
        self.CALIBRATION_DESCRIPTION_INPUT = Entry(master, text=self.CALIBRATION_DESCRIPTION, width=45)
        self.CALIBRATION_DESCRIPTION_INPUT.place(x=120, y=yPos+10)

        xPos = 500
        yPos = 5
        # If CT_METADATA_SPREADSHEET = True, then you need to map the column names below.
        # Refer to ctscan_sample1.csv for an example of how each default maps
        # name of the scan. Might equal a specimen name or batch designation
        self.NAME_SCAN_TEXT = Label(master, text='NAME SCAN:').place(x=xPos, y=yPos)
        self.NAME_SCAN = StringVar(master, value='scan_trip')
        self.NAME_SCAN_INPUT = Entry(master, text=self.NAME_SCAN, width=20)
        self.NAME_SCAN_INPUT.place(x=xPos+120, y=yPos)

        yPos+=35
        # voxel size X
        self.NAME_VOXELX_TEXT = Label(master, text='NAME VOXELX:').place(x=xPos, y=yPos)
        self.NAME_VOXELX = StringVar(master, value='X_voxel_size_mm')
        self.NAME_VOXELX_INPUT = Entry(master, text=self.NAME_VOXELX, width=20)
        self.NAME_VOXELX_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # voxel size Y
        self.NAME_VOXELY_TEXT = Label(master, text='NAME VOXELY:').place(x=xPos, y=yPos)
        self.NAME_VOXELY = StringVar(master, value='Y_voxel_size_mm')
        self.NAME_VOXELY_INPUT = Entry(master, text=self.NAME_VOXELY, width=20)
        self.NAME_VOXELY_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # voxel size Z
        self.NAME_VOXELZ_TEXT = Label(master, text='NAME VOXELZ:').place(x=xPos, y=yPos)
        self.NAME_VOXELZ = StringVar(master, value='Z_voxel_size_mm')
        self.NAME_VOXELZ_INPUT = Entry(master, text=self.NAME_VOXELZ, width=20)
        self.NAME_VOXELZ_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        #voltage
        self.NAME_VOLTAGE_TEXT = Label(master, text='NAME VOLTAGE:').place(x=xPos, y=yPos)
        self.NAME_VOLTAGE = StringVar(master, value='voltage_kv')
        self.NAME_VOLTAGE_INPUT = Entry(master, text=self.NAME_VOLTAGE, width=20)
        self.NAME_VOLTAGE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # amperage
        self.NAME_AMPERAGE_TEXT = Label(master, text='NAME AMPERAGE:').place(x=xPos, y=yPos)
        self.NAME_AMPERAGE = StringVar(master, value='amperage_ua')
        self.NAME_AMPERAGE_INPUT = Entry(master, text=self.NAME_AMPERAGE, width=20)
        self.NAME_AMPERAGE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # watts
        self.NAME_WATTS_TEXT = Label(master, text='NAME WATTS:').place(x=xPos, y=yPos)
        self.NAME_WATTS = StringVar(master, value='watts')
        self.NAME_WATTS_INPUT = Entry(master, text=self.NAME_WATTS, width=20)
        self.NAME_WATTS_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # exposure time
        self.NAME_EXPOSURE_TEXT = Label(master, text='NAME EXPOSURE:').place(x=xPos, y=yPos)
        self.NAME_EXPOSURE = StringVar(master, value='exposure_time')
        self.NAME_EXPOSURE_INPUT = Entry(master, text=self.NAME_EXPOSURE, width=20)
        self.NAME_EXPOSURE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # number of projections
        self.NAME_PROJECTIONS_TEXT = Label(master, text='NAME PROJECTIONS:').place(x=xPos, y=yPos)
        self.NAME_PROJECTIONS = StringVar(master, value='projections')
        self.NAME_PROJECTIONS_INPUT = Entry(master, text=self.NAME_PROJECTIONS, width=20)
        self.NAME_PROJECTIONS_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # frame averaging
        self.NAME_FRAME_TEXT = Label(master, text='NAME FRAME:').place(x=xPos, y=yPos)
        self.NAME_FRAME = StringVar(master, value='frame_averaging')
        self.NAME_FRAME_INPUT = Entry(master, text=self.NAME_FRAME, width=20)
        self.NAME_FRAME_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # filter
        self.NAME_FILTER_TEXT = Label(master, text='NAME FILTER:').place(x=xPos, y=yPos)
        self.NAME_FILTER = StringVar(master, value='filter')
        self.NAME_FILTER_INPUT = Entry(master, text=self.NAME_FILTER, width=20)
        self.NAME_FILTER_INPUT.place(x=xPos + 120, y=yPos)
        ###For each in filter: if 'Unknown', set to None
        # %% Spreadsheet mapping #######################################################
        # This section is one you will need if OTHER_METADATA_FILE = True and you want to map
        # variables that were not included in the CT metadata section.
        # Refer to input_sample1.csv for an example of how each default maps.
        yPos += 35
        self.NAME_SPECIMENS_TEXT = Label(master, text='NAME SPECIMENS:').place(x=xPos, y=yPos)
        self.NAME_SPECIMENS = StringVar(master, 'catalog_number')
        self.NAME_SPECIMENS_INPUT = Entry(master, text=self.NAME_SPECIMENS, width=20)
        self.NAME_SPECIMENS_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        self.NAME_GENUS_TEXT = Label(master, text='NAME GENUS:').place(x=xPos, y=yPos)
        self.NAME_GENUS = StringVar(master, value='None')
        self.NAME_GENUS_INPUT = Entry(master, text=self.NAME_GENUS, width=20)
        self.NAME_GENUS_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        self.NAME_SPECIES_TEXT = Label(master, text='NAME SPECIES:').place(x=xPos, y=yPos)
        self.NAME_SPECIES = StringVar(master, value='None')
        self.NAME_SPECIES_INPUT = Entry(master, text=self.NAME_SPECIES, width=20)
        self.NAME_SPECIES_INPUT.place(x=xPos + 120, y=yPos)

        # if you batch scanned, then you must have a spreadsheet in INPUT_DF.
        # Why? Because you need a key to match specimens to the batches they are a part of
        # Make sure you mapped NAME_SPECIMENS above, too.
        yPos += 35
        self.NAME_BATCH_TEXT = Label(master, text='NAME BATCH:').place(x=xPos, y=yPos)
        self.NAME_BATCH = StringVar(master, 'scan_metadata')
        self.NAME_BATCH_INPUT = Entry(master, text=self.NAME_BATCH, width=20)
        self.NAME_BATCH_INPUT.place(x=xPos + 120, y=yPos)
        # %% If not oVert, you need to set these variables, too ########################
        yPos += 35
        # Enter any grant funding as a string in quotes
        self.FUNDING_SOURCE_TEXT = Label(master, text='FUNDING SOURCE:').place(x=xPos, y=yPos)
        self.FUNDING_SOURCE = StringVar(master, value='NSF DGE 1315138 (NSV)')
        self.FUNDING_SOURCE_INPUT = Entry(master, text=self.FUNDING_SOURCE, width=20)
        self.FUNDING_SOURCE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        #this is the column name containing element information
        self.NAME_ELEMENT_TEXT = Label(master, text='NAME ELEMENT:').place(x=xPos, y=yPos)
        self.NAME_ELEMENT = StringVar(master, value="element")
        self.NAME_ELEMENT_INPUT = Entry(master, text=self.NAME_ELEMENT, width=20)
        self.NAME_ELEMENT_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # Note: when populating this column, text options are:
        # Not Applicable [use for 'whole body'], Unknown, Left, Right, Midline
        self.NAME_SIDE_TEXT = Label(master, text='NAME SIDE:').place(x=xPos, y=yPos)
        self.NAME_SIDE = StringVar(master, value='None')
        self.NAME_SIDE_INPUT = Entry(master, text=self.NAME_SIDE, width=20)
        self.NAME_SIDE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # The column name containing the file names to be uploaded.
        self.NAME_FILE_TEXT = Label(master, text='NAME FILE:').place(x=xPos, y=yPos)
        self.NAME_FILE = StringVar(master, value="None")
        self.NAME_FILE_INPUT = Entry(master, text=self.NAME_FILE, width=20)
        self.NAME_FILE_INPUT.place(x=xPos + 120, y=yPos)

        yPos += 35
        # Mesh settings: Do your meshes have suffixes? (ex: 'UF-M-12345_mesh.stl' or 'UF_M_12345_cropped.stl')?
        self.MESH_SUFFIX_TEXT = Label(master, text='MESH\nSUFFIX:', anchor='w').place(x=xPos, y=yPos)
        self.MESH_SUFFIX = BooleanVar(master, value=False)
        self.MESH_SUFFIX_CHECK = Checkbutton(master, text="TRUE", variable=self.MESH_SUFFIX)
        self.MESH_SUFFIX_CHECK.place(x=xPos + 50, y=yPos + 5)

        self.help = Button(master, text="HELP", command=self.OnHelp)
        self.help.place(x=620, y=675)

        self.submit = Button(master, text="SUBMIT", command=self.OnSubmit, height = 2, width = 10)
        self.submit.place(x=670, y=665)


    def CheckCTMetadataFolder(self, event):
        if len(self.CT_METADATA_FOLDER.get())==0:
            self.CT_METADATA_FILE_LOC.config(state='normal')
            self.CT_METADATA_FILE_BROWSE.config(state='normal')
        else:
            self.CT_METADATA_FILE_LOC.config(state='disable')
            self.CT_METADATA_FILE_BROWSE.config(state='disable')
            self.CT_METADATA_FILE.set('')
    def CheckCTMetadataFile(self, event):
        if len(self.CT_METADATA_FILE.get())==0:
            self.CT_METADATA_FOLDER_LOC.config(state='normal')
            self.CT_METADATA_FOLDER_BROWSE.config(state='normal')
        else:
            self.CT_METADATA_FOLDER_LOC.config(state='disable')
            self.CT_METADATA_FOLDER_BROWSE.config(state='disable')
            self.CT_METADATA_FOLDER.set('')
    def OnInputPathBrowse(self):
        # path to folder where all your inputs are stored
        filename = filedialog.askdirectory(title="Select Input Path:")
        self.INPUT_PATH.set(filename)

    def OnUploadFolderBrowse(self):
        # The name of the folder containing files to batch upload.
        filename = filedialog.askdirectory(title="Select Upload Folder:")
        self.UPLOAD_FOLDER.set(filename)

    def OnCTMetadataFolderBrowse(self):
        # The rest of your metadata should come from either a series of CT metadata files or a spreadsheet.
        # The name of the folder containing CT metadata files.
        filename = filedialog.askdirectory(title="Select CT Metadata Folder:")
        self.CT_METADATA_FOLDER.set(filename)

    def OnCTMetadataFileBrowse(self):
        # If CT scan metadata is already in a spreadsheet, enter file name.
        # Don't forget to set CT_METADATA_FOLDER = None in this case.
        filename = filedialog.askopenfilename(title="Select CT Metadata File", filetypes=(("Excel Files", "*.xlsx"),))
        self.CT_METADATA_FILE.set(filename)

    def OnOtherMetadataFileBrowse(self):
        # #If have additional metadata in a separate spreadsheet (.csv or .xlsx), put that file name here
        filename = filedialog.askopenfilename(title="Select Other Metadata File:",)
        self.OTHER_METADATA_FILE.set(filename)
        # Spreadsheet file options:
        # If you have a single spreadsheet with both CT metadata and other data,
        # then use only CT_METADATA_FILE and set OTHER_METADATA_FILE to None.

    def OnOutputFileBrowse(self):
        # Name of final output spreadsheet file, assuming same location as input
        # Note: no file ending. Will write to .xlsx
        filename = filedialog.askopenfilename(title="Select Output File:", filetypes=(("Excel Files", "*.xlsx"),))
        self.OUTPUT_FILE.set(filename)

    def OnSubmit(self):
        if "NONE" in self.INPUT_PATH.get().upper() or len(self.INPUT_PATH.get())==0:
            INPUT_PATH = None
        else:
            INPUT_PATH = self.INPUT_PATH.get()
        if "NONE" in self.UPLOAD_FOLDER.get().upper() or len(self.UPLOAD_FOLDER.get())==0:
            UPLOAD_FOLDER = None
        else:
            UPLOAD_FOLDER = self.UPLOAD_FOLDER.get()
        if "NONE" in self.CT_METADATA_FOLDER.get().upper() or len(self.CT_METADATA_FOLDER.get())==0:
            CT_METADATA_FOLDER = None
        else:
            CT_METADATA_FOLDER = self.CT_METADATA_FOLDER.get()
        if 'NONE' in self.CT_METADATA_FILE.get().upper() or len(self.CT_METADATA_FILE.get())==0:
            CT_METADATA_FILE = None
        else:
            CT_METADATA_FILE = self.CT_METADATA_FILE.get()
        if 'NONE' in self.OTHER_METADATA_FILE.get().upper() or len(self.OTHER_METADATA_FILE.get())==0:
            OTHER_METADATA_FILE = None
        else:
            OTHER_METADATA_FILE = self.OTHER_METADATA_FILE.get()
        if 'NONE' in self.OUTPUT_FILE.get().upper() or len(self.OUTPUT_FILE.get())==0:
            OUTPUT_FILE = None
        else:
            OUTPUT_FILE = self.OUTPUT_FILE.get()

        OVERT = self.OVERT.get()
        BATCH = self.BATCH.get()
        QUERY_IDIGBIO = self.QUERY_IDIGBIO.get()

        if 'NONE' in self.DELIMITER.get().upper() or len(self.DELIMITER.get())==0:
            DELIMITER=None
        else:
            DELIMITER = self.DELIMITER.get()
        if self.SEGMENT_MUSEUM.get()<0:
            SEGMENT_MUSEUM = None
        else:
            SEGMENT_MUSEUM = self.SEGMENT_MUSEUM.get()
        if self.SEGMENT_COLLECTION.get()<0:
            SEGMENT_COLLECTION = None
        else:
            SEGMENT_COLLECTION = self.SEGMENT_COLLECTION.get()
        if self.SEGMENT_NUMBER.get()<0:
            SEGMENT_NUMBER = None
        else:
            SEGMENT_NUMBER = self.SEGMENT_NUMBER.get()
        if self.SEGMENT_BODYPART.get() < 0:
            SEGMENT_BODYPART=None
        else:
            SEGMENT_BODYPART = self.SEGMENT_BODYPART.get()

        GRANT_SCANNING_INSTITUTION = self.GRANT_SCANNING_INSTITUTION_OPTIONS.index(self.GRANT_SCANNING_INSTITUTION.get())
        if GRANT_SCANNING_INSTITUTION == len(self.GRANT_SCANNING_INSTITUTION_OPTIONS)-1:
            GRANT_SCANNING_INSTITUTION=None

        if "NONE" in self.GRANT_SPECIMEN_PROVIDER.get().upper() or len(self.GRANT_SPECIMEN_PROVIDER.get())==0:
            GRANT_SPECIMEN_PROVIDER = None
        else:
            GRANT_SPECIMEN_PROVIDER = self.GRANT_SPECIMEN_PROVIDER.get()
        if 'NONE' in self.PROVIDER.get().upper() or len(self.PROVIDER.get())==0:
            PROVIDER = None
        else:
            PROVIDER = self.PROVIDER.get()

        COPY_PERMISSION = self.COPY_PERMISSION_OPTIONS.index(self.COPY_PERMISSION.get())
        if COPY_PERMISSION == len(self.COPY_PERMISSION_OPTIONS)-1:
            COPY_PERMISSION = None

        MEDIA_POLICY = self.MEDIA_POLICY_OPTIONS.index(self.MEDIA_POLICY.get())
        DOWNLOAD_POLICY = self.DOWNLOAD_POLICY_OPTIONS.index(self.DOWNLOAD_POLICY.get())

        if "NONE" in self.TECHNICIAN.get().upper() or len(self.TECHNICIAN.get())==0:
            TECHNICIAN=None
        else:
            TECHNICIAN=self.TECHNICIAN.get()
        if "NONE" in self.WEDGE.get().upper() or len(self.WEDGE.get())==0:
            WEDGE=None
        else:
            WEDGE=self.WEDGE.get()

        CALIBRATION_SHADE = self.CALIBRATION_SHADE.get()
        CALIBRATION_FLUX = self.CALIBRATION_FLUX.get()
        CALIBRATION_GEOMETRIC = self.CALIBRATION_GEOMETRIC.get()

        if "NONE" in self.CALIBRATION_DESCRIPTION.get().upper() or len(self.CALIBRATION_DESCRIPTION.get())==0:
            CALIBRATION_DESCRIPTION = None
        else:
            CALIBRATION_DESCRIPTION = self.CALIBRATION_DESCRIPTION.get()
        if "NONE" in self.NAME_SCAN.get().upper() or len(self.NAME_SCAN.get())==0:
            NAME_SCAN = None
        else:
            NAME_SCAN = self.NAME_SCAN.get()
        if 'NONE' in self.NAME_VOXELX.get().upper() or len(self.NAME_VOXELX.get())==0:
            NAME_VOXELX = None
        else:
            NAME_VOXELX = self.NAME_VOXELX.get()
        if "NONE" in self.NAME_VOXELY.get().upper() or len(self.NAME_VOXELY.get())==0:
            NAME_VOXELY = None
        else:
            NAME_VOXELY = self.NAME_VOXELY.get()
        if "NONE" in self.NAME_VOXELZ.get().upper() or len(self.NAME_VOXELZ.get())==0:
            NAME_VOXELZ = None
        else:
            NAME_VOXELZ = self.NAME_VOXELZ.get()
        if "NONE" in self.NAME_VOLTAGE.get().upper() or len(self.NAME_VOLTAGE.get())==0:
            NAME_VOLTAGE = None
        else:
            NAME_VOLTAGE = self.NAME_VOLTAGE.get()
        if "NONE" in self.NAME_AMPERAGE.get().upper() or len(self.NAME_AMPERAGE.get())==0:
            NAME_AMPERAGE = None
        else:
            NAME_AMPERAGE = self.NAME_AMPERAGE.get()
        if "NONE" in self.NAME_WATTS.get().upper() or len(self.NAME_WATTS.get())==0:
            NAME_WATTS = None
        else:
            NAME_WATTS = self.NAME_WATTS.get()
        if "NONE" in self.NAME_EXPOSURE.get().upper() or len(self.NAME_EXPOSURE.get())==0:
            NAME_EXPOSURE = None
        else:
            NAME_EXPOSURE = self.NAME_EXPOSURE.get()
        if "NONE" in self.NAME_PROJECTIONS.get().upper() or len(self.NAME_PROJECTIONS.get())==0:
            NAME_PROJECTIONS = None
        else:
            NAME_PROJECTIONS = self.NAME_PROJECTIONS.get()
        if "NONE" in self.NAME_FRAME.get().upper() or len(self.NAME_FRAME.get())==0:
            NAME_FRAME = None
        else:
            NAME_FRAME = self.NAME_FRAME.get()
        if "NONE" in self.NAME_FILTER.get().upper() or len(self.NAME_FILTER.get())==0:
            NAME_FILTER=None
        else:
            NAME_FILTER=self.NAME_FILTER.get()
        if "NONE" in self.NAME_SPECIMENS.get().upper() or len(self.NAME_SPECIMENS.get())==0:
            NAME_SPECIMENS = None
        else:
            NAME_SPECIMENS = self.NAME_SPECIMENS.get()
        if "NONE" in self.NAME_GENUS.get().upper() or len(self.NAME_GENUS.get())==0:
            NAME_GENUS = None
        else:
            NAME_GENUS = self.NAME_GENUS.get()
        if "NONE" in self.NAME_SPECIES.get().upper() or len(self.NAME_SPECIES.get())==0:
            NAME_SPECIES = None
        else:
            NAME_SPECIES = self.NAME_SPECIES.get()
        if "NONE" in self.NAME_BATCH.get().upper() or len(self.NAME_BATCH.get())==0:
            NAME_BATCH = None
        else:
            NAME_BATCH = self.NAME_BATCH.get()
        if "NONE" in self.FUNDING_SOURCE.get().upper() or len(self.FUNDING_SOURCE.get())==0:
            FUNDING_SOURCE = None
        else:
            FUNDING_SOURCE = self.FUNDING_SOURCE.get()
        if "NONE" in self.NAME_ELEMENT.get().upper() or len(self.NAME_ELEMENT.get())==0:
            NAME_ELEMENT = None
        else:
            NAME_ELEMENT = self.NAME_ELEMENT.get()
        if "NONE" in self.NAME_SIDE.get().upper() or len(self.NAME_SIDE.get())==0:
            NAME_SIDE = None
        else:
            NAME_SIDE = self.NAME_SIDE.get()
        if "NONE" in self.NAME_FILE.get().upper() or len(self.NAME_FILE.get())==0:
            NAME_FILE = None
        else:
            NAME_FILE = self.NAME_FILE.get()
        MESH_SUFFIX = self.MESH_SUFFIX.get()

        test=Window.config
        test.update(INPUT_PATH, UPLOAD_FOLDER, CT_METADATA_FOLDER, CT_METADATA_FILE, OTHER_METADATA_FILE, OUTPUT_FILE,
                  OVERT, BATCH, QUERY_IDIGBIO, DELIMITER, SEGMENT_MUSEUM, SEGMENT_COLLECTION, SEGMENT_NUMBER,
                  SEGMENT_BODYPART, GRANT_SCANNING_INSTITUTION, GRANT_SPECIMEN_PROVIDER, PROVIDER, COPY_PERMISSION,
                  MEDIA_POLICY, DOWNLOAD_POLICY, TECHNICIAN, WEDGE, CALIBRATION_SHADE, CALIBRATION_FLUX,
                  CALIBRATION_GEOMETRIC, CALIBRATION_DESCRIPTION, NAME_SCAN, NAME_VOXELX, NAME_VOXELY, NAME_VOXELZ,
                  NAME_VOLTAGE, NAME_AMPERAGE, NAME_WATTS, NAME_EXPOSURE, NAME_PROJECTIONS, NAME_FRAME, NAME_FILTER,
                  NAME_SPECIMENS, NAME_GENUS, NAME_SPECIES, NAME_BATCH, FUNDING_SOURCE, NAME_ELEMENT, NAME_SIDE,
                  NAME_FILE, MESH_SUFFIX)
        import GUIMain as run
        run

    def OnHelp(self):
        def on_configure(event):
            # update scrollregion after starting 'mainloop'
            # when all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))

        root = Tk()
        root.attributes("-fullscreen", True)
        # --- create canvas with scrollbar ---
        canvas = Canvas(root, width=1000, height=1000)
        canvas.place(x=0,y=0)

        scrollbar = Scrollbar(root, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', on_configure)
        # --- put frame in canvas ---
        frame = Frame(canvas)
        canvas.create_window((100, 100), window=frame, anchor='nw')
        # --- add widgets in frame ---
        msg=""
        with open("Help Info.txt", 'r') as myHelp:
            for lines in myHelp:
                msg+=lines
        l = Label(frame,text=msg,  anchor = 'e')
        l.pack()
        B1 = Button(root, text="CLOSE\nWINDOW", font="-size 20", background='red', command=root.destroy, height = 5, width = 10)
        B1.pack(side=RIGHT)
        # --- start program ---
        root.mainloop()


if __name__=="__main__":
    root = Tk()
    root.geometry('750x715')
    root.title("USER CONFIGURATION FOR BATCH UPLOAD")
    root.resizable(False, False)
    app = Window(root)
    root.mainloop()

