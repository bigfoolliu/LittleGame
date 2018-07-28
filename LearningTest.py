#!-*-coding:utf-8-*-
# !@Date: 2018/7/24 11:09
# !@Author: Liu Rui
# !@github: bigfoolliu


"""
step1: 窗口显示
"""
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

import pygame
import sys
from pygame.locals import *  # 导入相关常量
import math

grid_list = []  # 记录每个格子的信息,元素为{"position": , "center_coordinate": , occupy_flag": }


class Window(object):
	"""窗口类,显示基本信息"""
	# 窗口类的大小等信息
	window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

	def __init__(self, background_file, x, y):
		"""窗口初始化,包括定义背景以及窗口尺寸"""
		self.background_img = pygame.image.load(background_file)
		self.x = x
		self.y = y

	def __str__(self):
		"""显示窗口信息"""
		return "窗口尺寸为:{}x{}".format(self.x, self.y)

	def display(self):
		"""窗口显示"""
		self.window.blit(self.background_img, (self.x, self.y))


class ChessBoard(object):
	"""棋盘类"""

	def __init__(self, chess_board_img, x, y):
		# 初始位置坐标应为窗口的中央
		self.img = pygame.image.load(chess_board_img)
		self.x = x
		self.y = y

	def display(self, window):
		window.window.blit(self.img, (self.x, self.y))


class Chess:
	"""棋子类,包括圆和叉"""

	def __init__(self, chess_img):
		"""初始只需要加载图像"""
		self.img = pygame.image.load(chess_img)
		self.x = None
		self.y = None

	def display(self, window, x, y):
		"""显示的时候需要传入落子的位置"""
		self.x = x
		self.y = y
		window.window.blit(self.img, (self.x, self.y))


def put_chess(window, grids, chess_circle, chess_cross, put_x, put_y):
	"""
	放置棋子,偶数次数放置o, 奇数次数放置x
	:param window: 放置棋子的窗口
	:param grids: 格子列表,通过统计格子被占位信息来判断该下那颗棋子
	:param chess_circle: 棋子o
	:param chess_cross: 棋子x
	:param put_x: 棋子放置横坐标
	:param put_y: 棋子放置纵坐标
	"""
	occupy_times = 0

	for grid in grids:
		if grid["occupy_flag"] is True:
			occupy_times += 1

	if occupy_times % 2 == 0:
		chess_circle.display(window, put_x, put_y)
	else:
		chess_cross.display(window, put_x, put_y)


def judge_mouse(grids, mouse_x, mouse_y):
	"""
	判断鼠标的位置是否在可以放置
	:param mouse_x: 鼠标当前横坐标
	:param mouse_y: 鼠标当前纵坐标
	:param grids: 格子列表
	:return: bool
	"""
	area_width = 80  # 鼠标点击能触发的区域
	area_height = 80

	put_flag = False  # 能否放置棋子的标志,默认不能放置

	put_x = None
	put_y = None

	# 判断鼠标位置是否在格子的位置以及在第几个格子
	for grid in grids:
		if (math.fabs(mouse_x - grid["center_coordinate"][0]) <= area_width / 2) and \
				(math.fabs(mouse_y - grid["center_coordinate"][1]) <= area_height / 2):  # 找到当前的格子
			if grid["occupy_flag"] is False:  # 格子未放置棋子
				put_flag = True
				put_x = grid["center_coordinate"][0] - 30
				put_y = grid["center_coordinate"][1] - 30

	return put_flag, put_x, put_y


def create_grid():
	"""创建九宫格及其位置"""
	# grid_list = []  # 记录每个格子的信息,元素为{"position": , "center_coordinate": , occupy_flag": }

	for num in range(1, 10):
		if num <= 3:
			grid = {"position": num, "center_coordinate": (204 + 96 * (num - 1), 204), "occupy_flag": False}
			grid_list.append(grid)
		elif 3 < num <= 6:
			grid = {"position": num, "center_coordinate": (204 + 96 * (num - 4), 204 + 96 * 1), "occupy_flag": False}
			grid_list.append(grid)
		elif 6 < num <= 9:
			grid = {"position": num, "center_coordinate": (204 + 96 * (num - 7), 204 + 96 * 2), "occupy_flag": False}
			grid_list.append(grid)

	print(grid_list)

	return grid_list


def main():
	"""主函数"""
	pygame.init()

	main_window = Window("LearningTestFile/white_background.png", 0, 0)

	chess_board = ChessBoard("LearningTestFile/chess_board.png", 150, 150)

	chess_circle = Chess("LearningTestFile/circle.png")

	chess_cross = Chess("LearningTestFile/cross.png")

	grids = create_grid()  # 创建格子列表

	while True:

		main_window.display()
		chess_board.display(main_window)

		for event in pygame.event.get():
			if event.type == QUIT:  # 按下退出键
				print("退出")
				sys.exit()

			if event.type == MOUSEBUTTONDOWN and event.button == 1:  # 按下鼠标左键
				print("左键被按下.")
				mouse_x, mouse_y = pygame.mouse.get_pos()  # 获取鼠标当前的位置

				print(mouse_x, type(mouse_x), mouse_y, type(mouse_y))  # 测试鼠标位置是否正常

				judge_result = judge_mouse(grids, mouse_x, mouse_y)

				print(judge_result)  # TODO 测试判断结果返回是否正常

				if judge_result[0] is True:
					put_chess(main_window, grids, chess_circle, chess_cross, judge_result[1], judge_result[2])

		pygame.display.update()


if __name__ == "__main__":
	main()
