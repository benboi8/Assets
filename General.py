from math import *
from random import *
import datetime as dt
from itertools import *
import fileOps

sequences = []


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
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.length = None
		self.direction = None

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
		try:
			if type(self) == Vec2:
				return Vec2(self.x, self.y)
			elif type(self) == Vec3:
				return Vec3(self.x, self.y, self.z)
		except AttributeError:
			print("AttributeError")

	def Add(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x + vec.x, self.y + vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x + vec.x, self.y + vec.y, self.z + vec.z)
		except AttributeError:
			print("AttributeError")

	def Sub(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x - vec.x, self.y - vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x - vec.x, self.y - vec.y, self.z - vec.z)
		except AttributeError:
			print("AttributeError")

	def Multiply(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x * vec.x, self.y * vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x * vec.x, self.y * vec.y, self.z * vec.z)
		except AttributeError:
			print("AttributeError")

	def Divide(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x / vec.x, self.y / vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x / vec.x, self.y / vec.y, self.z / vec.z)
		except AttributeError:
			print("AttributeError")

	def IntDivide(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x // vec.x, self.y // vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x // vec.x, self.y // vec.y, self.z // vec.z)
		except AttributeError:
			print("AttributeError")

	def Magnitude(self):
		return sqrt(self.MagnitudeSquared())

	def MagnitudeSquared(self):
		try:
			if type(self) == Vec2:
				return self.x * self.x + self.y * self.y
			elif type(self) == Vec3:
				return self.x * self.x + self.y * self.y + self.z * self.z
		except AttributeError:
			print("AttributeError")

	def Dot(self, vec):
		try:
			if type(self) == Vec2:
				return self.x * vec.x + self.y * vec.y
			elif type(self) == Vec3:
				return self.x * vec.x + self.y * vec.y + self.z * vec.z
		except AttributeError:
			print("AttributeError")

	def Cross(self, vec):
		try:
			if type(self) == Vec2:
				return Vec2(self.x * vec.x - self.y * vec.y)
			elif type(self) == Vec3:
				return Vec3(self.x * vec.x - self.y * vec.y - self.z * vec.z)
		except AttributeError:
			print("AttributeError")

	def GetEuclideanDistance(self, vec):
		try:
			if type(self) == Vec2:
				return sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2)
			elif type(self) == Vec3:
				return sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2, (self.z - vec.z) ** 2)
		except AttributeError:
			print("AttributeError")

	def GetTaxicabDistance(self, vec):
		try:
			if type(self) == Vec2:
				return abs(self.x - vec.x) + abs(self.y - vec.y)
			elif type(self) == Vec3:
				return abs(self.x - vec.x) + abs(self.y - vec.y) + abs(self.z - vec.z)
		except AttributeError:
			print("AttributeError")

	def Normalize(self):
		length = self.Magnitude()
		if length != 0:
			try:
				if type(self) == Vec2:
					return self.Multiply(Vec2(1 / length, 1 / length))
				elif type(self) == Vec3:
					return self.Multiply(Vec3(1 / length, 1 / length, 1 / length))
			except AttributeError:
				print("AttributeError")

	def RotateRadians(self, angle):
		return (round(self.x * cos(angle) + self.y * sin(angle)), round(-self.x * sin(angle) + self.y * cos(angle)))

	def RotateDegrees(self, angle):
		angle = radians(angle)
		return (round(self.x * cos(angle) + self.y * sin(angle)), round(-self.x * sin(angle) + self.y * cos(angle)))


class Vec3(Vec2):
	def __init__(self, x, y, z):
		super().__init__(x, y)
		self.z = z

	def SetZ(self, z):
		self.z = z

	def ToString(self):
		return f"x:{self.x} y:{self.y} z:{self.z}"


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


class NumGrid:
	def __init__(self, gridSize, gridFunc=None):
		self.gridSize = gridSize
		self.gridFunc = gridFunc
		self.CreateGrid()

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


if __name__ == "__main__":
	def Main():
		timer = Timer()

		wait = Wait(0)


		print("------- Func test -------")
		f = Func(print, "one", "two")
		f()

		print("\n------- sequence test -------")
		s = Sequence(1, Func(print, "one"), 5, Func(print, "two", "three"))

		s.Start()

		print("\n------- timer test -------")
		def LargeLoop():
			x = 0
			for i in range(200):
				for j in range(1000):
					x += j * i
					if j == i:
						x *= j ** i
			return x
		timer.GetAverage(Func(LargeLoop), 10, printAllResults=False)

		v1 = Vec2(10, 4)
		v2 = Vec3(5, 20, 6)

		def GridConditions(x, y, xLen, yLen):
			if x == 0:
				return 1
			if x == xLen - 1:
				return 1

			if y == 0:
				return 1
			if y == yLen - 1:
				return 1

			return 0

		print("\n------- num grid test -------")
		grid = NumGrid((5, 3), Func(GridConditions)).PrintGrid("grid")

	v1 = Vec2(10, 4)
	v2 = v1.RotateRadians(3.14)
	v3 = v1.RotateDegrees(180)

	print((v1.x, v1.y), v2, v3)

	# Main()
