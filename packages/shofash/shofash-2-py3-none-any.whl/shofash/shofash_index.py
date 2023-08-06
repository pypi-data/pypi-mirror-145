# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

def shofash_index(dir_name, order, type): 
	
	import glob
	import os
	import time
	from .shofash_functions import shofash_path_to_title
	
	# Get a list of files or directories:
	if type == "file":
		pattern = os.path.join(dir_name,"*.html") # Long file name path + "*.html"
		list_of_files = filter( os.path.isfile, glob.glob(pattern) )
	else: # Directory
		pattern = os.path.join(dir_name,"*") # All
		list_of_files = filter( os.path.isdir, glob.glob(pattern) )

	# Order them correctly:
	if order == "blog": # Blog (ie date) order
		list_of_files = sorted( list_of_files, key = os.path.getmtime, reverse = True)
	elif order == "alpha": # Alphabetical order
		list_of_files = sorted( list_of_files )

	r = "<DIV CLASS='shofash_index_block'>\n"
	r += "<!-- " 
	r += order
	r += " "
	r += type
	r += " -->\n"
	
	for file_path in list_of_files:
		if file_path[-10:] != "index.html": # Skip the index file
			r += "<DIV CLASS='shofash_index_item'><A HREF='" 
			#splitted = os.path.split(file_path)
			file_name = os.path.basename(file_path)
			if type == "file":
				r += file_name
				r += "'>" 
				r += shofash_path_to_title(file_name[:-5])
			else: # Directory
				r += file_name
				r += "/index.html'>"
				r += shofash_path_to_title(file_name)
				r += "<SMALL>...</SMALL>"
				
			r += "</A></DIV>\n"
		
	r += "</DIV>\n"
	
	return r

# Returns an index tree structure
def shofash_index_tree(dir_name, order): 
	import os, glob
	from .shofash_functions import shofash_path_to_title

	froot = '.'

	# Get a list of directories:
	pattern = os.path.join(dir_name,"*") # All
	# list_of_files = filter( os.path.isdir, glob.glob(pattern) )
	list_of_files = glob.glob(pattern) 

	# Order them correctly:
	if order == "blog": # Blog (ie date) order
		list_of_files = sorted( list_of_files, key = os.path.getmtime, reverse = True)
	elif order == "alpha": # Alphabetical order
		list_of_files = sorted( list_of_files )

	r = "<DIV CLASS='shofash_index_block'>\n"
	
	for file_path in list_of_files:
	
		file_name = os.path.basename(file_path)	

		if os.path.isdir(file_path): # Dealing with a directory
			r += "<DIV CLASS='shofash_index_item'><A HREF='" 
			r += os.path.join(dir_name,file_name)
			r += "/index.html'>"
			r += shofash_path_to_title(file_name)
			r += "</A>\n"
			r += shofash_index_tree(os.path.join(dir_name,file_name), order) # Recurse to get subdirectories
			r += "</DIV>\n"
		elif os.path.isfile(file_path): #... a file
			if file_name[-5:] == ".html" and file_name != "index.html":
				r += "<DIV CLASS='shofash_index_item'><A HREF='" 
				r += os.path.join(dir_name,file_name)
				r += "'>"
				r += shofash_path_to_title(file_name)
				r += "</A>\n"
				r += "</DIV>\n"
			
	r += "</DIV>\n"
	
	return r

