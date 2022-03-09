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
# P:\Python Projects\2d platformer

# entity
# P:\Python Projects\2d platformer

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



# particle system
class ParticleSystem:
	# particle

	allParticles = []
	allEmitters = []
	maxParticles = 2000

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
				if not CheckFileExists(img_path.split("/")[-1], img_path[0:len(img_path.split("/")[-1])]):
					img = pg.image.load(img_path).convert_alpha()
					img_texture = pg.transform.smoothscale(img, (radius * 2, radius * 2))

					for x in range(img_texture.get_width()):
						for y in range(img_texture.get_height()):
							img_color = img_texture.get_at((x, y))
							img_texture.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

					img_textures.append(img_texture)

			return img_textures

		def __init__(self, x, y, startVelocity=None, startAcceleration=Vec2(0, 0), **kwargs):
			super().__init__(x, y, lists=[ParticleSystem.allParticles])

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
			self.acceleration = self.acceleration.Add(force)

		def Update(self):
			self.velocity = self.velocity.Add(self.acceleration)
			pos = self.Add(self.velocity)
			self.x, self.y = pos.x, pos.y
			self.acceleration = Vec2(0, 0, lists=[])

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
					self.velocity.y *= self.bounceloss.y

				if self.y <= self.radius:
					self.y = self.radius
					self.velocity.y *= self.bounceloss.y

			if x:
				if self.x >= width - self.radius:
					self.x = width - self.radius
					self.velocity.x *= self.bounceloss.x

				if self.x <= self.radius:
					self.x = self.radius
					self.velocity.x *= self.bounceloss.x


		def ApplyForces(self):
			for force in self.externalForces:
				self.ApplyForce(force)

			self.ApplyForce(self.gravity)

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
		particle_life_reduction = 5
		particle_gravity = Vec2(0, 0.3, lists=[])
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
			self.emission_rate = ParticleSystem.Emitter.emission_rate
			
			self.emission_area = ParticleSystem.Emitter.emission_area
			self.rect = pg.Rect(self.pos.x, self.pos.y, self.emission_area[0], self.emission_area[1])

			for key, value in kwargs.items():
				setattr(self, key, value)

			self.fpsLbl = Label((0, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False}, lists=[])
			self.numOfParticlesLbl = Label((30, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False}, lists=[])
		
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
					ParticleSystem.Particle(randint(self.rect.x, self.rect.x + self.rect.w), randint(self.rect.y, self.rect.y + self.rect.h), radius=self.particle_size, color=self.particle_color,
					 img_paths=self.particle_paths, lifeReduction=self.particle_life_reduction, bounceloss=self.particle_bounceloss, gravity=self.particle_gravity)

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
		screen.fill(darkGray)

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

	ParticleSystem.Emitter(width // 2, height // 2, particle_gravity=Vec2(0, 0.3))

	def Update():
		for particle in ParticleSystem.allParticles:
			particle.ApplyForces()
			particle.Update()
			particle.Edges()

		for emitter in ParticleSystem.allEmitters:
			emitter.Update()


	while running:
		clock.tick_busy_loop(fps)
		deltaTime = clock.get_time()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

			HandleEvents(event)

		Update()

		DrawLoop()
