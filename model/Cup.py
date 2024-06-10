import random

from model.BinaryTree import BinaryTree
from model.Criterias import Criterias
from model.ISerializable import ISerializable
from model.Match import Match
from model.Standing import Standing
from model.Team import Team
from view.QtUI import QtUI
from view.PyGameGraph import PyGameGraph


class Cup(ISerializable):
	def __init__(
		self,
		ui_path: str,
		groups: dict[str, list[Team]] = {}
	) -> None:
		self.groups = groups
		if len(groups) == 0:
			self.groups = { chr(i): [] for i in range(ord("A"), ord("I")) }
		self.ui = QtUI(
			ui_path,
			self.groups,
			{
				"add": self.add_team,
				"sim": self.simulate_jornada,
				"draw": self.show_brackets,
				"save": self.save_data,
				"load": self.load_data
			}
		)
		self.jornadas: list[list[BinaryTree]] = []
		self.group_size = 4
		self.num_groups = 8

	def get_ui(self) -> QtUI:
		return self.ui

	def get_groups(self) -> list[str]:
		return self.groups

	def get_jornadas(self) -> BinaryTree:
		return self.jornadas

	def get_group_size(self):
		return self.group_size

	def get_num_groups(self):
		return self.num_groups

	def get_max_teams(self):
		return self.num_groups * self.group_size

	def add_team(self):
		data = self.ui.get_team_form_data()
		name = data["name"]
		group = data["group"]
		del data["name"]
		del data["group"]

		if len(self.groups[group]) < 4:
			team = Team(
				group=group,
				name=name,
				stats=data
			)
			self.groups[group].append(team)
			self.ui.update_groups(self.groups)
		else:
			self.ui.warn(
				f"El equipo {group} ya tiene {len(self.groups[group])} integrantes." +
				"Ingrese el equipo a otro grupo."
			)

	# TODO
	def disqualify_team(self):
		pass

	def simulate_jornada(self, id_criteria: int):
		num_teams = self.count_teams()
		if num_teams != self.get_max_teams():
			self.ui.warn(
				f"Se requieren {self.get_max_teams()} equipos para simular la copa." +
				f"Se han recibido: {num_teams}"
			)
			return
		if len(self.jornadas) > 0:
			self.jornadas.append([])
			jornada = self.jornadas[-2]
			for t in range(0, len(jornada), 2):
				standing1: Standing = jornada[t].get_node()
				standing2: Standing = jornada[t + 1].get_node()
				match = Match(standing1, standing2, Criterias(id_criteria))
				if match.is_tied():
					goals = random.randint(0, 3)
					standing1.set_goals(goals)
					standing2.set_goals(goals)
				else:
					goals = [0, 0]
					while goals[0] == goals[1]:
						goals = sorted([random.randint(1, 5) for _ in range(2)])
					standing1.set_goals(goals[0])
					standing2.set_goals(goals[0])
					# Winner before upstreaming it in the tree
					lower_winner: Standing = [
						standing1, standing2
					][match.get_winner_index()]
					lower_winner.set_goals(goals[1])
					#print(goals, standing1, standing2)
				bintree = BinaryTree(match.get_winner().deep_copy(), jornada[t], jornada[t + 1])
				self.jornadas[-1].append(bintree)
		else:
			self.jornadas.append([])
			for g in self.groups:
				group = self.groups[g]
				# To find the correct standing again, team is left outside
				standings = {team: Standing(team) for team in group}
				for t1 in range(len(group) - 1):
					for t2 in range(1 + t1, len(group)):
						match = Match(
							standings[group[t1]],
							standings[group[t2]],
							Criterias(id_criteria)
						)
				winners = sorted(standings.values(), key=lambda s: s.get_score())[:2:]
				for winner in winners:
					self.jornadas[0].append(BinaryTree(winner))
		self.ui.update_jornadas(self.jornadas)

	# TODO - Show all possibilities
	def show_brackets(self):
		pgg = PyGameGraph(self.get_jornadas()[-1][0])
		pgg.run()

	# TODO
	def show_earnings(self):
		pass

	def load_data(self, data: dict):
		if not data:
			data = self.ui.open_file()
		for g in data:
			group: list[dict] = data[g]
			self.groups[g] = [Team(
				team["id"], g, team["name"], team["stats"]
			) for team in group]
		self.ui.update_groups(self.groups)

	def save_data(self):
		groups = {}
		for g in self.groups:
			groups[g] = [team.to_dict() for team in self.groups[g]]
		self.ui.save_file(groups)
	
	def count_teams(self) -> int:
		num_teams = 0
		for g in self.groups:
			num_teams += len(self.groups[g])
		return num_teams