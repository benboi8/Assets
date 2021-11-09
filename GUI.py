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
allLabels = {}
allTextBoxs = {}
allButtons = {}

fontName = "arial"

def ChangeFontName(name):
	global fontName
	fontName = name


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

		AddToListOrDict(lists, self)

	def Draw(self):
		# draw background
		if self.drawBackground:
			pg.draw.rect(self.surface, self.backgroundColor, self.rect)

		# draw border
		if self.drawBorder:
			DrawRectOutline(self.foregroundColor, self.rect, self.borderWidth, surface=self.surface)


class Label(Box):
	def __init__(self, rect, colors, text="", name="", surface=screen, drawData={}, textData={}, lists=[allLabels]):
		super().__init__(rect, colors, name, surface, drawData, lists)

		self.text = text
		self.fontSize = textData.get("fontSize", 24)
		self.fontName = textData.get("fontName", fontName)
		self.fontColor = textData.get("fontColor", white)
		self.alignText = textData.get("alignText", "center")
		self.multiline = textData.get("multiline", False)

		self.CreateTextObj()

	def CreateTextObj(self):
		self.textObjs = []
		try:
			self.font = pg.font.Font(self.fontName, self.fontSize)
		except FileNotFoundError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)
		except TypeError:
			self.font = pg.font.SysFont(self.fontName, self.fontSize)

		if not self.multiline:
			self.textSurface = self.font.render(str(self.text).strip("\n"), True, self.fontColor)
			self.textRect = AlignText(self.rect, self.textSurface, self.alignText, self.borderWidth)
			self.textObjs.append((self.textSurface, self.textRect))
		else:
			self.GetTextObjects()

	def GetTextObjects(self):
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
		# draw background
		if self.drawBackground:
			pg.draw.rect(self.surface, self.backgroundColor, self.rect)

		# draw border
		if self.drawBorder:
			DrawRectOutline(self.foregroundColor, self.rect, self.borderWidth)

		self.DrawText()

	def DrawText(self):
		for obj in self.textObjs:
			self.surface.blit(obj[0], obj[1])

	def UpdateText(self, text):
		self.text = text
		self.CreateTextObj()


class TextInputBox(Label):
	def __init__(self, rect, colors, name="", surface=screen, drawData={}, textData={}, inputData={}, lists=[allTextBoxs]):
		self.splashText = inputData.get("splashText", "Type here.")
		super().__init__(rect, colors, self.splashText, name, surface, drawData, textData, lists)
		self.backgroundColor = colors[0]
		self.inactiveColor = colors[1]
		self.activeColor = colors[2]
		self.foregroundColor = self.inactiveColor

		self.textColor = textData.get("textColor", white)

		self.charLimit = inputData.get("charLimit", -1)

		self.input = ""

		self.growRect = drawData.get("growRect", False)
		self.header = drawData.get("header", False)
		self.replaceSplashText = drawData.get("replaceSplashText", True)

		self.nonAllowedKeysFilePath = inputData.get("nonAllowedKeysFile", None)
		self.allowedKeysFilePath = inputData.get("allowedKeysFile", None)

		self.nonAllowedKeysList = inputData.get("nonAllowedKeysList", [])
		self.allowedKeysList = inputData.get("allowedKeysList", [])

		self.nonAllowedKeys = set()
		self.allowedKeys = set()

		self.pointer = len(self.text)

		self.GetKeys()

		if type(self.header) == str:
			self.MakeHeader()

		self.active = False

	def MakeHeader(self):
		self.headerTextSurface = self.font.render(self.header, True, self.textColor)
		self.headerRect = AlignText(self.rect, self.headerTextSurface, "center-top", self.borderWidth)
		self.rect.h += self.headerTextSurface.get_height() // 2
		try:
			if self.alignText.split("-")[1] == "top":
				self.alignText = self.alignText.split("-")[0]
		except:
			pass

	def GetKeys(self):
		if self.nonAllowedKeysFilePath != None:
			with open(self.nonAllowedKeysFilePath, "r") as nonAllowedKeysFile:
				nonAllowedKeysText = nonAllowedKeysFile.read()
				for char in nonAllowedKeysText:
					self.nonAllowedKeys.add(char)

		for char in self.nonAllowedKeysList:
			self.nonAllowedKeys.add(char)

		if self.allowedKeysFilePath != None:
			with open(self.allowedKeysFilePath, "r") as allowedKeysFile:
				allowedKeysText = allowedKeysFile.read()
				for char in allowedKeysText:
					self.allowedKeys.add(char)

		for char in self.allowedKeysList:
			self.allowedKeys.add(char)

	def HandleEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if self.rect.collidepoint(pg.mouse.get_pos()):
					self.pointer = len(self.text)
					self.active = not self.active
					if self.active:
						self.foregroundColor = self.activeColor
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
						self.text = self.text[: self.pointer - 1] + self.text[self.pointer :]
						self.pointer = max(len(self.splashText), self.pointer - 1)
				elif event.key == pg.K_DELETE:
					if textLength != 0 and self.text != self.splashText:
						self.text = self.text[: self.pointer] + self.text[self.pointer + 1:]
				else:
					if event.key != pg.K_LEFT and event.key != pg.K_RIGHT:
						self.FilterText(event.unicode)

				if self.text == "":
					self.text = self.splashText
				self.UpdateText()

		if self.replaceSplashText:
			self.input = self.text
		else:
			self.input = self.text[len(self.splashText):]

	def FilterText(self, key):
		if self.replaceSplashText:
			textLength = len(self.text)
		else:
			textLength = len(self.text) - len(self.splashText)

		if textLength + 1 <= self.charLimit or self.charLimit == -1:
			if self.replaceSplashText:
				if self.text == self.splashText:
					self.text = ""

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
						if key in self.allowedKeys:
							if self.pointer == len(self.text):
								self.text += key
							else:
								self.text = self.text[: self.pointer] + key + self.text[self.pointer :]
							self.pointer = min(len(self.text), self.pointer + 1)

				else:
					if key not in self.nonAllowedKeys:
						if self.pointer == len(self.text):
							self.text += key
						else:
							self.text = self.text[: self.pointer] + key + self.text[self.pointer :]
						self.pointer = min(len(self.text), self.pointer + 1)

	def Draw(self):
		pg.draw.rect(self.surface, self.backgroundColor, self.rect)
		DrawRectOutline(self.foregroundColor, self.rect, surface=self.surface, width=self.borderWidth)

		if self.active:
			if dt.datetime.now().microsecond % 1000000 > 500000:
				pg.draw.rect(self.surface, self.textColor, (self.textRect.x + (self.textSurface.get_width() / max(1, len(self.text)) * self.pointer), self.textRect.y, 2, self.textSurface.get_height()))

		self.surface.blit(self.textSurface, self.textRect)

		if type(self.header) == str:
			self.surface.blit(self.headerTextSurface, self.headerRect)

	def ClearText(self):
		self.text = self.splashText
		self.input = self.text
		self.UpdateText()

	def UpdateText(self):
		self.textSurface = self.font.render(self.text, True, self.textColor)
		if self.growRect:
			self.rect.w = max(self.rect.w, self.textSurface.get_width() + 12)


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

		self.keyBinds = inputData.get("keyBinds", {"clickType": pg.MOUSEBUTTONDOWN, "active": 1, "releaseType": pg.MOUSEBUTTONUP, "nameType": "mouse"})

	def HandleEvent(self, event):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			if event.type == self.keyBinds["clickType"]:
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


def DrawAllGUIObjects():
	for key in points:
		points[key].Draw()

	for key in lines:
		lines[key].Draw()

	for key in polygons:
		polygons[key].Draw()

	for key in allBoxs:
		allBoxs[key].Draw()

	for key in allLabels:
		allLabels[key].Draw()
		allLabels[key].DrawText()

	for key in allTextBoxs:
		allTextBoxs[key].Draw()

	for key in allButtons:
		allButtons[key].Draw()


def HandleGui(event):
	for key in allTextBoxs:
		allTextBoxs[key].HandleEvent(event)

	for key in allButtons:
		allButtons[key].HandleEvent(event)


if __name__ == "__main__":

	def DrawLoop():
		screen.fill(darkGray)

		DrawAllGUIObjects()

		pg.display.update()

	def HandleEvents(event):
		HandleGui(event)


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
