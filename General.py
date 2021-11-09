from math import *
from random import *
import math
import random
import datetime as dt
from itertools import *
import fileOps
from fileOps import *

sequences = []
all2DVectors = []
all3DVectors = []
numGrids = []


class Wait:
	def __init__(self, duration):
		self.duration = duration


# creates an instance of a function that can be used in a sequence or as an argument in another function e.g. a button being clicked
class Func:
	def __init__(self, functionName, *args, **kwargs):
		self.func = functionName
		self.args = args
		self.kwargs = kwargs
		self.finished = False

		# used with sequences
		self.delay = 0

	def __call__(self, *args, **kwargs):
		self.finished = True
		allArgs = [args, self.args]
		allKwargs = [kwargs, self.kwargs]

		args = tuple(chain.from_iterable(allArgs))
		kwargs = tuple(chain.from_iterable(allKwargs))
		return self.func(*args, **self.kwargs)


# used to chain multiple 'Func' together
class Sequence:
	defaultTimeStep = None

	def __init__(self, *args, **kwargs):
		self.args = list(args)
		self.t = 0
		self.timeStep = Sequence.defaultTimeStep
		self.duration = 0
		self.funcs = []
		self.started = False
		self.paused = True
		self.loop = False
		self.autoDestroy = True

		for key, value in kwargs.items():
			setattr(self, key, value)

		self.Generate()
		sequences.append(self)

	def Generate(self):
		self.funcs = []

		for arg in self.args:
			if isinstance(arg, Wait):
				self.duration += arg.duration
			elif isinstance(arg, (int, float)):
				self.duration += arg

			elif isinstance(arg, Func):
				arg.delay = self.duration
				self.funcs.append(arg)

	def append(self, arg):
		self.args.append(arg)

		if isinstance(arg, Wait):
			self.duration += arg.duration
		elif isinstance(arg, (int, float)):
			self.duration += arg
		elif isinstance(arg, Func):
			arg.delay = self.duration
			self.funcs.append(arg)

	def Start(self):
		self.started = True
		for f in self.funcs:
			f.finished = False

		self.t = 0
		self.paused = False
		self.Update()

	def Pause(self):
		self.paused = True

	def Resume(self):
		self.paused = False

	def Stop(self):
		self.t = self.duration
		self.paused = False

		self.Kill()

	def Kill(self):
		if self in sequences:
			sequences.remove(self)
			del self

	def Update(self):
		if not self.started:
			return

		if self.paused:
			return

		if self.timeStep is None:
			self.t += dt.datetime.now().second
		else:
			self.t += self.timeStep

		for f in self.funcs:
			if not f.finished and f.delay <= self.t:
				f()

		if self.t >= self.duration:
			if self.loop:
				for f in self.funcs:
					f.finished = False

				self.t = 0
				return

			if self.autoDestroy:
				self.Kill()


class Vec2:
	def __init__(self, x, y, lists=[all2DVectors]):
		self.x = x
		self.y = y
		self.origin = x, y

		AddToListOrDict(lists, self)

	def ToString(self):
		return f"x:{self.x} y:{self.y}"

	def Set(self, x, y):
		self.x = x
		self.y = y

	def SetX(self, x):
		self.x = x

	def SetY(self, y):
		self.y = y

	def Copy(self):
		return Vec2(self.x, self.y)

	def Add(self, vec):
		return Vec2(self.x + vec[0], self.y + vec[1])

	def Sub(self, vec):
		return Vec2(self.x - vec[0], self.y - vec[1])

	def Multiply(self, vec):
		return Vec2(self.x * vec[0], self.y * vec[1])

	def Divide(self, vec):
		return Vec2(self.x / vec[0], self.y / vec[1])

	def IntDivide(self, vec):
		return Vec2(self.x // vec[0], self.y // vec[1])

	def Magnitude(self):
		return sqrt(self.MagnitudeSquared())

	def MagnitudeSquared(self):
		return (self.x ** 2) + (self.y ** 2)

	def Direction(self, pointOfDirection):
		# return atan(pointOfDirection[1] - self.y / pointOfDirection[0] - self.x)
		# return tan(pointOfDirection[1] - self.y / pointOfDirection[0] - self.x)
		# return (self.x / abs(self.x), self.y / abs(self.y))
		return ((pointOfDirection[0] - self.x) / abs(pointOfDirection[0]), (pointOfDirection[1] - self.y) / abs(pointOfDirection[1]))

	def Dot(self, vec):
		return self.x * vec.x + self.y * vec.y

	def Cross(self, vec):
		return Vec2(self.x * vec.x - self.y * vec.y)

	def GetEuclideanDistance(self, pos):
		return sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)

	def GetTaxicabDistance(self, pos):
		return abs(self.x - pos[0]) + abs(self.y - pos[1])

	def Normalize(self):
		return self.Multiply(Vec2(1 / self.Magnitude(), 1 / self.Magnitude()))

	def RotateRadians(self, angle, distanceToRotPoint, pointOfRot=None):
		if pointOfRot == None:
			pointOfRot = self.origin
		angle += (225 * (pi / 180))
		angle *= -1
		return round(distanceToRotPoint * cos(angle) + distanceToRotPoint * sin(angle)) + pointOfRot[0], round(-distanceToRotPoint * sin(angle) + distanceToRotPoint * cos(angle)) + pointOfRot[1]

	def RotateDegrees(self, angle, distanceToRotPoint, pointOfRot=None):
		if pointOfRot == None:
			pointOfRot = self.origin
		angle = radians(angle)
		angle += (225 * (pi / 180))
		angle *= -1
		return round(distanceToRotPoint * cos(angle) + distanceToRotPoint * sin(angle)) + pointOfRot[0], round(-distanceToRotPoint * sin(angle) + distanceToRotPoint * cos(angle)) + pointOfRot[1]


class Vec3(Vec2):
	def __init__(self, x, y, z, lists=[all3DVectors]):
		super().__init__(x, y, lists)
		self.z = z

	def ToString(self):
		return f"x:{self.x} y:{self.y} z:{self.z}"

	def Set(self, x, y):
		self.x = x
		self.y = y

	def SetX(self, x):
		self.x = x

	def SetY(self, y):
		self.y = y

	def SetZ(self, z):
		self.z = z

	def Copy(self):
		return Vec3(self.x, self.y, self.z)

	def Add(self, vec):
		return (self.x + vec[0], self.y + vec[1], self.z + vec[2])

	def Sub(self, vec):
		return (self.x - vec[0], self.y - vec[1], self.z - vec[2])

	def Multiply(self, vec):
		return (self.x * vec[0], self.y * vec[1], self.z * vec[2])

	def Divide(self, vec):
		return (self.x / vec[0], self.y / vec[1], self.z / vec[2])

	def IntDivide(self, vec):
		return (self.x // vec[0], self.y // vec[1], self.z / vec[2])

	def Magnitude(self):
		return sqrt(self.MagnitudeSquared())

	def MagnitudeSquared(self):
		return (self.x ** 2) + (self.y ** 2) + (self.z ** 2)

	def Direction(self, pointOfDirection):
		return pointOfDirection[0] - self.x, pointOfDirection[1] - self.y, pointOfDirection[2] - self.z

	def Dot(self, vec):
		return self.x * vec.x + self.y * vec.y + self.z * vec.z

	def Cross(self, vec):
		return (self.x * vec.x - self.y * vec.y - self.z * vec.z)

	def GetEuclideanDistance(self, pos):
		return sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2 + (self.z - pos[2]) ** 2)

	def GetTaxicabDistance(self, pos):
		return abs(self.x - pos[0]) + abs(self.y - pos[1]) + abs(self.z - pos[2])

	def Normalize(self):
		return self.Multiply((1 / self.Magnitude(), 1 / self.Magnitude(), 1 / self.Magnitude()))

	# quaternions
	def RotateRadians(self, angle, distanceToRotPoint, pointOfRot=None):
		pass

	def RotateDegrees(self, angle, distanceToRotPoint, pointOfRot=None):
		pass


# used to time how long a function takes to run
class Timer:
	def __init__(self):
		self.startTime = dt.datetime.now()

	def Start(self):
		self.startTime = dt.datetime.now()

	def Stop(self, log=None, extraData={}, printResult=True):
		self.endTime = dt.datetime.now()
		difference = self.endTime - self.startTime

		if printResult:
			print(f"Start time: {self.startTime}, end time: {self.endTime}, difference: {difference}")
			for key in extraData:
				print(f"{key}: {extraData[key]}")

		return (self.startTime, self.endTime, difference)

		self.LogResults(log, extraData)

	def LogResults(self, log=None, extraData={}):
		if log != None:
			try:
				with open(log, "x") as file:
					file.close()
			except:
				pass

			if ".txt" in log:
				with open(log, "a") as file:
					file.write(f"Start time: {self.startTime}\n")
					file.write(f"End time: {self.endTime}\n")
					file.write(f"Difference: {difference}\n")

					for key in extraData:
						file.write(f"{key}: {extraData[key]}\n")

					file.write("\n")
					file.close()

			elif ".json" in log:
				try:
					with open(log, "r") as file:
						data = json.load(file)

						for key in data:
							pass

						key = int(key) + 1

						file.close()

				except json.decoder.JSONDecodeError:
					data = {}
					key = 0

				data[str(key)] = {}
				data[str(key)]["startTime"] = self.startTime.strftime("%Y-%m-%d %H:%M:%S:%f")
				data[str(key)]["endTime"] = self.endTime.strftime("%Y-%m-%d %H:%M:%S:%f")
				data[str(key)]["difference"] = f"{difference.seconds}.{difference.microseconds}"

				data[str(key)]["extraData"] = extraData

				with open(log, "w") as file:
					json.dump(data, fp=file, indent=2)

					file.close()

	# arg 'function' takes a 'Func' or a 'sequence'
	def Record(self, function, log=None, extraData={}, printResult=True, *args, **kwargs):
		self.Start()

		if isinstance(function, Func):
			function(*args, **kwargs)
		elif isinstance(function, Sequence):
			function.Start()
			function.Stop()
		else:
			Func(function, *args, **kwargs)()

		return self.Stop(log=log, extraData=extraData, printResult=printResult)

	def GetAverage(self, function, numOfIterations, log=None, extraData={}, printAllResults=False, printResult=True, *args, **kwargs):
		totalDifference = 0
		startTime = dt.datetime.now()
		for i in range(numOfIterations):
			result = self.Record(function, log, extraData, printResult=printAllResults, *args, **kwargs)[2]
			difference = float(f"{result.seconds}.{result.microseconds}")
			totalDifference += difference


		endTime = dt.datetime.now()

		average = totalDifference / numOfIterations

		if printResult:
			print(f"Start time: {startTime}, end time: {endTime}, total difference: {totalDifference}, number of iterations: {numOfIterations} average: {average}")

		self.LogResults(log, extraData)

		return (startTime, endTime, average)


# 2d array of numbers
class NumGrid:
	def __init__(self, gridSize, gridFunc=None, lists=[numGrids]):
		self.gridSize = gridSize
		self.gridFunc = gridFunc
		self.CreateGrid()

		AddToListOrDict(lists, self)

	def CreateGrid(self):
		if isinstance(self.gridFunc, Func):
			self.grid = [[self.gridFunc(x, y, self.gridSize[0], self.gridSize[1]) for x in range(self.gridSize[0])] for y in range(self.gridSize[1])]
		else:
			self.grid = [[0 for x in range(self.gridSize[0])] for y in range(self.gridSize[1])]

	def PrintGrid(self, name="Unknown", printWholeGrid=False):
		print(f"Grid name: {name}, length: {len(self.grid[0])}, height: {len(self.grid)}")
		if printWholeGrid:
			for row in self.grid:
				print(row)


def Lerp(v0, v1, t):
	return v0 + t * (v1 - v0)


# add an object to a list or a dict
def AddToListOrDict(lists, obj):
	for listToAppend in lists:
		if type(listToAppend) == list:
			listToAppend.append(obj)
		elif type(listToAppend) == dict:
			try:
				if obj.name == "":
					name = len(listToAppend)
				else:
					name = obj.name

				listToAppend[name] = obj
			except:
				listToAppend[type(obj)] = obj


# return the current time with a default format
def NowFormatted(timeFormat="%d/%m/%y %H:%M:%S"):
	return dt.datetime.now().strftime(timeFormat)


if __name__ == "__main__":
	pass
