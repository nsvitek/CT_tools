# Morphosource Batch Convert
A collection of python scripts that (hopefully) streamline the batch uploading process in Morphosource

The entry point for users is the `main_mbc.py` file. At the top of the file are path variables for users to set. Everything else in the script is run interactively.

### Quick Start

    1. Change the variables in ALL CAPS in `main_mbc.py` to your particular file names for a job
    2. Open the program Anaconda Prompt
    3. navigate to the location of the code location by typing 'cd C:\Path\to\morphosource_batch_convert'
    4. type 'python main_mbc.py'

This code is in very early stages. You are welcome to try it out and I am more than happy to hear your feedback, bug reports, etc. However, understand that the code is subject to rapid and dramatic change. It is still in active development. The code was developed and run within the Anaconda framework using Python 3.6.5. I have not tried using it in other implementations and versions.  

**Input:** In order to proceed, you will need:

* An .xlsx or .csv file containing, at minimum, a column with specimen numbers (ex: "UF 12345", "UF_12345", or "UF-collection-12345") of the specimens you want to upload to Morphosource
* A .csv file containing CT scan metadata, such as the kind output by `CT_extract-setting.py` in the general `CT_tools` project. 

**Output:** The script will write an .xlsx file formatted for direct use in Morphosource batch uploads.  

Code development is funded by the oVert TCN, NSF DBI-1701714. 