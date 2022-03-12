from random import *
from General import Lerp, Constrain


class Color(tuple):
	def __init__(self, color):
		super().__init__()

		self.r = color[0]
		self.g = color[1]
		self.b = color[2]
		self.a = 255
		if len(color) == 4:
			self.a = color[3]

	def __add__(self, c):
		return Color((Constrain(self.r + c.r, 0, 255), Constrain(self.g + c.g, 0, 255), Constrain(self.b + c.b, 0, 255)))

	def __sub__(self, c):
		return Color((Constrain(self.r - c.r, 0, 255), Constrain(self.g - c.g, 0, 255), Constrain(self.b - c.b, 0, 255)))
	
	def __mul__(self, c):
		return Color((Constrain(self.r * c.r, 0, 255), Constrain(self.g * c.g, 0, 255), Constrain(self.b * c.b, 0, 255)))
	
	def __mul__(self, c):
		return Color((Constrain(self.r * c.r, 0, 255), Constrain(self.g * c.g, 0, 255), Constrain(self.b * c.b, 0, 255)))

	def __floordiv__(self, c):
		return Color((Constrain(self.r // c.r, 0, 255), Constrain(self.g // c.g, 0, 255), Constrain(self.b // c.b, 0, 255), Constrain(self.a // c.a, 0, 255)))
	
	def __truediv__(self, c):
		return Color((Constrain(self.r / c.r, 0, 255), Constrain(self.g / c.g, 0, 255), Constrain(self.b / c.b, 0, 255), Constrain(self.a / c.a, 0, 255)))

	def __mod__(self, c):
		return Color((Constrain(self.r % c.r, 0, 255), Constrain(self.g % c.g, 0, 255), Constrain(self.b % c.b, 0, 255), Constrain(self.a % c.a, 0, 255)))
		
	def __mod__(self, c):
		return Color((Constrain(self.r ** c.r, 0, 255), Constrain(self.g ** c.g, 0, 255), Constrain(self.b ** c.b, 0, 255), Constrain(self.a ** c.a, 0, 255)))

	def __eq__(self, c):
		return self.r == c.r and self.g == c.g and self.b == c.b and self.a == c.a

	def __ne__(self, c):
		return self.r != c.r or self.g != c.g or self.b != c.b or self.a != c.a

	def __dir__(self):
		return {"red": self.r, "green": self.g, "blue": self.b, "alpha": self.a, "type": type(self)}

	def __str__(self):
		return f"red {self.r} green {self.g} blue {self.b} alpha {self.a} type {type(self)}"

	def ChangeBrightness(self, percentage):
		return Color((self.r * Constrain(percentage / 100, 0, 1), self.g * Constrain(percentage / 100, 0, 1), self.b * Constrain(percentage / 100, 0, 1)))

	def __invert__(self):
		return self.Invert()

	def Invert(self):
		return Color((255 - self.r, 255 - self.g, 255 - self.b, self.a))

	def Lerp(self, c, t):
		return (Lerp(self.r, c.r, t), Lerp(self.g, c.g, t), Lerp(self.b, c.b, t))

	def AsHex(self):
		return f"#{hex(self.r)[2:].zfill(2)}{hex(self.g)[2:].zfill(2)}{hex(self.b)[2:].zfill(2)}"


def RandomColor(minR = 0, minG = 0, minB = 0, maxR = 255, maxG = 255, maxB = 255):
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

	size = 20

	screenSize = (500, len(colors) * size)

	screen = pg.display.set_mode(screenSize)

	x, y = 0, 0
	rects = []

	texts = []
	font = pg.font.SysFont("arial", 16)

	for i, key in enumerate(colors):
		rects.append(pg.Rect(x, y, screenSize[0], size))
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
			screen.blit(texts[i], rects[i])

		pg.display.update()