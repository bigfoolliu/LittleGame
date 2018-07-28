#!-*-coding:utf-8-*-
# !@Date: 2018/7/27 16:40
# !@Author: Liu Rui
# !@github: bigfoolliu


import pygame
from pygame.locals import *
from sys import exit
import time  # 提升游戏性能


class Desktop(object):
	"""用于显示桌面信息"""

	def __init__(self, _screen):
		"""
		初始化需要传入screen
		"""
		self.screen = _screen
		self.grid_list = []

	def draw_interface(self):
		"""画桌面"""
		# 画棋盘
		for i in range(0, 9):
			if 0 <= i < 3:
				pygame.draw.rect(self.screen, (0, 0, 0), (150 + 100 * i, 150, 100, 100), 10)
			elif 3 <= i < 6:
				pygame.draw.rect(self.screen, (0, 0, 0), (150 + 100 * (i - 3), 250, 100, 100), 10)
			elif 6 <= i < 9:
				pygame.draw.rect(self.screen, (0, 0, 0), (150 + 100 * (i - 6), 350, 100, 100), 10)
		# 游戏标题显示
		game_caption = "Little Game"
		game_caption_font = pygame.font.SysFont("arial black", 40, bold=True)
		game_caption_surface = game_caption_font.render(game_caption, True, (0, 0, 0), (255, 255, 255))
		self.screen.blit(game_caption_surface, (155, 50))

		# 游戏版权表示
		version_info = "V1.0  By liu"
		game_version_font = pygame.font.SysFont("arial", 15, bold=True)
		version_info_surface = game_version_font.render(version_info, True, (0, 0, 0), (255, 255, 255))
		self.screen.blit(version_info_surface, (0, 0))

		# 游戏左右"Score"显示
		score = "Score:"
		score_font = pygame.font.SysFont("arial black", 20)
		score_surface = score_font.render(score, True, (0, 0, 0), (255, 255, 255))
		self.screen.blit(score_surface, (30, 370))
		self.screen.blit(score_surface, (490, 370))

		# 下棋顺序矩形框显示
		order_rect_area = Rect((40, 200), (50, 120))
		pygame.draw.rect(self.screen, (0, 0, 0), order_rect_area, 3)
		order_rect_area2 = Rect((500, 200), (50, 120))
		pygame.draw.rect(self.screen, (0, 0, 0), order_rect_area2, 3)

		# reset和restart矩形框显示
		reset_rect_area = Rect((4, 555), (100, 40))
		pygame.draw.rect(self.screen, (0, 0, 0), reset_rect_area, 3)
		reset_rect_area2 = Rect((495, 555), (100, 40))
		pygame.draw.rect(self.screen, (0, 0, 0), reset_rect_area2, 3)
		# Reset和Restart显示
		reset = "Reset"
		restart = "Restart"
		reset_surface = score_font.render(reset, True, (0, 0, 0), (255, 255, 255))  # 借用score的字体
		restart_surface = score_font.render(restart, True, (0, 0, 0), (255, 255, 255))
		self.screen.blit(reset_surface, (25, 560))
		self.screen.blit(restart_surface, (505, 560))

		# 左方O
		pygame.draw.circle(self.screen, (0, 0, 0), (65, 150), 25, 10)
		# 右方X
		pygame.draw.line(self.screen, (0, 0, 0), (505, 125), (545, 175), 10)
		pygame.draw.line(self.screen, (0, 0, 0), (545, 125), (505, 175), 10)

	def display_score(self, player_o, player_x):
		"""显示比分"""
		score_o_info = str(player_o.score)
		score_x_info = str(player_x.score)
		score_font = pygame.font.SysFont("arial black", 50)
		score_o_info_surface = score_font.render(score_o_info, True, (0, 0, 0), (255, 255, 255))
		score_x_info_surface = score_font.render(score_x_info, True, (0, 0, 0), (255, 255, 255))
		self.screen.blit(score_o_info_surface, (45, 395))
		self.screen.blit(score_x_info_surface, (510, 395))
		pygame.display.update()

	def create_grid(self):
		"""创建棋盘位置列表"""
		for row in range(0, 3):  # 遍历行
			list1 = []
			for col in range(0, 3):  # 遍历列
				grid = {}
				grid["num"] = (row, col)
				grid["coordinate"] = ((150 + 100 * col), (150 + 100 * row))
				grid["occupy_flag"] = 0  # 0表示默认未被占用
				grid["chess"] = None  # 记录每个棋盘放置的是什么棋子0表示o, 1表示叉
				list1.append(grid)
			self.grid_list.append(list1)

	def game_over_display(self, _winner, color_tuple):
		"""
		游戏结束显示信息, 颜色元组应为(0, 0, 0),之后清屏时应将其置为(255, 255, 255)
		:param _winner:
		:param color_tuple:
		:return:
		"""
		# Game Over显示
		game_over_font = pygame.font.SysFont("arial black", 40, bold=True)
		game_over_surface = game_over_font.render("Game Over", True, color_tuple, (255, 255, 255))
		# Surface对象用来表示图像
		# Rect对象用来储存矩形坐标,((left, top), (width, height)), 两者都是数据类型,类似int
		game_over_rect = Rect((160, 520), (200, 10))
		self.screen.blit(game_over_surface, game_over_rect)

		# .. Wins显示
		winner = _winner
		winner_font = pygame.font.SysFont("arial black", 40, bold=True)
		winner_surface = winner_font.render("{} Wins!".format(winner), True, color_tuple, (255, 255, 255))
		winner_rect = Rect((210, 470), (200, 10))
		self.screen.blit(winner_surface, winner_rect)

	def draw_light(self, _chess_num):
		"""显示下棋顺序"""
		# 下棋顺序圆形框显示,其内部应该可以填充颜色,上方为绿灯,表示下棋,下方为红灯,表示禁止下棋
		if _chess_num % 2 == 0:
			pygame.draw.circle(self.screen, (84, 155, 120), (65, 230), 25, 0)
			pygame.draw.circle(self.screen, (0, 0, 0), (65, 290), 25, 0)
			pygame.draw.circle(self.screen, (0, 0, 0), (525, 230), 25, 0)
			pygame.draw.circle(self.screen, (255, 0, 0), (525, 290), 25, 0)
		elif _chess_num % 2 == 1:
			pygame.draw.circle(self.screen, (0, 0, 0), (65, 230), 25, 0)
			pygame.draw.circle(self.screen, (255, 0, 0), (65, 290), 25, 0)
			pygame.draw.circle(self.screen, (84, 155, 120), (525, 230), 25, 0)
			pygame.draw.circle(self.screen, (0, 0, 0), (525, 290), 25, 0)

	def clear_grids(self):
		"""
		清空棋盘棋子
		:return:
		"""
		for i in range(0, 9):
			if 0 <= i < 3:
				pygame.draw.rect(self.screen, (255, 255, 255), (155 + 100 * i, 155, 90, 90), 0)
			elif 3 <= i < 6:
				pygame.draw.rect(self.screen, (255, 255, 255), (155 + 100 * (i - 3), 255, 90, 90), 0)
			elif 6 <= i < 9:
				pygame.draw.rect(self.screen, (255, 255, 255), (155 + 100 * (i - 6), 355, 90, 90), 0)


class Game(object):
	"""判断游戏胜负,是否按按钮"""

	def __init__(self):
		self.winner = None
		self.chess_num = 0

	def judge_winner(self, player_o, player_x):
		"""判断胜者"""
		if self.chess_num >= 6 and self.chess_num % 2 == 0:  # X赢
			player_x.score += 1  # TODO 此处分数不会传递给player
			self.winner = "X"
		elif self.chess_num >= 5 and self.chess_num % 2 == 1:  # O赢
			player_o.score += 1
			self.winner = "O"

	def judge_game_result(self, _grid_list, player_o, player_x):
		# 如果有横排胜利的
		for row in range(0, 3):
			if (_grid_list[row][0]["chess"] == _grid_list[row][1]["chess"] == _grid_list[row][2]["chess"] == 0) or \
					(_grid_list[row][0]["chess"] == _grid_list[row][1]["chess"] == _grid_list[row][2]["chess"] == 1):
				self.judge_winner(player_o, player_x)
				return

		# 如果有竖排胜利的
		for col in range(0, 3):
			if (_grid_list[0][col]["chess"] == _grid_list[1][col]["chess"] == _grid_list[2][col]["chess"] == 0) or \
					(_grid_list[0][col]["chess"] == _grid_list[1][col]["chess"] == _grid_list[2][col]["chess"] == 1):
				self.judge_winner(player_o, player_x)
				return

		# 如果有斜排胜利的
		if (_grid_list[0][0]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][2]["chess"] == 0) or \
				(_grid_list[0][2]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][0]["chess"] == 0) or \
				(_grid_list[0][0]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][2]["chess"] == 1) or \
				(_grid_list[0][2]["chess"] == _grid_list[1][1]["chess"] == _grid_list[2][0]["chess"] == 1):
			self.judge_winner(player_o, player_x)
			return

	def deal_game(self, mouse_pos, row, col, desktop, player_o, player_x):
		"""在棋盘落子的处理"""
		if (0 < mouse_pos[0] - desktop.grid_list[row][col]["coordinate"][0] < 100) and \
				(0 < mouse_pos[1] - desktop.grid_list[row][col]["coordinate"][1] < 100):  # 在棋盘区点击
			if desktop.grid_list[row][col]["occupy_flag"] == 0:  # 格子未放置棋子
				# 求得应该放置棋子的坐标
				put_x = desktop.grid_list[row][col]["coordinate"][0] + 20
				put_y = desktop.grid_list[row][col]["coordinate"][1] + 15

				# 判断是哪一位棋手下棋,并下棋
				player_o.put_chess(put_x, put_y, self.chess_num)

				# 下完棋,棋子数加1
				self.chess_num += 1
				desktop.grid_list[row][col]["occupy_flag"] = 1  # 放置棋子之后应更改该格的放置标志
				# 判断下完一颗棋子的赛果
				self.judge_game_result(desktop.grid_list, player_o.score, player_x.score)

	def game_restart(self, desktop):
		"""
		重新开始下一局游戏,将棋子清空,game over清空,light清空,与reset唯一的不同就是不会清空比分
		:param desktop: 需要清空的桌面
		:return:
		"""
		self.winner = None  # 重新将winner置为None
		desktop.clear_grids()  # 清空棋盘棋子
		desktop.game_over_display(self.winner, (255, 255, 255))  # 清空game over信息
		self.chess_num = 0  # 重新置零chess_num
		desktop.draw_light(self.chess_num)  # 重新配置light

	def game_reset(self, desktop, player_o, player_x):
		"""
		游戏重置,将比分,棋子,game over以及light都清空至游戏初始状态
		:return:
		"""
		self.game_restart(desktop)
		player_o.score = 0
		player_x.score = 0


class Player(object):
	"""玩家相关信息"""

	def __init__(self, _screen):
		self.screen = _screen
		self.score = 0

	def put_chess(self, position_x, position_y, _chess_num):
		"""
		放棋子
		:param position_x:
		:param position_y:
		:param _chess_num:
		:return:
		"""
		# 首先判断落什么棋子
		if _chess_num % 2 == 0:
			pygame.draw.circle(self.screen, (0, 0, 0), (position_x + 31, position_y + 35), 35, 10)  # 画圆
		elif _chess_num % 2 == 1:  # 画叉
			pygame.draw.line(self.screen, (0, 0, 0), (position_x, position_y), (position_x + 60, position_y + 70), 14)
			pygame.draw.line(self.screen, (0, 0, 0), (position_x + 60, position_y), (position_x, position_y + 70), 14)

	def score_reset(self):
		"""玩家游侠重置"""
		self.score = 0


def main():
	pygame.init()
	screen = pygame.display.set_mode((600, 600))

	screen.fill((255, 255, 255))  # 窗口背景填充为白色

	game = Game()

	player_o = Player(screen)
	player_x = Player(screen)

	desktop = Desktop(screen)  # 实例化桌面
	desktop.create_grid()  # 创建棋格字典
	desktop.draw_interface()  # 显示棋盘等
	desktop.draw_light(game.chess_num)  # 显示下棋顺序
	desktop.display_score(player_o, player_x)  # 显示初始比分

	# 需要动态更新的都要放置在游戏主循环
	while True:

		event = pygame.event.wait()
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # 退出
			exit()

		if game.winner is None:  # 还未产生胜负
			if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1:  # 按下鼠标左键
				mouse_pos = pygame.mouse.get_pos()  # 获得此时的鼠标位置
				# 鼠标在棋盘的位置按下
				for row in range(0, 3):
					for col in range(0, 3):
						game.deal_game(mouse_pos, row, col, desktop, player_o, player_x)

				# 鼠标按下reset
				if 4 <= mouse_pos[0] <= 104 and 555 <= mouse_pos[1] <= 595:
					# 玩家得分清零,屏幕棋盘棋子清空,有无game over都要将文字清空
					game.game_reset(desktop, player_o, player_x)
					print("reset")

				# 鼠标按下restart
				elif 495 <= mouse_pos[0] <= 595 and 555 <= mouse_pos[1] <= 595:
					game.game_restart(desktop)
					print("restart")

		else:  # 已经产生胜负
			# 先显示游戏结束信息,然后暂停数秒重新开始
			desktop.game_over_display(game.winner, (0, 0, 0))
			event = pygame.event.wait()
			if event.type == KEYDOWN and event.key == K_RETURN:  # 按下回车键游戏重新开始
				game.game_restart(desktop)

		pygame.display.update()

		time.sleep(0.02)  # 降低cpu的消耗


if __name__ == "__main__":
	main()
