import tkinter as tk

from .add import NewProcedureWindow
from .hzzobod import HZZOBodWindow

class MainWindow(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		
		if master:
			self.master = master
		
		self.createMenu()
		
	
	def createMenu(self):
		menubar = tk.Menu(self)
		
		#Add 'Options' menu
		optionsMenu = tk.Menu(menubar)
		optionsMenu.add_command(label = "HZZO bod", command = self.editBod)
		optionsMenu.add_separator()
		optionsMenu.add_command(label = "Izlaz", command = self.master.quit)
		menubar.add_cascade(label = "Opcije", menu = optionsMenu)
		
		#Add 'Pretrage' menu
		procMenu = tk.Menu(menubar)
		procMenu.add_command(label = "Dodaj pretragu", command = self.addProcedure)
		procMenu.add_command(label = "Uredi pretrage", command = self.editProcedure)
		menubar.add_cascade(label = "Pretrage", menu = procMenu)
		
		self.master.config(menu = menubar)
	
	
	def editBod(self):
		hzzoBodWindow = HZZOBodWindow(self.master, title = "HZZO bod")
		if hzzoBodWindow.result:
			print("Postavljeni bodovi: {0:2f}".format(hzzoBodWindow.result))
	
	
	def addProcedure(self):
		addProcedureWindow = NewProcedureWindow(self.master, title = "Dodavanje nove pretrage")
		if not addProcedureWindow.result:
			print("Dodana nova pretraga")
	
	def editProcedure(self):
		pass