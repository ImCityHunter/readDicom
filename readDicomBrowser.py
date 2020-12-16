import pydicom
import os
from datetime import datetime
import os.path
from os import path
import shutil
import string
import Tkinter
import tkFileDialog
import tkMessageBox

arr = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ] #used to number of people in each age group, [ 10, 20 , 30 , ... 80]
unavaliable = 0

def _findAgeGroup(age_str):
	age = int(filter(str.isdigit, age_str))
	if(age>10 and age<=20):		
		return 10
	elif (age>20 and age<=30):
		return 20
	elif (age>30 and age<=40):
		return 30
	elif (age>40 and age<=50):
		return 40
	elif (age>50 and age<=60):
		return 50
	elif (age>60 and age<=70):
		return 60
	elif (age>70 and age<=80):
		return 70
	elif (age>80):
		return 80
	else:
		_incrementBadData()
		return -1

def _countAgeGroup(age):
	if (age == 10):
		_increment(0)
	elif (age == 20):
		_increment(1)
	elif (age == 30):
		_increment(2)
	elif (age == 40):
		_increment(3)
	elif (age == 50):
		_increment(4)
	elif (age == 60):
		_increment(5)				
	elif (age == 70):
		_increment(6)
	elif (age == 80):
		_increment(7)		
	else:
		return -1

def _increment(index):
	global arr
	arr[index] += 1

def _incrementBadData():
	global unavaliable
	unavaliable += 1

def _storeTheFile(jpeg_file, dcm_file, age_group, name, src_path, dest_path):
	age_path = os.path.join(dest_path, str(age_group)) # create age folder 
	if not os.path.exists(age_path):
		os.makedirs(age_path)

	store_path = os.path.join(age_path, name) # create name folder
	if not os.path.exists(store_path):
		_countAgeGroup(age_group) # count age group
		os.makedirs(store_path)
	
	# copy and paste file
	if(path.isfile(jpeg_file) and path.isfile(dcm_file)):
		shutil.copy2(jpeg_file, store_path)
		shutil.copy2(dcm_file, store_path)

def _validFile (dataset, jpeg_file, dcm_file):
	return ("PatientAge" in dataset and "PatientName" in dataset and path.isfile(jpeg_file) and path.isfile(dcm_file))

def _readFiles (src_path, dest_path):
	# traverse root directory, and list directories as dirs and files as files
	for currentpath, folders, files in os.walk(src_path):
	    for file in files:
	        # make action only for DCM file
	        if file.endswith(".dcm"):
	        	dcm_file = os.path.join(currentpath, file)
	        	dataset = pydicom.dcmread(dcm_file)
	        	root, ext = os.path.splitext(dcm_file) # seperate path + '.ext'
	        	jpeg_file = root+'.jpg' # path to current location
	        	if (_validFile(dataset, jpeg_file, dcm_file)):
		        	age = dataset.PatientAge # example
		        	name = dataset.PatientName # get patient name
		        	age_group = _findAgeGroup(age)
		        	_storeTheFile(jpeg_file, dcm_file, age_group, name, src_path, dest_path)
		        elif (path.isfile(jpeg_file) and path.isfile(dcm_file)):
		        	_incrementBadData()

def _getPath():
	root = Tkinter.Tk()
	root.withdraw() #use to hide tkinter window
	currdir = os.getcwd()
	tempdir = tkFileDialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
	if len(tempdir) > 0:
		print "You chose %s" % tempdir
		return tempdir
	else:
		print("Choose Path fail")
		exit()

def main():
	'''
	Function: main
	Summary: 

	Recursively read the files from src_path and find all the dcm files,
	find the age group, and relocate the dcm and its jpg to a destinated folder
	'''
	tkMessageBox.showinfo(title="Message", message="Choose DCM folder")
	src_path = _getPath()
	tkMessageBox.showinfo(title="Message", message="Choose Destination folder")
	dest_path = _getPath()
	global arr
	_readFiles(src_path, dest_path)

	age = 10
	total = 0
	for i in arr:
		print("%d has: %d " %(age,i))
		total += i
		age += 10
	print("total valid is %d " %total)
	print("invalid file is %d " %unavaliable)

if __name__ == "__main__":
    main()