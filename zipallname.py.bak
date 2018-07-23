#! /bin/env python
### script to automatically zip tif image stacks in every folder that matches a given specimen name

import pandas, zipfile, os, glob, logging, time
#weird import call is because I generally test outside of scripts directory.
#if in scripts directory, can simply run line:
import goldenmole
#from scripts import goldenmole
goldenmole = goldenmole.goldenmole
#for the 'from...' line to work, must have '__init__.py' file in scripts folder
logging.basicConfig(level=logging.INFO,filename='zipallname'+time.strftime('%Y-%m-%d')+'.log',filemode='a')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # .
# set variables

#set the container folder where the script should start looking for folders
ContainerName = '/cygdrive/d/CT_maniculatus_repositing'

#set the file/column location for the list of desired specimens
DeciderFile = 'C://Users/N.S/Documents/Dissertation/modern/podomys/podomys_access.csv'
ColName = 'specimen_num'

#set search levels for folder tree. If more levels, code will need more tweaking
# HighestSearch = 'podomys_floridanus'
HighestSearch = 'maniculatus*'

#decide if you want to zip data from all specimens or a select list (Raw?), or all specimens that have a certain prefix (RawPrefix)
#and then decide if you want to zip .tiff's only or if you want to zip up all files.
Raw = True
RawPrefix = ''
ImgOnly = True

# End variable setting.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # .

# get full path for Container
Container = os.path.join(os.path.expanduser('~'),ContainerName)
# read the file containing specimen names
# Decider = pandas.read_csv(DeciderFile)
# def get_spec(csv, column_name):
	# return getattr(csv,column_name)

# #make an object containing all of the specimen names
# Specimen = get_spec(Decider,ColName)
# Specimens = Specimen.tolist()

#for each entry in the list, find a folder that contains that string
level1 = goldenmole(Container,HighestSearch,desire='folder')
level2 = []
 
for directory in level1:
	for subdirectory in os.listdir(os.path.join(directory)):
		if os.path.isdir(os.path.join(directory, subdirectory))==True:
			level2.append(os.path.join(directory, subdirectory))

###QUICK CHANGE
# level2 = goldenmole(level1[0],'checked',desire='folder')
###END CHANGE
level3=[]

if Raw == True:
	# # # # # # # # # # # # # # # Use these loops to zip raw data
	if ImgOnly == True:
		# # # # # # # # # # # # # # # # zip only tif stacks
		for directory in level2:
			answer = goldenmole(directory,'.*[0-9]',desire='folder')
			if answer:
				level3.append(answer)
	if ImgOnly == False:
		# # # # # # # # # # # # # # # zip entire folder with prefix RawPrefix
		for directory in level2:
			answer = goldenmole(directory,RawPrefix,desire='folder')
			if answer:
				level3.append(answer)
	
if Raw != True:
	# # # # # # # # # # # # # # # Use these loops to zip specimen folders
	count = 1
	for specimen in Specimens:
		for directory in level2:
			answer = goldenmole(directory,'.*'+specimen,desire='folder')
			if answer:
				level3.append(answer)
				print('.')
				count = len(level3)
		if count != len(level3):
			print('cannot find folder '+specimen)
			logging.info('Folder %s not found', specimen)
			count = count 


# navigate to desired folder, make a zip file and open it
counter = 0
if Raw != True:
	for specimen in level3:
		print 'zipping ' + level3[counter][0].split('/')[-1]
		os.chdir(level3[counter][0])
		#if there are .tif files in there and the folder doesn't already exist, go ahead.
		if not os.path.exists(level3[counter][0].split('/')[-1]+'img.zip'):
			file = zipfile.ZipFile(level3[counter][0].split('/')[-1]+'_tif.zip', 'w',allowZip64=True)
			for name in glob.glob('*.tif'):
				print name
				file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
			#if there are no files, print "is this already zipped?"
			file.close()
			os.chdir(Container)
			print 'finished zipping ' + level3[counter][0].split('/')[-1]
		else: 
			print 'FOLDER ALREADY EXISTS. SKIPPED.'
			logging.info('Folder %s already exists', level3[counter][0].split('/')[-1])
		counter = counter + 1

####QUICK CHANGE
# level3 = [level2]
####END CHANGE

if Raw == True: 
	for folder in level3:
		counter2 = 0
		for multifolder in level3[counter]:
			os.chdir(level3[counter][counter2])
			if ImgOnly == True:
				#check if folder exists
				if not os.path.exists(level3[counter][counter2].split('/')[-1]+'_mandible.zip'):
					print 'zipping ' + level3[counter][counter2].split('/')[-1] + '_mandible'
					file = zipfile.ZipFile(level3[counter][counter2].split('/')[-1]+'_mandible.zip', 'w',allowZip64=True)
					for name in glob.glob('*.tif'):
						print name
						file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
				
					file.close()
				else:
					print 'FOLDER ALREADY EXISTS. SKIPPED.'
					logging.info('Folder %s already exists', level3[counter][counter2].split('/')[-1])
				
			if ImgOnly == False:
				#check if folder already exists
				if not os.path.exists(level3[counter][counter2]+'.zip'):
					os.chdir('..')
					#check one level up, too.
					if not os.path.exists(level3[counter][counter2]+'.zip'):				
						print 'zipping ' + level3[counter][counter2].split('/')[-1]
						file = zipfile.ZipFile(level3[counter][counter2].split('/')[-1]+'.zip', 'w',allowZip64=True)
						for root, _, filenames in os.walk(os.path.basename(level3[counter][counter2])):
							for name in filenames:
								name = os.path.join(root, name)
								name = os.path.normpath(name)
								file.write(name, name)
						
						file.close()
				
					else:
						print 'FOLDER IN FOLDER. SKIPPED.'
						logging.info('Folder %s already exists in folder', level3[counter][counter2].split('/')[-1])
			
				else:
					print 'FOLDER ALREADY EXISTS. SKIPPED.'
					logging.info('Folder %s already exists', level3[counter][counter2].split('/')[-1])
			
			print 'finished zipping ' + os.getcwd().split('/')[-1]
			logging.info('Finished zipping ' + level3[counter][counter2].split('/')[-1])
			os.chdir(Container)
			
			counter2 = counter2 + 1
		counter = counter + 1

logging.info('End of script.')
logging.close()