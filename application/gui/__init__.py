import tkinter as tk

from .main import MainWindow
from ..jsondb import jsondb

class Gui:
	
	def __init__(self, width, height):
		self.applicationRoot = None	
		self.jsonData = None
		self.size = str(width) + 'x' + str(height)
	
	def startApplication(self, pathToDB):
		self.dbHandler = jsondb.DbOperations(pathToDB)
		self.applicationRoot = tk.Tk()
		self.applicationRoot.title("Specijalna bolnica za medicinsku rehabilitaciju Varazdinske Toplice")
		#self.applicationRoot.geometry(self.size)
		self.applicationRoot.resizable(False, False)
		window = MainWindow(self.applicationRoot, self.dbHandler)
		self.applicationRoot.mainloop()