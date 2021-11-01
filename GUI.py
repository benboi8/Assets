from General import *
from colors import *

import pygame as pg
from pygame import *
from pygame import gfxdraw

pg.init()
clock = pg.time.Clock()

width, height = 1280, 720
screen = pg.display.set_mode((width, height))
running = True

centerOfScreen = (width / 2, height / 2)

fps = 60

points = {}
lines = {}
polygons = {}

allBoxs = {}


def DrawVector(vector, colors, magnitude=None, radius=3, surface=screen):
	if magnitude == None:
		magnitude = vector.Magnitude()

	pg.draw.circle(surface, colors[0], (vector.x, vector.y), radius)
	d = vector.Direction(centerOfScreen)
	pg.draw.line(surface, colors[1], (vector.x, vector.y), (vector.x + (d * magnitude), vector.y + (d * magnitude)))


def DrawRectOutline(color, rect, width=1, surface=screen):
	x, y, w, h = rect

	width = min(min(max(width, 1), w//2), h//2)

	for i in range(int(width)):
		pg.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)


class RayCast:
	def Cast(self, p1, p2, walls):
		for wall in walls:
			x1, y1 = p1
			x2, y2 = p2

			x3, y3 = wall[0]
			x4, y4 = wall[1]

			den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
			if den != 0:
				t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
				if 0 <= t <= 1:
					l1 = ((x1 + t * (x2 - x1)), (y1 + t * (y2 - y1)))
					if l1 > (x3, y3) and l1 < (x4, y4):
						self.ray = Vec2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
						return True
		return False


class Point(Vec2):
	def __init__(self, x, y, color, radius, name="", surface=screen, lists=[points]):
		super().__init__(x, y, lists=[])
		self.name = name
		self.surface = surface
		self.color = color
		self.radius = radius

		AddToListOrDict(lists, self)


	def Draw(self):
		pg.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)


class Line:
	def __init__(self, startPos, endPos, color, startPointRadius=3, endPointRadius=3, name="", surface=screen, lists=[lines]):
		self.start = Point(startPos[0], startPos[1], color, startPointRadius, surface, lists=[])
		self.end = Point(endPos[0], endPos[1], color, endPointRadius, surface, lists=[])
		self.name = name

		self.surface = surface
		self.startPos = startPos
		self.endPos = endPos
		self.color = color

		AddToListOrDict(lists, self)

	def Draw(self):
		self.start.Draw()
		self.end.Draw()
		pg.draw.line(self.surface, self.color, self.startPos, self.endPos)


class Polygon:
	def __init__(self, center, numOfSides, color, lineSize, drawCenter=False, drawLineCircle=False, rotAngle=0, pointRadius=2, sidePoints=[], name="", surface=screen, lists=[polygons]):
		self.surface = screen
		self.name = name
		self.pointRadius = pointRadius
		self.numOfSides = numOfSides
		self.color = color
		self.lineSize = lineSize
		self.rotAngle = rotAngle
		self.center = Point(center[0], center[1], self.color, self.pointRadius, lists=[])
		self.drawCenter = drawCenter
		self.drawLineCircle = drawLineCircle
		self.sidePoints = sidePoints
		self.pixels = []
		self.checkPos = [(self.center.x, self.center.y)]

		self.CreateSides()

		AddToListOrDict(lists, self)

	def CreateSides(self):
		self.points = []
		self.lines = []
		angle = 360 / self.numOfSides

		for i in range(self.numOfSides):
			x, y = self.center.x, self.center.y
			p = Point(x, y, self.color, self.pointRadius, lists=[])

			length = sqrt(self.lineSize ** 2 + self.lineSize ** 2) / 2

			p.x, p.y = p.RotateDegrees((angle * i) + self.rotAngle, p.GetEuclideanDistance((x, y - length)))

			if len(self.sidePoints) > 0:
				p.x, p.y = self.sidePoints[i]

			self.points.append(p)

		for i, p in enumerate(self.points):
			for j in range(-1, 2):
				self.lines.append(Line((self.points[i - 1].x, self.points[i - 1].y), (p.x, p.y), self.color, startPointRadius=self.pointRadius, endPointRadius=self.pointRadius, lists=[]))

		self.Fill()

	def Fill(self):
		# bounding box around polygon
		xs, ys = [], []
		boundingBox = []

		for p in self.points:
			xs.append(p.x)
			ys.append(p.y)

		e = 5
		xMin = min(xs) - e
		xMax = max(xs) + e
		yMin = min(ys) - e
		yMax = max(ys) + e

		for x in range(width):
			for y in range(height):
				if x < xMin or x > xMax or y < yMin or y > yMax:
					pass
				else:
					boundingBox.append((x, y))

		for point in boundingBox:

			walls = []

			for i, p in enumerate(self.points):
				walls.append(((self.points[i - 1].x - 1, self.points[i - 1].y - 1), (p.x + 1, p.y + 1)))

		ray = RayCast()
		for p in boundingBox:
			if not ray.Cast((self.center.x - self.center.Direction((p[0], p[1])), self.center.y - self.center.Direction((p[0], p[1]))), (p[0], p[1]), walls):
				self.pixels.append(p)


	def Draw(self):
		if self.drawCenter:
			self.center.Draw()

		if self.drawLineCircle:
			pg.gfxdraw.aacircle(self.surface, self.center.x, self.center.y, self.lineSize, self.color)

		for p in self.points:
			p.Draw()

		for p in self.pixels:
			pg.gfxdraw.pixel(self.surface, p[0], p[1], red)

		for l in self.lines:
			l.Draw()

	def ChangeNumOfSides(self, numOfSides):
		self.numOfSides = numOfSides
		self.CreateSides()

	def MoveShape(self, centerPos):
		self.center = Point(centerPos[0], centerPos[1], self.color, self.pointRadius, lists=[])
		self.CreateSides()

	def ChangeLineSize(self, lineSize):
		self.lineSize = lineSize
		self.CreateSides()

	def ChangeColor(self, color):
		self.color = color
		self.CreateSides()

	def ChangeRotAngle(self, rotAngle):
		self.rotAngle = rotAngle
		self.CreateSides()

	def ChangePointRadius(self, pointRadius):
		self.pointRadius = pointRadius
		self.CreateSides()


class Box:
	def __init__(self, rect, colors, name="", surface=screen, drawData={}, lists=[allBoxs]):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.forgroundColor = colors[1]
		self.name = name
		self.surface = surface
		self.drawData = drawData

		self.drawBorder = drawData.get("drawBorder", True)
		self.borderWidth = drawData.get("borderWidth", 1)
		self.drawBackground = drawData.get("drawBackground", True)

		AddToListOrDict(lists, self)

	def Draw(self):
		# draw background
		if self.drawBackground:
			pg.draw.rect(self.surface, self.backgroundColor, self.rect)

		# draw border
		if self.drawBorder:
			DrawRectOutline(self.forgroundColor, self.rect, self.borderWidth)


def DrawAllGUIObjects():
	for key in points:
		points[key].Draw()

	for key in lines:
		lines[key].Draw()

	for key in polygons:
		polygons[key].Draw()

	for key in allBoxs:
		allBoxs[key].Draw()


if __name__ == "__main__":

	vs = []
	scale = 80
	for x in range(1, scale):
		for y in range(1, scale):
			vs.append(Vec2(x * (width / scale), y * (height / scale)))

	# Polygon(centerOfScreen, 5, white, 100)

	def DrawLoop():
		screen.fill(darkGray)

		DrawAllGUIObjects()

		for v in vs:
			DrawVector(v, [(55, 55, 205), red], 10)

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
