from typing import Tuple
import pygame as pg
from pygame._sdl2 import Window

from model.BinaryTree import BinaryTree
from model.Standing import Standing


class PyGame:
	def __init__(self, window_size: Tuple[int, int] = (1280, 720), caption: str = ""):
		pg.init()
		pg.font.init()
		self.FONT = pg.font.Font("./src/soccer-brackets/view/fonts/Akshar/static/Akshar-Regular.ttf", 13)
		#self.FONT = pg.font.Font("./src/soccer-brackets/view/fonts/VT323/VT323-Regular.ttf", 14)

		self.window = pg.display.set_mode(window_size, pg.RESIZABLE)
		Window.from_display_module().maximize()
		self.surfaces = {
			"bg": [
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA)
			],
			"fg": [
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA),
				pg.surface.Surface(self.window.get_size(), pg.SRCALPHA)
			]
		}
		self.clock = pg.time.Clock()
		self.lifespan = self.clock.tick()
		self.is_running = True
		self.is_paused = False
		if caption: pg.display.set_caption(caption)
	
	def game(self):
		text = self.FONT.render("game() is not yet implemented", True, "purple")
		self.window.blit(text, text.get_rect(center=self.window.get_rect().center))

	def run(self):
		while self.is_running:
			# If window is prompted to close
			if pg.event.get(pg.QUIT):
				self.is_running = False

			# Clear the canvas
			for layer in self.surfaces:
				for n in self.surfaces[layer]:
					n.fill((255, 255, 255, 0))
			self.window.fill("black")

			# Game logic
			self.game()
			
			# Update the canvas
			for layer in self.surfaces:
				for n in self.surfaces[layer]:
					self.window.blit(n, (0, 0))
			pg.display.update()

			if not self.is_paused:
				self.clock.tick()
				self.lifespan += self.clock.get_time()
			elif pg.event.get(pg.MOUSEBUTTONUP):
				self.is_paused = False
		pg.quit()

class PyGameGraph(PyGame):
	def __init__(
		self, tree: BinaryTree, window_size: Tuple[int, int] = (1366, 768), caption: str = ""
	):
		super().__init__(window_size, caption)
		self.tree = tree
		self.node_radius = 20
		self.background = pg.image.load("./src/soccer-brackets/view/images/Zakumi-BnW.png")
	
	def draw_tree(self, tree: BinaryTree, position: tuple[int], is_root = False):
		if tree:
			self.draw_node(tree, position, is_root)
			offset_x = 2 ** (tree.height(tree) - 2) * 0.03 * self.window.get_size()[0]
			if tree.get_left():
				# pos_left = (center - offset, top + trivial_value * diameter)
				pos_left = (position[0] - offset_x, position[1] + tree.height(tree) * 2 * self.node_radius)
				pg.draw.line(self.surfaces["bg"][1], "coral", position, pos_left, 3)
				self.draw_tree(tree.get_left(), pos_left)
			if tree.get_right():
				pos_right = (position[0] + offset_x, position[1] + tree.height(tree) * 2 * self.node_radius)
				pg.draw.line(self.surfaces["bg"][1], "coral", position, pos_right, 3)
				self.draw_tree(tree.get_right(), pos_right)
	
	def game(self):
		self.background = pg.transform.scale(self.background, self.window.get_size())
		self.surfaces["bg"][0].blit(self.background, self.window.get_rect())
		if self.tree:
			self.draw_tree(
				self.tree,
				(
					self.window.get_size()[0] / 2,
					self.window.get_size()[1] / 12
				),
				True
			)
			
	def draw_node(self, tree: BinaryTree, position: tuple[int] = (800, 450), is_root = False):
		node: Standing = tree.get_node()
		team_name = self.FONT.render(node.get_team().get_name(), True, "purple", "lightgreen")
		circle = pg.draw.circle(self.surfaces["bg"][2], "purple", position, self.node_radius)
		self.surfaces["fg"][0].blit(team_name, team_name.get_rect(center=circle.center))
		
		if not is_root:
			team_scores = self.FONT.render(f"{node.get_goals()}", True, "purple", "lightgreen")
			self.surfaces["fg"][0].blit(team_scores, team_scores.get_rect(center=(circle.center[0], circle.center[1] + 30)))

	# TODO
	def highlight_path(self):
		pass

	def __str__(self):
		pass