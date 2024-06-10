import json

class JsonService:
	def __init__(self, verbose = False) -> None:
		self.verbose = verbose

	def save_json(cls, file_path: str, content: dict | list) -> None:
		with open(file_path, "w", encoding="utf-8") as fp:
			json.dump(content, fp, indent=4, ensure_ascii=False)
			if cls.verbose:
				print(f"{file_path} written successfully!")
	
	def load_json(cls, file_path: str) -> any:
		with open(file_path, "r", encoding="utf-8") as fp:
			data = json.loads(fp.read())
			if cls.verbose:
				print(f"{file_path} loaded successfully!")
			return data