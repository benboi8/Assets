# conversions of file types
# shutil
# multiple input and output for file types
# robust input systems

import os
from os import path
import json

def CheckFolderExists(folderName):
	return os.path.exists(folderName)


def CheckFileExists(fileName, folder="/"):
	if CheckFolderExists(folder):
		return os.path.isfile(folder + fileName)
	return False


def CreateFolder(folderName):
	if not CheckFolderExists(folderName):
		os.mkdir(folderName)
		return True
	return False


def CreateFile(fileName, folder="/"):
	if not CheckFileExists(folder, fileName):
		with open(folder + fileName, "w") as file:
			file.close()
			return True
	return False


def GetAllFoldersInFolder(folder="/"):
	folders = []
	for root, dirs, files in os.walk(folder):
		for name in dirs:
			if root == folder:
				folders.append(name)

	return folders


def GetAllFilesInFolder(folder="/"):
	filesInFolder = []
	for root, dirs, files in os.walk(folder):
		for name in files:
			if root == folder:
				filesInFolder.append(name)

	return filesInFolder


def RecursiveReadList(l, returnData=[]):
	for data in l:
		if type(data) == list:
			RecursiveReadList(data, returnData)

		elif type(data) == dict:
			RecursiveReadDict(data, returnData)

		else:
			returnData.append(data)

	return returnData


def RecursiveReadDict(d, returnData=[]):
	for key in d:
		value = d[key]
		if type(value) == dict:
			RecursiveReadDict(value, returnData)

		elif type(value) == list:
			RecursiveReadList(value, returnData)

		else:
			returnData.append((key, value))

	return returnData


def GetPath(folder, fileName, fileType):
	if fileType == "":
		if "." in fileName:
			fileType = "." + fileName.split(".")[1]
			fileName = fileName.split(".")[0]
		else:
			print(f"{folder}{fileName} has no file type. Specify a file type in the name or with the fileType variable.")
			return False

	if folder == "":
		folder = os.getcwd()
	else:
		folder = os.getcwd() + folder

	folder = folder.replace("/", "\\")
	fileName = fileName.strip("/\\")

	if "." not in fileType:
		fileType = "." + fileType

	folder += "\\"
	return f"{folder}{fileName}{fileType}", folder, fileName, fileType


def Save(fileName, data, folder="/", fileType="", fileIOType="w", createNewFolderOrFile=True):
	path, folder, fileName, fileType = GetPath(folder, fileName, fileType)

	if not CheckFolderExists(folder):
		if createNewFolderOrFile:
			CreateFolder(folder)
		else:
			print(f"No folder with name '{folder}'")
			return False

	if not CheckFileExists(fileName + fileType, folder):
		if createNewFolderOrFile:
			CreateFile(fileName + fileType, folder)
		else:
			print(f"No file with name '{fileName + fileType}'' in folder '{folder}'")
			return False


	if fileType == ".txt":
		if type(data) == list:
			writeData = RecursiveReadList(data)

		elif type(data) == dict:
			writeData = RecursiveReadDict(data)

		else:
			writeData = [data]

		with open(path, fileIOType) as file:
			for d in writeData:
				if fileIOType == "w":
					if type(d) == tuple:
						file.write(f"{d[0]}:{d[1]}\n")
					else:
						file.write(f"{d}\n")
				elif fileIOType == "a":
					if type(d) == tuple:
						file.append(f"{d[0]}:{d[1]}\n")
					else:
						file.append(f"{d}\n")

			file.close()


	if fileType == ".json":
		if type(data) == dict:
			if fileIOType == "a":
				with open(path, "r") as file:
					oldData = json.load(file)
					ile.close()

				data.update(oldData)

			with open(path, "w") as file:
				json.dump(data, file, indent=2)
				file.close()
		else:
			print("Data isn't type dict.")
			return False

	return True


def Load(fileName, folder="", fileType=""):
	path, folder, fileName, fileType = GetPath(folder, fileName, fileType)

	data = "File can't be found or is empty."

	if not CheckFolderExists(folder):
		return False

	if not CheckFileExists(fileName + fileType, folder):
		return False

	if fileType == ".txt":
		with open(path, "r") as file:
			data = file.read()

			file.close()

	if fileType == ".json":
		with open(path, "r") as file:
			data = json.load(file)

			file.close()

	return data


def JsonToTxt(data):
	return data


def TxtToJson(txt):
	return txt


if __name__ == "__main__":
	Save("file", {"one": 1, "two": 2}, folder="/saves", fileType=".json", fileIOType="w", createNewFolderOrFile=False)
	print(Load("file", "/saves", ".json"))
