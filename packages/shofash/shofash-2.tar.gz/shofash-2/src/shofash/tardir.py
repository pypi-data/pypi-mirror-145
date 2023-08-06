# Copyright 2022 Frazer Melton                                                                                                       
#
# This file is part of shofash.
#
# shofash is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# shofash is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with shofash. If not, see <https://www.gnu.org/licenses/>. 

def tardir(path, tar_name, ftime, doAll,tfc):
	import os, sys, datetime,tarfile

	with tarfile.open(tar_name, "w:gz") as tar_handle:
		for root, dirs, files in os.walk(path):
			for file in files:
				fname = os.path.join(root,file)
				# See if is in list of files to store
				name_parts = file.split(".")
				ext = name_parts[-1] # Get last item ie extension
				if ext in ("html","css","png","jpg","jpeg"):
					if os.path.getmtime(fname) > ftime or doAll:
						print(os.path.join(root, file))
						tfc.write(os.path.join(root, file) + "\n")
						aname = os.path.join(root,file)
						aname = aname[ len(path) + 1 :] # Trim off path variable
						tar_handle.add(fname, arcname=aname)
				#else:
				#	print("Skipping: " + os.path.join(root, file))
					
		tar_handle.close()
