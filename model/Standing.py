from copy import deepcopy

from model.ISerializable import ISerializable
from model.Team import Team


class Standing(ISerializable):
	def __init__(self, team: Team = None, goals: int = 0, score: int = 0) -> None:
		self.team = team
		self.goals = goals
		self.score = score
	
	def get_team(self):
		return self.team
	
	def get_goals(self):
		return self.goals
	
	def get_score(self):
		return self.score

	def set_goals(self, goals: int):
		self.goals = goals

	def set_score(self, score: int):
		self.score = score

	def deep_copy(self):
		return deepcopy(self)

	def __str__(self) -> str:
		return f"({self.get_goals()}, {self.get_score()}) {self.team.get_name()}"