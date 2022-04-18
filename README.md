General:

- Wait:
	Used with Sequences to add a delay to a function call

	self.duration = duration
  

- Func:
	Used as a container for function calls, can have any number of arguments.

	self.func = function_name
	self.args = args
	self.kwargs = kwargs

	# used with Sequences
	self.finished = False
	self.delay = 0

	E.G:
	In : Func(print, "Hello World")()
	Out: Hello World

	In : example_func = Func(print, "Hello World")
		   example_func()
	Out: Hello World


- Sequence:
	Used to chain multiple functions together into a single process.

	Sequence.defaultTimeStep = None

	self.args = list(args)
	self.t = 0
	self.timeStep = Sequence.defaultTimeStep
	self.duration = 0
	self.funcs = []
	self.started = False
	self.paused = true
	self.loop = False
	self.autoDestroy = True
	self.loopCount = 0

	self.Generate() # adds all functions and waits to the list of functions, 'self.func'
	self.append(arg) # adds an argument to the list of arguments, if the argument is a function or Wait then it will be added to self.func
	self.Start() # starts the sequence
	self.Pause() # pauses the sequence
	self.Stop() # stops the sequence
	self.Kill() # removes the sequence
	self.Update() # checks for sequence start, pause, stop, increments self.t by self.timeStep, increments self.loopCount by 1 for each loop it completes, destroys its self if self.autoDestroy is True


	E.G:
	In : Sequence(Wait(1), Func(print, "Hello World"), 2, Func(print, "Delayed")).Start()
	Out: Hello World
		   Delayed

	In : example_sequence = Sequence(Wait(1), Func(print, "Hello World"), 2, Func(print, "Delayed"))
		   example_sequence()
	Out: Hello World
		   Delayed


- Vec2
	A 2D vector, which can be used like a list of two numbers

	Vec2.origin = (0, 0)

	self.x = x
	self.y = y

	Vec2.Random(minX=-1, maxX=1, minY=-1, maxY=1) # returns a random vector within the bounds of minX, maxX and minY, maxY
	Vec2.GetAngle(p1, p2, inDegrees=False) # returns the angle between two points, p1 and p2 can be any sub-scriptable data type, if inDegrees is True the angle will be returned in degrees otherwise it will be in radians
	Vec2.FromAngle(angle, inDegrees=False) # returns a new vector from an angle inDegrees specifies if the angle is in radians or degrees

	operations:
	addition
	subtraction
	multiplication
	floor division
	true division
	exponent
	floor
	ceil
	trunc
	equal
	not equal
	modulus
	round
	int
	float
	dot product
	cross product
	
  incremental addition
	incremental subtraction
	incremental multiplication
	incremental floor division
	incremental true division
	incremental exponent
	incremental modulus

	@properties
	mag # returns the magnitude of the vector
	magSq # returns the square of the magnitude
	dir # returns the direction of the vector
	direction # returns the direction of the vector

	self.Set(x, y) # set x and y
	self.SetX(x) # set x
	self.SetY(y) # set y
	self.Copy() # return a copy of the vector
	self.SetMag(mag) # return a vector with the magnitude specified
	self.Limit(maxValue) # returns a vector with the magnitude limited to the maxValue
	self.DirectionToPoint(pointOfDirection) # returns the direction the point
	self.GetEDistance(pos) # get Euclidean distance between the vector and pos
	self.GetTDistance(pos) # get 'Taxicab' distance between the vector and pos
	self.Normalize() # returns a normalized vector
	self.Rotate(angle, distanceToRotPoint=0, pointOfRot=None, inDegrees=False) # returns a vector which has been rotated by the specified angle, inDegrees specifies if the angle being passed is in degrees (True) or radians (False), distanceToRotPoint is the distance to a rotation point, pointOfRot is the rotation pivot point the default is a copy of the current vector
	self.Heading(inDegrees=False) # return the heading of a vector, if inDegrees is True then the heading returned will be in degrees other wise it will be in radians

	E.G:
	In : v1 = Vec2(0.15, 5.3)
		   v1 = floor(v1)
		   v2 = Vec2(1, 1.5)
	 	   v3 = (v1 + v2) * v2
		   print(v3)

	Out: x:1 y:9.75

	In : print(Vec2.FromAngle(52))

	Out: x:-0.16299078079570548 y:0.9866275920404853


- Vec3
	Same as Vec2 but with x, y, z

	- no rotation methods yet

	- Timer:
	Times how long a function takes to finish
	Starts timing on creation
	Can not get a difference smaller than one microsecond
	may be a few microseconds inaccurate

	self.Start() # set the start time
	self.GetDiff() # return the difference between the start and the current time
	self.Stop(log=None, extraData={}, printResult=True) # stop the timer, log is a file name string, extraData is dictionary which is written to the log, if printResult is True then the start time, end time and difference is printed, returns start time, end time, difference
	self.LogResults(log=None, extraData={}) # logs the result using log as a file name and extraData as a dictionary of things to write to the file the file type can be either json or txt
	self.Record(function, log=None, extraData={}, printResult=True, *args, **kwargs) # can be used to record a function directly by passing in the function as a Sequence or function name, returns start time, end time, difference
	self.GetAverage(function, numOfIterations, log=None, extraData={}, printAllResults=False, printResult=True, *args, **kwargs) # Gets the average time taken to complete a function


	E.G:
	In : def A(a):
			total = 0
			for i, rows in enumerate(a):
				for j, value in enumerate(rows):
					total += sqrt(value)
		  t = Timer()
		  t.GetAverage(A, 100, None, {}, False, True, a=[[(i ** j) for i in range(100)] for j in range(100)])

	Out: Start time: 2022-04-18 11:34:54.631094, end time: 2022-04-18 11:34:54.794667, total difference: 47.77269999999999, number of iterations: 100 average:  0.47772699999999996


- Lerp(v0, v1, t) # Linear interpolation between two numbers, v0, v1, t is a number to represent time, 0 is equal to v0 and 1 is equal to v1
	In : print(Lerp(0, 15, 0.5))
	Out: 7.5


- AddToListOrDict(lists, obj, key=None):
	lists is a list of references to lists or dicts
	obj is the thing being added to each list or dict in lists
	key is the key used for a dict if it is none then it will attempt to used a name value if the obj doesn't have a name it will use to type


- NowFormatted(timeFormat="%d/%m/%y %H:%M:%S")
	returns the current time with the format of timeFormat
	In : print(NowFormatted())
	Out: 18/04/22 11:41:47


- Constrain(v, mini, maxi):
	constrain v to a value between mini and maxi
	equivalent to writing 'max(mini, min(maxi, v))'

	In : print(Constrain(5.5, 0, 1))
	Out: 1


- Map(value, start1, stop1, start2, stop2)
	maps one range of values to another range of values

	In : n = 0.5
	  	 print(Map(n, 0, 1, 0, 10))

	Out: 5.0

	In : n = 0.31
		   print(Map(n, 0, 1, 5, 20))

	Out: 9.65
