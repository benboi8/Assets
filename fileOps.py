# conversions of file types
# shutil
# multiple input and output for file types
# robust input systems

import os
from os import path
import json

def CheckFolderExists(folderName):
	return os.path.exists(folderName)


def CheckFileExists(folder, fileName):
	if CheckFolderExists(folder):
		return os.path.isfile(folder + fileName)
	return False


def CreateFolder(folderName):
	if not CheckFolderExists(folderName):
		os.mkdir(folderName)
		return True
	return False


def CreateFile(folder, fileName):
	if not CheckFileExists(folder, fileName):
		with open(folder + fileName, "w") as file:
			file.close()
			return True
	return False


def GetAllFoldersInFolder(folder):
	folders = []
	for root, dirs, files in os.walk(folder):
		for name in dirs:
			if root == folder:
				folders.append(name)

	return folders


def GetAllFilesInFolder(folder):
	filesInFolder = []
	for root, dirs, files in os.walk(folder):
		for name in files:
			if root == folder:
				filesInFolder.append(name)

	return filesInFolder


def Save(folder, fileName, data):
	pass


def Load(folder, fileName):
	pass


if __name__ == "__main__":
	pass
