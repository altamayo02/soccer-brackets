import random

from model.ISerializable import ISerializable
from model.Criterias import Criterias
import services.Random as rnd


class Team(ISerializable):
	def __init__(
		self,
		id: str = None,
		group: str = "Z",
		name: str = "Los innombrables",
		stats: dict[Criterias, float] = {},
	) -> None:
		self.id = id
		if not id:
			self.id = f"T-{rnd.random_alphanumerical(6)}"
		self.name = name
		self.group = group
		self.stats = {}
		if len(stats) == 0:
			for i in range(1, len(Criterias) + 1):
				#self.stats[Criterias(i).name] = 0
				self.stats[Criterias(i).name] = random.randint(1, 10)
		else:
			self.stats = stats
	
	def get_id(self):
		return self.id
	
	def get_name(self):
		return self.name
	
	def get_group(self):
		return self.group
	
	def get_stats(self):
		return self.stats

	def set_id(self, id):
		self.id = id

	def set_name(self, name):
		self.name = name

	def set_group(self, group):
		self.group = group

	def set_stats(self, stats):
		self.stats = stats
	
	def __str__(self) -> str:
		return f"({self.group}) {self.name}: {self.stats}"
	
	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"stats": self.stats
		}