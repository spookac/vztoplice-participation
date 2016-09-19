import json
import os

from .model import JSONDB
from .model import Procedure

class DbOperations:
	def __init__(self, filename):
		self.filename = filename
	
	def loadData(self):
		data = None
		with open(self.filename) as jsondata:
			data = json.load(jsondata, encoding="utf-8")
		return JSONDB(data["hzzo-factor"], data["procedures"])
	
	def saveData(self, data):
		with open(self.filename, "w+") as jsonFile:
			json.dump(data, jsonFile, sort_keys = True, indent = 4, ensure_ascii = True)
		
	def getHzzoBod(self):
		data = self.loadData()
		return data.hzzobod
	
	def updateHzzoBod(self, hzzoBodValue):
		data = self.loadData()
		data.hzzobod = hzzoBodValue
		dataToSave = data.toJson()
		self.saveData(dataToSave)
	
	def addProcedure(self, procedure):
		data = self.loadData()
		if not self.procedureExists(data, procedure):
			data.procedures.append(JSONDB.fromProcedure(procedure))
			dataToSave = data.toJson()
			self.saveData(dataToSave)
		else:
			self.updateProcedure(procedure)
		
	def updateProcedure(self, procedure):
		data = self.loadData()
		currentProcedure = self.findProcedureByIdOrName(data, procedure.id, procedure.name)
		if currentProcedure != None:
			currentProcedure[0].id = procedure.id
			currentProcedure[0].name = procedure.name
			currentProcedure[0].hzzobod = procedure.hzzobod
			currentProcedure[0].price = procedure.price
			currentProcedure[0].category = procedure.category
			data.procedures[currentProcedure[1]] = JSONDB.fromProcedure(currentProcedure[0])
		dataToSave = data.toJson()
		self.saveData(dataToSave)		
	
	def procedureExists(self, data, procedure):
		for proc in data.procedures:
			procTemp = JSONDB.toProcedure(proc)
			if procTemp.id == procedure.id or procTemp.name == procedure.name:
				return True
				break
		return False
	
	def findProcedureByIdOrName(self, data, id=None, name=None):
		if not id and not name:
			raise ValueError("At least one of the parameters 'id' or 'name' must be provided")
		i = 0
		for proc in data.procedures:
			procTemp = JSONDB.toProcedure(proc)
			if procTemp.id == id or procTemp.name == name:
				return list([procTemp, i])
			i = i + 1
		return None
		
	def getProceduresASProceduresList(self):
		procedurelist = []
		jsondb = self.loadData()
		for procedure in jsondb.procedures:
			procedurelist.append(JSONDB.toProcedure(procedure))
		return procedurelist
		
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
	newProc = Procedure("LB004","Ime procedure", 0.45, 49.02)
	db.addProcedure(newProc)