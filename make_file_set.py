#! /bin/env python
### script to make folders for a csv column of specimen names

import os, sys, pandas

# input location of csv file with file names
path_input = ""
path_input = raw_input("Enter the path of your folder or file. Don't use quotes, just enter the path.")

path_output = raw_input("Enter the path of the location where you want your new folders to be created. Don't use quotes, just enter the path.")

if os.path.isdir(path_output): #check to make sure the folder exists
	print('Output path found. Good start')
else:
	print('Path not found. Try again.')

Decider = pandas.read_csv(path_input)

print("Here are the available column names")
print(list(Decider.columns.values))
ColName = raw_input("Enter the column name that contains desired folder names.")

# define a short, helpful function
def get_spec(csv, column_name):
	return getattr(csv,column_name)

# set column name of interest from names in csv
Specimen = get_spec(Decider,ColName)
Specimens = Specimen.tolist()

#print the list of desired specimens and check for folder existence. Does it look correct?
print "Are these the names you want?"
print Specimens
print "\nNumber of names:"
print(len(Specimens))

#continue?
user_input = raw_input('\nAre the folders ready to be named? [y/n] ')
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
