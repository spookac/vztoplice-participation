import json
import os

class DbOperations:
	def __init__(self, filename):
		self.filename = filename
		self.data = None
	
	def loadData(self):
		with open(self.filename) as jsondata:
			data = json.load(jsondata)
			return data
		
if __name__ == "__main__":
	db = DbOperations("db/procedures.json")
	data = db.loadData()
	for d in data:
		pretrag=None
		if d == 'procedures':
			print(data[d][0]["id"])
			print('Procedures, pretvaram u listu')
			pretrag = list(data[d])
			for i in range(0,len(pretrag)):
				singlePretrag = dict(pretrag[i])
				for k in singlePretrag.keys():
					print("Property: ", str(k), ", value: ", str(singlePretrag[k]))