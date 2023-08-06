# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

# Get the text of a command
def shofash_getCommand( commandLine, sources, directory, file_name, system_flags ):

	from .shofash_index import shofash_index, shofash_index_tree
	from .shofash_functions import shofash_latest, shofash_text_to_anchor, shofash_anchor_to_text, skip_to_root, shofash_sources
	from .shofash_expandMacros import shofash_expandMacros


	words = commandLine.split()
	cmd = words[0]
	cmd = cmd.lower()
	r = ""
	out_title = "" # Output title
	
	if cmd == "img":
		r = "<IMG SRC='" + file_name + words[1] + "' HEIGHT='" + words[2] + "' WIDTH='" + words[3] + "' ALT='"
		if len( words ) > 3:
			caption = " ".join(words[4:])
		else:
			caption = ""
			
		r = r + caption.replace("\'","\\'") + "'>"
		r = "<DIV CLASS='img'>" + r + "<BR>" + caption + "</DIV>\n" 
		
	elif cmd == "h1":
		out_title = " ".join(words[1:])
		#r = "<H1>" + out_title + "</H1>\n" 
		
	elif cmd == "h2":
		h2 = " ".join(words[1:])
		anchor = shofash_text_to_anchor(h2)
		r = "<A CLASS='anchor' ID='" + anchor + "'><H2>" + h2 + "</H2></A>\n" 
		
		if "sources_h2" in system_flags: # Put out previous sources?
			r = shofash_sources( sources ) + "\n" + r
			sources.clear() # Remove all list items
	
	# Process definition terms 
	elif cmd == "def":
		r = "<DT><A CLASS='anchor' ID='" + words[1].lower() + "'>" + shofash_anchor_to_text(words[1]) + "</A></DT>\n<DD>" 
		r += shofash_expandMacros( " ".join(words[2:]), skip_to_root(file_name), system_flags ) # Expand out any macros in the line
		r += "</DD>\n"
		
	elif cmd == "source":
		r = "" # Nothing to return
		sourceText = " ".join( words[2:] )
		
		if len( words ) < 2:
			sources.append("Editorial")
		else:
			if words[1] == "TEXT": # Textual source
				sources.append( sourceText )
			else: # URL
				if len( sourceText ) < 1: # No source text?
					sourceText = words[1]
				
				# 2022jan04+
				#linkString = "<A HREF='" + words[1] + "' TARGET=_BLANK TITLE='Open in new window'>" + sourceText + "</A>"
				if "links_live" in system_flags: # Allow live links if specified
					linkString = "<A HREF='" + words[1] + "' TARGET=_BLANK TITLE='Open in new window'>" + sourceText + "</A>"
				else: # default to links_dead
					linkString = sourceText
				# 2022jan04- 
				
				sources.append(linkString)
				
	elif cmd == "index_blog": # A clickable list of .html files in current directory in newest first date order
		r = shofash_index(directory, "blog","file")
		
	elif cmd == "index_alpha": # A clickable list of .html files in current directory in alphabetical
		r = shofash_index(directory, "alpha","file")

	elif cmd == "index_directory_blog": # A clickable list of directories in current directory in newest first date order
		r = shofash_index(directory, "blog","directory")

	elif cmd == "index_directory_alpha": # A clickable list of directories in current directory in newest first date order
		r = shofash_index(directory, "alpha","directory")
		
	elif cmd == "index_tree": # An index tree
		if len(words)>1 and words[1] == "blog":
			r = shofash_index_tree(directory,"blog")
		else:
			r = shofash_index_tree(directory,"alpha")

	elif cmd == "latest_changes": # A clickable list of the latest changed files
		r = shofash_latest()

	else: # Unknown command!
		print("Unknown command: " + cmd )
			
	return [r, out_title]


if __name__ == "__main__":
	# Put testing code from command line here ...
	pass
