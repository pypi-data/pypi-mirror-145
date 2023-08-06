# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

import os, sys

# Returns a DIV block containing sources
def shofash_sources( sources ):
	# Put out the Sources section if there are any ...
	fo = ""
	if len( sources ) == 1 :
		fo += "<DIV CLASS='source'>\n"
		fo += "\t<SPAN CLASS='sourceHeading'>Source: </SPAN>\n"
		fo += sources[0]
		fo += "</DIV>\n"
	elif len( sources ) > 1 :
		fo += "<DIV CLASS='source'>\n"
		fo += "\t<DIV CLASS='sourceHeading'>Source"
		if len( sources ) > 1 :
			fo += "s"
		
		fo += ":</DIV>\n"
		
		for source in sources:
			fo += "\t<DIV CLASS='sourceLink'>" + source + "</DIV>\n"
		fo += "</DIV>\n"
	
	return fo
	
	

# Returns a human readable title from a file path
def shofash_path_to_title(path):
	base = os.path.basename(path) # Remove directory leader
	base = base.replace("_"," ")
	if ".html" in base:
		base = base[:-5] # Cut off html
	
	return base



# 2022feb01 Added. 
# Returns an anchor link from text
def shofash_text_to_anchor(text):
	text = text.replace(" ","_")
	return text
	
# 2022feb16 Added. Returns an text from an anchor
def shofash_anchor_to_text(anchor):
	anchor = anchor.replace("_"," ")
	return anchor
	

# Return a formatted, clickable list of the latest changed files
def shofash_latest():
	f_latest = "latest.shofash" # List of changed files
	r = "<DIV CLASS='shofash_index_block'>\n"
	
	if os.path.exists(f_latest): 
		with open(f_latest,"r") as file:
			lines = file.readlines()
			file.close()
			for line in lines:
				line = line.strip()
				if (len(line)>0):
					bits = line.split("\t")
					file_name = bits[0]
					if len(bits) > 1:
						title = bits[1]	
					else:
						title = shofash_path_to_title(file_name)
	
					r += "<DIV CLASS='shofash_index_item'><A HREF='" 
					r+= file_name
					r += "'>" 
					r += title
					r += "</A></DIV>\n"
		
	r += "</DIV>\n"
	return r



def split_path(path):
	allparts = []
	while True:
		parts = os.path.split(path)
		if parts[0] == path:  # Absolute path
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path: # Relative path
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
			
	return allparts

# Return a string that will skip down to root folder (ie "../../")
def skip_to_root( path ):
	parts = split_path( path )
	skip = ".." + os.sep
	return skip * (len(parts)-2)
	
