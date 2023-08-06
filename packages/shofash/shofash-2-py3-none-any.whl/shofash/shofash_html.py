# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

# Build the output .php file
# 2022jan04 def shofash_html( textFile, directory ):
def shofash_html( textFile, directory, system_flags, macros ):
	import re
	import os
	from collections import deque

	from .shofash_expandMacros import shofash_expandMacros
	from .shofash_getCommand import shofash_getCommand
	from .shofash_functions import skip_to_root, shofash_sources

	sources = [] # A list of # sources in file
	stack = deque() # Stack of para endings
	stack.append("P")
	stackLevel = 1 # Number of items on stack
	fo = ""
	out_title = "" # Title output
	fi = open(textFile, "r")
	file_name = os.path.basename(textFile) # Get the filename without the path to it

	# Now process all remaining lines ...
	lineNumber = 0
	lines = fi.readlines()
	fi.close()
	for line in lines:
		lineNumber = lineNumber + 1
		tabs = "\t" * (stackLevel-1)
		fo += tabs # Indent
		line = line.strip()
		if len(line) < 1: # Skip empty lines
			continue
			
		#2022feb09+ Replace any macros ...
		for macro in macros:
			line = line.replace(macro[0],macro[1])
		#-
		
		# Process this line ...		
		c1 = line[0] # First character is command
		c1 = c1.lower()
		cmd = line[1:] # Get rest of line as parameters
		cmd = cmd.strip()
		
		if c1 == "+": # Start of list
			if len( cmd ) < 1: # Default to UL?
				cmd = "UL"
				
			fo += "<%s>\n" % (cmd) 
			stack.append(cmd)
			stackLevel = stackLevel + 1
		elif c1 == "-": # End of list
			if stackLevel > 1:
				tag = stack.pop()
				fo += "</%s>\n" % ( tag ) 
				stackLevel = stackLevel - 1	
			else:
				print("File: %s Line: %d Too many items popped off list!\n" % ( textFile, lineNumber))

		elif c1 == "#": # Command
			# 2022jan04 command_output = shofash_getCommand( cmd , sources, directory, file_name[:-4] )
			command_output = shofash_getCommand( cmd , sources, directory, file_name[:-4], system_flags )
			#fo += shofash_getCommand( cmd , sources, directory, file_name[:-4] )
			fo += command_output[0]
			if len(command_output[1]) > 0:
				out_title = command_output[1]
			
		elif c1 == "<": # HTML
			fo += line 
			fo += "\n" 
			
		# 2021jun15+ Add new comment and end commands
		elif c1 == "/": # Comment 
			continue # Skip to next line
		
		elif c1 =="!": # Quit
			break # Leave loop to stop processing lines
			
		# 2021jun15-
		
		else: # Normal line
			# 2022jan04 line = shofash_expandMacros( line, skip_to_root(textFile) ) # Expand out any macros in the line
			line = shofash_expandMacros( line, skip_to_root(textFile), system_flags ) # Expand out any macros in the line
			tag = stack[-1]
			
			if tag == "P":
				fo +="<P>" + line + "</P>\n"
			else:
				#fo += "<LI>" + line + "</LI>\n" 
				fo += "<LI>" + line + "\n" # For w3 validity nested lists
	
	fo += shofash_sources( sources ) # Get sources block
	
	## Put out the Sources section if there are any ...
	#if len( sources ) > 0 :
	#	fo += "<DIV CLASS='source'>\n"
	#	fo += "\t<DIV CLASS='sourceHeading'>Source"
	#	if len( sources ) > 1 :
	#		fo += "s"
	#	
	#	fo += ":</DIV>\n"
	#	
	#	for source in sources:
	#		fo += "\t<DIV CLASS='sourceLink'>" + source + "</DIV>\n"
	#	fo += "</DIV>\n"
		
	return [fo,out_title]


if __name__ == "__main__":
	# Put testing code from command line here ...
	pass
