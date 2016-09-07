# CT_tools
collection of scripts for processing and working with CT data

Described in order of addition

### CT_extract-settings.py

A python script designed to extract and organize metadata for a scan. It is designed to work with pca files that are produced by GE Phoenix line CT scanners

**Input:** The script takes a small amount of user input (you will have to type if you want the script to draw from a single pca file or a folder containing multiple pca files, then you will have to specify the file path of your choice, then you will have to specify the name of the output table), and either (a) a single pca file, or (b) the location of a folder that contains multiple pca files. If drawing metadata from multiple files, those pca files can be nested in various subfolders within the folder you specify. The idea is that you don't have to change your file structure in order to extract data from multiple scans. 

**Output:** The script will write a .csv file of a set of settings commonly used in processing scans or in sharing scan data. If some parameters of interest to you are not included in the output, please contact me and I'll see what I can do. 
