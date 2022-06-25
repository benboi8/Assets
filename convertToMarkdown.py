import os

fileName = "GUI.py"

markDown = ""

readingInstanceVars = False
cls_name = ""
readClsName = False
readingMethods = False
readingClassMethods = False
readingClassVars = False

with open(fileName, "r") as file:

	for line in file.readlines():
		if len(line) > 1:
			line = line.strip("\n")
			if "#" not in line and "import" not in line:
				if "class" in line:
					cls_name = line[len("class"):-1]
					if "(" in cls_name:
						cls_name = line[len("class"):line.find("(")]
					markDown += f"\n#{cls_name}\n\n> CLASS_DESCRIPTION_HERE\n"
					readClsName = True
					readingMethods = False	
					readingClassMethods = False
					readingInstanceVars = False
					readingClassVars = False

				if readClsName and not readingInstanceVars and not readingMethods and "__init__" not in line:
					if "def " in line:
						if not readingClassMethods:
							markDown += f"\n## Class Methods\n"
							readingClassMethods = True

						l = line.strip(" 	")
						l = l[4:-1]
						
						arg = f"({line[line.find('(') + 1:line.find(')')]})"
						n = arg if arg != "()" else ""
						markDown += f"### {cls_name.strip(' ')}.{l[:line.find('(') - 5]}\n{n}\n> METHOD_DESCRIPTION_HERE\n"

					if " = " in line and line.count("	") == 1:
						if not readingClassVars:
							markDown += f"\n## Class Variables\n"
							readingClassVars = True

						l = line.strip(" 	")
						markDown += f"	{cls_name.strip(' ')}.{l}\n"


				if "__init__" in line and "super" not in line:
					if ", " in line:
						if not readingInstanceVars:
							markDown += "\n## \\_\\_init\\_\\_\n"

						t = "REPLACE_WITH_TYPE"
						nl = f" : {t}\n    "
						line = line.replace("*", "")
						
						markDown += f"    {line[len('	def __init__(self, '): - 2].replace(', ', nl)} : {t}\n\n## Instance Variables\n"
					readingInstanceVars = True
				
				elif "	def " in line:
					if "self" in line:
						if readingInstanceVars:
							markDown += f"\n## Methods\n"
							readingInstanceVars = False
							readingMethods = True
						
						uscore = "\_"
						arg = f"({line[line.find('(') + 7:line.find(')')]})"
						n = arg if arg != "()" else ""
						markDown += f"### self.{line.strip('	')[len('def '):line.find('(') - 1].replace('_', uscore)}\n {n}\n> METHOD_DESCRIPTION_HERE\n"

				if "self." in line and "=" in line and readingInstanceVars:
					markDown += f"	{line.strip('	')}\n"

				if "def " in line and "self" not in line and "	" not in line:
					nl = "\n> "
					markDown += f"\n\n# {line[4:line.find('(')]}\n	({line[line.find('(') + 1: - 2]})\n> {line[line.find('(') + 1: - 2].replace(', ', nl)}"


file.close()

with open("README.md", "w") as file:
	file.write(markDown)
	file.close()