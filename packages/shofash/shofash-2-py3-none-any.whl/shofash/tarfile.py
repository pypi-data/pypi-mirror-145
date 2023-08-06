#!/usr/bin/python3

# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

import os, sys, datetime,tarfile
from .tardir import tardir

def run():
	# Main program..............................................................
	
	rc = 0 # Return code (0=ok)	

	doAll = False
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "all":
			doAll = True
			
	# Backup the file if it already exists
	tarFileName = 'shofash.tar.gz'
	infoFileName = "tarfile_info.shofash"
	versionFileName = "version.shofash" # Name of file used to store last version time
	versionTime = 0 # Time of last version
	
	#ext = '.tar.gz'
	
	if os.path.isfile(versionFileName):
		versionTime = os.path.getmtime(versionFileName)
	else: # tar all files
		doAll = True
	
	now = datetime.datetime.now()
			
	# Build the file. Include all files updated later than Textfile.info...
	with open("tarfile_contents.shofash","w") as tfc:
		print("Creating: " + tarFileName + " tarfile_contents.shofash\n")
		tfc.write(tarFileName + "\n")
		tfc.write(now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
		tardir('.', tarFileName, versionTime, doAll, tfc)
		tfc.close()
	
	# Note the time of update
	tfi = open(infoFileName,"a")
	#now = datetime.datetime.now()
	tfi.write("\nLast build: ")
	tfi.write(now.strftime("%Y-%m-%d %H:%M:%S"))
	tfi.write("\n")
	tfi.close()
	
	return rc
