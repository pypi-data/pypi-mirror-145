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

import sys
import os
import time
from os.path import join, getsize, exists
from .shofash_html import shofash_html
from .shofash_index import shofash_index
from .shofash_write_html import shofash_write_html
from .shofash_default_menu import shofash_default_menu

def run():
	
	sys.path.append(".") # Add in current directoy
	
	rc = 0 # Return code (0=ok)	
	
	# Globals setup ____________________________________________________________
	
	doAll = False
	froot = '.'
	htmlSystem = "<!-- ERROR: system.shofash not found -->\n"
	f_template = os.path.join(froot,"template.shofash") # Template html file
	f_flags = os.path.join(froot,"flags.shofash") # 2022jan04 Flags file
	system_flags = [] # 2022jan04 Flags to control program
	f_last_build = os.path.join(froot,"last_build.shofash") # Last build file
	f_latest = os.path.join(froot,"latest.shofash") # List of changed files
	tm_last_build = 0 # Default
	latest_files = []
	latest_files_max = 5 # Max number of files in rss/blog feed
	f_sitemap_source = "Sitemap.txt" # Sitemap file
	f_sitemap_html = "Sitemap.html" # HTML loutput
	f_sitemap_title = "Sitemap" # Sitemap title
	
	if os.path.exists(f_template): # Now get the system.shofash file
		with open(f_template, 'r') as file:
			htmlSystem = file.read()
	else:
		print("ERROR: File " + f_template + " not found")
		quit()
	
	# 2022jan04+
	if os.path.exists(f_flags): # Now get the system.shofash file
		with open(f_flags, 'r') as file:
			print("flags.shofash:")
			flags = file.readlines()
			for flag in flags:
				flag = flag.strip()
				if len(flag) > 0 and not flag[0] == "#": # Add on uncommented flags
					print("\t" + flag)
					system_flags.append(flag)
	else:
		print("ERROR: File flags.shofash not found")
		quit()
	#-
	
	# 2022feb09+
	macros = [] # Macros file (empty)
	if os.path.exists("macros.shofash"): # Get the macros (if any) in macros.shofash
		with open("macros.shofash", 'r') as file:
			print("macros.shofash:")
			lines = file.readlines()
			for line in lines:
				line = line.strip()
				if len(line) > 0: 
					items = line.split(maxsplit=1) # Split on whitespace
					if len(items) == 2:
						macro_key = items[0].strip()
						macro_replacement = items[1].strip()
						macros.append( [ macro_key, macro_replacement ] )
						print("Key=" + macro_key + " Replacement=" + macro_replacement)				
	#-
	
	if os.path.exists(f_last_build): # Check the time of last build
		tm_last_build = os.path.getmtime(f_last_build)
	else: # Not built before
		doAll = True # Build all files
		tm_last_build = 0
	
	# Get the list of latest files from latest.shofash ...
	if os.path.exists(f_latest): 
		with open(f_latest,"r") as file:
			lines = file.readlines()
			file.close()
			for line in lines:
				line = line.strip()
				if (len(line)>0):
					latest_files.append(line)
	
	if os.path.getmtime(f_template) > tm_last_build: # Has template.shofash been updated after last build?
		doAll = True
	
	# 2022jan04+ Has flags file been altered since the last build?
	if os.path.getmtime(f_flags) > tm_last_build: # Has flags.shofash been updated after last build?
		doAll = True
	# 2022jan04-
	
	# Process the txt files into html ____________________________________________
	
	for root, dirs, files in os.walk(froot,topdown = False):
		
		for name in files:
			if name.endswith("txt"):
				# Put out the interpreted file if file does not exist or is too old ...
				fname = os.path.join(root,name) # Long file name
				fmenu = os.path.join(root,"menu.shofash") # Menu file
				htmlFile = fname[:-4] + ".html"
				title = name[:-4]
				htmlTitle = title.replace("_"," ")
	
				# Build the html file if it: 1) doesn't exist 2) its source txt file has been updated
				#if not os.path.exists(htmlFile) or os.path.getmtime(htmlFile) < os.path.getmtime(fname) or doAll:
				if name != "index.txt" and ( not os.path.exists(htmlFile) or os.path.getmtime(fname) > tm_last_build or doAll or name == f_sitemap_source) :
					# 2022jan04 htmlOut = shofash_html(fname,root)
					htmlOut = shofash_html(fname,root,system_flags,macros)
					htmlContent = htmlOut[0]
					if len(htmlOut[1]) > 0:
						htmlTitle = htmlOut[1]
					
					htmlMenu = "<!-- no menu -->\n"
					if os.path.exists(fmenu): # Now get the menu file menu.shofash
						with open(fmenu, 'r') as file:
							htmlMenu = file.read()
	
					htmlMenu = shofash_default_menu( htmlFile )
					shofash_write_html(htmlFile,htmlSystem,htmlTitle,htmlMenu, htmlContent)
					
					# Update the list of latest files if not index.html and not Sitemap
					if name != "index.txt" and name != f_sitemap_source :
						latest_file = htmlFile[2:] + "\t" + htmlTitle
						try:
							list_ix = latest_files.index(latest_file) # Search for existing entry
						except: # Not found so nothing to do
							pass 
						else: # Must have been found ...
							del latest_files[list_ix]
							
						latest_files.insert(0, latest_file)
						if len(latest_files) > latest_files_max:
							latest_files = latest_files[:-1]
		
		
	# Write out the list of latest files ==================================================================
	
	with open(f_latest,"w") as file:
		for file_name in latest_files:
			file.write(file_name)
			file.write("\n")
		file.close()
	
	# Now go through and create any index.html files that need doing =======================================
	# Build the index.html file if it: 1) doesn't exist 2) its source txt file is newer than the html file 3) if any file/directory is newer than index.html
	for root, dirs, files in os.walk(froot,topdown = True):
			
		qBuild = False # Should the index.html file be built?
		indexFile = os.path.join(root,"index.html")
		indexSourceFile = os.path.join(root,"index.txt")
		htmlTitle = "Index"		
		
		if doAll:
			qBuild = True
		else:
			if not os.path.exists(indexFile): # File does not exist, so create
				qBuild = True
			elif len(root) < 2: # Is root index?
				qBuild = True
			else: # File exists, so check if needs updating
				indexTime = os.path.getmtime(indexFile) # Time the file was updated
				
				if os.path.getmtime(root) > indexTime: # Has root file changed?
					qBuild = True
				else: # Test if any files or directories are newer than index file ...
					for name in files: # Check through all files
						fname = os.path.join(root,name) # Long file name
						if os.path.getmtime(fname) > indexTime:
							qBuild = True
							break # No need to continue
		
					if not qBuild: # Do not check if already set to build
						for name in dirs: # Check through all directories
							fname = os.path.join(root,name) # Long file name
							if os.path.getmtime(fname) > indexTime:
								qBuild = True
								break # No need to continue
									
  	# Now actually build the file if needed ==============		
		if qBuild: 
			htmlContent = "" 
			if os.path.exists(indexSourceFile):
				#htmlContent = shofash_html(indexSourceFile,root)
				# 2022jan04 htmlOut = shofash_html(indexSourceFile,root)
				htmlOut = shofash_html(indexSourceFile,root,system_flags,macros)
				htmlContent = htmlOut[0]
				if len(htmlOut[1]) > 0:
					htmlTitle = htmlOut[1]
	
			else: # Does not exist so create a default index file
				htmlContent = shofash_index(root,"blog","file") # Default to a blog file index
	
			htmlMenu = shofash_default_menu( indexFile )
			if htmlTitle == "Index":
				htmlTitle = os.path.basename(root)
				
			shofash_write_html(indexFile,htmlSystem,htmlTitle,htmlMenu, htmlContent)
	
	
	# Put out the current time in last_build.shofash _______________________________
	
	with open(f_last_build, 'w') as file:
		file.write(time.strftime("%Y-%b-%d %H:%M:%S\n"))
	
	# End of file
	
	return rc
