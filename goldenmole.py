#! /bin/env python

def goldenmole(StartPath,PatternMatch,desire={'folder','file'}):	
	Usage = """
	goldenmole - version 1.0
	Searches a path (StartPath) to match a regular expression (PatternMatch).
	Needs to know if you want it to search for files or folders (desire={'folder','file'}).
	"""
	#relies on re, os modules
	import re, os
	FindPattern = re.compile(PatternMatch)
	MatchedPaths = []
	#if user didn't specify file/folder correctly, give them a hint
	if not (desire.lower() == 'folder' or desire.lower() == 'file'):
		print(Usage)
	for names in os.listdir(StartPath):
		if desire.lower() == 'folder':
			#search only directories
			if os.path.isdir(os.path.join(StartPath, names)):
				#match regex
				if FindPattern.match(names):
					#make an object of matched directories
					MatchedPaths.append(os.path.join(StartPath, names))
		if desire.lower() == 'file':
			#search only files
			if os.path.isfile(os.path.join(StartPath, names)):
				#match regex
				if FindPattern.match(names):
					#make an object of matched directories
					MatchedPaths.append(os.path.join(StartPath, names))
	
	#print result
	return MatchedPaths
	
# ###old version		
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