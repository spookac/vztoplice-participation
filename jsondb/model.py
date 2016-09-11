class Procedure:
	def __init__(self, id, name, hzzobod, price, category=None):
		self.id = id
		self.name = name
		self.hzzobod = hzzobod
		self.price = price
		if category:
			self.category = category

class JSONDB:
	def __init__(self, hzzobod, procedures):
		self.hzzobod = hzzobod
		self.procedures = procedures