class userConfig:
    INPUT_PATH = ''
    UPLOAD_FOLDER = ''
    CT_METADATA_FOLDER = None
    CT_METADATA_FILE = ''
    OTHER_METADATA_FILE = ""
    OUTPUT_FILE = ''
    OVERT = False
    BATCH = False
    QUERY_IDIGBIO = False
    DELIMITER = ''
    SEGMENT_MUSEUM = None
    SEGMENT_COLLECTION = None
    SEGMENT_NUMBER = None
    SEGMENT_BODYPART = None
    GRANT_SCANNING_INSTITUTION = 0
    GRANT_SPECIMEN_PROVIDER = None
    PROVIDER = ""
    COPY_PERMISSION = 0
    MEDIA_POLICY = 0
    DOWNLOAD_POLICY = 0
    TECHNICIAN = ''
    WEDGE = ""
    CALIBRATION_SHADE = False
    CALIBRATION_FLUX = False
    CALIBRATION_GEOMETRIC = False
    CALIBRATION_DESCRIPTION = False
    NAME_SCAN = ''  # name of the scan. Might equal a specimen name or batch designation
    NAME_VOXELX = ''  # voxel size
    NAME_VOXELY = ''  # voxel size
    NAME_VOXELZ = ''  # voxel size
    NAME_VOLTAGE = ''  # voltage
    NAME_AMPERAGE = ''  # amperage
    NAME_WATTS = ''  # watts
    NAME_EXPOSURE = ''  # exposure time
    NAME_PROJECTIONS = ''  # number of projections
    NAME_FRAME = ''  # frame averaging
    NAME_FILTER = ''  # filter
    NAME_SPECIMENS = ''
    NAME_GENUS = None
    NAME_SPECIES = None
    NAME_BATCH = ''
    FUNDING_SOURCE = ''
    NAME_ELEMENT = ""
    NAME_SIDE = None
    NAME_FILE = None
    MESH_SUFFIX = True
    def __init__(self):
        userConfig.printVar()
        pass
    @classmethod
    def update(cls, input_path, upload_folder, ct_metadata_folder, ct_metadata_file, other_metadata_file, output_file,
               overt, batch, query_idigbio, delimiter, segment_museum, segment_collection, segment_number,
               segment_bodypart, grant_scanning_institution, grant_specimen_provider, provider, copy_permission,
               media_policy, download_policy, technician, wedge, calibration_shade, calibration_flux,
               calibration_geometric, calibration_description, name_scan, name_voxelx, name_voxely, name_voxelz,
               name_voltage, name_amperage, name_watts, name_exposure, name_projections, name_frame, name_filter,
               name_specimens, name_genus, name_species, name_batch, funding_source, name_element, name_side,
               name_file, mesh_suffix):
        cls.INPUT_PATH = input_path
        cls.UPLOAD_FOLDER = upload_folder
        cls.CT_METADATA_FOLDER = ct_metadata_folder
        cls.CT_METADATA_FILE = ct_metadata_file
        cls.OTHER_METADATA_FILE = other_metadata_file
        cls.OUTPUT_FILE = output_file
        cls.OVERT = overt
        cls.BATCH = batch
        cls.QUERY_IDIGBIO = query_idigbio
        cls.DELIMITER = delimiter
        cls.SEGMENT_MUSEUM = segment_museum
        cls.SEGMENT_COLLECTION = segment_collection
        cls.SEGMENT_NUMBER = segment_number
        cls.SEGMENT_BODYPART = segment_bodypart
        cls.GRANT_SCANNING_INSTITUTION = grant_scanning_institution
        cls.GRANT_SPECIMEN_PROVIDER = grant_specimen_provider
        cls.PROVIDER = provider
        cls.COPY_PERMISSION = copy_permission
        cls.MEDIA_POLICY = media_policy
        cls.DOWNLOAD_POLICY = download_policy
        cls.TECHNICIAN = technician
        cls.WEDGE = wedge
        cls.CALIBRATION_SHADE = calibration_shade
        cls.CALIBRATION_FLUX = calibration_flux
        cls.CALIBRATION_GEOMETRIC = calibration_geometric
        cls.CALIBRATION_DESCRIPTION = calibration_description
        cls.NAME_SCAN = name_scan
        cls.NAME_VOXELX = name_voxelx
        cls.NAME_VOXELY = name_voxely
        cls.NAME_VOXELZ = name_voxelz
        cls.NAME_VOLTAGE = name_voltage
        cls.NAME_AMPERAGE = name_amperage
        cls.NAME_WATTS = name_watts
        cls.NAME_EXPOSURE = name_exposure
        cls.NAME_PROJECTIONS = name_projections
        cls.NAME_FRAME = name_frame
        cls.NAME_FILTER = name_filter
        cls.NAME_SPECIMENS = name_specimens
        cls.NAME_GENUS = name_genus
        cls.NAME_SPECIES = name_species
        cls.NAME_BATCH = name_batch
        cls.FUNDING_SOURCE = funding_source
        cls.NAME_ELEMENT = name_element
        cls.NAME_SIDE = name_side
        cls.NAME_FILE = name_file
        cls.MESH_SUFFIX = mesh_suffix

    @classmethod
    def printVar(cls):
        print("INPUT_PATH:", cls.INPUT_PATH)
        print("UPLOAD_FOLDER:", cls.UPLOAD_FOLDER)
        print("CT_METADATA_FOLDER:", cls.CT_METADATA_FOLDER)
        print("CT_METADATA_FILE:", cls.CT_METADATA_FILE)
        print("OTHER_METADATA_FILE:", cls.OTHER_METADATA_FILE)
        print("OUTPUT_FILE:", cls.OUTPUT_FILE)
        print("OVERT:", cls.OVERT)
        print("BATCH:", cls.BATCH)
        print("QUERY_IDIGBIO:", cls.QUERY_IDIGBIO)
        print("DELIMITER:", cls.DELIMITER)
        print("SEGMENT_MUSEUM:", cls.SEGMENT_MUSEUM)
        print("SEGMENT_COLLECTION:", cls.SEGMENT_COLLECTION)
        print("SEGMENT_NUMBER:", cls.SEGMENT_NUMBER)
        print("SEGMENT_BODYPART:", cls.SEGMENT_BODYPART)
        print("GRANT_SCANNING_INSTITUTION:", cls.GRANT_SCANNING_INSTITUTION)
        print("GRANT_SPECIMEN_PROVIDER:", cls.GRANT_SPECIMEN_PROVIDER)
        print("PROVIDER:", cls.PROVIDER)
        print("COPY_PERMISSION:", cls.COPY_PERMISSION)
        print("MEDIA_POLICY:", cls.MEDIA_POLICY)
        print("DOWNLOAD_POLICY:", cls.DOWNLOAD_POLICY)
        print("TECHNICIAN:", cls.TECHNICIAN)
        print("WEDGE:", cls.WEDGE)
        print("CALIBRATION_SHADE:", cls.CALIBRATION_SHADE)
        print("CALIBRATION_FLUX:", cls.CALIBRATION_FLUX)
        print("CALIBRATION_GEOMETRIC:", cls.CALIBRATION_GEOMETRIC)
        print("CALIBRATION_DESCRIPTION:", cls.CALIBRATION_DESCRIPTION)
        print("NAME_SCAN:", cls.NAME_SCAN)
        print("NAME_VOXELX:", cls.NAME_VOXELX)
        print("NAME_VOXELY:", cls.NAME_VOXELY)
        print("NAME_VOXELZ:", cls.NAME_VOXELZ)
        print("NAME_VOLTAGE:", cls.NAME_VOLTAGE)
        print("NAME_AMPERAGE:", cls.NAME_AMPERAGE)
        print("NAME_WATTS:", cls.NAME_WATTS)
        print("NAME_EXPOSURE:", cls.NAME_EXPOSURE)
        print("NAME_PROJECTIONS:", cls.NAME_PROJECTIONS)
        print("NAME_FRAME:", cls.NAME_FRAME)
        print("NAME_FILTER:", cls.NAME_FILTER)
        print("NAME_SPECIMENS:", cls.NAME_SPECIMENS)
        print("NAME_GENUS:", cls.NAME_GENUS)
        print("NAME_SPECIES:", cls.NAME_SPECIES)
        print("NAME_BATCH:", cls.NAME_BATCH)
        print("FUNDING_SOURCE:", cls.FUNDING_SOURCE)
        print("NAME_ELEMENT:", cls.NAME_ELEMENT)
        print("NAME_SIDE:", cls.NAME_SIDE)
        print("NAME_FILE:", cls.NAME_FILE)
        print("MESH_SUFFIX:", cls.MESH_SUFFIX)