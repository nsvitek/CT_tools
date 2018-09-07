# Morphosource Batch Convert
A collection of python scripts that streamlines the batch uploading process in Morphosource

The entry point for users is the `user_configuration.py` file.

If you want to create a custom configuration file interactively, step by step, you can do that, too. First, follow steps 1-3 in the Quick Start guide. Then, type in `python interactive_configuration.py`. Follow the instructions on your screen. **CAUTION:** This program will overwite the original configuration file (`user_configuration.py`) with a new file that is missing the notes and commentary in the original file. If you need to go back to that original user configuration script, it is preserved as `user_configuration_original.py`. 

#### Dependencies
The code depends on the packages `pandas`, `idigbio`, and `future`. See more on installing pandas [here](https://pandas.pydata.org/pandas-docs/stable/install.html) and on installing idigbio [here](https://pypi.org/project/idigbio/). Installing `future` is best done using the code `pip install future`. 

    Update 20 August 2018: The code has been updated for Python 2 compatibility but not tested. If you are running Python 2 and running into issues, please contact me. 

## Quick Start

1. Open `user_configuration.py` in a text editor and change the variables in ALL CAPS to the correct settings for your job.
2. Open a terminal window on a machine with Python installed (for more on installing Python, see guide [here](https://realpython.com/installing-python/) or, if on Windows, consider the [Anaconda distribution](https://docs.anaconda.com/anaconda/install/windows)).
3. Navigate to the location of the code by typing `cd C:\Path\to\morphosource_batch_convert`
4. Type `python main_mbc.py`

## Workflow
At minimum, you must provide the following via the variables in `user_configuration.py`:

* CT scanning metadata (information like voxel size, voltage, etc.)
* the file names that you want to upload as part of the batch
* grant and policy settings (can use default settings, though you should change the copyright holder)

**Recommended setup**: A quick workflow is to create a single folder that contains all of the files that you want to use in a batch upload job. You can include raw files, derivative files, as well as the raw CT metadata files output by a CT scanner (ex: .pca, .xkekct files) all in the folder. If you have additional metadata about each specimen, format those data as a .csv or .xlsx spreadsheet.  Specimens or scans should be in rows. Attributes should be in columns. Store the spreadsheet just outside of your single upload folder. Set that additional spreadsheet name as the `OTHER_METADATA_FILE` variable. Use the `INPUT_PATH` variable to the folder where all input files (including spreadsheets) are stored. See the `sample_data` folder and the sample configuration files within for setup examples.

If a folder of files to upload or raw CT metadata files will not fit with your workflow, information can also be input entirely though spreadsheets. See guidelines below for how to set variables in `user_configuration.py` to  work with those alternative setups.

### CT scan metadata
If your CT scanner outputs `.pca`, `.xtekct`, or `.log` files, the code can read CT scan metadata directly from those files. If you want to use that option, set the `CT_METADATA_FOLDER` variable equal to the folder that contains all of the metadata files you want to use. Set the `CT_METADATA_FILE` equal to `None`. 

Alternatively, the code can read CT scan metadata from a spreadsheet. In that case, set `CT_METADATA_FILE` equal to the name of the spreadsheet file you want to use (in .csv or .xlsx format) and set `CT_METADATA_FOLDER` equal to `None`. Then, set the variables in the `CT metadata` section of `user_configuration.py` so that each variable matches the name of the matching column in your spreadsheet. For example, `NAME_VOLTAGE` should equal the name of the column containing voltage information. 

Additional CT metadata settings that are not necessarily included in raw scanner output files (example: the wedge used) can also be set with variables in the `CT metadata` section.

**Standalone use:** If you want to extract CT scan metadata without running the entire morphosource batch convert script, use the script `user_extract_CT.py` script. It replaces the old `CT_extract-settings.py` script and depends on functions in the `ct_metadata.py` script. To use, open `user_extract_CT.py` in a text editor and change the input paths and output names in ALL CAPS. Then, run the script just as you would run `main_mbc.py`. 

**Use with batch scans:** If multiple specimens are associated with the same CT metadata file, the user should provide a spreadsheet (`OTHER_METADATA_FILE`) that contains, at minimum, a column of specimen names (`NAME_SPECIMENS`) and a column with the names of the batch scan containing that specimen (`NAME_BATCH`). That same spreadsheet can optionally contain additional metadata. 

### File names for upload
If you have a single folder containing all the files you want to upload, including  zipped .tiff stacks and mesh files, the code can read those file names and match them to specimen metadata. In that case, set `UPLOAD_FOLDER` equal to the name of that single folder.

If you do not have such a folder, you can also include the file names as a column in a spreadsheet. In that case, set `OTHER_METADATA_FILE` equal to the name of your spreadsheet and `UPLOAD_FOLDER` equal to `None`.

Your file names should be standardized to include at least the museum code and specimen number, if not also the collections code. Each of those pieces of information should be in the same part of the file name each time and be separated by a delimiter (example: "UF-M-12345"). Currently, the code supports " ", "_", and "-" as delimiters. If you can work with regular expressions and want to use a different set of delimiters, edit the `DELIMITER` variable. 

If your file names are set up as described above, then the code will break the specimen name into segments, which are numbered starting from zero. Specify which segments of the file name equal which pieces of catalog information (musuem code: `SEGMENT_MUSEUM`, collection code: `SEGMENT_COLLECTION`, and specimen number: `SEGMENT_NUMBER`). If your code also contains information about the element scanned, that can also be included (`SEGMENT_BODYPART`). For example, in 'UF-M-12345_head', the museum code ('UF') is in segment 0, the collection code is in segment 1, the specimen number is in segment 2, and information about the element is in segment 3.

If your names are successfully segmented, then the code will query the iDigBio API to aquire occurrence IDs for each specimen. The user will have to interactively choose the correct collection for the batch upload, regardless of whether or not they include collection code information, because of the idiosyncracies of collections codes on iDigBio.

_Note:_ If you are working with a spreadsheet of specimens, the specimen naming conventions should match the naming conventions of the files you want to upload.  

**Mesh Files**: The code assumes that mesh files have identical names to the zip files except for file ending (ex: 'UF-M-12345.zip', 'UF-M-12345.stl'), unless there are multiple meshes per specimen (ex: 'UF-M-12345.zip', 'UF-M-12345_raw.stl', 'UF-M-12345_crop.stl'). If your mesh files have suffixes regardless (ex: 'UF-M-12345.zip', 'UF-M-12345_mesh.stl'), set `MESH_SUFFIX` to `True`.

### Grant and policy settings
The `Media Permissions` section of `user_configuration.py` has lists of the copyright permission options and media policy options used by Morphosource. Set each variable to the number of the option you want to use. Set `PROVIDER` equal to the name of the copyright holder with the name in quotes. 

If the scans are a part of the oVert grant, there is also a section (`oVert-specific settings`) to designate the scanning and specimen institutions for automated grant acknowledgment formatting. 

### Example configurations
See `sample_UF_user_configuration.py` and the dummy files in `sample_data` for an example setup that works without spreadsheets. See `sample_batch_user_configuration.py` and associated dummy files in `sample_data` for an example of a setup with batch scans, as well as how to work with additional spreadsheets.

### Output 
The script will write an .xlsx file formatted for direct use in Morphosource batch uploads.  

 The code was developed and run within the Anaconda framework using Python 3.6.5. Code development is funded by the oVert TCN, NSF DBI-1701714. 