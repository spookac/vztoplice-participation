import tkinter as tk
import itertools as it

from .add import NewProcedureWindow
from .edit import EditProcedureWindow
from .numberedit import FloatEditWindow

from ..jsondb import jsondb

class MainWindow(tk.Frame):
	def __init__(self, master=None, dbHandler=None):
		self.dbHandler = dbHandler
		
		self.tempProc = None
		self.listBoxIndexes = []
		
		#GUI elements
		self.listBox = None
		self.chosenFrame=None
		self.chosenProcedures=[]
		
		tk.Frame.__init__(self, master)
		self.pack()
		
		if master:
			self.master = master
		
		self.createMenu()
		
		body = tk.Frame(self)
		self.initial_focus = self.body(body) #Set initial focus to the body of the window
		#body.pack(padx=5, pady=5, fill="both", expand=1, side="left")
		body.columnconfigure(0, weight=1, minsize=310)
		body.columnconfigure(1, weight=1, minsize=310)
		body.grid(padx=10, pady=10)
		
		#Populate procedures
		self._reset()
	
	def createMenu(self):
		menubar = tk.Menu(self)
		
		#Add 'Options' menu
		optionsMenu = tk.Menu(menubar, tearoff=False)
		optionsMenu.add_command(label = "HZZO bod", command = self.editBod)
		optionsMenu.add_command(label = "Postotak participacije", command = self.editParticipationPercentage)
		optionsMenu.add_separator()
		optionsMenu.add_command(label = "Izlaz", command = self.master.quit)
		menubar.add_cascade(label = "Opcije", menu = optionsMenu)
		
		#Add 'Pretrage' menu
		procMenu = tk.Menu(menubar, tearoff=False)
		procMenu.add_command(label = "Dodaj pretragu", command = self.addProcedure)
		procMenu.add_command(label = "Uredi pretrage", command = self.editProcedure)
		menubar.add_cascade(label = "Pretrage", menu = procMenu)
		
		self.master.config(menu = menubar)
	
	def body(self, master):
		tk.Label(master, text = "Kliknite dvaput na pretragu kako biste ju dodali u izračun", foreground = "red").grid(row = 0, column = 0, sticky = "w", columnspan=2, in_=master)
		self.listBox = tk.Listbox(master, width=40, height=15)
		self.listBox.bind("<Double-Button-1>", self._addProcedureToList)
		self.listBox.grid(in_=master, sticky = "w", row=1, column=0)
		#self.listBox.grid(row = 1, column = 0, rowspan = 10)
		#chosenFrame = tk.Frame(mainFrame)
		#chosenFrame.grid(row = 1, column = 1)
		#tk.Label(chosenFrame, text = "Ovdje idu izabrane pretrage", foreground = "red").grid(row=0, column=0)
		tk.Label(master, text = "Odabrane pretrage").grid(row=0, column=1, sticky="n")
		self.chosenFrame = tk.Frame(master)
		self.chosenFrame.columnconfigure(0, weight=1)
		self.chosenFrame.columnconfigure(1, weight=1)
		self.chosenFrame.columnconfigure(2, weight=1)
		self.chosenFrame.grid(in_=master, row=1, column=1, sticky="n")
	
	def editBod(self):
		hzzoBodWindow = FloatEditWindow(self.master, title = "Uređivanje HZZO boda", floatNumber = self.dbHandler.getHzzoBod())
		if hzzoBodWindow.result:
			self.dbHandler.updateHzzoBod(hzzoBodWindow.result)
	
	def editParticipationPercentage(self):
		partWindow = FloatEditWindow(self.master, title = "Uređivanje postotka participacije", floatNumber = self.dbHandler.getParticipationPercentage())
		if partWindow.result:
			self.dbHandler.updateParticipationPercentage(partWindow.result)
	
	def addProcedure(self):
		addProcedureWindow = NewProcedureWindow(self.master, title = "Dodavanje nove pretrage")
		if addProcedureWindow.result and addProcedureWindow.result[0]:
			self.dbHandler.addProcedure(addProcedureWindow.result[0])
			if addProcedureWindow.result[1] == True:
				self.addProcedure()
	
	def editProcedure(self):
		editProcedureWindow = EditProcedureWindow(self.master, title = "Uređivanje pretraga", dbHandler = self.dbHandler)
		
	def _updateListbox(self):
		self.listBox.delete(0,"end")
		del self.listBoxIndexes[:]
		for procedure in self.procedures:
			if not procedure[1]:
				self.listBox.insert("end",procedure[0])
				self.listBoxIndexes.append(procedure[2])
	
	def _reset(self):
		tempProc = self.dbHandler.getProceduresASProceduresList()
		self.procedures = [[procedure, False, index] for index, procedure in enumerate(tempProc)]
		del self.listBoxIndexes[:]
		self._updateListbox()
		self._populateChosenProcedures()
	
	def _removeProcedureFromList(self, index, event=None):
		self.procedures[index][1]=False
		self._updateListbox()
	
	def _addProcedureToList(self, event=None):
		lbIndex = int(self.listBox.curselection()[0])
		realIndex = self.listBoxIndexes[lbIndex]
		self.procedures[realIndex][1]=True
		self._updateListbox()
		self._populateChosenProcedures()
	
	def _populateChosenProcedures(self):
		index = 0
		for widget in self.chosenFrame.winfo_children():
			widget.destroy()
		for procedure in self.procedures:
			if procedure[1]:
				tk.Label(self.chosenFrame, text = procedure[0].name).grid(row=index, column=0, sticky="nw")
				tk.Label(self.chosenFrame, text = (procedure[0].price, "kn")).grid(row=index, column=1, sticky="ne")
				def _removeProcedureFromList(event, self=self, index=procedure[2]): #To be able to give index to callback method
					return self.__removeProcedureFromList(event,index)
				w = tk.Label(self.chosenFrame, text = "Obriši", foreground="blue", cursor="hand2")
				w.grid(row=index, column=2, sticky="ne")
				w.bind("<Button-1>", _removeProcedureFromList)
				index+=1
	
	def __removeProcedureFromList(self, event=None, index=None):
		self.procedures[index][1]=False
		self._updateListbox()
		self._populateChosenProcedures()