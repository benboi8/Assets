# import os
# import sys

# os.chdir(sys.path[0])
# sys.path.insert(1, "P://Python Projects/assets/")

# from GUI import *

from General import *
from colors import *

import pygame as pg
from pygame import *
from pygame import gfxdraw

import webbrowser

pg.init()
clock = pg.time.Clock()

running = True

fps = 60

points = {}
lines = {}
polygons = {}

allBoxs = {}
allLabels = {}
allTextBoxs = {}
allButtons = {}
allSliders = {}
allScrollBars = {}
allMessageBoxs = {}
allHyperLinks = {}
allSwitches = {}
allMultiselectButtons = {}
allProgressBars = {}
allRadioButtons = {}

allCollections = {}
allExpandableMenus = {}


def ChangeFontName(name):
	global fontName
	fontName = name


def ChangeFontSize(size):
	global fontSize
	fontSize = size


def ChangeScreenSize(w, h, vsync=1, flags=None):
	global width, height, screen, centerOfScreen
	# width, height
	width, height = w, h
	# screen

	if flags != None:
		screen = pg.display.set_mode((width, height), flags, vsync=vsync)
	else:
		screen = pg.display.set_mode((width, height), vsync=vsync)

	# center of screen
	centerOfScreen = (width / 2, height / 2)
	return width, height


# set up
# create screen
ChangeScreenSize(1280, 720)
# set font
ChangeFontName("arial")
ChangeFontSize(24)



def DrawVector(vector, colors, magnitude=None, directionPoint=centerOfScreen, radius=2, surface=screen):
	if magnitude == None:
		magnitude = vector.Magnitude()

	pg.draw.circle(surface, colors[0], (vector.x, vector.y), radius)
	# d = vector.Direction(directionPoint)
	# pg.draw.line(surface, colors[1], (vector.x, vector.y), (vector.x + (d[0] * magnitude), vector.y + (d[1] * magnitude)))

	# vector = vector.Normalize()
	d = radians(vector.Direction())
	pg.draw.line(surface, colors[1], (vector.x, vector.y), (vector.x + (10 * cos(d)), vector.y + (10 * sin(d))))


def DrawRectOutline(color, rect, width=1, surface=screen):
	x, y, w, h = rect

	width = min(min(max(width, 1), w//2), h//2)

	for i in range(int(width)):
		pg.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)


def AlignText(rect, textSurface, alignment="center", width=2):
	x, y, w, h = rect

	# get horizontal and vertical alignments
	alignment = str(alignment).lower().strip()

	if "-" in alignment:
		align = alignment.split("-")
		horizontal, vertical = align[0], align[1]

	else:
		if alignment == "center":
			horizontal, vertical = alignment, alignment
		elif alignment == "left" or alignment == "right":
			horizontal, vertical = alignment, "center"
		elif alignment == "top" or alignment == "bottom":
			horizontal, vertical = "center", alignment
		else:
			horizontal, vertical = "center", "center"

	# check horizontal alignment
	if horizontal == "center":
		x += w // 2 - textSurface.get_width() // 2
	elif horizontal == "left":
		x += width + 2
	elif horizontal == "right":
		x += w - textSurface.get_width() - (width + 2)

	# check vertical alignment
	if vertical == "center":
		y += h // 2 - textSurface.get_height() // 2
	elif vertical == "top":
		y += width + 2
	elif vertical == "bottom":
		y += h - textSurface.get_height() - (width + 2)

	return pg.Rect(x, y, w, h)


def DrawRoundedRect(rect, colors, roundness=2, borderWidth=2, activeCorners={}, surface=screen, drawBorder=True, drawBackground=True):
	try:
		rect = pg.Rect(rect)
		backgroundColor = colors[0]
		borderColor = colors[1]

		# get radius and offsets
		if rect.w > rect.h:
			radius = rect.h // max(2, int(roundness))
		else:
			radius = rect.w // max(2, int(roundness))

		xOffSet = rect.w - radius * 2 - (borderWidth // 2)
		yOffSet = rect.h - radius * 2 - (borderWidth // 2)

		offSetRectX = pg.Rect(rect.x + radius, rect.y, rect.w - radius * 2, rect.h)
		offSetRectY = pg.Rect(rect.x, rect.y + radius, rect.w, rect.h - radius * 2)


		# draw background
		if drawBackground:
			pg.draw.rect(surface, backgroundColor, offSetRectX)
			pg.draw.rect(surface, backgroundColor, offSetRectY)

			if activeCorners.get("topLeft", True):
				pg.draw.circle(surface, backgroundColor, (offSetRectX.x, offSetRectY.y), radius)
			else:
				pg.draw.rect(surface, backgroundColor, (rect.x, rect.y, abs(rect.x - offSetRectX.x), abs(rect.y - offSetRectY.y)))

			if activeCorners.get("topRight", True):
				pg.draw.circle(surface, backgroundColor, (offSetRectX.x + offSetRectX.w, offSetRectY.y), radius)
			else:
				pg.draw.rect(surface, backgroundColor, (offSetRectX.x + offSetRectX.w, rect.y, abs(rect.w - offSetRectX.w)//2, abs(rect.y - offSetRectY.y)))

			if activeCorners.get("bottomRight", True):
				pg.draw.circle(surface, backgroundColor, (offSetRectX.x + offSetRectX.w, offSetRectY.y + offSetRectY.h), radius)
			else:
				pg.draw.rect(surface, backgroundColor, (offSetRectX.x + offSetRectX.w, offSetRectY.y + offSetRectY.h, abs(rect.w - offSetRectX.w)//2, abs(rect.h - offSetRectY.h)//2))

			if activeCorners.get("bottomLeft", True):
				pg.draw.circle(surface, backgroundColor, (offSetRectX.x, offSetRectY.y + offSetRectY.h), radius)
			else:
				pg.draw.rect(surface, backgroundColor, (rect.x, offSetRectY.y + offSetRectY.h, abs(rect.x - offSetRectX.x), abs(rect.h - offSetRectY.h)//2))


		# draw border
		# curves
		if drawBorder:
			for i in range(-borderWidth//2, borderWidth//2 + 1):
				for j in range(-1, 2):
					if activeCorners.get("topLeft", True):
						# top left
						pg.gfxdraw.arc(surface, rect.x + radius + j, rect.y + radius + j, radius + (i + j), 180 + i, 270 + i, borderColor)
					else:
						pg.draw.aaline(surface, borderColor, (rect.x - borderWidth / 2, rect.y + i), (offSetRectX.x, rect.y + i))
						pg.draw.aaline(surface, borderColor, (rect.x + i, rect.y - borderWidth / 2), (rect.x + i, offSetRectY.y))

					if activeCorners.get("topRight", True):
						# top right
						pg.gfxdraw.arc(surface, rect.x + radius - j + xOffSet, rect.y + radius + j, radius + (i + j), 270 + i, 0 + i, borderColor)
					else:
						pg.draw.aaline(surface, borderColor, (rect.x + rect.w - borderWidth / 2, rect.y + i), (offSetRectX.x + offSetRectX.w, rect.y + i))
						pg.draw.aaline(surface, borderColor, (rect.x + rect.w - (borderWidth // 2) + i, rect.y - borderWidth / 2), (rect.x + rect.w - (borderWidth // 2) + i, offSetRectY.y + offSetRectY.h))

					if activeCorners.get("bottomRight", True):
						# bottom right
						pg.gfxdraw.arc(surface, rect.x + radius - j + xOffSet, rect.y + radius - j + yOffSet, radius + (i + j), 0 + i, 90 + i, borderColor)
					else:
						pg.draw.aaline(surface, borderColor, (rect.x + rect.w - (borderWidth // 2) + i, rect.y + rect.h), (rect.x + rect.w - (borderWidth // 2) + i, offSetRectY.y))
						pg.draw.aaline(surface, borderColor, (rect.x + rect.w, rect.y + rect.h - (borderWidth // 2) + i), (offSetRectX.x + offSetRectX.w, rect.y + rect.h - (borderWidth // 2) + i))

					if activeCorners.get("bottomLeft", True):
						# bottom left
						pg.gfxdraw.arc(surface, rect.x + radius + j, rect.y + radius - j + yOffSet, radius + (i + j), 90 + i, 180 + i, borderColor)
					else:
						pg.draw.aaline(surface, borderColor, (rect.x, rect.y + rect.h - (borderWidth // 2) + i), (offSetRectX.x + offSetRectX.w, rect.y + rect.h - (borderWidth // 2) + i))
						pg.draw.aaline(surface, borderColor, (rect.x + i, rect.y + rect.h), (rect.x + i, offSetRectY.y + offSetRectY.h))


				# connecting lines
				# top
				pg.draw.aaline(surface, borderColor, (offSetRectX.x, rect.y + i), (offSetRectX.x + offSetRectX.w, rect.y + i))

				# bottom
				pg.draw.aaline(surface, borderColor, (offSetRectX.x, rect.y + i + rect.h - borderWidth // 2), (offSetRectX.x + offSetRectX.w, rect.y + i + rect.h - borderWidth // 2))

				# left
				pg.draw.aaline(surface, borderColor, (rect.x + i, offSetRectY.y), (rect.x + i, offSetRectY.y + offSetRectY.h))

				# right
				pg.draw.aaline(surface, borderColor, (rect.x + i + rect.w - borderWidth // 2, offSetRectY.y), (rect.x + i + rect.w - borderWidth // 2, offSetRectY.y + offSetRectY.h))
	except:
		pass


def MoveRectWithoutCenter(startPos, startRect):
	# get current mouse pos
	mouseX, mouseY = pg.mouse.get_pos()

	# get difference from start x and start y to mouse cursor for movement
	differenceX = startPos[0] - startRect.x
	differenceY = startPos[1] - startRect.y

	# get new pos
	x = mouseX - differenceX
	y = mouseY - differenceY

	return pg.Rect(x, y, startRect.w, startRect.h)


def DrawRectAlpha(surface, color, rect):
	shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
	pg.draw.rect(shape_surf, color, shape_surf.get_rect())
	surface.blit(shape_surf, rect)


def DrawCircleAlpha(surface, color, center, radius):
	target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
	shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
	pg.draw.circle(shape_surf, color, (radius, radius), radius)
	surface.blit(shape_surf, target_rect)


def DrawPolygonAlpha(surface, color, points):
	lx, ly = zip(*points)
	min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
	target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
	shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
	pg.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
	surface.blit(shape_surf, target_rect)


def CircleLineSegmentIntersection(circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
	(p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
	(x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
	dx, dy = (x2 - x1), (y2 - y1)
	dr = (dx ** 2 + dy ** 2)**.5
	big_d = x1 * y2 - x2 * y1
	discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

	if discriminant < 0:  # No intersection between circle and line
		return []
	else:  # There may be 0, 1, or 2 intersections with the segment
		intersections = [(cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2, cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2) for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
		if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
			fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
			intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
		if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
			return [intersections[0]]
		else:
			return intersections


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
	def __init__(self, startPos, endPos, color, startPointRadius=3, endPointRadius=3, aa=False, name="", surface=screen, lists=[lines]):
		self.start = Point(startPos[0], startPos[1], color, startPointRadius, surface, lists=[])
		self.end = Point(endPos[0], endPos[1], color, endPointRadius, surface, lists=[])
		self.name = name

		self.surface = surface
		self.startPos = (self.start.x, self.start.y)
		self.endPos = (self.end.x, self.end.y)

		self.color = color

		self.aa = aa

		AddToListOrDict(lists, self)

	def Draw(self):
		self.startPos = (self.start.x, self.start.y)
		self.endPos = (self.end.x, self.end.y)

		self.start.Draw()
		self.end.Draw()
		if not self.aa:
			pg.draw.line(self.surface, self.color, self.startPos, self.endPos)
		else:
			pg.draw.aaline(self.surface, self.color, self.startPos, self.endPos)


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

		# self.Fill()

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
			if not ray.Cast((self.center.x - self.center.Direction((p[0], p[1]))[0], self.center.y - self.center.Direction((p[0], p[1]))[1]), (p[0], p[1]), walls):
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
		self.borderColor = colors[1]
		self.name = name
		self.surface = surface
		self.drawData = drawData

		self.disabled = drawData.get("disabled", False)

		self.drawBorder = drawData.get("drawBorder", True)
		self.drawBackground = drawData.get("drawBackground", True)
		self.roundedCorners = drawData.get("roundedCorners", False)
		self.borderWidth = drawData.get("borderWidth", 1 if self.roundedCorners else 2)
		self.roundness = drawData.get("roundness", 4)
		self.activeCorners = drawData.get("activeCorners", {})

		AddToListOrDict(lists, self)

	def Draw(self):
		if not self.disabled:
			self.DrawBackground()
			self.DrawBorder()

	def DrawBackground(self):
		if self.drawBackground:
			if not self.roundedCorners:
				pg.draw.rect(self.surface, self.backgroundColor, self.rect)

	def DrawBorder(self):
		if not self.roundedCorners:
			if self.drawBorder:
				DrawRectOutline(self.borderColor, self.rect, self.borderWidth, surface=self.surface)
		else:
			DrawRoundedRect(self.rect, (self.backgroundColor, self.borderColor), self.roundness, self.borderWidth, self.activeCorners, self.surface, drawBorder=self.drawBorder, drawBackground=self.drawBackground)

	def UpdateRect(self, rect):
		self.rect = pg.Rect(rect)


class Label(Box):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, lists=[allLabels]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		self.text = text
		self.fontSize = textData.get("fontSize", fontSize)
		self.fontName = textData.get("fontName", fontName)
		self.fontColor = textData.get("fontColor", white)
		self.alignText = textData.get("alignText", "center")
		self.fitRectToText = textData.get("fitRectToText", False)

		self.scrollLevel = 0
		self.minWidth, self.minHeight = self.rect.w, self.rect.h

		self.CreateTextObjects()

	def CreateTextObjects(self, recursive=False, minWidth=None, minHeight=None):
		if minWidth == None:
			self.minWidth = self.rect.w
		if minHeight == None:
			self.minHeight = self.rect.h

		try:
			self.font = pg.font.Font(self.fontName, self.fontSize)
		except FileNotFoundError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)
		except TypeError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)
		except:
			print(f"ERROR: Font '{self.fontName}' not found{f' for obj with name {self.name}' if self.name != '' else f'. Obj has no name. Text is: [{self.text}]'}\nEnd of text. Font has defaulted to arial.\n Note that some other error may have occured.")
			self.font = pg.font.SysFont("arial", self.fontSize)

		# -- test --
		if not ("\n" in self.text or "\\n" in self.text):
			if self.font.render(self.text, True, self.fontColor).get_width() >= self.rect.w:
				oneCharWidth = self.font.render("W", True, self.fontColor).get_width()
				total = 0
				for i, char in enumerate(self.text):
					total += 1
					if char == " " and total * oneCharWidth > self.rect.w:
						self.text = f"{self.text[:i]}\n{self.text[i + 1:]}"
						total = 0

		self.textObjs = []
		self.text = str(self.text)
		if "\\n" in self.text:
			text = self.text.split("\\n")
		else:
			text = self.text.split("\n")

		rect = pg.Rect(self.rect.x, self.rect.y, self.minWidth, self.minHeight)
		for i, t in enumerate(text):
			textSurface = self.font.render(str(t), True, self.fontColor)
			if "center" in self.text and "top" not in self.text:
				y = rect.y + ((i - len(text) // 2) * textSurface.get_height())
			else:
				y = rect.y + (i * textSurface.get_height())
			
			self.textObjs.append((textSurface, AlignText(pg.Rect(rect.x, y, rect.w, rect.h), textSurface, self.alignText, self.borderWidth)))
			self.textHeight = textSurface.get_height()
		
			self.minWidth, self.minHeight = min(self.minWidth, textSurface.get_width() + self.borderWidth + 10), min(self.minHeight, textSurface.get_height() + self.borderWidth + 5)
			

		if self.name == "test":
			print(len(self.textObjs))

		if self.fitRectToText:
			self.rect.w = self.minWidth + 200
			self.rect.h = (self.minHeight * len(self.textObjs)) + (self.borderWidth + 20)
			if not recursive:
				self.CreateTextObjects(True, self.minWidth, self.minHeight)

	def Draw(self, byPassRectCheck=False):
		if not self.disabled:
			self.DrawBackground()
			self.DrawBorder()
			self.DrawText(byPassRectCheck)

	def DrawText(self, byPassRectCheck=False):
		for obj in self.textObjs:
			rect = pg.Rect(obj[1][0], obj[1][1] - (self.scrollLevel * obj[0].get_height()), obj[0].get_width(), obj[0].get_height())
			if self.rect.x < rect.x and self.rect.y < rect.y and self.rect.x + self.rect.w > rect.x + rect.w and self.rect.y + self.rect.h > rect.y + rect.h or byPassRectCheck:
				self.surface.blit(obj[0], rect)

	def UpdateText(self, text):
		self.text = str(text)
		self.CreateTextObjects()
		self.scrollLevel = len(self.textObjs) - (self.rect.h / self.textHeight) if (self.rect.h / self.textHeight) < len(self.textObjs) else 0

	def UpdateRect(self, rect):
		self.rect = pg.Rect(rect)
		self.UpdateText(self.text)


class Hint(Label):
	def __init__(self, rect, colors, parent, text="", delay=60000, name="", surface=screen, drawData={}, textData={}):
		"""Delay: In microseconds, max of 1 minute"""

		super().__init__(rect, colors, text, name, surface, drawData, textData, [])

		self.parent = parent
		self.delay = abs(min(delay, 60000000))
		self.startTime = dt.datetime.now()
		self.hasStartTimeUpdated = False
		self.showHint = False

	def Draw(self):
		if not self.disabled:
			if self.delay != None:
				if self.parent.rect.collidepoint(pg.mouse.get_pos()):
					if not self.hasStartTimeUpdated:
						self.startTime = dt.datetime.now()
						self.hasStartTimeUpdated = True
					else:
						diff = (dt.datetime.now() - self.startTime)
						if self.delay <= 1000000: # number of microseconds in a second
							if diff.microseconds >= self.delay:
								self.showHint = True

						else:
							if self.delay <= 60000000: # number of microseconds in a minute
								if diff.seconds >= self.delay / 1000000 and diff.microseconds >= self.delay % 1000000:
									self.showHint = False
				else:
					self.showHint = False
					self.hasStartTimeUpdated = False

			if self.showHint or self.delay == None:
				self.DrawBackground()
				self.DrawBorder()
				self.DrawText()


class TextInputBox(Label):
	def __init__(self, rect, colors, splashText="Type here:", name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allTextBoxs]):
		self.splashText = splashText
		super().__init__(rect, colors, self.splashText, name, surface, drawData, textData, lists)
		self.ogBackgroundColor = self.backgroundColor
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]

		self.input = ""

		self.headerFontColor = textData.get("headerFontColor", self.fontColor)
		self.headerAlignText = textData.get("headerAlignText", "center")
		self.headerOffSet = textData.get("headerOffSet", [0, 0])

		self.growRect = drawData.get("growRect", False)
		self.header = drawData.get("header", False)
		self.replaceSplashText = drawData.get("replaceSplashText", True)
		self.CursorTime = drawData.get("CursorTime", self.DefaultCursorTime)

		self.darkenPercentage = drawData.get("darkenPercentage", 80)

		self.charLimit = inputData.get("charLimit", -1)

		self.nonAllowedKeysFilePath = inputData.get("nonAllowedKeysFilePath", None)
		self.allowedKeysFilePath = inputData.get("allowedKeysFilePath", None)
		self.closeOnMisInput = inputData.get("closeOnMisInput", True)

		self.nonAllowedKeys = set()
		self.allowedKeys = set()

		self.pointer = len(self.text)

		self.GetKeys()

		if type(self.header) == str:
			self.MakeHeader()

		self.active = False

		self.textSurface = self.font.render(str(self.text), True, self.fontColor)
		self.textRect = AlignText(self.rect, self.textSurface, self.alignText, self.borderWidth)

		self.t = 0
		self.step = 0.05

	def MakeHeader(self):
		self.headerTextSurface = self.font.render(self.header, True, self.headerFontColor)
		self.headerRect = pg.Rect(self.rect.x + self.headerOffSet[0], self.rect.y - (self.rect.h + self.borderWidth + self.headerOffSet[1]), self.rect.w, self.rect.h)
		self.headerTextRect = AlignText(self.headerRect, self.headerTextSurface, self.headerAlignText, self.borderWidth)

	def GetKeys(self):
		try:
			if self.nonAllowedKeysFilePath != None:
				path, name, fileType = SplitFileFromFolderPath(self.nonAllowedKeysFilePath)
				for char in OpenFile(name, f"/{path}", fileType):
					self.nonAllowedKeys.add(char)
		except:
			with open(self.nonAllowedKeysFilePath, "r") as file:
				data = file.read()
				for char in data:
					self.nonAllowedKeys.add(char)

				file.close()

		try:
			if self.allowedKeysFilePath != None:
				path, name, fileType = SplitFileFromFolderPath(self.allowedKeysFilePath)
				for char in OpenFile(name, f"/{path}", fileType):
					self.allowedKeys.add(char)
		except:
			with open(self.allowedKeysFilePath, "r") as file:
				data = file.read()
				for char in data:
					self.allowedKeys.add(char)

				file.close()

	def HandleEvent(self, event):
		if not self.disabled:
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.rect.collidepoint(pg.mouse.get_pos()):
						if type(allTextBoxs) == dict:
							for key in allTextBoxs:
								if allTextBoxs[key] != self:
									if allTextBoxs[key].active:
										return

						elif type(allTextBoxs) == list:
							for obj in allTextBoxs:
								if obj != self:
									if obj.active:
										return

						self.pointer = len(self.text)
						self.active = not self.active

						if self.active:
							self.borderColor = self.activeColor
							self.activeTime = dt.datetime.now()
						else:
							self.borderColor = self.inactiveColor
					else:
						if self.closeOnMisInput:
							self.active = False
							self.borderColor = self.inactiveColor

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_RETURN:
					if self.closeOnMisInput:
						self.active = False
						self.borderColor = self.inactiveColor

				if event.key == pg.K_RIGHT:
					self.pointer = min(len(self.text), self.pointer + 1)
				if event.key == pg.K_LEFT:
					if not self.replaceSplashText:
						self.pointer = max(len(self.splashText), self.pointer - 1)
					else:
						self.pointer = max(0, self.pointer - 1)

			if self.active:
				self.HandleKeyboard(event)

	def HandleKeyboard(self, event):
		if self.active:
			if self.replaceSplashText:
				textLength = len(self.text)
			else:
				textLength = len(self.text) - len(self.splashText)

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_BACKSPACE:
					if textLength != 0 and self.text != self.splashText:
						if self.pointer > 0:
							self.text = self.text[: self.pointer - 1] + self.text[self.pointer :]
							self.pointer = max(0, self.pointer - 1)

				elif event.key == pg.K_DELETE:
					if textLength != 0 and self.text != self.splashText:
						self.text = self.text[: self.pointer] + self.text[self.pointer + 1:]

				else:
					if event.key != pg.K_LEFT and event.key != pg.K_RIGHT and event.key != pg.K_TAB and event.key != pg.K_ESCAPE:
						self.FilterText(event.unicode)

				if self.text == "":
					self.text = self.splashText
					self.pointer = len(self.text)

				self.UpdateText(self.text)

		if self.replaceSplashText:
			self.input = self.text
		else:
			self.input = self.text[len(self.splashText):]

	def FilterText(self, key):
		self.activeTime = dt.datetime.now()
		if self.replaceSplashText:
			textLength = len(self.text)
		else:
			textLength = len(self.text) - len(self.splashText)

		if textLength + 1 <= self.charLimit or self.charLimit == -1:
			if self.replaceSplashText:
				if self.text == self.splashText:
					self.text = ""
		else:
			return

		if self.font.render(str(self.text + key), True, self.fontColor).get_width() + 2 >= self.rect.w:
			return

		if len(self.nonAllowedKeys) == 0:
			if len(self.allowedKeys) == 0:
				if self.pointer == len(self.text):
					self.text += key
				else:
					self.text = self.text[: self.pointer] + key + self.text[self.pointer:]
				self.pointer = min(len(self.text), self.pointer + 1)

			else:
				if key in self.allowedKeys:
					if self.pointer == len(self.text):
						self.text += key
					else:
						self.text = self.text[: self.pointer] + key + self.text[self.pointer :]
					self.pointer = min(len(self.text), self.pointer + 1)

		else:
			if len(self.allowedKeys) == 0:
				if key not in self.nonAllowedKeys:
					if self.pointer == len(self.text):
						self.text += key
					else:
						self.text = self.text[: self.pointer] + key + self.text[self.pointer :]
					self.pointer = min(len(self.text), self.pointer + 1)

			else:
				if key not in self.nonAllowedKeys:
					if key in self.allowedKeys:
						if self.pointer == len(self.text):
							self.text += key
						else:
							self.text = self.text[: self.pointer] + key + self.text[self.pointer :]
						self.pointer = min(len(self.text), self.pointer + 1)

		self.UpdateText(self.text)

	def Draw(self):
		if not self.disabled:
			self.DrawBackground()
			self.DrawBorder()
			self.DrawText()

			if self.rect.collidepoint(pg.mouse.get_pos()):
				if self.t < 1:
					self.t += self.step

				self.t = min(max(self.t, 0), 1)
				self.backgroundColor = LerpColor(self.backgroundColor, ChangeColorBrightness(self.ogBackgroundColor, self.darkenPercentage), self.t)
			else:
				if self.t > 0:
					self.t -= self.step

				self.t = min(max(self.t, 0), 1)
				self.backgroundColor = LerpColor(self.backgroundColor, self.ogBackgroundColor, self.t)

			if type(self.header) == str:
				pg.draw.rect(self.surface, self.ogBackgroundColor, self.headerRect)
				if not self.roundedCorners:
					DrawRectOutline(self.borderColor, self.headerRect, self.borderWidth, surface=self.surface)
				else:
					DrawRoundedRect(self.headerRect, (self.ogBackgroundColor, self.borderColor), self.roundness, self.borderWidth, self.activeCorners, self.surface)

				self.surface.blit(self.headerTextSurface, self.headerTextRect)

			if self.active:
				if self.CursorTime():
					pg.draw.rect(self.surface, self.fontColor, (self.textRect.x + (self.textSurface.get_width() / max(1, len(self.text)) * self.pointer), self.textRect.y + 3, 2, self.textSurface.get_height() - 6))

	def DefaultCursorTime(self):
		return dt.datetime.now().microsecond % 1000000 > 500000 or (dt.datetime.now() - self.activeTime).seconds <= 2

	def UpdateText(self, text):
		self.text = text
		self.CreateTextObjects()
		self.textSurface = self.font.render(str(self.text), True, self.fontColor)
		self.textRect = AlignText(self.rect, self.textSurface, self.alignText, self.borderWidth)


class Button(Label):
	def __init__(self, rect, colors, onClick=None, onClickArgs=[], text="", name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allButtons]):
		super().__init__(rect, colors, text, name, surface, drawData, textData, lists)

		self.onClick = onClick
		self.onClickArgs = onClickArgs
		# add on release 
		
		self.disabled = False
		self.active = inputData.get("active", False)
		self.result = None

		self.backgroundColor = colors[0]
		self.ogBackgroundColor = self.backgroundColor
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]
		self.borderColor = self.inactiveColor
		self.toggle = inputData.get("toggle", False)

		self.hint = drawData.get("hint", None)

		self.darkenPercentage = drawData.get("darkenPercentage", 80)

		self.keyBinds = inputData.get("keyBinds", {"activeType": pg.MOUSEBUTTONDOWN, "active": 1, "releaseType": pg.MOUSEBUTTONUP, "nameType": "mouse"})

		self.t = 0
		self.step = 0.05

	def Draw(self):
		if not self.disabled:
			self.DrawBackground()
			self.DrawBorder()
			self.DrawText()

			if self.hint != None:
				self.hint.Draw()

			if self.rect.collidepoint(pg.mouse.get_pos()):
				self.t += self.step

				self.t = min(max(self.t, 0), 1)
				self.backgroundColor = LerpColor(self.backgroundColor, ChangeColorBrightness(self.ogBackgroundColor, self.darkenPercentage), self.t)

			else:
				self.t -= self.step

				self.t = min(max(self.t, 0), 1)
				self.backgroundColor = LerpColor(self.ogBackgroundColor, self.backgroundColor, self.t)

	def HandleEvent(self, event):
		if not self.disabled:
			if self.rect.collidepoint(pg.mouse.get_pos()):
				if event.type == self.keyBinds["activeType"]:
					if self.keyBinds["nameType"] == "mouse":
						if event.button == self.keyBinds["active"]:
							if not self.toggle:
								self.Click()
							else:
								if self.active:
									self.Release()
								else:
									self.Click()

					elif self.keyBinds["nameType"] == "key":
						if event.key == self.keyBinds["active"]:
							if not self.toggle:
								self.Click()
							else:
								if self.active:
									self.Release()
								else:
									self.Click()

			if not self.toggle:
				if event.type == self.keyBinds["releaseType"]:
					if self.keyBinds["nameType"] == "mouse":
						if event.button == self.keyBinds["active"]:
							self.Release()

					elif self.keyBinds["nameType"] == "key":
						if event.key == self.keyBinds["active"]:
							self.Release()

	def Click(self):
		if self.disabled:
			return

		if callable(self.onClick):
			self.result = self.onClick(*self.onClickArgs)

		elif isinstance(self.onClick, Sequence):
			self.onClick.Start()

		self.active = True
		self.borderColor = self.activeColor

	def Release(self):
		self.active = False
		self.borderColor = self.inactiveColor


# add disabled var to all below

# slider - value change button rect function - test
class Slider(Label):
	def __init__(self, rect, colors, name="", surface=screen, drawData={}, textData={}, inputData={}, buttonData={}, lists=[allSliders]):
		super().__init__(rect, colors, name=name, surface=surface, drawData=drawData, textData=textData, lists=lists)

		self.isVertical = inputData.get("isVertical", True if self.rect.w < self.rect.h else False)
		self.startingValue = inputData.get("startingValue", 0)
		self.onValueChange = inputData.get("onValueChange", None)
		self.sliderButtonSize = drawData.get("sliderButtonSize", [self.rect.w / 10, self.rect.h] if not self.isVertical else [self.rect.w, self.rect.h / 10])

		self.buttonData = buttonData

		self.headerFontColor = textData.get("headerFontColor", self.fontColor)
		self.headerAlignText = textData.get("headerAlignText", "center")
		self.headerOffSet = textData.get("headerOffSet", [0, 0])

		self.header = drawData.get("header", False)

		if type(self.header) == str:
			self.MakeHeader()

		self.CreateSliderButton()

	def MakeHeader(self):
		self.headerTextSurface = self.font.render(self.header, True, self.headerFontColor)

		if not self.isVertical:
			self.headerRect = pg.Rect(self.rect.x + self.headerOffSet[0], self.rect.y - (self.rect.h + self.borderWidth + self.headerOffSet[1]), self.rect.w, self.rect.h)
		else:
			self.headerRect = pg.Rect(self.rect.x - (self.rect.h // 2) + (self.rect.w//2), self.rect.y - self.rect.w - 2, self.rect.h, self.rect.w)

		self.headerTextRect = AlignText(self.headerRect, self.headerTextSurface, self.headerAlignText, self.borderWidth)

	def CreateSliderButton(self):
		if self.isVertical:
			rect = pg.Rect(self.rect.x + self.borderWidth, self.rect.y + self.borderWidth, self.sliderButtonSize[0] - self.borderWidth * 2, self.sliderButtonSize[1])
		else:
			rect = pg.Rect(self.rect.x + self.borderWidth, self.rect.y + self.borderWidth, self.sliderButtonSize[0], self.sliderButtonSize[1] - self.borderWidth * 2)

		self.sliderButton = Button(rect, (self.buttonData.get("backgroundColor", self.backgroundColor), self.buttonData.get("inactiveColor", self.borderColor), self.buttonData.get("activeColor", InvertColor(self.borderColor))), onClick=self.GetMousePos, text=self.buttonData.get("text", ""), name=f"{self.name}'s sliderButton", surface=self.surface, drawData=self.buttonData.get("drawData", self.drawData), textData=self.buttonData.get("textData", {}), inputData=self.buttonData.get("inputData", {}), lists=[])
		self.SetValue(self.startingValue)

	def GetMousePos(self):
		self.startMousePos = pg.mouse.get_pos()
		self.startSliderButtonRect = pg.Rect(self.sliderButton.rect)

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()

		self.sliderButton.Draw()

		if type(self.header) == str:
			if not self.roundedCorners:
				pg.draw.rect(self.surface, self.backgroundColor, self.headerRect)
				DrawRectOutline(self.borderColor, self.headerRect, self.borderWidth, surface=self.surface)
			else:
				DrawRoundedRect(self.headerRect, (self.backgroundColor, self.borderColor), self.roundness, self.borderWidth, self.activeCorners, self.surface)

			self.surface.blit(self.headerTextSurface, self.headerTextRect)

	def HandleEvent(self, event):
		self.sliderButton.HandleEvent(event)

		if self.sliderButton.active:
			rect = MoveRectWithoutCenter(self.startMousePos, self.startSliderButtonRect)
			if not self.isVertical:
				self.sliderButton.rect.x = max(min(rect.x, self.rect.x + self.rect.w - self.borderWidth * 2 - self.sliderButton.rect.w), self.rect.x + self.borderWidth)
			else:
				self.sliderButton.rect.y = max(min(rect.y, self.rect.y + self.rect.h - self.borderWidth * 2 - self.sliderButton.rect.h), self.rect.y + self.borderWidth)

		self.GetValue()

	def GetValue(self, n=3):
		if not self.isVertical:
			self.value = round((self.sliderButton.rect.x - self.rect.x - self.borderWidth) / (self.rect.w - (self.borderWidth * 2) - self.sliderButton.rect.h), n)
		else:
			self.value = round((self.sliderButton.rect.y - self.rect.y - self.borderWidth) / (self.rect.h - (self.borderWidth * 2) - self.sliderButton.rect.h), n)

		if self.onValueChange != None:
			if callable(self.onValueChange):
				self.result = self.onValueChange(self.value)

		return self.value

	def SetValue(self, value):
		self.value = min(1, max(0, value))
		if not self.isVertical:
			self.sliderButton.rect.x = ((self.rect.w - (self.borderWidth * 2) - self.sliderButton.rect.h) * self.value) + self.borderWidth + self.rect.x
		else:
			self.sliderButton.rect.y = ((self.rect.h - (self.borderWidth * 2) - self.sliderButton.rect.h) * self.value) + self.borderWidth + self.rect.y


class ScollBar(Slider):
	def __init__(self, rect, colors, scrollObj, name="", surface=screen, drawData={}, textData={}, inputData={}, buttonData={}, keyBinds={}, lists=[allScrollBars]):
		self.scrollObj = scrollObj
		super().__init__(rect, colors, name=name, surface=surface, drawData=drawData, textData=textData, inputData=inputData, buttonData=buttonData, lists=lists)

		self.keyBinds = keyBinds
		self.scrollObj = scrollObj

	def HandleEvent(self, event):
		self.sliderButton.HandleEvent(event)

		if self.sliderButton.active:
			rect = MoveRectWithoutCenter(self.startMousePos, self.startSliderButtonRect)
			if not self.isVertical:
				self.sliderButton.rect.x = max(min(rect.x, self.rect.x + self.rect.w - self.borderWidth * 2 - self.sliderButton.rect.w), self.rect.x + self.borderWidth)
			else:
				self.sliderButton.rect.y = max(min(rect.y, self.rect.y + self.rect.h - self.borderWidth * 2 - self.sliderButton.rect.h), self.rect.y + self.borderWidth)

			self.Scroll()

		if self.rect.collidepoint(pg.mouse.get_pos()) or self.scrollObj.rect.collidepoint(pg.mouse.get_pos()):
			if event.type == pg.MOUSEBUTTONDOWN:
				# down
				if event.button == 5:
					self.ScrollDown()
				# up
				if event.button == 4:
					self.ScrollUp()

				self.UpdateRect()

			if event.type == pg.KEYDOWN:
				if event.key == self.keyBinds.get("scrollDown", pg.K_DOWN):
					self.ScrollDown()

				if event.key == self.keyBinds.get("scrollUp", pg.K_UP):
					self.ScrollUp()

				self.UpdateRect()

		self.GetValue()

	def ScrollUp(self):
		if hasattr(self.scrollObj, "scrollLevel"):
			if self.scrollObj.scrollLevel - 1 >= 0:
				self.scrollObj.scrollLevel -= 1

	def ScrollDown(self):
		if hasattr(self.scrollObj, "scrollLevel"):
			if self.scrollObj.scrollLevel + 1 <= len(self.scrollObj.textObjs) - (self.scrollObj.rect.h / self.scrollObj.textHeight // 2):
				self.scrollObj.scrollLevel += 1

	def Scroll(self):
		if hasattr(self.scrollObj, "scrollLevel"):
			self.GetValue()
			self.scrollObj.scrollLevel = max(0, self.value * len(self.scrollObj.textObjs) - (self.scrollObj.rect.h / self.scrollObj.textHeight // 2))

	def UpdateRect(self):
		try:
			if not self.isVertical:
				self.sliderButton.rect.x = self.rect.x + self.borderWidth + (self.scrollObj.scrollLevel / (len(self.scrollObj.textObjs) - 3) * (self.rect.w - self.sliderButton.rect.w - (self.borderWidth * 2)))
			else:
				self.sliderButton.rect.y = self.rect.y + self.borderWidth + (self.scrollObj.scrollLevel / (len(self.scrollObj.textObjs) - 3) * (self.rect.h - self.sliderButton.rect.h - (self.borderWidth * 2)))
		except ZeroDivisionError:
			pass


class ProgressBar(Box):
	def __init__(self, rect, colors, text="", name="", surface=screen, value=0, drawData={}, textData={}, headerData={}, lists=[allProgressBars]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		if headerData.get("enableHeader", True):
			self.header = Label((self.rect.x, self.rect.y - headerData.get("headerHeight", 35), headerData.get("headerWidth", self.rect.w), 35), colors, text, name, surface, drawData, textData, lists=[])
		else:
			self.header = None

		self.value = value

		self.bar = Box((self.rect.x + self.borderWidth, self.rect.y + self.borderWidth, self.rect.w * self.value - self.borderWidth * 2, self.rect.h - self.borderWidth * 2), (colors[2], colors[2]), drawData=drawData, lists=[])

		self.ChangeValue(value)

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()
		if self.header != None:
			self.header.Draw()
		self.bar.Draw()

	def ChangeValue(self, v):
		self.value = v
		self.bar.rect.w = self.rect.w * self.value - self.borderWidth * 2
		if self.roundedCorners:
			self.bar.roundness = self.roundness + self.value


class MessageBox(Label):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={"alignText": "center-top"}, inputData={}, messageBoxData={}, confirmButtonData={}, cancelButtonData={}, lists=[allMessageBoxs]):
		super().__init__(rect, colors, text=text, name=name, surface=screen, drawData=drawData, textData=textData, lists=lists)

		confirmButtonSize = confirmButtonData.get("size", (self.rect.w / 3, self.rect.h / 6))
		confirmButtonColors = confirmButtonData.get("colors", (colors[0], colors[1], InvertColor(colors[1])))
		confirmButtonTextData = confirmButtonData.get("textData", {})
		confirmButtonRect = confirmButtonData.get("rect", (self.rect.x + self.rect.w - confirmButtonSize[0] - 10, self.rect.y + self.rect.h - confirmButtonSize[1] - 10, confirmButtonSize[0], confirmButtonSize[1]))
		self.confirmButton = Button(confirmButtonRect, confirmButtonColors, onClick = confirmButtonData.get("onClick", print), onClickArgs = confirmButtonData.get("onclickArgs", ["confirm"] if confirmButtonData.get("onClick", print) == print else []), text = confirmButtonData.get("text", "Confirm"), name=confirmButtonData.get("name", f"{self.name}-confirmButton"), surface=self.surface, drawData=drawData, textData=confirmButtonTextData, inputData=confirmButtonData.get("inputData", {}), lists=[])

		cancelButtonSize = cancelButtonData.get("size", (self.rect.w / 3, self.rect.h / 6))
		cancelButtonColors = cancelButtonData.get("colors", (colors[0], colors[1], InvertColor(colors[1])))
		cancelButtonTextData = cancelButtonData.get("textData", {})
		cancelButtonRect = cancelButtonData.get("rect", (self.rect.x + self.rect.w - cancelButtonSize[0] - 20 - confirmButtonSize[0], self.rect.y + self.rect.h - cancelButtonSize[1] - 10, cancelButtonSize[0], cancelButtonSize[1]))
		self.cancelButton = Button(cancelButtonRect, cancelButtonColors, onClick = cancelButtonData.get("onClick", print), onClickArgs = cancelButtonData.get("onclickArgs", ["cancel"] if cancelButtonData.get("onClick", print) == print else []), text = cancelButtonData.get("text", "Cancel"), name=cancelButtonData.get("name", f"{self.name}-cancelButton"), surface=self.surface, drawData=drawData, textData=cancelButtonTextData, inputData=cancelButtonData.get("inputData", {}), lists=[])

		messageBoxButtonColors = messageBoxData.get("colors", (colors[0], colors[1]))
		messageBoxButtonTextData = messageBoxData.get("textData", {})
		messageBoxButtonRect = messageBoxData.get("rect", (self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 20, self.rect.h - (self.textHeight * len(self.textObjs)) * 2 - confirmButtonSize[1]))
		self.messageBox = Label(messageBoxButtonRect, messageBoxButtonColors, text = messageBoxData.get("text", "Message box"), name=messageBoxData.get("name", f"{self.name}-messageBox"), surface=self.surface, drawData=drawData, textData=messageBoxButtonTextData, lists=[])

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

		self.confirmButton.Draw()
		self.cancelButton.Draw()
		self.messageBox.Draw()

	def HandleEvent(self, event):
		self.confirmButton.HandleEvent(event)
		self.cancelButton.HandleEvent(event)


class HyperLink(Button):
	def __init__(self, rect, colors, url, text="", name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allHyperLinks]):
		super().__init__(rect, colors, self.OpenLink, [url], text if text != "" else url, name, surface, drawData, textData, inputData, lists)

	def OpenLink(self, url):
		webbrowser.open(url, new=2, autoraise=True)


class Switch(Box):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allSwitches]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		self.firstChoiceColor = colors[2]
		self.lastChoiceColor = colors[3]

		if text != "":
			self.header = Label((self.rect.x, self.rect.y - drawData.get("headerYoffSet", 50), self.rect.w, drawData.get("headerYoffSet", 50)), (self.backgroundColor, self.borderColor), text=text, name=name, surface=screen, drawData=drawData, textData=textData, lists=[])
		else:
			self.header = None

		TD = textData
		TD["alignText"] = inputData.get("optionAlignText", "center-top")
		self.firstChoice = Button((self.rect.x, self.rect.y, self.rect.w // 2, self.rect.h), (self.backgroundColor, self.borderColor, self.firstChoiceColor), text=inputData.get("firstChoiceText", ""), name=f"{self.name}_firstChoice", surface=self.surface, drawData=drawData, textData=TD, lists=[])
		self.lastChoice = Button((self.rect.x + self.rect.w // 2, self.rect.y, self.rect.w // 2, self.rect.h), (self.backgroundColor, self.borderColor, self.lastChoiceColor), text=inputData.get("lastChoiceText", ""), name=f"{self.name}_lastChoice", surface=self.surface, drawData=drawData, textData=TD, lists=[])

		self.activeChoice = self.firstChoice

	def HandleEvent(self, event):
		self.firstChoice.HandleEvent(event)
		self.lastChoice.HandleEvent(event)

		if self.activeChoice == self.firstChoice:
			if self.lastChoice.active:
				self.activeChoice = self.lastChoice
		else:
			if self.firstChoice.active:
				self.activeChoice = self.firstChoice

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()

		if self.header != None:
			self.header.Draw()

		self.firstChoice.Draw()
		self.lastChoice.Draw()

		if self.roundedCorners:
			if self.activeChoice.t <= 0.7:
				self.activeChoice.t = 0.7
			DrawRoundedRect((self.activeChoice.rect.x + self.borderWidth, self.activeChoice.rect.y + self.borderWidth, self.activeChoice.rect.w - self.borderWidth * 2, self.activeChoice.rect.h - self.borderWidth * 2), (LerpColor(self.activeChoice.activeColor, ChangeColorBrightness(self.activeChoice.activeColor, 80), self.activeChoice.t / 0.5), LerpColor(self.activeChoice.activeColor, ChangeColorBrightness(self.activeChoice.activeColor, 80), self.activeChoice.t / 0.5)), self.roundness, self.borderWidth, self.activeCorners, self.surface)
		else:
			if self.activeChoice.t <= 0.7:
				self.activeChoice.t = 0.7
			pg.draw.rect(self.surface, LerpColor(self.activeChoice.activeColor, ChangeColorBrightness(self.activeChoice.activeColor, 80), self.activeChoice.t / 0.5), (self.activeChoice.rect.x + self.borderWidth, self.activeChoice.rect.y + self.borderWidth, self.activeChoice.rect.w - self.borderWidth * 2, self.activeChoice.rect.h - self.borderWidth * 2))

		self.firstChoice.DrawText()
		self.lastChoice.DrawText()


class MultiselectButton(Label):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, optionData={}, lists=[allMultiselectButtons]):
		try:
			if "-" in textData["alignText"]:
				textData["alignText"] = textData["alignText"].split("-")[0] + "-top"
		except:
			textData["alignText"] = "top"

		self.drawData = drawData
		self.textData = textData

		super().__init__(rect, colors, text, name, surface, drawData, textData, lists)

		self.inactiveColor = colors[1]
		self.activeColor = colors[2]

		self.optionNames = optionData.get("options", [])
		self.numOfOptions = len(self.optionNames)
		self.optionAlignText = optionData.get("optionAlignText", self.alignText)
		self.startActiveOption = optionData.get("startActiveOption", 0)
		self.optionsWidth = optionData.get("optionsWidth", self.rect.w)
		self.optionsHeight = optionData.get("optionsHeight", self.textHeight + 10)
		self.isScrollable = optionData.get("isScrollable", False)
		self.allowNoSelection = optionData.get("allowNoSelection", False)
		self.xOffSet = optionData.get("xOffSet", 5)

		self.CreateOptions()

		self.activeSelection = self.options[optionData.get("activeSelection", self.startActiveOption)] if not self.allowNoSelection else None

	def CreateOptions(self):
		self.options = []

		drawData = self.drawData

		textData = self.textData

		textData["alignText"] = self.optionAlignText

		rect = pg.Rect(self.rect.x + self.borderWidth + self.xOffSet, self.rect.y + self.textHeight + 10, self.optionsWidth - (self.borderWidth + self.xOffSet) * 2, self.optionsHeight)
		for i in range(self.numOfOptions):
			self.options.append(Button(rect, (self.backgroundColor, self.inactiveColor, self.activeColor), text=self.optionNames[i], onClick=self.SelectButton, onClickArgs=[i], name=f"{self.name}-option-{self.optionNames[i]}", surface=self.surface, drawData=self.drawData, textData=self.textData, lists=[]))
			rect.y += self.optionsHeight + 2

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

		if self.activeSelection != None:
			self.activeSelection.borderColor = self.activeSelection.activeColor

		for option in self.options:
			option.Draw()

	def HandleEvent(self, event):
		for option in self.options:
			option.HandleEvent(event)

	def SelectButton(self, index):
		if self.allowNoSelection:
			if self.activeSelection == self.options[index]:
				self.activeSelection = None
			else:
				self.activeSelection = self.options[index]
		else:
			self.activeSelection = self.options[index]


# add custom button
# add better way to add buttons
class RadioButton(Label):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, buttons=[], lists=[allRadioButtons]):
		super().__init__(rect, colors, text, name, surface, drawData, textData, lists)

		self.buttons = buttons

	def AddButton(self, button):
		if type(button) == Button:
			self.buttons.append(button)
		elif type(button) == dict:
			rect = button.get("rect")
			colors = button.get("colors")
			onClick = button.get("onClick", None)
			onClickArgs = button.get("onClickArgs", [])
			text = button.get("text", "")
			name = button.get("name", "")
			drawData = button.get("drawData", {})
			textData = button.get("textData", {})
			inputData = button.get("inputData", {})

			self.buttons.append(Button(rect, colors, onClick, onClickArgs, text, name, drawData, textData, inputData))			

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

		for button in self.buttons:
			button.Draw()

	def HandleEvent(self, event):
		for button in self.buttons:
			button.HandleEvent(event)


# dropdown menu


# large text input box



class Collection:
	def __init__(self, objects=[], name="", addToList=True):
		self.objects = objects
		self.name = name

		if addToList:
			AddToListOrDict(allCollections, self, self.name if self.name != "" else f"collection-{len(self.objects)}")

	def Add(self, obj):
		self.objects.append(obj)

	def Draw(self):
		for obj in self.objects:
			obj.Draw()

	def HandleEvent(self, event):
		for obj in self.objects:
			if callable(getattr(obj, "HandleEvent", None)):
				obj.HandleEvent(event)


class ExpandableMenu(Box):
	def __init__(self, rect, colors, openButton=None, name="", surface=screen, drawData={}, textData={}, inputData={}, closedData={}, openData={}, options=Collection(), lists=[allExpandableMenus]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		self.openRect = pg.Rect(rect)
		self.closedRect = pg.Rect(rect[0], rect[1], closedData.get("size", [55, 55])[0], closedData.get("size", [55, 55])[1])

		self.closedData = closedData
		self.openData = openData

		self.rect = self.closedRect

		if type(openButton) == dict:
			self.openButton = Button(openButton.get("rect", (self.rect.x + 5, self.rect.y + 5, 45, 45)), openButton.get("colors", (colors)), self.ToggleMenu, [], openButton.get("text", "Open"), openButton.get("name", f"{name if name != '' else 'expandleMenu'}-toggleButton"), openButton.get("surface", surface), openButton.get("drawData", drawData), openButton.get("textData", textData), openButton.get("inputData", inputData), [])
		elif type(openButton) == Button:
			self.openButton = openButton
			self.openButton.onClick = self.ToggleMenu
		else:
			textData["fontSize"] = 15
			self.openButton = Button((self.rect.x + 5, self.rect.y + 5, 45, 45), colors, self.ToggleMenu, [], "Open", f"{name if name != '' else 'expandleMenu'}-toggleButton", surface, drawData, textData, inputData, [])

		self.opened = False
		self.options = options

	def ToggleMenu(self):
		self.opened = not self.opened

		if self.opened:
			self.rect = self.openRect
			if self.roundedCorners:
				self.roundness = self.openData.get("roundness", self.roundness)
		else:
			self.rect = self.closedRect
			if self.roundedCorners:
				self.roundness = self.closedData.get("roundness", self.roundness)
		
		self.openButton.UpdateText("Open" if not self.opened else "Close")

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()

		self.openButton.Draw()

		if self.opened:
			self.options.Draw()

	def HandleEvent(self, event):
		self.openButton.HandleEvent(event)

		if self.opened:
			self.options.HandleEvent(event)


def DrawAllGUIObjects():
	if type(points) == dict:
		for key in points:
			points[key].Draw()

	elif type(points) == list:
		for obj in points:
			obj.Draw()

	if type(lines) == dict:
		for key in lines:
			lines[key].Draw()

	elif type(lines) == list:
		for obj in lines:
			obj.Draw()

	if type(polygons) == dict:
		for key in polygons:
			polygons[key].Draw()

	elif type(polygons) == list:
		for obj in polygons:
			obj.Draw()

	if type(allBoxs) == dict:
		for key in allBoxs:
			allBoxs[key].Draw()

	elif type(allBoxs) == list:
		for obj in allBoxs:
			obj.Draw()

	if type(allLabels) == dict:
		for key in allLabels:
			allLabels[key].Draw()

	elif type(allLabels) == list:
		for obj in allLabels:
			obj.Draw()

	if type(allTextBoxs) == dict:
		for key in allTextBoxs:
			allTextBoxs[key].Draw()

	elif type(allTextBoxs) == list:
		for obj in allTextBoxs:
			obj.Draw()

	if type(allButtons) == dict:
		for key in allButtons:
			allButtons[key].Draw()

	elif type(allButtons) == list:
		for obj in allButtons:
			obj.Draw()

	if type(allSliders) == dict:
		for key in allSliders:
			allSliders[key].Draw()

	elif type(allSliders) == list:
		for obj in allSliders:
			obj.Draw()

	if type(allScrollBars) == dict:
		for key in allScrollBars:
			allScrollBars[key].Draw()

	elif type(allScrollBars) == list:
		for obj in allScrollBars:
			obj.Draw()

	if type(allMessageBoxs) == dict:
		for key in allMessageBoxs:
			allMessageBoxs[key].Draw()

	elif type(allMessageBoxs) == list:
		for obj in allMessageBoxs:
			obj.Draw()

	if type(allHyperLinks) == dict:
		for key in allHyperLinks:
			allHyperLinks[key].Draw()

	elif type(allHyperLinks) == list:
		for obj in allHyperLinks:
			obj.Draw()

	if type(allSwitches) == dict:
		for key in allSwitches:
			allSwitches[key].Draw()

	elif type(allSwitches) == list:
		for obj in allSwitches:
			obj.Draw()

	if type(allMultiselectButtons) == dict:
		for key in allMultiselectButtons:
			allMultiselectButtons[key].Draw()

	elif type(allMultiselectButtons) == list:
		for obj in allMultiselectButtons:
			obj.Draw()

	if type(allProgressBars) == dict:
		for key in allProgressBars:
			allProgressBars[key].Draw()

	elif type(allProgressBars) == list:
		for obj in allProgressBars:
			obj.Draw()

	if type(allRadioButtons) == dict:
		for key in allRadioButtons:
			allRadioButtons[key].Draw()

	elif type(allRadioButtons) == list:
		for obj in allRadioButtons:
			obj.Draw()

	if type(allCollections) == dict:
		for key in allCollections:
			allCollections[key].Draw()

	elif type(allCollections) == list:
		for obj in allCollections:
			obj.Draw()

	if type(allExpandableMenus) == dict:
		for key in allExpandableMenus:
			allExpandableMenus[key].Draw()

	elif type(allExpandableMenus) == list:
		for obj in allExpandableMenus:
			obj.Draw()


def HandleGui(event):
	if type(allTextBoxs) == dict:
		for key in allTextBoxs:
			allTextBoxs[key].HandleEvent(event)
	else:
		for obj in allTextBoxs:
			obj.HandleEvent(event)

	if type(allButtons) == dict:
		for key in allButtons:
			allButtons[key].HandleEvent(event)
	else:
		for obj in allButtons:
			obj.HandleEvent(event)

	if type(allSliders) == dict:
		for key in allSliders:
			allSliders[key].HandleEvent(event)
	else:
		for obj in allSliders:
			obj.HandleEvent(event)

	if type(allScrollBars) == dict:
		for key in allScrollBars:
			allScrollBars[key].HandleEvent(event)
	else:
		for obj in allScrollBars:
			obj.HandleEvent(event)

	if type(allMessageBoxs) == dict:
		for key in allMessageBoxs:
			allMessageBoxs[key].HandleEvent(event)
	else:
		for obj in allMessageBoxs:
			obj.HandleEvent(event)

	if type(allHyperLinks) == dict:
		for key in allHyperLinks:
			allHyperLinks[key].HandleEvent(event)
	else:
		for obj in allHyperLinks:
			obj.HandleEvent(event)

	if type(allSwitches) == dict:
		for key in allSwitches:
			allSwitches[key].HandleEvent(event)
	else:
		for obj in allSwitches:
			obj.HandleEvent(event)

	if type(allMultiselectButtons) == dict:
		for key in allMultiselectButtons:
			allMultiselectButtons[key].HandleEvent(event)
	else:
		for obj in allMultiselectButtons:
			obj.HandleEvent(event)

	if type(allRadioButtons) == dict:
		for key in allRadioButtons:
			allRadioButtons[key].Draw()

	elif type(allRadioButtons) == list:
		for obj in allRadioButtons:
			obj.Draw()

	if type(allCollections) == dict:
		for key in allCollections:
			allCollections[key].HandleEvent(event)
	else:
		for obj in allCollections:
			obj.HandleEvent(event)

	if type(allExpandableMenus) == dict:
		for key in allExpandableMenus:
			allExpandableMenus[key].HandleEvent(event)
	else:
		for obj in allExpandableMenus:
			obj.HandleEvent(event)



if __name__ == "__main__":
	def DrawLoop():
		screen.fill(darkGray)

		DrawAllGUIObjects()

		for vector in all2DVectors:
			DrawVector(vector, (white, white))


		pg.display.update()

	def HandleEvents(event):
		HandleGui(event)

	def CreateTests():
		Box((50, 50, 100, 100), (lightBlack, white), drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}})
		Label((50, 160, 100, 100), (lightBlack, white), drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}}, text="This is\nsome\ntext", textData={"alignText": "center-top", "fontName": "comic-sans", "fontSize": 20, "fontColor": white})
		Button((50, 270, 100, 100), (lightBlack, white, lightRed), onClick=print, onClickArgs=[1, 2, 3, 4, 5])
		TextInputBox((50, 450, 300, 35), (lightBlack, white, lightRed), "Splash:", textData={"alignText": "left"}, drawData={"header": "HEADER"})
		TextInputBox((50, 500, 300, 35), (lightBlack, white, lightRed), "Splash:", textData={"alignText": "left"}, drawData={"header": None})

		Slider((50, 600, 300, 35), (lightBlack, darkWhite), drawData={"header": "HEADER", "roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}}, buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed})
		Slider((360, 400, 35, 300), (lightBlack, darkWhite), drawData={"header": "HEADER", "roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}}, buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed})
		Slider((50, 650, 300, 35), (lightBlack, darkWhite), buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}, "background": True})
		Slider((440, 410, 35, 290), (lightBlack, darkWhite), buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}, "background": True})

		scroll_label_1 = Label((540, 490, 150, 150), (lightBlack, darkWhite), text="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velitesse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", textData={"fontSize": 18, "alignText": "center-top"})
		scroll_label_2 = Label((700, 490, 150, 150), (lightBlack, darkWhite), text="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velitesse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", textData={"fontSize": 18, "alignText": "center-top"})
		ScollBar((540, 640, 150, 25), (lightBlack, darkWhite), buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, scrollObj=scroll_label_1, name="horizontal")
		ScollBar((850, 490, 25, 150), (lightBlack, darkWhite), buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, scrollObj=scroll_label_2, name="vertical")

		MessageBox((180, 10, 300, 200), (lightBlack, darkWhite), text="Message box title", messageBoxData={"colors": (lightBlack, darkWhite), "text": "This is message box"}, confirmButtonData={"colors": (lightBlack, darkWhite, lightRed)}, cancelButtonData={"colors": (lightBlack, darkWhite, lightRed)})

		h = HyperLink((180, 230, 200, 50), (lightBlack, white, lightRed), "https://www.youtube.com/", "YouTube")
		h.hint = Hint((180, 285, 200, 50), (lightBlack, white), h, "https://www.youtube.com/", textData={"fontSize": 15})

		Switch((540, 160, 200, 100), (lightBlack, white, lightRed, lightBlue), text="Switch", inputData={"firstChoiceText": "First\nchoice", "lastChoiceText": "Last\nchoice"})
		Switch((540, 270, 200, 100), (lightBlack, white, lightRed, lightBlue), drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}})
		Switch((540, 380, 200, 100), (lightBlack, white, lightRed, lightBlue), inputData={"firstChoiceText": "First\nchoice", "lastChoiceText": "Last\nchoice"}, textData={"alignText": "center-top"}, drawData={"roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False, "topRight": False}})

		MultiselectButton((750, 50, 200, 200), (lightBlack, white, lightRed), "Mutli-select button", optionData={"options": ["option 1", "option 2", "option 3", "option 4"]})
		MultiselectButton((960, 50, 200, 200), (lightBlack, white, lightRed), "Mutli-select button", optionData={"options": ["option 1", "option 2", "option 3", "option 4"], "allowNoSelection": True, "optionAlignText": "top"})

		c1 = Collection([
			Label((805, 265, 140, 45), (lightBlack, white), text="Expandable Menu", textData={"fontSize": 17}, lists=[]),
			Button((755, 315, 190, 50), (lightBlack, white, lightRed), text="Button 1", lists=[], onClick=print, onClickArgs=[1]),
			Button((755, 370, 190, 50), (lightBlack, white, lightRed), text="Button 2", lists=[], onClick=print, onClickArgs=[2]),
			Button((755, 425, 190, 50), (lightBlack, white, lightRed), text="Button 3", lists=[], onClick=print, onClickArgs=[3]),
			Button((755, 480, 190, 50), (lightBlack, white, lightRed), text="Button 4", lists=[], onClick=print, onClickArgs=[4]),
			Button((755, 535, 190, 50), (lightBlack, white, lightRed), text="Button 5", lists=[], onClick=print, onClickArgs=[5]),
			Button((755, 590, 190, 50), (lightBlack, white, lightRed), text="Button 6", lists=[], onClick=print, onClickArgs=[6])
			], addToList=False)

		c2 = Collection([
			Label((865, 265, 140, 45), (lightBlack, white), text="Expandable Menu", textData={"fontSize": 17}, lists=[], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 315, 190, 50), (lightBlack, white, lightRed), text="Button 1", lists=[], onClick=print, onClickArgs=[1], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 370, 190, 50), (lightBlack, white, lightRed), text="Button 2", lists=[], onClick=print, onClickArgs=[2], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 425, 190, 50), (lightBlack, white, lightRed), text="Button 3", lists=[], onClick=print, onClickArgs=[3], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 480, 190, 50), (lightBlack, white, lightRed), text="Button 4", lists=[], onClick=print, onClickArgs=[4], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 535, 190, 50), (lightBlack, white, lightRed), text="Button 5", lists=[], onClick=print, onClickArgs=[5], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1}),
			Button((815, 590, 190, 50), (lightBlack, white, lightRed), text="Button 6", lists=[], onClick=print, onClickArgs=[6], drawData={"roundedCorners": True, "roundness": 5, "borderWidth": 1})
			], addToList=False)

		ExpandableMenu((750, 260, 200, 385), (lightBlack, darkWhite, lightRed), options=c1)
		ExpandableMenu((810, 260, 200, 385), (lightBlack, darkWhite, lightRed), options=c2, drawData={"roundedCorners": True, "roundness": 5}, closedData={"roundness": 5}, openData={"roundness": 20}, openButton={"drawData": {"roundedCorners": True, "roundness": 5, "borderWidth": 1}})

		ProgressBar((900, 520, 200, 35), (lightBlack, darkWhite, lightRed), text="Progress", value=0.7)
		pb2 = ProgressBar((900, 600, 200, 35), (lightBlack, darkWhite, lightRed), text="Progress", drawData={"roundedCorners": True, "roundness": 3}, value=0.2)

		# RadioButton((960, 260, 200, 200), (lightBlack, darkWhite), text="Radio Button", textData={"alignText": "top"})

	CreateTests()

	# Vec2.origin = (width // 2, height // 2)

	n = 100
	for x in range(width // n):
		for y in range(height // n):
			Vec2((x + 1) * n, (y + 1) * n)



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

		DrawLoop()
