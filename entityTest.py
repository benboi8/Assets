import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *



class Collider:
	allColliders = []

	def __init__(self, rect, bounceLoss, colors):
		self.rect = pg.Rect(rect)
		self.bounceLoss = Vec2(bounceLoss[0], bounceLoss[1])
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		AddToListOrDict([Collider.allColliders], self)

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect)


class Entity(Vec2):
	allEntities = []

	def __init__(self, pos, size, colors, **kwargs):
		super().__init__(pos[0], pos[1], lists=[Entity.allEntities])

		self.velocity = Vec2(0, 0)
		self.acceleration = Vec2(0, 0)

		self.size = size

		self.UpdateBoundingBox()

		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

	@property
	def acc(self):
		return self.acceleration	
	
	@property
	def vel(self):
		return self.velocity

	@property
	def pos(self):
		return self.Copy()

	@property
	def position(self):
		return self.Copy()

	def UpdateBoundingBox(self):
		if isinstance(self.size, (int, float)):
			self.boundingBox = pg.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
		else:
			self.boundingBox = pg.Rect(self.x, self.y, self.size[0], self.size[1])

	def ApplyForce(self, vec):
		self.acceleration = self.acceleration.Add(vec)

	def PhysicsUpdate(self):
		self.velocity = self.velocity.Add(self.acceleration)
		pos = self.Add(self.velocity)
		self.x, self.y = pos.x, pos.y
		self.acceleration.Set(0, 0)

	def Update(self, colliders=[]):
		self.PhysicsUpdate()
		self.UpdateBoundingBox()
		self.Collide(colliders)
		self.UpdateBoundingBox()

	def Collide(self, colliders, collideWithScreen=True):
		bounceLoss = Vec2(-1, -1)
		size = (self.boundingBox.w, self.boundingBox.h)

		if collideWithScreen:
			if self.boundingBox.y >= height - size[1]:
				self.boundingBox.y = height - size[1]
				self.velocity.y *= bounceLoss.y

			if self.boundingBox.y <= 0:
				self.boundingBox.y = 0
				self.velocity.y *= bounceLoss.y
			
			if self.boundingBox.x >= width - size[0]:
				self.boundingBox.x = width - size[0]
				self.velocity.x *= bounceLoss.x

			if self.boundingBox.x <= 0:
				self.boundingBox.x = 0
				self.velocity.x *= bounceLoss.x

		for collider in colliders:
			if collider.rect.colliderect(self.boundingBox):
				if self.boundingBox.x + self.boundingBox.w >= collider.rect.x + 6 and self.boundingBox.x <= collider.rect.x + collider.rect.w - 6:
					# top
					if self.boundingBox.y <= collider.rect.y:
						if isinstance(self.size, (int, float)):
							self.y = collider.rect.y - self.size
						else:
							self.y = collider.rect.y - self.size[1]
						self.velocity.y *= collider.bounceLoss.y

					# bottom
					if self.boundingBox.y + self.boundingBox.h >= collider.rect.y + collider.rect.h:
						if isinstance(self.size, (int, float)):
							self.y = collider.rect.y + collider.rect.h + self.size
						else:
							self.y = collider.rect.y + collider.rect.h
						self.velocity.y *= collider.bounceLoss.y

				if self.boundingBox.y + self.boundingBox.h >= collider.rect.y + 6 and self.boundingBox.y <= collider.rect.y + collider.rect.h - 6:
					# left
					if self.boundingBox.x <= collider.rect.x:
						if isinstance(self.size, (int, float)):
							self.x = collider.rect.x - self.size
						else:
							self.x = collider.rect.x - self.size[0]
						self.velocity.x *= collider.bounceLoss.x

					# right
					if self.boundingBox.x + self.boundingBox.w >= collider.rect.x + collider.rect.w:
						if isinstance(self.size, (int, float)):
							self.x = collider.rect.x + collider.rect.w + self.size
						else:
							self.x = collider.rect.x + collider.rect.w
						self.velocity.x *= collider.bounceLoss.x

	def Draw(self):
		if isinstance(self.size, (int, float)):
			pg.draw.circle(screen, self.borderColor, (self.x, self.y), self.size)
			pg.draw.circle(screen, self.backgroundColor, (self.x, self.y), self.size - 1)
		else:
			pg.draw.rect(screen, self.backgroundColor, (self.x, self.y, self.size[0], self.size[1]))
			DrawRectOutline(self.borderColor, (self.x, self.y, self.size[0], self.size[1]))



speed = 6

e = Entity((75, height // 2), 25, (red, white))
e.ApplyForce(Vec2(speed, speed))
e = Entity((100, height // 2 - 25), (50, 50), (red, white))
e.ApplyForce(Vec2(speed, speed))


e = Entity((width // 2, 75), 25, (red, white))
e.ApplyForce(Vec2(speed, speed))
e = Entity((width // 2 - 25, 100), (50, 50), (red, white))
e.ApplyForce(Vec2(speed, speed))


e = Entity((width - 75, height // 2), 25, (red, white))
e.ApplyForce(Vec2(-speed, -speed))
e = Entity((width - 150, height // 2 - 25), (50, 50), (red, white))
e.ApplyForce(Vec2(-speed, -speed))


e = Entity((width // 2, height - 75), 25, (red, white))
e.ApplyForce(Vec2(-speed, -speed))
e = Entity((width // 2 - 25, height - 150), (50, 50), (red, white))
e.ApplyForce(Vec2(-speed, -speed))

Collider((width // 2 - 700 // 2, height // 2 - 150, 700, 300), (-1, -1), (lightBlack, darkWhite))



def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	for collider in Collider.allColliders:
		collider.Draw()

	for entity in Entity.allEntities:
		entity.Draw()

	pg.display.update()



def HandleEvents(event):
	HandleGui(event)

	if event.type == pg.KEYDOWN:
		if event.key == pg.K_SPACE:
			for entity in Entity.allEntities:
				entity.velocity = entity.velocity * 0.05

		if event.key == pg.K_RETURN:
			for entity in Entity.allEntities:
				entity.velocity = entity.velocity / 0.05

def Update():
	for entity in Entity.allEntities:
		entity.Update(Collider.allColliders)


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
