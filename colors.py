from random import *
from General import Lerp, Constrain, Map


class Color(tuple):
	mode = (0, 255)
	allColors = []

	def ChangeMode(mode):
		prevMode = Color.mode
		Color.mode = mode
		for color in Color.allColors:
			color.Mode(prevMode)

	def HSVToRGB(hue, sat, value):
		# chroma
		C = value * sat

		# H prime
		Hp = hue / 60

		X = C * (1 - abs((Hp  % 2) - 1))

		if 0 <= Hp < 1:
			r, g, b = C, X, 0

		if 1 <= Hp < 2:
			r, g, b = X, C, 0

		if 2 <= Hp < 3:
			r, g, b = 0, C, X

		if 3 <= Hp < 4:
			r, g, b = 0, X, C

		if 4 <= Hp < 5:
			r, g, b = X, 0, C

		if 5 <= Hp < 6:
			r, g, b = C, 0, X

		m = value - C

		return Color((int(r + m), int(g + m), int(b + m)))

	def RGBToHex(color):
		return f"#{hex(color[0])[2:].zfill(2)}{hex(color[1])[2:].zfill(2)}{hex(color[2])[2:].zfill(2)}"

	def HexToRGB(hexString):
		hexString = hexString.strip("#").strip(" ")
		if len(hexString) == 6:
			return Color((int(hexString[0:2], 16), int(hexString[2:4], 16), int(hexString[4:6], 16)))
		else:
			raise ValueError("Hex string not 6 characters")

	def __init__(self, color):
		super().__init__()

		self.r = color[0]
		self.g = color[1]
		self.b = color[2]
		self.a = Color.mode[1]
		if len(color) == 4:
			self.a = color[3]

		Color.allColors.append(self)

	def Mode(self, prevMode):
		self.r = Map(self.r, prevMode[0], prevMode[1], Color.mode[0], Color.mode[1])
		self.g = Map(self.g, prevMode[0], prevMode[1], Color.mode[0], Color.mode[1])
		self.b = Map(self.b, prevMode[0], prevMode[1], Color.mode[0], Color.mode[1])
		self.a = Map(self.a, prevMode[0], prevMode[1], Color.mode[0], Color.mode[1])

	def __add__(self, c):
		return Color((Constrain(self.r + c.r, Color.mode[0], Color.mode[1]), Constrain(self.g + c.g, Color.mode[0], Color.mode[1]), Constrain(self.b + c.b, Color.mode[0], Color.mode[1])))

	def __sub__(self, c):
		return Color((Constrain(self.r - c.r, Color.mode[0], Color.mode[1]), Constrain(self.g - c.g, Color.mode[0], Color.mode[1]), Constrain(self.b - c.b, Color.mode[0], Color.mode[1])))
	
	def __mul__(self, c):
		return Color((Constrain(self.r * c.r, Color.mode[0], Color.mode[1]), Constrain(self.g * c.g, Color.mode[0], Color.mode[1]), Constrain(self.b * c.b, Color.mode[0], Color.mode[1])))
	
	def __floordiv__(self, c):
		return Color((Constrain(self.r // c.r, Color.mode[0], Color.mode[1]), Constrain(self.g // c.g, Color.mode[0], Color.mode[1]), Constrain(self.b // c.b, Color.mode[0], Color.mode[1])))
	
	def __truediv__(self, c):
		return Color((Constrain(self.r / c.r, Color.mode[0], Color.mode[1]), Constrain(self.g / c.g, Color.mode[0], Color.mode[1]), Constrain(self.b / c.b, Color.mode[0], Color.mode[1])))

	def __mod__(self, c):
		return Color((Constrain(self.r % c.r, Color.mode[0], Color.mode[1]), Constrain(self.g % c.g, Color.mode[0], Color.mode[1]), Constrain(self.b % c.b, Color.mode[0], Color.mode[1])))
		
	def __pow__(self, c):
		return Color((Constrain(self.r ** c.r, Color.mode[0], Color.mode[1]), Constrain(self.g ** c.g, Color.mode[0], Color.mode[1]), Constrain(self.b ** c.b, Color.mode[0], Color.mode[1])))

	def __eq__(self, c):
		return self.r == c.r and self.g == c.g and self.b == c.b

	def __ne__(self, c):
		if isinstance(c, tuple):
			return self.r != c.r or self.g != c.g or self.b != c.b
		else:
			return False

	def __dir__(self):
		return {"red": self.r, "green": self.g, "blue": self.b, "alpha": self.a, "type": type(self)}

	def __str__(self):
		return f"red {self.r} green {self.g} blue {self.b} alpha {self.a} type {type(self)}"

	def ChangeBrightness(self, percentage):
		return Color((self.r * Constrain(percentage / 100, 0, 1), self.g * Constrain(percentage / 100, 0, 1), self.b * Constrain(percentage / 100, 0, 1)))

	def __invert__(self):
		return self.Invert

	def Copy(self):
		return Color((self.r, self.g, self.b, self.a))

	@property
	def Invert(self):
		return Color((Color.mode[1] - self.r, Color.mode[1] - self.g, Color.mode[1] - self.b, self.a))

	def Lerp(self, c, t):
		return (Lerp(self.r, c[0], t), Lerp(self.g, c[1], t), Lerp(self.b, c[2], t))

	@property
	def AsHex(self):
		return Color.RGBToHex(self)
	
	@property
	def hex(self):
		return self.AsHex

	@property
	def Hex(self):
		return self.AsHex
	

def RandomColor(minR = 0, maxR = 255, minG = 0, maxG = 255, minB = 255, maxB = 255):
	return (randint(minR, maxR), randint(minG, maxG), randint(minB, maxB))\

def LerpColorElement(minColorElement, maxColorElement, t):
	return Lerp(minColorElement, maxColorElement, t)

def LerpColor(color1, color2, t):
	return (Lerp(color1[0], color2[0], t), Lerp(color1[1], color2[1], t), Lerp(color1[2], color2[2], t))

def InvertColor(color):
	return (255 - color[0], 255 - color[1], 255 - color[2])

def ChangeColorBrightness(color, percentage):
	return Color((color[0] * Constrain(percentage / 100, 0, 1), color[1] * Constrain(percentage / 100, 0, 1), color[2] * Constrain(percentage / 100, 0, 1)))


# pre-defined colors

white = Color((255, 255, 255))
black = Color((0, 0, 0))
lightGray = Color((205, 205, 205))
darkGray = Color((55, 55, 55))
gray = Color((100, 100, 100))
darkWhite = Color((215, 215, 215))
lightBlack = Color((35, 35, 35))
red = Color((255, 0, 0))
green = Color((0, 255, 0))
blue = Color((0, 0, 255))
lightRed = Color((255, 41, 41))
lightGreen = Color((41, 255, 41))
lightBlue = Color((4, 179, 255))
darkRed = Color((165, 0, 0))
darkGreen = Color((0, 100, 0))
darkBlue = Color((0, 0, 139))
yellow = Color((255, 255, 0))
magenta = Color((255, 0, 255))
cyan = Color((0, 255, 255))
orange = Color((255, 145, 0))
pink = Color((255, 4, 179))
brown = Color((56, 27, 8))
purple = Color((128, 0, 128))
olive = Color((128, 128, 0))
beige = Color((245, 245, 220))
tan = Color((210, 180, 140))
peach = Color((255, 153, 102))
bloodRed = Color((153, 25, 25))


if __name__ == "__main__":
	import pygame as pg
	pg.init()
	
	colors = {}
	globs = globals().copy()
	
	for c in globs:
		if isinstance(globals()[c], tuple):
			colors[c] = (globals()[c])
			colors[f"~{c}"] = ~(globals()[c])

	size = 20

	screenSize = (500, (len(colors) // 2) * size)

	screen = pg.display.set_mode(screenSize)

	x, y = 0, 0
	rects = []

	texts = []
	font = pg.font.SysFont("arial", 16)

	for i, key in enumerate(colors):
		rects.append(pg.Rect(x, y, screenSize[0] / 2, size))
		rects.append(pg.Rect(x + screenSize[0] / 2, y, screenSize[0] / 2, size))
		y += size

		texts.append(font.render(str(key), True, black, white))

	running = True
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

		screen.fill(darkGray)
		
		for i, key in enumerate(colors):
			pg.draw.rect(screen, colors[key], rects[i])
			if rects[i].x >= screenSize[0] // 2:
				screen.blit(texts[i], (rects[i][0] + screenSize[0] / 2 - texts[i].get_width(), rects[i][1]))
			else:
				screen.blit(texts[i], rects[i])

		pg.display.update()