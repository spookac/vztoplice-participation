import tkinter as tk

from .add import NewProcedureWindow
from .hzzobod import HZZOBodWindow

from ..jsondb import jsondb

class MainWindow(tk.Frame):
	def __init__(self, master=None, dbHandler=None):
		self.dbHandler = dbHandler
		
		tk.Frame.__init__(self, master)
		self.pack()
		
		if master:
			self.master = master
		
		self.createMenu()
		
	
	def createMenu(self):
		menubar = tk.Menu(self)
		
		#Add 'Options' menu
		optionsMenu = tk.Menu(menubar, tearoff=False)
		optionsMenu.add_command(label = "HZZO bod", command = self.editBod)
		optionsMenu.add_separator()
		optionsMenu.add_command(label = "Izlaz", command = self.master.quit)
		menubar.add_cascade(label = "Opcije", menu = optionsMenu)
		
		#Add 'Pretrage' menu
		procMenu = tk.Menu(menubar, tearoff=False)
		procMenu.add_command(label = "Dodaj pretragu", command = self.addProcedure)
		procMenu.add_command(label = "Uredi pretrage", command = self.editProcedure)
		menubar.add_cascade(label = "Pretrage", menu = procMenu)
		
		self.master.config(menu = menubar)
	
	
	def editBod(self):
		hzzoBodWindow = HZZOBodWindow(self.master, title = "HZZO bod", hzzoFactor = self.dbHandler.getHzzoBod())
		if hzzoBodWindow.result:
			self.dbHandler.updateHzzoBod(hzzoBodWindow.result)
	
	
	def addProcedure(self):
		addProcedureWindow = NewProcedureWindow(self.master, title = "Dodavanje nove pretrage")
		if addProcedureWindow.result and addProcedureWindow.result[0]:
			self.dbHandler.addProcedure(addProcedureWindow.result[0])
			if addProcedureWindow.result[1] == True:
				self.addProcedure()
	
	def editProcedure(self):
		pass