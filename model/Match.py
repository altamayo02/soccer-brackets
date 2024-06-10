import random

from model.ISerializable import ISerializable
from model.Standing import Standing
from model.Criterias import Criterias


class Match(ISerializable):
	def __init__(self, s1: Standing, s2: Standing, criteria: Criterias) -> None:
		self.criteria = criteria
		self.winner = None
		self.winner_index = None
		self.loser = None
		self.tie = False
		self._faceoff(s1, s2, criteria)
	
	def _faceoff(self, standing1: Standing, standing2: Standing, criteria: Criterias, definitive = False):
		crtr1 = standing1.get_team().get_stats()[criteria.name]
		crtr2 = standing2.get_team().get_stats()[criteria.name]
		if criteria.name == "ACCURACY":
			crtr1 = ["Baja", "Media", "Alta"].index(crtr1)
			crtr2 = ["Baja", "Media", "Alta"].index(crtr2)
		if crtr1 > crtr2:
			self.winner = standing1
			self.loser = standing2
			self.winner_index = 0
		elif crtr1 < crtr2:
			self.winner = standing2
			self.loser = standing1
			self.winner_index = 1
		elif not definitive:
			self._faceoff(standing1, standing2, Criterias((criteria.value + 1) % 4), True)
			return
		else:
			self.tie = True
			self.winner_index = random.randint(0, 1)
			self.winner = [standing1, standing2][self.winner_index]
			self.winner.set_score(self.winner.get_score() + 1)
			return
		self.winner.set_score(self.winner.get_score() + 3)
	
	def get_criteria(self):
		return self.criteria
	
	def get_winner(self):
		return self.winner
	
	def get_winner_index(self):
		return self.winner_index

	def get_loser(self):
		return self.loser
	
	def is_tied(self):
		return self.tie