# -*- coding: utf-8 -*-

class Procedure:
	def __init__(self, id, name, hzzobod, price, category=None):
		self.id = id
		self.name = name
		self.hzzobod = hzzobod
		self.price = price
		self.category=None
		if category:
			self.category = category
	
	def __str__(self):
		return self.name

class JSONDB:
	def __init__(self, hzzobod, procedures):
		self.hzzobod = hzzobod
		self.procedures = procedures
	
	def toJson(self):
		json = {}
		json["hzzo-factor"] = self.hzzobod
		json["procedures"] = []
		for i in range(0,len(self.procedures)):
			json["procedures"].append(JSONDB.fromProcedure(JSONDB.toProcedure(self.procedures[i])))
		return json
	
	@staticmethod
	def toProcedure(procedure):
		id = procedure["id"]
		name = procedure["name"]
		hzzobod = procedure["hzzo-score"]
		price = procedure["hospital-price"]
		category = None
		if procedure["category"]:
			category = procedure["category"]
		return Procedure(id, name, hzzobod, price, category)
	
	@staticmethod
	def fromProcedure(procedure):
		jsonRecord = {
			"id": procedure.id,
			"name": procedure.name,
			"hzzo-score": procedure.hzzobod,
			"hospital-price": procedure.price,
			"category": procedure.category
		}
		return jsonRecord
	