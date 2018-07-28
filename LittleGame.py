#!-*-coding:utf-8-*-
# !@Date: 2018/7/20 17:28
# !@Author: Liu Rui
# !@github: bigfoolliu

import pygame
from pygame.locals import *
from sys import exit
import time  # 提升游戏性能

grid_list = []
grid_state_list = []
chess_num = 0  # 棋盘上的棋子数量,默认为0,最多为9

score_o = 0
score_x = 0


def draw_rect(screen):
	"""
	画棋盘
	:param screen:
	:return:
	"""
	for i in range(0, 9):
		if 0 <= i < 3:
			pygame.draw.rect(screen, (0, 0, 0), (150 + 100 * i, 150, 100, 100), 10)
		elif 3 <= i < 6:
			pygame.draw.rect(screen, (0, 0, 0), (150 + 100 * (i - 3), 250, 100, 100), 10)
		elif 6 <= i < 9:
			pygame.draw.rect(screen, (0, 0, 0), (150 + 100 * (i - 6), 350, 100, 100), 10)


def start_font_display(screen):
	"""
	显示游戏标题,游戏信息,版权等
	:param screen:
	:return:
	"""
	# 游戏标题显示
	game_caption = "Little Game"
	game_caption_font = pygame.font.SysFont("arial black", 40, bold=True)
	game_caption_surface = game_caption_font.render(game_caption, True, (0, 0, 0), (255, 255, 255))
	screen.blit(game_caption_surface, (155, 50))

	# 游戏版权表示
	version_info = "V1.0  By liu"
	game_version_font = pygame.font.SysFont("arial", 15, bold=True)
	version_info_surface = game_version_font.render(version_info, True, (0, 0, 0), (255, 255, 255))
	screen.blit(version_info_surface, (0, 0))

	# 游戏左右"Score"显示
	score = "Score:"
	score_font = pygame.font.SysFont("arial black", 20)
	score_surface = score_font.render(score, True, (0, 0, 0), (255, 255, 255))
	screen.blit(score_surface, (30, 370))
	screen.blit(score_surface, (490, 370))

	# 下棋顺序矩形框显示
	order_rect_area = Rect((40, 200), (50, 120))
	pygame.draw.rect(screen, (0, 0, 0), order_rect_area, 3)
	order_rect_area2 = Rect((500, 200), (50, 120))
	pygame.draw.rect(screen, (0, 0, 0), order_rect_area2, 3)

	# reset和restart矩形框显示
	reset_rect_area = Rect((4, 555), (100, 40))
	pygame.draw.rect(screen, (0, 0, 0), reset_rect_area, 3)
	reset_rect_area2 = Rect((495, 555), (100, 40))
	pygame.draw.rect(screen, (0, 0, 0), reset_rect_area2, 3)
	# Reset和Restart显示
	reset = "Reset"
	restart = "Restart"
	reset_surface = score_font.render(reset, True, (0, 0, 0), (255, 255, 255))  # 借用score的字体
	restart_surface = score_font.render(restart, True, (0, 0, 0), (255, 255, 255))
	screen.blit(reset_surface, (25, 560))
	screen.blit(restart_surface, (505, 560))

	# 左方
	pygame.draw.circle(screen, (0, 0, 0), (65, 150), 25, 10)
	# 右方
	pygame.draw.line(screen, (0, 0, 0), (505, 125), (545, 175), 10)
	pygame.draw.line(screen, (0, 0, 0), (545, 125), (505, 175), 10)


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


def game_over_font_display(screen, winner):
	"""
	游戏结束时显示文字
	:param screen:
	:param winner: str, game胜者
	:return:
	"""
	# Game Over显示
	game_over_font = pygame.font.SysFont("arial black", 40, bold=True)
	game_over_surface = game_over_font.render("Game Over", True, (0, 0, 0), (255, 255, 255))
	# Surface对象用来表示图像
	# Rect对象用来储存矩形坐标,((left, top), (width, height)), 两者都是数据类型,类似int
	game_over_rect = Rect((160, 520), (200, 10))
	screen.blit(game_over_surface, game_over_rect)

	# .. Wins显示
	winner = winner
	winner_font = pygame.font.SysFont("arial black", 40, bold=True)
	winner_surface = winner_font.render("{} Wins!".format(winner), True, (0, 0, 0), (255, 255, 255))
	winner_rect = Rect((210, 470), (200, 10))
	screen.blit(winner_surface, winner_rect)

	pygame.display.update()


def draw_circle(screen, position_x, position_y, radis, width=0):
	"""
	画圆
	:param screen:
	:param position_x: 所画圆的中心位置横坐标
	:param position_y: 所画圆的中心位置的纵坐标
	:param radis: 圆的直径
	:param width: 圆的线宽
	:return:
	"""
	circle = pygame.draw.circle(screen, (0, 0, 0), (position_x, position_y), radis, width)
	return circle


def draw_line(screen, position_x, position_y):
	"""
	画叉
	:param screen:
	:param position_x: 所画叉的左上角横坐标
	:param position_y: 所画叉的左上角纵坐标
	:return:
	"""
	line1 = pygame.draw.line(screen, (0, 0, 0), (position_x, position_y), (position_x + 60, position_y + 70), 14)
	line2 = pygame.draw.line(screen, (0, 0, 0), (position_x + 60, position_y), (position_x, position_y + 70), 14)
	return line1, line2


def create_grid():
	"""
	创建棋盘的位置列表
	:return:
	"""
	for row in range(0, 3):  # 遍历行
		list1 = []
		for col in range(0, 3):  # 遍历列
			grid = {}
			grid["num"] = (row, col)
			grid["coordinate"] = ((150 + 100 * col), (150 + 100 * row))
			grid["occupy_flag"] = 0  # 0表示默认未被占用
			grid["chess"] = None  # 记录每个棋盘放置的是什么棋子0表示o, 1表示叉
			list1.append(grid)
		grid_list.append(list1)


def traffic_light(screen):
	"""
	显示该哪方下棋
	:return:
	"""
	# 下棋顺序圆形框显示,其内部应该可以填充颜色,上方为绿灯,表示下棋,下方为红灯,表示禁止下棋
	if chess_num % 2 == 0:
		pygame.draw.circle(screen, (84, 155, 120), (65, 230), 25, 25)
		pygame.draw.circle(screen, (0, 0, 0), (65, 290), 25, 25)
		pygame.draw.circle(screen, (0, 0, 0), (525, 230), 25, 25)
		pygame.draw.circle(screen, (255, 0, 0), (525, 290), 25, 25)
	elif chess_num % 2 == 1:
		pygame.draw.circle(screen, (0, 0, 0), (65, 230), 25, 25)
		pygame.draw.circle(screen, (255, 0, 0), (65, 290), 25, 25)
		pygame.draw.circle(screen, (84, 155, 120), (525, 230), 25, 25)
		pygame.draw.circle(screen, (0, 0, 0), (525, 290), 25, 25)

	pygame.display.update()


def put_chess(screen, grid, position_x, position_y):
	"""
	落子
	:param grid:
	:param screen:
	:param position_x: 默认落子的横坐标
	:param position_y: 默认落子的纵坐标
	:return:
	"""
	global chess_num
	# 首先判断落什么棋子
	if chess_num % 2 == 0:
		draw_circle(screen, position_x + 31, position_y + 35, 35, 10)
		grid["chess"] = 0
	else:
		draw_line(screen, position_x, position_y)
		grid["chess"] = 1

	chess_num += 1


def judge_game(_grid_list):
	"""
	判断赛果
	:param _grid_list: 全局棋盘信息
	:return:
	"""
	# 判断横着的是否有胜利的
	for row in range(0, 3):
		if (_grid_list[row][0]["chess"] == _grid_list[row][1]["chess"] == _grid_list[row][2]["chess"] == 0) or \
				(_grid_list[row][0]["chess"] == _grid_list[row][1]["chess"] == _grid_list[row][2]["chess"] == 1):
			return True

	# 判断竖着的是否有胜利的
	for col in range(0, 3):
		if (_grid_list[0][col]["chess"] == _grid_list[1][col]["chess"] == _grid_list[2][col]["chess"] == 0) or \
				(_grid_list[0][col]["chess"] == _grid_list[1][col]["chess"] == _grid_list[2][col]["chess"] == 1):
			return True

	# 判断斜的是否有胜利的
	if (_grid_list[0][0]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][2]["chess"] == 0) or \
			(_grid_list[0][2]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][0]["chess"] == 0) or \
			(_grid_list[0][0]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][2]["chess"] == 1) or \
			(_grid_list[0][2]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][0]["chess"] == 1):
		return True


def judge_winner(_score_x, _score_o):
	"""
	游戏结束时棋盘上的棋子
	:return:
	"""
	if chess_num >= 6 and chess_num % 2 == 0:  # X赢
		_score_x += 1
		return "X"
	elif chess_num >= 5 and chess_num % 2 == 1:  # O赢
		_score_o += 1
		return "O"


def game_reset(mouse_pos, screen):
	"""
	按下reset,将游戏的比分重置
	:param screen:
	:param mouse_pos:
	:return:
	"""
	global score_o, score_x
	if 4 <= mouse_pos[0] <= 104 and 555 <= mouse_pos[1] <= 595:
		print("reset")
		score_o = 0
		score_x = 0
		score_display(screen, score_o, score_x)


def game_restart(mouse_pos):
	"""

	:param mouse_pos:
	:return:
	"""
	if 495 <= mouse_pos[0] <= 595 and 555 <= mouse_pos[1] <= 595:
		print("restart")


def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 600))

	screen.fill((255, 255, 255))  # 窗口背景填充为白色

	draw_rect(screen)  # 画棋盘
	start_font_display(screen)  # 显示初始信息

	score_display(screen, score_o, score_x)  # 屏幕显示比分

	pygame.display.update()  # 这里更新,已显示背景,即不变得部分

	create_grid()  # 创建每个棋格的信息

	# 需要动态更新的都要放置在游戏主循环
	while True:

		traffic_light(screen)  # 显示下棋顺序
		score_display(screen, score_o, score_x)  # 显示游戏比分

		mouse_pos = pygame.mouse.get_pos()

		event = pygame.event.wait()
		# 发生退出事件
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			exit()

		# 按下鼠标按键
		if event.type == MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			if pressed_array[0] == 1:  # 鼠标左键按下

				# 判断鼠标是否按下reset以及restart的反应
				game_reset(mouse_pos, screen)
				game_restart(mouse_pos)

				# 如果鼠标在棋盘里按下按下去
				for row in range(0, 3):
					for col in range(0, 3):

						if (0 < mouse_pos[0] - grid_list[row][col]["coordinate"][0] < 100) and \
								(0 < mouse_pos[1] - grid_list[row][col]["coordinate"][1] < 100):  # 获取鼠标当前在棋盘的位置
							if grid_list[row][col]["occupy_flag"] == 0:  # 格子未放置棋子
								put_x = grid_list[row][col]["coordinate"][0] + 20
								put_y = grid_list[row][col]["coordinate"][1] + 15

								put_chess(screen, grid_list[row][col], put_x, put_y)  # 放置棋子
								grid_list[row][col]["occupy_flag"] = 1  # 放置棋子之后应更改该格的放置标志

								# out_put_test2(grid)

								game_result = judge_game(grid_list)
								game_winner = judge_winner(score_x, score_o)
								print(game_result)
								if game_result is True:  # 游戏胜者产生,游戏结束
									game_over_font_display(screen, game_winner)  # 显示胜者信息

				if 4 <= mouse_pos[0] <= 104 and 555 <= mouse_pos[1] <= 595:
					game_reset(mouse_pos, screen)
				elif 495 <= mouse_pos[0] <= 595 and 555 <= mouse_pos[1] <= 595:
					# game_restart(mouse_pos)
					pass
				else:
					pygame.event.set_blocked(MOUSEBUTTONDOWN)  # 此时不再响应鼠标的按键按下

			pygame.event.set_allowed(MOUSEBUTTONDOWN)

		pygame.display.update()

		time.sleep(0.02)  # 降低cpu的消耗


if __name__ == "__main__":
	main()
