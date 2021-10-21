from General import *

import pygame as pg
from pygame import *
from pygame import gfxdraw

pg.init()
clock = pg.time.Clock()

sf = 2
programState = "all"

running = True

fps = 60


if __name__ == "__main__":

	def DrawLoop():
		screen.fill((55, 55, 55))

		pg.display.update()


	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

		DrawLoop()

