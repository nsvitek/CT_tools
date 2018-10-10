#! /bin/env python
### script to make folders for a csv column of specimen names

#from __future__ import print_function
from builtins import input
import os, sys, re, pandas

# input location of csv file with file names
path_input = ""
path_input = input("Enter the path of your folder or file. Don't use quotes, just enter the path.")

path_output = input("Enter the path of the location where you want your new folders to be created. Don't use quotes, just enter the path.")

if os.path.isdir(path_output): #check to make sure the folder exists
	print('Output path found. Good start')
else:
	sys.exit('Path not found. Try again.')

def read_user_input(input_file):
    """ reads in user-provided specimen data """
    file_suffix = re.match('.*\.(.*)$',input_file).group(1) #get file ending
    if (file_suffix == "csv"): #if file is csv
        user_input_raw = pandas.read_csv(input_file)
    if (file_suffix == "xlsx"): #if file is excel spreadsheet
        user_input_raw = pandas.read_excel(input_file)
    if (file_suffix not in ('csv', 'xlsx')):
        ErrorMessage = f'File ending {file_suffix} is not csv or xlsx.'
        print(ErrorMessage)
    return user_input_raw

Decider = read_user_input(path_input)

print("Here are the available column names")
print(list(Decider.columns.values))
ColName = input("Enter the column name that contains desired folder names.")

# define a short, helpful function
def get_spec(csv, column_name):
	return getattr(csv,column_name)

# set column name of interest from names in csv
Specimen = get_spec(Decider,ColName)
Specimens = Specimen.tolist()

#print the list of desired specimens and check for folder existence. Does it look correct?
print("Are these the names you want?")
print(Specimens)
print("\nNumber of names:")
print(len(Specimens))

#continue?
user_input = input('\nAre the folders ready to be named? [y/n] ')
if user_input == 'n':
	print('Okay. Fix it then try again.')
	quit()
elif user_input == 'y':
	print('Good. Onward.')
else:
	print('I do not understand. Fail.')


for index in Specimens:
    newpath = ((path_output + '/%s') % (index)) 
    if not os.path.exists(newpath): os.makedirs(newpath)
