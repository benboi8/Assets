from General import *
from colors import *

import pygame as pg
from pygame import *
from pygame import gfxdraw

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



def DrawVector(vector, colors, magnitude=None, directionPoint=centerOfScreen, radius=3, surface=screen):
	if magnitude == None:
		magnitude = vector.Magnitude()

	pg.draw.circle(surface, colors[0], (vector.x, vector.y), radius)
	d = vector.Direction(directionPoint)
	pg.draw.line(surface, colors[1], (vector.x, vector.y), (vector.x + (d[0] * magnitude), vector.y + (d[1] * magnitude)))


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


def DrawRoundedRect(rect, colors, roundness=2, borderWidth=2, activeCorners={}, surface=screen):
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


		# connecting d
		# top
		pg.draw.aaline(surface, borderColor, (offSetRectX.x, rect.y + i), (offSetRectX.x + offSetRectX.w, rect.y + i))

		# bottom
		pg.draw.aaline(surface, borderColor, (offSetRectX.x, rect.y + i + rect.h - borderWidth // 2), (offSetRectX.x + offSetRectX.w, rect.y + i + rect.h - borderWidth // 2))

		# left
		pg.draw.aaline(surface, borderColor, (rect.x + i, offSetRectY.y), (rect.x + i, offSetRectY.y + offSetRectY.h))

		# right
		pg.draw.aaline(surface, borderColor, (rect.x + i + rect.w - borderWidth // 2, offSetRectY.y), (rect.x + i + rect.w - borderWidth // 2, offSetRectY.y + offSetRectY.h))


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
		self.foregroundColor = colors[1]
		self.name = name
		self.surface = surface
		self.drawData = drawData

		self.drawBorder = drawData.get("drawBorder", True)
		self.borderWidth = drawData.get("borderWidth", 2)
		self.drawBackground = drawData.get("drawBackground", True)
		self.roundedCorners = drawData.get("roundedCorners", False)
		self.roundness = drawData.get("roundness", 4)
		self.activeCorners = drawData.get("activeCorners", {})

		AddToListOrDict(lists, self)

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()

	def DrawBackground(self):
		if not self.roundedCorners:
			# draw background
			if self.drawBackground:
				pg.draw.rect(self.surface, self.backgroundColor, self.rect)

	def DrawBorder(self):
		if not self.roundedCorners:
			# draw border
			if self.drawBorder:
				DrawRectOutline(self.foregroundColor, self.rect, self.borderWidth, surface=self.surface)
		else:
			DrawRoundedRect(self.rect, (self.backgroundColor, self.foregroundColor), self.roundness, self.borderWidth, self.activeCorners, self.surface)


class Label(Box):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, lists=[allLabels]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		self.text = text
		self.fontSize = textData.get("fontSize", fontSize)
		self.fontName = textData.get("fontName", fontName)
		self.fontColor = textData.get("fontColor", white)
		self.alignText = textData.get("alignText", "center")

		self.CreateTextObjects()

	def CreateTextObjects(self):
		try:
			self.font = pg.font.Font(self.fontName, self.fontSize)
		except FileNotFoundError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)
		except TypeError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)
		except:
			print(f"ERROR: Font '{self.fontName}' not found{f' for obj with name {self.name}' if self.name != '' else f'. Obj has no name. Text is: [{self.text}]'}\nEnd of text. Font has defaulted to arial.\n Note that some other error may have occured.")
			self.font = pg.font.SysFont("arial", self.fontSize)

		self.textObjs = []
		self.text = str(self.text)
		if "\\n" in self.text:
			text = self.text.split("\\n")
		else:
			text = self.text.split("\n")

		rect = self.rect
		for i, t in enumerate(text):
			textSurface = self.font.render(str(t), True, self.fontColor)
			self.textObjs.append((textSurface, AlignText(pg.Rect(rect.x, rect.y + (i * textSurface.get_height()), rect.w, rect.h), textSurface, self.alignText, self.borderWidth)))

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

	def DrawText(self):
		for obj in self.textObjs:
			self.surface.blit(obj[0], obj[1])

	def UpdateText(self, text):
		self.text = text
		self.CreateTextObjects()


# testing, data validation
class TextInputBox(Label):
	def __init__(self, rect, colors, splashText="Type here:", name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allTextBoxs]):
		self.splashText = splashText
		super().__init__(rect, colors, self.splashText, name, surface, drawData, textData, lists)
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]

		self.input = ""

		self.headerFontColor = textData.get("headerFontColor", self.fontColor)
		self.headerAlignText = textData.get("headerAlignText", "center")
		self.headerOffSet = textData.get("headerOffSet", [0, 0])

		self.growRect = drawData.get("growRect", False)
		self.header = drawData.get("header", False)
		self.replaceSplashText = drawData.get("replaceSplashText", True)

		self.charLimit = inputData.get("charLimit", -1)

		self.nonAllowedKeysFilePath = inputData.get("nonAllowedKeysFilePath", None)
		self.allowedKeysFilePath = inputData.get("allowedKeysFilePath", None)

		self.nonAllowedKeys = set()
		self.allowedKeys = set()

		self.pointer = len(self.text)

		self.GetKeys()

		if type(self.header) == str:
			self.MakeHeader()

		self.active = False

		self.textSurface = self.font.render(str(self.text), True, self.fontColor)
		self.textRect = AlignText(self.rect, self.textSurface, self.alignText, self.borderWidth)

	def MakeHeader(self):
		self.headerTextSurface = self.font.render(self.header, True, self.headerFontColor)
		self.headerRect = pg.Rect(self.rect.x + self.headerOffSet[0], self.rect.y - (self.rect.h + self.borderWidth + self.headerOffSet[1]), self.rect.w, self.rect.h)
		self.headerTextRect = AlignText(self.headerRect, self.headerTextSurface, self.headerAlignText, self.borderWidth)

	def GetKeys(self):
		if self.nonAllowedKeysFilePath != None:
			path, name, fileType = SplitFileFromFolderPath(self.nonAllowedKeysFilePath)
			for char in OpenFile(name, f"/{path}", fileType):
				self.nonAllowedKeys.add(char)

		if self.allowedKeysFilePath != None:
			path, name, fileType = SplitFileFromFolderPath(self.allowedKeysFilePath)
			for char in OpenFile(name, f"/{path}", fileType):
				self.allowedKeys.add(char)

	def HandleEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if self.rect.collidepoint(pg.mouse.get_pos()):
					self.pointer = len(self.text)
					self.active = not self.active
					if self.active:
						self.foregroundColor = self.activeColor
						self.activeTime = dt.datetime.now()
					else:
						self.foregroundColor = self.inactiveColor
				else:
					self.active = False
					self.foregroundColor = self.inactiveColor

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_RETURN:
				self.active = False
				self.foregroundColor = self.inactiveColor

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
		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

		if type(self.header) == str:
			pg.draw.rect(self.surface, self.backgroundColor, self.headerRect)
			if not self.roundedCorners:
				DrawRectOutline(self.foregroundColor, self.headerRect, self.borderWidth, surface=self.surface)
			else:
				DrawRoundedRect(self.headerRect, (self.backgroundColor, self.foregroundColor), self.roundness, self.borderWidth, self.activeCorners, self.surface)

			self.surface.blit(self.headerTextSurface, self.headerTextRect)

		if self.active:
			if dt.datetime.now().microsecond % 1000000 > 500000 or (dt.datetime.now() - self.activeTime).seconds <= 2:
				pg.draw.rect(self.surface, self.fontColor, (self.textRect.x + (self.textSurface.get_width() / max(1, len(self.text)) * self.pointer), self.textRect.y + 3, 2, self.textSurface.get_height() - 6))

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
		self.disabled = False
		self.active = False
		self.result = None

		self.backgroundColor = colors[0]
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]
		self.foregroundColor = self.inactiveColor
		self.toggle = inputData.get("toggle", False)

		self.keyBinds = inputData.get("keyBinds", {"activeType": pg.MOUSEBUTTONDOWN, "active": 1, "releaseType": pg.MOUSEBUTTONUP, "nameType": "mouse"})

	def HandleEvent(self, event):
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
		self.foregroundColor = self.activeColor

	def Release(self):
		self.active = False
		self.foregroundColor = self.inactiveColor


class Slider(Label):
	def __init__(self, rect, colors, name="", surface=screen, drawData={}, textData={}, inputData={}, buttonData={}, lists=[allSliders]):
		super().__init__(rect, colors, name=name, surface=surface, drawData=drawData, textData=textData, lists=lists)

		self.isVertical = inputData.get("isVertical", True if self.rect.w < self.rect.h else False)
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

		self.sliderButton = Button(rect, (self.buttonData.get("backgroundColor", self.backgroundColor), self.buttonData.get("inactiveColor", self.foregroundColor), self.buttonData.get("activeColor", ReverseColor(self.foregroundColor))), onClick=self.GetMousePos, text=self.buttonData.get("text", ""), name=f"{self.name}'s sliderButton", surface=self.surface, drawData=self.buttonData.get("drawData", self.drawData), textData=self.buttonData.get("textData", {}), inputData=self.buttonData.get("inputData", {}), lists=[])

	def GetMousePos(self):
		self.startMousePos = pg.mouse.get_pos()
		self.startSliderButtonRect = pg.Rect(self.sliderButton.rect)

	def Draw(self):
		self.DrawBackground()
		self.DrawBorder()

		self.sliderButton.Draw()

		if type(self.header) == str:
			pg.draw.rect(self.surface, self.backgroundColor, self.headerRect)
			if not self.roundedCorners:
				DrawRectOutline(self.foregroundColor, self.headerRect, self.borderWidth, surface=self.surface)
			else:
				DrawRoundedRect(self.headerRect, (self.backgroundColor, self.foregroundColor), self.roundness, self.borderWidth, self.activeCorners, self.surface)

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

		return self.value


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
			allLabels[key].DrawText()

	elif type(allLabels) == list:
		for obj in allLabels:
			obj.Draw()
			obj.DrawText()

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



if __name__ == "__main__":

	def DrawLoop():
		screen.fill(darkGray)

		DrawAllGUIObjects()

		pg.display.update()

	def HandleEvents(event):
		HandleGui(event)

	Box((50, 50, 100, 100), (lightBlue, lightRed), drawData={"borderWidth": 2, "roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}})
	Label((50, 160, 100, 100), (lightBlue, lightRed), drawData={"borderWidth": 2, "roundedCorners": True, "roundness": 3, "activeCorners": {"topLeft": False}}, text="This is\nsome\ntext", textData={"alignText": "center-top", "fontName": "comic-sans", "fontSize": 20, "fontColor": black})
	Button((50, 270, 100, 100), (lightBlue, lightRed, white), onClick=print, onClickArgs=[1, 2, 3, 4, 5])
	TextInputBox((50, 450, 300, 35), (lightBlack, lightRed, white), "Splash:", textData={"alignText": "left"}, drawData={"header": "HEADER"})
	TextInputBox((50, 500, 300, 35), (lightBlack, lightRed, white), "Splash:", textData={"alignText": "left"}, drawData={"header": None})

	Slider((50, 600, 300, 35), (lightBlack, lightRed), drawData={"header": "HEADER"}, buttonData={"backgroundColor": black, "inactiveColor": black, "activeColor": lightBlue})
	Slider((360, 400, 35, 300), (lightBlack, lightRed), drawData={"header": "HEADER"}, buttonData={"backgroundColor": black, "inactiveColor": black, "activeColor": lightBlue})
	Slider((50, 650, 300, 35), (lightBlack, lightRed), buttonData={"backgroundColor": black, "inactiveColor": black, "activeColor": lightBlue})
	Slider((440, 410, 35, 290), (lightBlack, lightRed), buttonData={"backgroundColor": black, "inactiveColor": black, "activeColor": lightBlue})

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
