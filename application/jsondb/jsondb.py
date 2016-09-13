import json
import os

from model import JSONDB
from model import Procedure

class DbOperations:
	def __init__(self, filename):
		self.filename = filename
		self.data = None
	
	def loadData(self):
		data = None
		with open(self.filename) as jsondata:
			data = json.load(jsondata, encoding="utf-8")
		return JSONDB(data["hzzo-factor"], data["procedures"])
	
	def saveData(self, data):
		with open(self.filename) as jsonFile:
			json.dump(data, jsonFile)
		
	def addProcedure(self, procedure):
		data = self.loadData()
		data.procedures.append(JSONDB.fromProcedure(procedure))
		dataToSave = data.toJson()
		self.saveData(dataToSave)
		
		
if __name__ == "__main__":
	db = DbOperations("db/procedures.json")
	data = db.loadData()
	print("HZZO Bod: ", data.hzzobod)
	i = 0
	for procedure in data.procedures:
		proc = JSONDB.toProcedure(procedure)
		i = i + 1
		print("---- Pretraga {0} ----". format(i))
		print("ID:", repr(proc.id))
		print("Name: ", (proc.name).encode("utf-8"))
		print("HZZO bod: ", repr(proc.hzzobod))
		print("Price: ", repr(proc.price))
		print("Category: ", repr(proc.category))
	newProc = Procedure("LB004","Ime procedure", 0.43, 45.05)
	db.addProcedure(newProc)