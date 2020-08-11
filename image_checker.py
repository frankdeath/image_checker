#!/usr/bin/env python3

import sys
import re
import os.path

def getExtension(filename):
	#
	filenamePattern = "(.*)\.([^.]+)"
	filenameRegex = re.compile(filenamePattern)
	return filenameRegex.match(filename)

def getImageType(filename):
	imageType = None
	#
	if os.path.isfile(filename):
		# Read the first two bytes of the file
		# png - 0x89 0x50
		# jpg - 0xff 0xd8		
		fh = open(filename, 'rb')
		firstBytes = fh.read(2)
		fh.close()
		
		if firstBytes == b'\xff\xd8':
			imageType = 'jpg'
		elif firstBytes == b'\x89P':
			imageType = 'png'
		else:
			# leave imageType set to None for other file types
			pass
	return imageType
	

def main(args):
	#
	renameFiles = args.fix_filenames
	filesToCheck = args.image_files
	
	for f in filesToCheck:
		imageType = getImageType(f)
		if imageType != None:
			# File is a jpeg or png file
			result = getExtension(f)
			if result != None:
				filePrefix, fileExt = result.groups()
				fileExtLower = fileExt.lower()
				if fileExtLower in ('jpg', 'jpeg'):
					# filename implies jpeg
					if imageType == 'jpg':
						# file is named correctly
						print("{} is ok".format(f))
					elif imageType == 'png':
						# file is named incorrectly
						print("Rename {} to {}.{}".format(f, filePrefix, imageType))
				elif fileExtLower == 'png':
					# filename implies png
					if imageType == 'png':
						# file is named correctly
						print("{} is ok".format(f))
					elif imageType == 'jpg':
						# file is named incorrectly
						print("Rename {} to {}.{}".format(f, filePrefix, imageType))
				else:
					# filename has a different extension
					print("WTF?")
			else:
				print("{} doesn't have an extension".format(f))
		else:
			print("{} isn't a jpeg or a png file".format(f))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Correct .jpg and .png file extensions")
	parser.add_argument('-f', '--fix', dest='fix_filenames', action='store_true', help="rename files")
	parser.add_argument('image_files', metavar='image_file', nargs='+')

	args = parser.parse_args(sys.argv[1:])
	#!print(args)
	main(args)
