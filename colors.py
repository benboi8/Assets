from random import *
from General import Lerp

# pre-defined colors

white = (255, 255, 255)
black = (0, 0, 0)
lightGray = (205, 205, 205)
darkGray = (55, 55, 55)
gray = (100, 100, 100)
darkWhite = (215, 215, 215)
lightBlack = (45, 45, 45)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightRed = (215, 0, 0)
lightGreen = (0, 215, 0)
lightBlue = (0, 0, 215)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
orange = (255, 145, 0)
pink = (204, 126, 183)


def RandomColor(minR = 0, minG = 0, minB = 0, maxR = 255, maxG = 255, maxB = 255):
	return (randint(minR, maxR), randint(minG, maxG), randint(minB, maxB))

def ScaleColorElement(minColorElement, maxColorElement, t):
	return Lerp(minColorElement, maxColorElement, t)

def ScaleColor(color1, color2, t):
	return (Lerp(color1[0], color2[0], t), Lerp(color1[1], color2[1], t), Lerp(color1[2], color2[2], t))

