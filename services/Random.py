import random

def random_alphanumerical(length: int) -> str:
	string = ""
	for _ in range(length):
		string += random.choice([
			chr(random.randint(ord("a"), ord("z"))),
			chr(random.randint(ord("a"), ord("z"))).upper()
		])
	return string