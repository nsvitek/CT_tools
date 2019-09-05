#! /bin/env python

#script to collect cropped ply files from many folders for analysis based on a list of specimen numbers

from __future__ import print_function
from __future__ import absolute_import
import pandas, zipfile, os, glob, logging, time, shutil, re
#weird import call is because I generally test outside of scripts directory.
#if in scripts directory, can simply run line:
import goldenmole
#from scripts import goldenmole
goldenmole = goldenmole.goldenmole
#for the 'from...' line to work, must have '__init__.py' file in scripts folder
#logging.basicConfig(level=logging.INFO,filename='assembdat'+time.strftime('%Y-%m-%d')+'.log',filemode='a')

##### SET VARIABLES HERE #####
#set the container folder for specimen data
# Container = '/cygdrive/d/'
# Container = '/cygdrive/f/CT_maniculatus'
Container = 'E://'


#set the destination folder
Pen = 'D://ms'
# Pen = 'D://Dropbox/Documents/Dissertation/modern/onychomys_leucogaster/ol_m1_raw'
# Pen = 'C://Users/N.S/Dropbox/Documents/Dissertation/sys_eulipotyphla/talpavoides_QC_raw'

# Pen = '/cygdrive/d/pen'

#set the file/column location for the list of desired specimens
DeciderFile = 'D://NeedZips.csv'
# DeciderFile = 'D://Dropbox/Documents/Dissertation/modern/onychomys_leucogaster/ol_m1_raw.csv'
# DeciderFile = 'C://Users/N.S/Dropbox/Documents/Dissertation/PETMperadectes/all_marsupials/all_marsupials_scanned.csv'
# ColName = 'fullname'
# DeciderFile = 'C://Users/N.S/Documents/UCMP.csv'
# DeciderFile = 'C://Users/N.S/Documents/Dissertation/PETMerinaceomorph/PETMmacro.csv'
# DeciderFile = 'C://Users/N.S/Documents/Dissertation/PETMerinaceomorph/p_4/macrocranion_p_4.csv'
ColName = 'scan_name'

#set the string pattern to catch the kinds of files you want
# Pattern = '.*p4.*_crop.*.ply'
# Pattern = '.*m[x123].*_crop.*.ply'
Pattern = '.*.zip'
#Pattern = '.*_raw.*.ply'

#Pattern = '.*.png'
# Prefix = 'pf_' #in case your folders start with a prefix. MUST BE SET. If there is no prefix, then set as ''
Prefix = ''
Suffix = ''
# Suffix = '_hi'
#set the pattern you want to match for highest folder names
# HighestSearch = 'maniculatus' #formerly FolderPattern
HighestSearch = 'CT' #formerly FolderPattern

#set the number of intermediate folder levels (folders with unimportant names between HighestFolder and the folder containing your specimen number)
NumberIntermeds = 2
##### END VARIABLE SETTING #####

#Check to see if all looks in order
Decider = pandas.read_csv(DeciderFile)
def get_spec(csv, column_name):
	return getattr(csv,column_name)

Specimen = get_spec(Decider,ColName)
Specimens = Specimen.tolist()

#print the list of desired specimens and check for folder existence. Does it look correct?
print("Are these the specimens you want?")
print(Specimens)
print("\nNumber of specimens:")
print(len(Specimens))
print("\nCHECK: The source folder exists: True or False?")
print(os.path.isdir(Container))
print("\nCHECK: The destination folder exists: True or False?")
print(os.path.isdir(Pen))

#continue?
user_input = raw_input('\nAre the folders ready to be checked? [y/n] ')
if user_input == 'n':
	print('Okay. Fix it then try again.')
	quit()
elif user_input == 'y':
	print('Good. Onward.')
else:
	print('I do not understand. Fail.')

# get full path for Container
Container = os.path.join(os.path.expanduser('~'),Container)

#root around (like a mole) to find search hits for level 1
level1 = goldenmole(Container,HighestSearch,desire='folder')

#if no intermediate levels to search, skip level 2...
if NumberIntermeds == 0:
	level2 = level1
else:
	level2 = []

#...if not, build however many intermediate levels you need in a list of lists. This part doesn't work. 
for directory in level1:
	for subdirectory in os.listdir(os.path.join(directory)):
		if os.path.isdir(os.path.join(directory, subdirectory))==True:
			level2.append(os.path.join(directory, subdirectory))

#search for a folder for each specimen at the end of intermediate levels
SpecimenFolder = []
# count = 0
for specimen in Specimens: #[len(Specimens)-1]
	for directory in level2: #choose last list in list
		answer = goldenmole(directory,'^'+Prefix+specimen+'.*'+Suffix,desire='folder')
		if answer:
			SpecimenFolder.append(answer)
			print('.') #let's you know it's running
			# count = len(SpecimenFolder)
	# if count != len(SpecimenFolder):
		# print('cannot find folder '+specimen)s
		# logging.info('Folder %s not found', specimen)
		# count = count 

#short loop to temporarily fix problem where "raw" folder is often first search hit, but unwanted.
for i in SpecimenFolder:
	if re.search('raw',i[0]):
		i[0] = i[1]		

#match folder paths to specimens by building dictionary of folders that match specimens in list
#Lookup = dict([ (specimen, [ folder[0] for folder in SpecimenFolder if re.search('/'+Prefix+specimen, folder[0]) ]) for specimen in Specimens])
Lookup = dict([ (specimen, [ folder[0] for folder in SpecimenFolder if re.search(specimen, folder[0]) ]) for specimen in Specimens])

#check for specimens that couldn't be matched to folders
for specimen in Specimens:
	pleasematch = Lookup.get(specimen)
	if pleasematch:
		print('*')
	if not pleasematch:
		print('\nERROR: no folder found for %s' %specimen)
		logging.info('Folder %s not found', specimen)

print("That's all of 'em.")

#continue?	Can stop here if fixes need to be made to folders/files.
#note that copying will just skip over specimens with missing folders with no warning
user_input = raw_input('Are the files ready to be grabbed? [y/n] ')
if user_input == 'n':
	print('Okay. Fix it then try again.')
	quit()
elif user_input == 'y':
	print('Good. Onward.')
else:
	print('I do not understand. Fail.')

#For each element in the list, copy the cropped ply file into the destination folder. 
for specimen in Specimens:
	FilePattern = '(.*'+specimen+'.*'+Pattern+')'
	Grail = goldenmole(Lookup[specimen][0],FilePattern,desire='file')
	if not Grail:
		print('\nERROR: File for %s not found!' % specimen)
		print('Attempted path = '+ FilePattern)
		logging.info('File for %s not found!', specimen)
	else:
		print('*')
		if len(Grail)>=2:
			print('\n %s has multiple file options. All copied.' % specimen)
			logging.info('%s has multiple file options. All copied.', specimen)
		for file in Grail:
				shutil.copy2(file,Pen)
			
print('\nEnd of code.')
logging.info('End of code.')


# # Old, inflexible version:
# folderPattern = re.compile('CT')
# destinationFolderPattern = re.compile('fake13')
# matchedDestinationFolderPaths = []
# for names in os.listdir(Container):
	# if os.path.isdir(os.path.join(Container, names)):
		# #match regex
		# if folderPattern.match(names):
			# #we have our matched folders, now get our subdirs in that folder
			# testNameBuilder = os.path.join(Container, names)
			# for subdirectoryName in os.listdir(os.path.join(testNameBuilder)):
				# #now we're in the subdirectories, we want to loop through all of this layers subdirectories and then match on a pattern.				
				# subDirectoryPath = os.path.join(testNameBuilder, subdirectoryName)
				# for destinationDirectoryName in os.listdir(subDirectoryPath):
					# if destinationFolderPattern.match(destinationDirectoryName):
						# matchedDestinationFolderPaths.append(os.path.join(subDirectoryPath, destinationDirectoryName))
						# print matchedDestinationFolderPaths
# #build dictionary of folders that match specimens in list
# Lookup = dict([ (r, [ i for i in Potential if re.search(r, i) ]) for r in Specimens])

###NOTES:
# C://Users/N.S/Documents/Dissertation/recent_db_20150826.txt
#cd E://scan201507/peromyscus_gossypinus
#ConPath = os.path.abspath(Container)
#ls -d */ #list all the  directories in shell
#/cygdrive/c/Users/N.S/scripts
# might also be helpful:
#folder must be pre-created
#find . -name \*_m2__crop.ply -exec cp {} temp \;