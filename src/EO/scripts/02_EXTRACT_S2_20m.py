'''
Name: EXTRACT_S2_20m.py
Author: Alessio Di Lorenzo
Description:
    For each Sentinel 2 zipped archive:
        1) verify that the image is not already present in the archive of extracted data
        2) Decompress the zip file into a .SAFE folder
        3) Clean the .SAFE folder, leaving only the 20-meter bands
        4) Rename the MSK consistently with the other bands, necessary for archives after March 2018
        5) Remove the "VIS" images, present only for archives before April 2018
'''
import zipfile
from datetime import date, datetime
import os, fnmatch
from shutil import copyfile, rmtree
from GENERAL_CONFIG import download_dir, extracted_dir


# Create extraction dir if not exists
if not os.path.exists(extracted_dir):
    os.makedirs(extracted_dir)

# Create zipped files list
zipped_files = [f for f in os.listdir(download_dir)]
print( "[Num. "+str(len(zipped_files))+" files found]" )

for zipped_file in zipped_files:
	if os.path.exists(os.path.join(extracted_dir, zipped_file.replace(".zip",".SAFE"))):
		# Check if the SAFE folder for the archive exists. If found, proceed to the next zip, otherwise extract the data
		print(str(zipped_file).replace(".zip","")+" already exists")
	else:
		print("Start: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		# Copia file zippato in locale
		# *****************************************************************
		print("Copy {0} into the working dir".format(zipped_file))
		copyfile(os.path.join(download_dir, zipped_file), os.path.join(extracted_dir, zipped_file))
		# .SAFE Extraction
		# *****************************************************************
		print("Extract {0} in .SAFE".format(zipped_file))
		zip_ref = zipfile.ZipFile(os.path.join(extracted_dir,zipped_file),'r')
		zip_ref.extractall(extracted_dir)
		zip_ref.close()
		# Remove zipped file from the working dir
		# *****************************************************************
		print("Removing zipped file from the working dir")
		os.remove(os.path.join(extracted_dir, zipped_file))
		# Clean .SAFE folder
		# *****************************************************************
		print("Clean .SAFE folder")
		safe_dir = os.path.join(extracted_dir, zipped_file.replace('.zip','.SAFE'))
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if fnmatch.fnmatch(name, '*_20m.jp2'):
					copyfile(os.path.join(root,name), os.path.join(safe_dir,name))
				else:
					os.remove(os.path.join(root,name))
		# Remove empty subfolders from .SAFE folder
		# *****************************************************************
		for element in os.listdir(safe_dir):
			if element in ['AUX_DATA','DATASTRIP','GRANULE','HTML','rep_info']:
				rmtree(os.path.join(safe_dir,element))
		# *****************************************************************
		print("Rename MSK - mandatory for data from March 2018 onwards")
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if len(name) == 38:
					os.rename(os.path.join(root,name),os.path.join(root,name[4:]))
				if fnmatch.fnmatch(name, '*MSK_*'):
					substring = root[-27:-21]+"_"+root[-54:-39]+"_"
					original_name = os.path.join(root, name)
					renamed_name = os.path.join(root, str(substring)+name.replace("MSK_","").replace("PRB",""))
					os.rename(original_name,renamed_name)
		# *****************************************************************
		print("Remove 'VIS' images, existing only for data before April 2018; Add 'S2A_' or 'S2B_' prefix")
		for root, dirs, files in os.walk(safe_dir):
			for name in files:
				if fnmatch.fnmatch(name, '*_VIS_*'):
					# remove 'VIS'
					os.remove(os.path.join(root,name))
				else:
					# add 'S2A_' o 'S2B_' prefix
					original_name = os.path.join(root, name)
					prefix = os.path.basename(safe_dir)[0:3]
					prefix_name = os.path.join(root, prefix+"_"+name)
					os.rename(original_name, prefix_name)
		# *****************************************************************
		print("Fine: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 