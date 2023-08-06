# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

# Expand out any macros in the line
# 2022jan04 def shofash_expandMacros( line, path_to_root ):
# 2022feb01 Added support for "[...]" links

import re
import os

# 2022feb01+
def shofash_expandMacros_link( url, live_link, link_text, path_to_root ):

	if url[0] == "@": # Force a live link because of [@...|...] 
		url = url[1:]
		live_link = True
	
	if len(link_text) < 1 :
		link_text = url
		
	if "http" == url[:4] : # WWW link
		if live_link : # Are live links allowed by default
			linkString = "<A HREF='" + url + "' TARGET='_BLANK' TITLE='Open in new window'>" + link_text + "</A>"
		else: # Default to dead links
			linkString = link_text
	elif url[0] == "#": # Link within page ie [#anchor]
		linkString = "<A HREF='" + url.lower() + "' TITLE='Move within page'>" + url[1:] + "</A>"
	else: # Local link
		if os.path.exists(url): # File exists
			url = path_to_root + url
			linkString = "<A HREF='" + url + "' TITLE='Open page'>" + link_text + "</A>"
		else: # Broken link
			print("ERROR: Broken link: " + url)
			linkString = link_text
	
	return linkString
	
	

# Expand all macros found in the text
def shofash_expandMacros( line, path_to_root, system_flags ):

	while True :
		found = re.search(r'\[([^\|]+)\|([^\]]+)\]', line )
		if found:
			url = found.group(1)
			live_link = "links_live" in system_flags # Are live links allowed by default
			link_text = found.group(2)
			linkString = shofash_expandMacros_link( url, live_link, link_text, path_to_root )
			line = line.replace(found.group(),linkString )
			continue
		else: # No more found
			break
			
	# 2022feb01+ Support for "[URL]" links
	while True :
		#found = re.search(r'\[([^\|]+)\]', line )
		found = re.search(r'\[([^\|\]]+)\]', line ) # Non-greedy search to allow multiple instances in line
		if found:
			url = found.group(1)
	
			live_link = "links_live" in system_flags # Are live links allowed by default
			link_text = "www"
			linkString = shofash_expandMacros_link( url, live_link, "", path_to_root )
			line = line.replace(found.group(),linkString )
			continue
		else: # No more found
			break
	
	# { Quoted text} => <SPAN CLASS='quote'>Quoted text</SPAN>
	while True : 
		found = re.search(r'\{([^\}]+)\}', line ) 
		if found:
			linkString = "<SPAN CLASS='quote'>" + found.group(1) + "</SPAN>"
			line = line.replace(found.group(),linkString )
			continue
		else: # No more found
			break

	# Dateline at start of line 2021may10.
	found = re.search(r'^20\d{2}[a-zA-Z]{3}\d{2}', line ) 
	if found:
		linkString = "<A CLASS='anchor' ID='" + found.group(0) + "'>" + found.group(0) + "</A>"
		line = line.replace(found.group(0),linkString )

	return line

   
if __name__ == "__main__":
	# Put testing code from command line here ...
	pass
