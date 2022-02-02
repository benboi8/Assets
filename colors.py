from random import *
from General import Lerp

# pre-defined colors

white = (255, 255, 255)
black = (0, 0, 0)
lightGray = (205, 205, 205)
darkGray = (55, 55, 55)
gray = (100, 100, 100)
darkWhite = (215, 215, 215)
lightBlack = (35, 35, 35)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightRed = (255, 41, 41)
lightGreen = (41, 255, 41)
lightBlue = (4, 179, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
orange = (255, 145, 0)
pink = (255, 4, 179)
brown = (56, 27, 8)
purple = (128, 0, 128)
beige = (245, 245, 220)
tan = (210, 180, 140)
peach = (255, 153, 102)


def RandomColor(minR = 0, minG = 0, minB = 0, maxR = 255, maxG = 255, maxB = 255):
	return (randint(minR, maxR), randint(minG, maxG), randint(minB, maxB))\

def LerpColorElement(minColorElement, maxColorElement, t):
	return Lerp(minColorElement, maxColorElement, t)

def LerpColor(color1, color2, t):
	return (Lerp(color1[0], color2[0], t), Lerp(color1[1], color2[1], t), Lerp(color1[2], color2[2], t))

def InvertColor(color):
	return (255 - color[0], 255 - color[1], 255 - color[2])

def ChangeColorBrightness(color, percentage):
	return (color[0] * (max(min(percentage, 100), 0) / 100), color[1] * (max(min(percentage, 100), 0) / 100), color[2] * (max(min(percentage, 100), 0) / 100))


if __name__ == "__main__":
	import pygame as pg
	pg.init()
	
	colors = {
		"white": white, 
		"black": black, 
		"lightGray": lightGray, 
		"darkGray": darkGray, 
		"gray": gray, 
		"darkWhite": darkWhite, 
		"lightBlack": lightBlack, 
		"red": red, 
		"green": green, 
		"blue": blue, 
		"lightRed": lightRed, 
		"lightGreen": lightGreen, 
		"lightBlue": lightBlue, 
		"yellow": yellow, 
		"magenta": magenta, 
		"cyan": cyan, 
		"orange": orange, 
		"pink": pink, 
		"brown": brown,
		"purple": purple,
		"beige": beige,
		"tan": tan,
		"peach": peach,
		}

	size = 20

	screenSize = (500, 500)

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