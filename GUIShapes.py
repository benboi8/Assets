from GUI import *

triangles = []
squares = []


class Shape:
	def __init__(self, center, sideLength, color, rotAngle=0, sidePoints=[], name="", lists=[triangles]):
		self.center = center
		self.sideLength = sideLength
		self.color = color
		self.rotAngle = rotAngle
		self.name = name

		AddToListOrDict(lists, self)


class Triangle(Shape):
	def __init__(self, center, sideLength, color, rotAngle=0, sidePoints=[], name="", lists=[triangles]):
		super().__init__(center, sideLength, color, rotAngle, sidePoints, name, lists)

		self.body = Polygon(self.center, 3, self.color, self.sideLength, self.rotAngle, sidePoints=sidePoints, lists=[])

	def Draw(self):
		self.body.Draw()


class Square(Shape):
	def __init__(self, center, sideLength, color, rotAngle=0, sidePoints=[], name="", lists=[squares]):
		super().__init__(center, sideLength, color, rotAngle, sidePoints, name, lists)

		self.body = Polygon(self.center, 4, self.color, self.sideLength, self.rotAngle, sidePoints=sidePoints, lists=[])

	def Draw(self):
		self.body.Draw()


def DrawShapes():
	for tri in triangles:
		tri.Draw()

	for square in squares:
		square.Draw()


if __name__ == "__main__":

	tri = Triangle((width / 2, height / 2), 100, red)

	square = Square((width / 2, height / 2), 100, red)

	def DrawLoop():
		global i
		screen.fill(darkGray)

		DrawAllGUIObjects()
		DrawShapes()

		pg.display.update()

	while running:
		clock.tick_busy_loop(fps)
		deltaTime = clock.get_time()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False


		DrawLoop()
