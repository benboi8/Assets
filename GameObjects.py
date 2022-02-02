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

# entity

# player controller

# tiles

# interactive tiles

# specialised tiles
# - door
# - storage
# - npc

# physics engine

# input handler

# time manager

# sound manager



if __name__ == "__main__":

	def DrawLoop():
		screen.fill(darkGray)

		DrawAllGUIObjects()

		pg.display.update()


	def HandleEvents(event):
		HandleGui(event)


	def Update():
		pass

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
