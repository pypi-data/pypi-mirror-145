# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

def shofash_write_html( filename, system, title, menu, content ):
	from .shofash_functions import skip_to_root
	
	# Replace the macros  	
	htmlOut = system				
	htmlOut = htmlOut.replace("{{{TITLE}}}",title)
	htmlOut = htmlOut.replace("{{{MENU}}}",menu)
	htmlOut = htmlOut.replace("{{{CONTENT}}}",content)
	htmlOut = htmlOut.replace("{{{ROOT}}}",skip_to_root(filename))
	
	# Finally write the file ...
	with open(filename, 'w') as file:
			print(filename)
			file.write(htmlOut)
