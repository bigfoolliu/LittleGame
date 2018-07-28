#!-*-coding:utf-8-*-
# !@Date: 2018/7/26 11:33
# !@Author: Liu Rui
# !@github: bigfoolliu


import pygame
from pygame import *
from sys import exit
import time


def draw_rect(_screen, _x):
	rect1 = pygame.draw.rect(_screen, (0, 255, 0), (_x, 100, 100, 100), 10)
	# rect1_surface = Surface(rect1)
	# rect1_surface.fill((255, 0, 0))

	return rect1


def draw_circle(_screen, pos):
	circle1 = pygame.draw.circle(_screen, (255, 0, 0), pos, 50, 10)
	print(type(circle1), circle1)
	return circle1


def score_display(screen, _score_o, _score_x):
	"""
	显示游戏的得分
	:param screen:
	:param _score_o: int
	:param _score_x: int
	:return:
	"""
	score_o_info = str(_score_o)
	score_x_info = str(_score_x)
	score_font = pygame.font.SysFont("arial black", 50)
	score_o_info_surface = score_font.render(score_o_info, True, (0, 0, 0), (255, 255, 255))
	score_x_info_surface = score_font.render(score_x_info, True, (0, 0, 0), (255, 255, 255))
	screen.blit(score_o_info_surface, (45, 395))
	screen.blit(score_x_info_surface, (510, 395))
	pygame.display.update()


def solid_grid(screen):
	for i in range(0, 9):
		if 0 <= i < 3:
			pygame.draw.rect(screen, (0, 0, 0), (145 + 100 * i, 145, 90, 90), 0)
		elif 3 <= i < 6:
			pygame.draw.rect(screen, (0, 0, 0), (145 + 100 * (i - 3), 245, 90, 90), 0)
		elif 6 <= i < 9:
			pygame.draw.rect(screen, (0, 0, 0), (145 + 100 * (i - 6), 345, 90, 90), 0)


def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 600))

	screen.fill((255, 255, 255))

	while True:
		game_event = pygame.event.wait()

		if game_event.type == QUIT:
			exit()

		pygame.draw.rect(screen, (0, 0, 0), ((100, 100), (100, 100)), 0)  # 将宽度设为0,即可得到实心矩形
		pygame.draw.circle(screen, (0, 0, 0), (200, 200), 50, 0)  # 将宽度设为0,即可得到实心圆

		pygame.draw.circle(screen, (84, 155, 120), (65, 230), 25, 0)
		pygame.draw.circle(screen, (0, 0, 0), (65, 290), 25, 0)
		pygame.draw.circle(screen, (0, 0, 0), (525, 230), 25, 0)
		pygame.draw.circle(screen, (255, 0, 0), (525, 290), 25, 0)

		solid_grid(screen)

		pygame.display.update()
		time.sleep(0.05)


if __name__ == "__main__":
	main()

# a = 5
# b = str(a)
# print(a, b)
