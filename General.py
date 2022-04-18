# import os
# import sys

# os.chdir(sys.path[0])
# sys.path.insert(1, "P://Python Projects/assets/")

# from General import *

from math import *
from random import *
import math
import random
import datetime as dt
import time as t
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

		self.loopCount = 0

		for key, value in kwargs.items():
			setattr(self, key, value)

		self.Generate()
		sequences.append(self)

	def __str__(self):
		return f"duration:{self.duration}, started:{self.started}, paused:{self.paused}, looping:{self.loop}, autoDestroy:{self.autoDestroy}, timeStep:{self.timeStep}, t:{self.t}"

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

	def __call__(self):
		self.Start()

	def Start(self):
		self.started = True
		for f in self.funcs:
			f.finished = False

		self.loopCount = 0
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
		self.loopCount = 0

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
				self.loopCount += 1
				for f in self.funcs:
					f.finished = False

				self.t = 0
				return

			if self.autoDestroy:
				self.Kill()


class Vec2:
	origin = (0, 0)

	def Random(minX=-1, maxX=1, minY=-1, maxY=1):
		return Vec2(randint(minX * 1000, maxX * 1000) / 1000, randint(minY * 1000, maxY * 1000) / 1000)

	def GetAngle(p1, p2, inDegrees=False):
		p1 = Vec2(p1[0], p1[1])
		p2 = Vec2(p2[0], p2[1])
		p3 = p1 + Vec2(10, 0)
		
		mult = 1
		if p3[1] > p2[1]:
			mult = -1

		a = p1.GetEuclideanDistance(p2) ** 2 + p1.GetEuclideanDistance(p3) ** 2 - p2.GetEuclideanDistance(p3) ** 2
		b = 2 * p1.GetEuclideanDistance(p2) * p1.GetEuclideanDistance(p3)

		angle = acos(a / b) * mult

		if inDegrees:
			return degrees(angle)

		return angle

	def FromAngle(angle, inDegrees=False):
		if not inDegrees:
			return Vec2(cos(angle), sin(angle))
		else:
			return Vec2(cos(radians(angle)), sin(radians(angle)))

	def __init__(self, x, y, lists=[]):
		self.x = x
		self.y = y
		AddToListOrDict(lists, self)

	def __add__(self, vec):
		return self.Add(vec)

	def __sub__(self, vec):
		return self.Sub(vec)

	def __mul__(self, vec):
		return self.Multiply(vec)

	def __floordiv__(self, vec):
		return self.IntDivide(vec)

	def __truediv__(self, vec):
		return self.Divide(vec)

	def __iadd__(self, vec):
		if isinstance(vec, (int, float)):
			self.x += vec
			self.y += vec 
		else:
			self.x += vec[0]
			self.y += vec[1]
		
		return self

	def __isub__(self, vec):
		if isinstance(vec, (int, float)):
			self.x -= vec
			self.y -= vec
		else:
			self.x -= vec[0]
			self.y -= vec[1]
		
		return self

	def __imul__(self, vec):
		if isinstance(vec, (int, float)):
			self.x *= vec
			self.y *= vec
		else:
			self.x *= vec[0]
			self.y *= vec[1]
		
		return self
	
	def __ifloordiv__(self, vec):
		if isinstance(vec, (int, float)):
			self.x //= vec
			self.y //= vec
		else:
			self.x //= vec[0]
			self.y //= vec[1]

		return self

	def __itruediv__(self, vec):
		if isinstance(vec, (int, float)):
			self.x /= vec
			self.y /= vec
		else:
			self.x /= vec[0]
			self.y /= vec[1]

		return self

	def __imod__(self, vec):
		if isinstance(vec, (int, float)):
			self.x %= vec
			self.y %= vec
		else:
			self.x %= vec[0]
			self.y %= vec[1]
		
		return self

	def __ipow__(self, vec):
		if isinstance(vec, (int, float)):
			self.x **= vec
			self.y **= vec
		else:
			self.x **= vec[0]
			self.y **= vec[1]
		
		return self

	def __pos__(self):
		return Vec2(abs(self.x), abs(self.y))
	
	def __neg__(self):
		return Vec2(-abs(self.x), -abs(self.y))

	def __abs__(self):
		return Vec2(abs(self.x), abs(self.y))

	def __floor__(self):
		return Vec2(floor(self.x), floor(self.y))

	def __ceil__(self):
		return Vec2(ceil(self.x), ceil(self.y))
	
	def __trunc__(self):
		return Vec2(trunc(self.x), trunc(self.y))

	def __eq__(self, vec):
		if vec == None:
			return False

		return self.x == vec[0] and self.y == vec[1]

	def __ne__(self, vec):
		return self.x != vec[0] or self.y != vec[1]

	def __pow__(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x ** vec, self.y ** vec)			

		return Vec2(self.x ** vec[0], self.y ** vec[1])

	def __mod__(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x % vec, self.y % vec)

		return Vec2(self.x % vec[0], self.y % vec[1])

	def __dir__(self):
		return {"x": self.x, "y": self.y, "magnitude": self.Magnitude(), "direction": self.Direction(), "type": type(self)}

	def __str__(self):
		return f"x:{self.x} y:{self.y}"

	def __round__(self, n=1):
		return Vec2(round(self.x, n), round(self.y, n))

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		else:
			raise IndexError

	def __int__(self):
		return Vec2(int(self.x), int(self.y))

	def __float__(self):
		return Vec2(float(self.x), float(self.y))

	@property
	def mag(self):
		return self.Magnitude()

	@property
	def magSq(self):
		return self.MagnitudeSquared()

	@property
	def dir(self):
		return self.Direction()

	@property
	def direction(self):
		return self.dir

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
		if isinstance(vec, (int, float)):
			return Vec2(self.x + vec, self.y + vec)
		
		return Vec2(self.x + vec[0], self.y + vec[1])

	def Sub(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x - vec, self.y - vec)

		return Vec2(self.x - vec[0], self.y - vec[1])

	def Multiply(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x * vec, self.y * vec)

		return Vec2(self.x * vec[0], self.y * vec[1])

	def Divide(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x / vec, self.y / vec)

		return Vec2(self.x / vec[0], self.y / vec[1])

	def IntDivide(self, vec):
		if isinstance(vec, (int, float)):
			return Vec2(self.x // vec, self.y // vec)

		return Vec2(self.x // vec[0], self.y // vec[1])

	def Magnitude(self):
		return sqrt(self.MagnitudeSquared())

	def MagnitudeSquared(self):
		return (self.x ** 2) + (self.y ** 2)

	def SetMagnitude(self, mag):
		# try:
		return Vec2(self.x * (mag / self.Magnitude()), self.y * (mag / self.Magnitude()))
		# except ZeroDivisionError:
			# return self.Copy()

	def SetMag(self, mag):
		return self.SetMagnitude(mag)

	def Limit(self, maxValue):
		magSq = self.MagnitudeSquared()
		if magSq > maxValue ** 2:
			return self.Divide((sqrt(magSq), sqrt(magSq))).Multiply((maxValue, maxValue))
		return self.Copy()

	def DirectionToPoint(self, pointOfDirection):
		return ((pointOfDirection[0] - self.x) / max(0.00001, abs(pointOfDirection[0])), (pointOfDirection[1] - self.y) / max(0.00001, abs(pointOfDirection[1])))

	def Direction(self):
		try:
			d = degrees(Vec2.GetAngle(Vec2.origin, self))
			return d
		except ZeroDivisionError:
			return 0.0

	def Dot(self, vec):
		return self.x * vec.x + self.y * vec.y

	def Cross(self, vec):
		return self.x * vec.x - self.y * vec.y

	def GetEuclideanDistance(self, pos):
		return sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)

	def GetTaxicabDistance(self, pos):
		return abs(self.x - pos[0]) + abs(self.y - pos[1])

	def GetEDistance(self, pos):
		return self.GetEuclideanDistance(pos)
	
	def GetTDistance(self, pos):
		return self.GetTaxicabDistance(pos)

	def Normalize(self):
		try:
			return Vec2(self.x / self.Magnitude(), self.y / self.Magnitude())
		except ZeroDivisionError:
			return Vec2(0, 0)
	
	# depreciated 
	def RotateRadians(self, angle, distanceToRotPoint=0, pointOfRot=None):
		if pointOfRot == None:
			pointOfRot = self.Copy()

		angle += (225 * (pi / 180))
		angle *= -1
		return round(distanceToRotPoint * cos(angle) + distanceToRotPoint * sin(angle)) + pointOfRot[0], round(-distanceToRotPoint * sin(angle) + distanceToRotPoint * cos(angle)) + pointOfRot[1]

	# depreciated 
	def RotateDegrees(self, angle, distanceToRotPoint=0, pointOfRot=None):
		if pointOfRot == None:
			pointOfRot = self.Copy()

		angle = radians(angle)
		angle += (225 * (pi / 180))
		angle *= -1
		return round(distanceToRotPoint * cos(angle) + distanceToRotPoint * sin(angle)) + pointOfRot[0], round(-distanceToRotPoint * sin(angle) + distanceToRotPoint * cos(angle)) + pointOfRot[1]

	# preferred
	def Rotate(self, angle, distanceToRotPoint=0, pointOfRot=None, inDegrees=False):
		if pointOfRot == None:
			pointOfRot = self.Copy()
		else:
			if distanceToRotPoint == 0:
				distanceToRotPoint = self.GetEuclideanDistance(pointOfRot)

		if inDegrees:
			angle = radians(angle)
			angle += (255 * (pi / 180))
			angle *= -1
		
		return round(distanceToRotPoint * cos(angle) + distanceToRotPoint * sin(angle)) + pointOfRot[0], round(-distanceToRotPoint * sin(angle) + distanceToRotPoint * cos(angle)) + pointOfRot[1]

	# check
	def Heading(self, inDegrees=False):
		h = atan2(self.y, self.x)
		if inDegrees:
			return degrees(h)
		else:
			return h


class Vec3:
	origin = (0, 0, 0)

	def Random(minX=1, maxX=1, minY=-1, maxY=1, minZ=-1, maxZ=1):
		return Vec3(randint(minX * 1000, maxX * 1000) / 1000, randint(minY * 1000, maxY * 1000) / 1000, randint(minZ * 1000, maxZ * 1000) / 1000)

	def GetAngle(p1, p2, inDegrees=False):
		if inDegrees:
			return degrees(acos((p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]) / (sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2) * sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2))))
		return radians(acos((p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]) / (sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2) * sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2))))

	def __init__(self, x, y, z, lists=[]):
		self.x = x
		self.y = y
		self.z = z

		AddToListOrDict(lists, self)

	def __add__(self, vec):
		return self.Add(vec)

	def __iadd__(self, vec):
		if isinstance(vec, (int, float)):
			self.x += vec
			self.y += vec
			self.z += vec
		else:
			self.x += vec[0]
			self.y += vec[1]
			self.z += vec[2]

		return self

	def __sub__(self, vec):
		return self.Sub(vec)

	def __isub__(self, vec):
		if isinstance(vec, (int, float)):
			self.x -= vec
			self.y -= vec
			self.z -= vec
		else:
			self.x -= vec[0]
			self.y -= vec[1]
			self.z -= vec[2]

		return self

	def __mul__(self, vec):
		return self.Multiply(vec)

	def __imul__(self, vec):
		if isinstance(vec, (int, float)):
			self.x *= vec
			self.y *= vec
			self.z *= vec
		else:
			self.x *= vec[0]
			self.y *= vec[1]
			self.z *= vec[2]

		return self

	def __floordiv__(self, vec):
		return self.IntDivide(vec)

	def __ifloordiv__(self, vec):
		if isinstance(vec, (int, float)):
			self.x //= vec
			self.y //= vec
			self.z //= vec
		else:
			self.x //= vec[0]
			self.y //= vec[1]
			self.z //= vec[2]

		return self

	def __truediv__(self, vec):
		return self.Divide(vec)

	def __itruediv__(self, vec):
		if isinstance(vec, (int, float)):
			self.x /= vec
			self.y /= vec
			self.z /= vec
		else:
			self.x /= vec[0]
			self.y /= vec[1]
			self.z /= vec[2]

		return self

	def __mod__(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x % vec, self.y % vec, self.z % vec)

		return Vec3(self.x % vec[0], self.y % vec[1], self.z % vec[2])

	def __imod__(self, vec):
		if isinstance(vec, (int, float)):
			self.x %= vec
			self.y %= vec
			self.z %= vec
		else:
			self.x %= vec[0]
			self.y %= vec[1]
			self.z %= vec[2]

		return self

	def __pow__(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x ** vec, self.y ** vec, self.z ** vec)

		return Vec3(self.x ** vec[0], self.y ** vec[1], self.z ** vec[2])

	def __ipow__(self, vec):
		if isinstance(vec, (int, float)):
			self.x **= vec
			self.y **= vec
			self.z **= vec
		else:
			self.x **= vec[0]
			self.y **= vec[1]
			self.z **= vec[2]

		return self

	def __pos__(self):
		return Vec3(+self.x, +self.y, +self.z)

	def __neg__(self):
		return Vec3(-self.x, -self.y, -self.z)

	def __abs__(self):
		return Vec3(abs(self.x), abs(self.y), abs(self.z))

	def __floor__(self):
		return Vec3(floor(self.x), floor(self.y), floor(self.z))

	def __ceil__(self):
		return Vec3(ceil(self.x), ceil(self.y), ceil(self.z))

	def __trunc__(self):
		return Vec3(trunc(self.x), trunc(self.y), trunc(self.z))

	def __eq__(self, vec):
		return self.x == vec[0] and self.y == vec[1] and self.z == vec[2]

	def __ne__(self, vec):
		return self.x != vec[0] or self.y != vec[1] or self.z != vec[2]

	def __dir__(self):
		return {"x": self.x, "y": self.y, "z": self.z, "magnitude": self.Magnitude(), "direction": self.Direction(), "type": type(self)}

	def __str__(self):
		return f"x:{self.x} y:{self.y} z:{self.z}"

	def __round__(self, n=1):
		return Vec3(round(self.x, n), round(self.y, n), round(self.z, n))

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		elif i == 2:
			return self.z
		else:
			raise IndexError

	def __int__(self):
		return Vec3(int(self.x), int(self.y), int(self.z))

	def __float__(self):
		return Vec3(float(self.x), float(self.y), float(self.z))

	@property
	def mag(self):
		return self.Magnitude()

	@property
	def magSq(self):
		return self.MagnitudeSquared()

	@property
	def dir(self):
		return self.Direction()

	@property
	def direction(self):
		return self.dir

	def Set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def SetX(self, x):
		self.x = x

	def SetY(self, y):
		self.y = y

	def SetZ(self, z):
		self.z = z

	def Copy(self):
		return Vec3(self.x, self.y, self.z)

	def Add(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x + vec, self.y + vec, self.z + vec)

		return Vec3(self.x + vec[0], self.y + vec[1], self.z + vec[2])

	def Sub(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x - vec, self.y - vec, self.z - vec)

		return Vec3(self.x - vec[0], self.y - vec[1], self.z - vec[2])

	def Multiply(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x * vec, self.y * vec, self.z * vec)

		return Vec3(self.x * vec[0], self.y * vec[1], self.z * vec[2])

	def Divide(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x / vec, self.y / vec, self.z / vec)

		return Vec3(self.x / vec[0], self.y / vec[1], self.z / vec[2])

	def IntDivide(self, vec):
		if isinstance(vec, (int, float)):
			return Vec3(self.x // vec, self.y // vec, self.z // vec)

		return Vec3(self.x // vec[0], self.y // vec[1], self.z // vec[2])

	def Magnitude(self):
		return sqrt(self.MagnitudeSquared())

	def MagnitudeSquared(self):
		return (self.x ** 2) + (self.y ** 2) + (self.z ** 2)

	def SetMagnitude(self):
		try:
			return Vec3(self.x * mag / self.Magnitude(), self.y * mag / self.Magnitude(), self.z * mag / self.Magnitude())
		except:
			return self.Copy()

	def Limit(self, maxValue):
		magSq = self.MagnitudeSquared()
		if magSq > maxValue ** 2:
			return self.Divide((sqrt(magSq), sqrt(magSq), sqrt(magSq))).Multiply((maxValue, maxValue, maxValue))
		return self.Copy()

	def DirectionToPoint(self, pointOfDirection):
		return ((pointOfDirection[0] - self.x) / max(0.00001, abs(pointOfDirection[0])), (pointOfDirection[1] - self.y) / max(0.00001, abs(pointOfDirection[1])), (pointOfDirection[2] - self.z) / max(0.00001, abs(pointOfDirection[2])))

	def Direction(self):
		try:
			d = Vec3.GetAngle(Vec3.origin, self, inDegrees=True)
			return d
		except ZeroDivisionError:
			return 0.0

	def Dot(self, vec):
		return self.x * vec[0] + self.y * vec[1] + self.z * vec[2]

	def Cross(self, vec):
		return self.x * vec[0] - self.y * vec[1] - self.z * vec[2]

	def GetEuclideanDistance(self, pos):
		return sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2 + (self.z - pos[2]) ** 2)

	def GetTaxicabDistance(self, pos):
		return abs(self.x - pos[0]) + abs(self.y - pos[1]) + abs(self.z - pos[2])

	def Normalize(self):
		try:
			return Vec3(self.x / self.Magnitude(), self.y / self.Magnitude(), self.z / self.Magnitude())
		except ZeroDivisionError:
			return self.Copy()

	# https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
	# add axis 
	def Rotate(self, angle, distanceToRotPoint=0, pointOfRot=None, inDegrees=False):
		pass



# used to time how long a function takes to run
class Timer:
	def __init__(self):
		self.Start()

	def Start(self):
		self.startTime = dt.datetime.now()

	def GetDiff(self):
		return dt.datetime.now() - self.startTime

	def Stop(self, log=None, extraData={}, printResult=True):
		self.endTime = dt.datetime.now()
		difference = self.GetDiff()

		if printResult:
			print(f"Start time: {self.startTime}, end time: {self.endTime}, difference: {difference}")
			for key in extraData:
				print(f"{key}: {extraData[key]}")

		self.LogResults(log, extraData)
		
		return self.startTime, self.endTime, difference

	def LogResults(self, log=None, extraData={}):
		difference = self.GetDiff()
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


def Lerp(v0, v1, t):
	return v0 + t * (v1 - v0)


# add an object to a list or a dict
def AddToListOrDict(lists, obj, key=None):
	if type(lists) == list:
		for listToAppend in lists:
			if type(listToAppend) == list:
				listToAppend.append(obj)
			elif type(listToAppend) == dict:
				try:
					if key == None:
						if obj.name == "":
							name = len(listToAppend)
						else:
							name = obj.name
					else:
						name = key

					listToAppend[name] = obj
				except:
					listToAppend[type(obj)] = obj


# return the current time with a default format
def NowFormatted(timeFormat="%d/%m/%y %H:%M:%S"):
	return dt.datetime.now().strftime(timeFormat)


# return angle between 3 points
def GetAngle(p1, p2, p3):
	if isinstance(p1, (tuple, list)):
		p1 = Vec2(p1[0], p1[1])
	if isinstance(p1, dict):
		p1 = Vec2(p1["x"], p1["y"])
	
	if isinstance(p2, (tuple, list)):
		p2 = Vec2(p2[0], p2[1])
	if isinstance(p2, dict):
		p2 = Vec2(p2["x"], p2["y"])
	
	if isinstance(p3, (tuple, list)):
		p3 = Vec2(p3[0], p3[1])
	if isinstance(p3, dict):
		p3 = Vec2(p3["x"], p3["y"])

	mult = 1
	if p3.y > p2.y:
		mult = -1
	return (acos((p1.GetEuclideanDistance((p2.x, p2.y)) ** 2 + p1.GetEuclideanDistance((p3.x, p3.y)) ** 2 - p2.GetEuclideanDistance((p3.x, p3.y)) ** 2) / (2 * p1.GetEuclideanDistance((p2.x, p2.y)) * p1.GetEuclideanDistance((p3.x, p3.y))))) * mult


def Constrain(v, mini, maxi):
	return max(mini, min(maxi, v))


# different to python 'map'
def Map(value, start1, stop1, start2, stop2, withinBounds=True):
	newVal = (value - start1) / (stop1 - start1) * (stop2 - start2) + start2

	if not withinBounds:
		return newVal

	if start2 < stop2:
		return Constrain(newVal, start2, stop2)
	else:
		return Constrain(newVal, stop2, start2)


if __name__ == "__main__":
	n = 0.31
	print(Map(n, 0, 1, 5, 20))
