import pygame as pg


def draw_text(screen, x, y, text, size, color, TILESIZE=1):
	font = pg.font.Font('freesansbold.ttf', size)
	text = font.render(text, True, color)
	textRect = text.get_rect()
	textRect.center = (x*TILESIZE, y*TILESIZE)
	screen.blit(text, textRect)

