# import os
# import sys

# os.chdir(sys.path[0])
# sys.path.insert(1, "P://Python Projects/assets/")

# from GameObjects import *


from GUI import *

allImages = []


class Image(Box):
	def __init__(self, rect, imagePath, name="", surface=screen, lists=[allImages]):
		super().__init__(rect, ((0, 0, 0), (0, 0, 0)), name, surface, drawData={"drawBackground": False}, lists=lists)

		self.imagePath = imagePath

		self.resize = False

		self.ScaleImage(pg.image.load(self.imagePath) if self.imagePath != None else None, (self.rect.w, self.rect.h))

	def Draw(self):
		if self.image != None:
			self.surface.blit(self.image, self.rect)

	def ScaleImage(self, image, size):
		if image != None:
			self.image = pg.transform.scale(pg.image.load(self.imagePath), size)
		else:
			self.image = None

	def Replace(self, colorA, colorB):

		pixelArray = pg.PixelArray(self.image)
		pixelArray.replace(colorA, colorB)

		self.image = pixelArray.make_surface().convert_alpha()

	def SetImage(self, imagePath):
		self.imagePath = imagePath
		self.ScaleImage(pg.image.load(self.imagePath) if self.imagePath != None else None, (self.rect.w, self.rect.h))


class Cell:
	def __init__(self, pos, size, color=red):
		self.x, self.y = pos[0], pos[1]
		self.size = size
		self.color = color


# map / world
class World:
	def __init__(self, rect, size, cellData={}):
		self.rect = pg.Rect(rect)
		self.size = size

		self.cellData = cellData
		self.CreateGrid()

	def CreateGrid(self):
		self.grid = [[self.cellData.get("cell", Cell)(self.GetPosFromIndex(x, y), self.size, data=self.cellData) for x in range(self.rect.w // self.size)] for y in range(self.rect.h // self.size)]

	def Draw(self):
		DrawRectOutline(black, (self.rect.x - 1, self.rect.y - 1, self.rect.w - (self.rect.w % self.size) + 2, self.rect.h - (self.rect.h % self.size) + 2))

	def GetPosFromIndex(self, i, j):
		return self.rect.x + (i * self.size), self.rect.y + (j * self.size)

	def GetIndexFromPos(self, x, y):
		return (x - self.rect.x) // self.size, (y - self.rect.y) // self.size

	def CheckIfPosInBounds(self, x, y):
		return self.rect.x <= x < (self.rect.x + self.rect.w) - (self.rect.w % self.size) and self.rect.y <= y < (self.rect.y + self.rect.h) - (self.rect.h % self.size)


# camera

class CameraBase:
	w, h = width, height
	rect = pg.Rect(0, 0, w, h)
	defaultPos = (rect.x, rect.y)

	def Draw():
		DrawRectOutline(black, CameraBase.rect)

	def ChangePos(x, y):
		CameraBase.rect = pg.Rect(x, y, CameraBase.rect.x, CameraBase.rect.h)
		CameraBase.defaultPos = (CameraBase.rect.x, CameraBase.rect.y)

	def ChangeSize(w, h):
		CameraBase.rect = pg.Rect(CameraBase.rect.x, CameraBase.rect.y, w, h)


# entity




# player controller
# P:\Python Projects\2d platformer

# tiles
# P:\Python Projects\2d platformer

# interactive tiles

# specialized tiles
# - door
# - storage
# - npc

# physics engine
# P:\Python Projects\gravity sim

# input handler

# time manager

# sound manager
# P:\Python Projects\2d platformer
# P:\Python Projects\mp3 player


# animator 
class Animation:
	allAnimations = []

	def SetColor(surface, colors):
		# easier to crate different images with different colors instead
		for color_pairs in colors:
			colorA, colorB = color_pairs

			pixelArray = pg.PixelArray(surface)
			pixelArray.replace(colorA, colorB)

			surface = pixelArray.make_surface().convert_alpha()

		return surface

	def __init__(self, rect, filePath, numOfFrames, fps=12, loop=False, autoPlay=False, reversable=False):
		self.rect = pg.Rect(rect)

		self.filePath = filePath

		self.numOfFrames = numOfFrames
		self.LoadImg()

		self.fps = fps
		self.loop = loop
		self.autoPlay = autoPlay

		self.reversable = reversable
		self.reversed = False

		self.updateFrame = Sequence(loop=True, autoDestroy=False, duration=self.numOfFrames, timeStep=(self.numOfFrames / FPS) * self.fps)

		self.updateFrame.append(Func(self.IncrementFrame))

		self.startFunc = None
		self.stopFunc = None

		Animation.allAnimations.append(self)

		self.shouldDraw = True

		if self.autoPlay:
			self.updateFrame.Start()

	def LoadImg(self, img=None):
		self.fullImg = None
		self.frames = []
		self.currentFrame = None
		if isinstance(self.filePath, (Image, pg.Surface)):
			self.fullImg = self.filePath
		else:
			if CheckFileExists(self.filePath):
				if img == None:
					self.fullImg = pg.image.load(self.filePath)
				else:
					self.fullImg = img

		if self.fullImg != None:
			img_width, img_height = self.fullImg.get_width(), self.fullImg.get_height()

			y = 0
			frameHeight = img_height // self.numOfFrames

			self.frames = [pg.transform.scale(self.fullImg.subsurface((0, y + (i * frameHeight), img_width, frameHeight)), (self.rect.w, self.rect.h)) for i in range(img_height // frameHeight)]
			self.currentFrame = 0

	def Draw(self):
		if self.shouldDraw:
			if self.fullImg != None:
				screen.blit(self.frames[self.currentFrame], self.rect)
				self.updateFrame.timeStep = (self.updateFrame.duration / clock.get_fps()) * self.fps if clock.get_fps() != 0 else 0
				
				self.updateFrame.Update()

				if not self.loop:
					if self.updateFrame.loopCount >= self.numOfFrames:
						self.Stop()

	def IncrementFrame(self):
		if self.shouldDraw:
			if self.reversed:
				self.currentFrame -= 1
				
				if self.currentFrame < 0:
					self.reversed = False
					self.currentFrame = 0			

			else:
				self.currentFrame += 1

				if self.currentFrame >= len(self.frames):
					if self.reversable:
						self.reversed = True
						self.currentFrame = len(self.frames) - 1
					else:
						self.currentFrame = 0

	def Start(self):
		self.updateFrame.Start()
		if self.startFunc != None:
			if isinstance(self.startFunc, Sequence):
				self.startFunc.Start()
			else:
				self.startFunc()

	def Stop(self):
		self.updateFrame.Stop()
		if self.stopFunc != None:
			if isinstance(self.stopFunc, Sequence):
				self.stopFunc.Start()
			else:
				self.stopFunc()

	def Show(self):
		self.shouldDraw = True

	def Hide(self):
		self.shouldDraw = False

	# expensive
	def ChangeColor(self, colors):
		self.fullImg = Animation.SetColor(self.fullImg, colors)
		self.LoadImg(self.fullImg)



class Animator:
	allAnimators = []

	def __init__(self, animations={}, active=[]):
		self.animations = {}

		for key in animations:
			self.append(key, animations[key])

		self.activeAnimations = []

		for key in active:
			if key in self.animations:
				self.activeAnimations.append(self.animations[key])

		self.previousAnimation = None

		Animator.allAnimators.append(self)

	def __str__(self):
		return f"allAnimations: {len(self.animations)}, activeAnimations: {len(self.activeAnimations)}"

	def Draw(self):
		for animation in self.activeAnimations:
			animation.Draw()

	def append(self, key, animation):
		if type(animation) == Animation:
			
			animation.stopFunc = Func(self.RemoveActive, key)
			
			animation.startFunc = Func(self.AddActive, key)

			self.animations[key] = animation
		else:
			raise TypeError(f"Animation is not of type {Animation}")

	def remove(self, key):
		if key in self.animations:
			self.animations.pop(key)
		else:
			raise ValueError("Key not in dict")

	def UpdatePos(self, pos):
		for key in self.animations:
			self.animations[key].rect.x = pos[0]
			self.animations[key].rect.y = pos[1]

	def UpdateSize(self, size):
		pass

	def AddActive(self, key, onStop=None):
		if key in self.animations:
			if self.animations[key] not in self.activeAnimations:
				self.activeAnimations.append(self.animations[key])
				self.animations[key].Start()

				if onStop != None:
					self.animations[key].stopFunc = Sequence(Func(self.RemoveActive, key), Func(self.AddActive, onStop))

	def RemoveActive(self, key):
		if key in self.animations:
			if self.animations[key] in self.activeAnimations:
				self.activeAnimations.remove(self.animations[key])
				self.animations[key].Stop()
				self.previousAnimation = key

	def RemoveAll(self):
		self.previousAnimation = None
		if len(self.activeAnimations) > 0:
			for animation in self.activeAnimations:
				animation.Stop()

			for key in self.animations:
				if self.animations[key] == animation:
					self.previousAnimation = key

		self.activeAnimations = []

	def StartActiveAnimations(self):
		for animation in self.activeAnimations:
			animation.Start()

	def StopActiveAnimations(self):
		for animation in self.activeAnimations:
			animation.Stop()


# particle system
class ParticleSystem:
	# particle

	allParticles = []
	allEmitters = []
	maxParticles = 2000

	# fix particle forces being applied
	# acceleration not being calculated correctly 
	# replicate p:\Python Projects\particle systems\main.py

	class Particle(Vec2):
		# default values
		gravity = Vec2(0, 0.1)
		externalForces = []
		lifeTime = 255
		lifeReduction = 1
		bounceloss = Vec2(-0.95, -0.95)
		radius = 10
		color = white
		img_paths = [(color, "textures/particles/soft_1.png")]

		def LoadImg(img_paths, color, radius):
			img_textures = []
			for color, img_path in img_paths:
				if CheckFileExists(img_path):
					img = pg.image.load(img_path).convert_alpha()
					img_texture = pg.transform.smoothscale(img, (radius * 2, radius * 2))

					if color != None:
						for x in range(img_texture.get_width()):
							for y in range(img_texture.get_height()):
								img_color = img_texture.get_at((x, y))
								img_texture.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

					img_textures.append(img_texture)

			return img_textures

		def __init__(self, x, y, startVelocity=None, startAcceleration=Vec2(0, 0), **kwargs):
			super().__init__(x, y, lists=[ParticleSystem.allParticles])

			if isinstance(startVelocity, str):
				startVelocity = self.ConvertStringToRandom(startVelocity)
			self.velocity = Vec2.Random(-3, 3, -3, 3) if startVelocity == None else startVelocity
			self.acceleration = startAcceleration

			self.gravity = ParticleSystem.Particle.gravity
			self.externalForces = ParticleSystem.Particle.externalForces
			self.lifeTime = ParticleSystem.Particle.lifeTime
			self.lifeReduction = ParticleSystem.Particle.lifeReduction
			self.bounceloss = ParticleSystem.Particle.bounceloss
			self.radius = ParticleSystem.Particle.radius
			self.color = ParticleSystem.Particle.color
			self.img_paths = ParticleSystem.Particle.img_paths

			for key, value in kwargs.items():
				setattr(self, key, value)

			self.img_textures = ParticleSystem.Particle.LoadImg(self.img_paths, self.color, self.radius)
			self.img_texture = self.img_textures[randint(0, len(self.img_textures)-1)] if len(self.img_textures) > 0 else None

		def Draw(self):
			if self.img_texture == None:
				DrawCircleAlpha(screen, (self.color[0], self.color[1], self.color[2], Constrain(self.lifeTime, 0, 255)), (self.x, self.y), self.radius)
			else:
				self.img_texture.set_alpha(Constrain(self.lifeTime, 0, 255))
				screen.blit(self.img_texture, (self.x - self.radius, self.y - self.radius))	

		def ApplyForce(self, force):
			self.acceleration = self.acceleration + force

		def Update(self):
			self.velocity = self.velocity + self.acceleration
			pos = self + self.velocity
			self.x, self.y = pos.x, pos.y
			self.acceleration = Vec2(0, 0)

			if self.lifeTime != -1:
				self.lifeTime -= self.lifeReduction

				if self.lifeTime <= 0:
					self.Kill()

		def Kill(self):
			if self in ParticleSystem.allParticles:
				ParticleSystem.allParticles.remove(self)

		def Edges(self, y=True, x=True):
			if y:
				if self.y >= height - self.radius:
					self.y = height - self.radius
					self.velocity.y *= self.bounceloss[1]

				if self.y <= self.radius:
					self.y = self.radius
					self.velocity.y *= self.bounceloss[1]

			if x:
				if self.x >= width - self.radius:
					self.x = width - self.radius
					self.velocity.x *= self.bounceloss[0]

				if self.x <= self.radius:
					self.x = self.radius
					self.velocity.x *= self.bounceloss[0]

		def ApplyForces(self):
			for force in self.externalForces:
				if isinstance(force, str):
					force = self.ConvertStringToRandom(force)	

				self.ApplyForce(force * Map(self.lifeTime, 0, 255, 1, 0))

			self.ApplyForce(self.gravity)

		def ConvertStringToRandom(self, string):
			if "random" in string:
				string = string.split(":")[1].split(",")

			force = []
			for s in string:
				force.append(float(s))

			return Vec2.Random(force[0], force[1], force[2], force[3])


		# water
		# fire
		# smoke

	# emitter
		# particle size
		# particle color
		# particle texture
		# particle emission_rate
		# particle force / force over time
		# particle colliders
		# particle life time

		# emission area
		# max particles

		# start
		# stop
		# duration
		# loop

	class Emitter:
		maxNumOfParticles = 300

		particle_size = 20
		particle_color = white
		particle_paths = [(white, "textures/particles/soft_1.png")]
		particle_colliders = []
		particle_externalForces = []
		particle_life_reduction = 5
		particle_gravity = Vec2(0, 0.3, lists=[])
		particle_startVelocity = None
		particle_bounceloss = Vec2(-0.95, -randint(3, 4) / 10, lists=[])
		emission_rate = 3
		emission_area = (3, 3)

		def __init__(self, x, y, **kwargs):
			AddToListOrDict([ParticleSystem.allEmitters], self)
			self.pos = Vec2(x, y)

			self.emittedParticles = []
			self.maxNumOfParticles = ParticleSystem.Emitter.maxNumOfParticles
			self.shouldDraw = False
			self.showDebug = False

			self.particle_size = ParticleSystem.Emitter.particle_size
			self.particle_color = ParticleSystem.Emitter.particle_color
			self.particle_paths = ParticleSystem.Emitter.particle_paths
			self.particle_colliders = ParticleSystem.Emitter.particle_colliders
			self.particle_gravity = ParticleSystem.Emitter.particle_gravity
			self.particle_life_reduction = ParticleSystem.Emitter.particle_life_reduction
			self.particle_startVelocity = ParticleSystem.Emitter.particle_startVelocity
			self.particle_externalForces = ParticleSystem.Emitter.particle_externalForces
			self.emission_rate = ParticleSystem.Emitter.emission_rate
			self.emission_area = ParticleSystem.Emitter.emission_area

			self.rect = pg.Rect(self.pos.x, self.pos.y, self.emission_area[0], self.emission_area[1])

			for key, value in kwargs.items():
				setattr(self, key, value)

			self.fpsLbl = Label((0, 0, 100, 50), (lightBlack, darkWhite), str(FPS), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False}, lists=[])
			self.numOfParticlesLbl = Label((30, 0, 100, 50), (lightBlack, darkWhite), str(FPS), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False}, lists=[])
		
		def Draw(self):
			if self.shouldDraw:
				DrawRectOutline(darkWhite, (self.pos.x, self.pos.y, self.emission_area[0], self.emission_area[1]))
			
			if self.showDebug:
				self.fpsLbl.UpdateText(f"{round(clock.get_fps())}")
				self.fpsLbl.Draw()
				self.numOfParticlesLbl.UpdateText(f"{len(ParticleSystem.allParticles)}")
				self.numOfParticlesLbl.Draw()

		def CreateParticle(self):
			for i in range(self.emission_rate):
				if len(self.emittedParticles) <= self.maxNumOfParticles and len(ParticleSystem.allParticles) <= ParticleSystem.maxParticles:
					ParticleSystem.Particle(randint(self.rect.x, self.rect.x + self.emission_area[0]), randint(self.rect.y, self.rect.y + self.emission_area[1]), radius=self.particle_size, 
						color=self.particle_color, img_paths=self.particle_paths, lifeReduction=self.particle_life_reduction, bounceloss=self.particle_bounceloss, 
						gravity=self.particle_gravity, externalForces=self.particle_externalForces, startVelocity=self.particle_startVelocity)

		def Update(self):
			self.CreateParticle()

		def HandleEvent(self, event):
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_F3:
					self.showDebug = not self.showDebug


# auto agents
# P:\Python Projects\auto agents

# gravity sim / physics obj
# P:\Python Projects\gravity sim
# P:\Python Projects\particle systems

if __name__ == "__main__":

	def DrawLoop():
		screen.fill(black)

		DrawAllGUIObjects()

		for particle in ParticleSystem.allParticles:
			particle.Draw()

		for emitter in ParticleSystem.allEmitters:
			emitter.Draw()

		pg.display.update()

	def HandleEvents(event):
		HandleGui(event)

		for emitter in ParticleSystem.allEmitters:
			emitter.HandleEvent(event)

	ParticleSystem.Emitter(width // 2 - 25, height - 40, emission_area=(50, 10), particle_bounceloss=(1, 1), particle_startVelocity="random:-0.5,0.5,-3,-2",
	 particle_gravity=Vec2(0, 0), particle_life_reduction=1, particle_paths=[(LerpColor((45, 51, 46), white, 0.3), "textures/particles/smoke_1.png"),
	  (LerpColor((45, 51, 46), white, 0.3), "textures/particles/smoke_2.png")], particle_externalForces=[Vec2(0.04, 0)])
	
	def Update():
		for particle in ParticleSystem.allParticles:
			particle.ApplyForces()
			particle.Update()
			particle.Edges()

		for emitter in ParticleSystem.allEmitters:
			emitter.Update()


	while RUNNING:
		clock.tick_busy_loop(FPS)
		deltaTime = clock.get_time()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				RUNNING = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					RUNNING = False

			HandleEvents(event)

		Update()

		DrawLoop()
