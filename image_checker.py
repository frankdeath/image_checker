#!/usr/bin/env python3
#
# Correct file extensions for jpeg and png files
#

import sys
import re
import os.path

def getExtension(filename):
	#
	filenamePattern = "(.*)\.([^.]+)"
	filenameRegex = re.compile(filenamePattern)
	return filenameRegex.match(filename)

def getImageType(filename):
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
		imageType = None

	return imageType
	
def main(args):
	#
	renameFiles = args.fix_filenames
	filesToCheck = args.image_files
	
	for f in filesToCheck:
		# Check for file existence
		if os.path.isfile(f):
			# Determine image type
			imageType = getImageType(f)
			if imageType != None:
				# File is a jpeg or png file
				result = getExtension(f)
				if result != None:
					filePrefix, fileExt = result.groups()
					fileExtLower = fileExt.lower()
					#
					if ((fileExtLower in ('jpg', 'jpeg')) and (imageType == 'png')) or ((fileExtLower == 'png') and (imageType == 'jpg')) :
						# file is named incorrectly
						print("Rename {} to {}.{}".format(f, filePrefix, imageType))
					else:
						# file is named correclty or filename has a different extension--no action is required
						print("{} is ok".format(f))
				else:
					if imageType == 'jpg' or imageType == 'png':
						# file lacks an appropriate extension
						print("Rename {} to {}.{}".format(f, f, imageType))
					else:
						print("{} doesn't have an extension and isn't a jpeg or a png".format(f))
			else:
				print("{} isn't a jpeg or a png file".format(f))
		else:
			print("{} doesn't exist".format(f))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Correct .jpg and .png file extensions")
	parser.add_argument('-f', '--fix', dest='fix_filenames', action='store_true', help="rename files")
	parser.add_argument('image_files', metavar='image_file', nargs='+')

	args = parser.parse_args(sys.argv[1:])
	#!print(args)
	main(args)
