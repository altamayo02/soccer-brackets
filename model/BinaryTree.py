from typing import Self
from .ISerializable import ISerializable


class BinaryTree(ISerializable):
	def __init__(self, node = None, left: Self = None, right: Self = None):
		self.node = node
		self.left = left
		self.right = right
	
	def get_node(self) -> any:
		#if type(self.node) is SoccerTeam:
		#if type(self.node).__class__.__module__ != "__builtin__":
		#if issubclass(type(self.node), ISerializable):
			# Only for the static analyzer
			#self.node: ISerializable
			#return self.node.to_dict()
		return self.node
	
	def get_left(self) -> Self:
		return self.left

	def get_right(self) -> Self:
		return self.right
	
	def set_node(self, node):
		self.node = node

	def set_left(self, left):
		self.left = left

	def set_right(self, right):
		self.right = right
	
	def in_order(self, tree: Self, f = None, *args):
		if tree:
			if not f:
				f = tree.get_node
			return (
				self.in_order(tree.get_left(), f, *args) +
				[f(tree)] +
				self.in_order(tree.get_right(), f, *args)
			)
		return []
		
	def pre_order(self, tree: Self, f = None, *args):
		if tree:
			if not f:
				f = tree.get_node
			return (
				[f(tree, *args)] +
				self.pre_order(tree.get_left(), f, *args) +
				self.pre_order(tree.get_right(), f, *args)
			)
		return []

	def post_order(self, tree: Self, f = None, *args):
		if tree:
			if not f:
				f = tree.get_node
			return (
				self.post_order(tree.get_left(), f, *args) +
				self.post_order(tree.get_right(), f, *args) +
				[f(tree)]
			)
		return []
		
	def height(self, tree: Self):
		if tree:
			return max(
				self.height(tree.get_left()) + 1,
				self.height(tree.get_right()) + 1
			)
		return 0

	def weight(self, tree: Self):
		if tree:
			return 1 + (
				self.weight(tree.get_left()) +
				self.weight(tree.get_right())
			)
		return 0

	def min(self, tree: Self):
		if tree:
			if not tree.get_left():
				return tree.get_node()
			return self.min(tree.get_left())
		return None

	def max(self, tree: Self):
		if tree:
			if not tree.get_right():
				return tree.get_node()
			return self.max(tree.get_right())
		return None

	def balance(self, tree: Self):
		return self.height(tree.get_left()) - self.height(tree.get_right())

	def levels(self, tree: Self):
		queue = [tree]
		while queue:
			first = queue.pop(0)
			print(first.get_node())
			if first.get_left():
				queue.append(first.get_left())
			if first.get_right():
				queue.append(first.get_left())

	def branch(self, node: Self):
		# This is private!!! Encapsulation!!!
		# Cierra el goteo (?)
		def visit_branch(tree: Self, branch: list, branches: list):
			if not tree:
				return
			branch.append(tree.get_node())
			if not tree.get_left() and not tree.get_right():
				branches.append(branch.copy())
			else:
				visit_branch(tree.get_left(), branch, branches)
				visit_branch(tree.get_right(), branch, branches)
			branch.pop()
		return visit_branch(node, [], [])

	def to_dict(self, tree: Self = None) -> dict:
		if self.node:
			if not tree:
				tree = self
			return {
				"node": tree.get_node(),
				"left": self.to_dict(tree.get_left()) if tree.get_left() else None,
				"right": self.to_dict(tree.get_right()) if tree.get_right() else None
			}
	
	def __str__(self) -> str:
		left = self.left.get_node() if self.left else "."
		right = self.right.get_node() if self.right else "."
		return f"[{left} <- {self.node} -> {right}]"