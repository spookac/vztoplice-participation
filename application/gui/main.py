import tkinter as tk
import itertools as it

from tkinter import StringVar

from .add import NewProcedureWindow
from .edit import EditProcedureWindow
from .numberedit import FloatEditWindow

from ..jsondb import jsondb

class MainWindow(tk.Frame):
	def __init__(self, master=None, dbHandler=None):
		self.dbHandler = dbHandler
		
		self.listBoxIndexes = []
		
		#GUI elements
		self.listBox = None
		self.chosenFrame=None
		self.chosenProcedures = []
		
		#Prices
		self.priceHzzo = StringVar()
		self.priceParticipation = StringVar()
		self.priceHospital = StringVar()

		#Factors
		self.hzzobod = 0
		self.participation = 0
		
		tk.Frame.__init__(self, master)
		self.pack()
		
		if master:
			self.master = master
		
		self.createMenu()
		
		body = tk.Frame(self)
		self.initial_focus = self.body(body) #Set initial focus to the body of the window
		body.columnconfigure(0, weight=1, minsize=310)
		body.columnconfigure(1, weight=1, minsize=310)
		body.grid(padx=10, pady=10)
		
		#Populate procedures
		self._reset()
		self._getFactors()
	
	def createMenu(self):
		menubar = tk.Menu(self)
		
		#Add 'Options' menu
		optionsMenu = tk.Menu(menubar, tearoff=False)
		optionsMenu.add_command(label = "Novi izračun", command = self.new)
		optionsMenu.add_separator()
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
		frameListBox = tk.Frame(master)
		self.listBox = tk.Listbox(frameListBox, width=40, height=15)
		self.listBox.bind("<Double-Button-1>", self._addProcedureToList)
		scrollbar = tk.Scrollbar(frameListBox)
		scrollbar.grid(row=0, column=1, sticky="nsw")
		self.listBox.grid(in_=frameListBox, sticky = "w", row=0, column=0)
		self.listBox.config(yscrollcommand = scrollbar.set)
		scrollbar.config(command=self.listBox.yview)
		frameListBox.grid(row=1, column=0, sticky="nw", in_=master)
		tk.Label(master, text = "Odabrane pretrage").grid(row=0, column=1, sticky="n")
		self.chosenFrame = tk.Frame(master, width=310)
		self.chosenFrame.columnconfigure(0, weight=1, minsize=200)
		self.chosenFrame.columnconfigure(1, weight=1, minsize=50)
		self.chosenFrame.columnconfigure(2, weight=1, minsize=50)
		self.chosenFrame.grid(in_=master, row=1, column=1, sticky="n")
		pricesFrame = tk.Frame(master, width=620)
		pricesFrame.columnconfigure(0, weight=1, minsize=120)
		pricesFrame.columnconfigure(1, weight=1, minsize=85)
		pricesFrame.columnconfigure(2, weight=1, minsize=120)
		pricesFrame.columnconfigure(3, weight=1, minsize=85)
		pricesFrame.columnconfigure(4, weight=1, minsize=120)
		pricesFrame.columnconfigure(5, weight=1, minsize=85)
		tk.Label(pricesFrame, text = "Ukupna HZZO Cijena: ", font = "Helvetica 11").grid(row=0, column=0, sticky="nw")
		tk.Label(pricesFrame, text = self.priceHzzo, textvariable = self.priceHzzo, font = "Helvetica 11 bold").grid(row=0, column=1, sticky="nsw")
		tk.Label(pricesFrame, text = "Iznos participacije: ", font = "Helvetica 11").grid(row=0, column=2, sticky="nw")
		tk.Label(pricesFrame, text = self.priceParticipation, textvariable = self.priceParticipation, font = "Helvetica 11 bold", fg="orange red").grid(row=0, column=3, sticky="nw")
		tk.Label(pricesFrame, text = "Privatno plaćanje: ", font = "Helvetica 11").grid(row=0, column=4, sticky="nw")
		tk.Label(pricesFrame, text = self.priceHospital, textvariable=self.priceHospital, font = "Helvetica 11 bold", fg="red").grid(row=0, column=5, sticky="nw")
		pricesFrame.grid(row=2, column=0, columnspan=2, pady=15)
	
	def new(self):
		self._reset()
	
	def editBod(self):
		hzzoBodWindow = FloatEditWindow(self.master, title = "Uređivanje HZZO boda", floatNumber = self.dbHandler.getHzzoBod())
		if hzzoBodWindow.result:
			self.dbHandler.updateHzzoBod(hzzoBodWindow.result)
			self._getFactors()
			self._updatePrices()
	
	def editParticipationPercentage(self):
		partWindow = FloatEditWindow(self.master, title = "Uređivanje postotka participacije", floatNumber = self.dbHandler.getParticipationPercentage())
		if partWindow.result:
			self.dbHandler.updateParticipationPercentage(partWindow.result)
			self._getFactors()
			self._updatePrices()
	
	def addProcedure(self):
		addProcedureWindow = NewProcedureWindow(self.master, title = "Dodavanje nove pretrage")
		if addProcedureWindow.result and addProcedureWindow.result[0]:
			self.dbHandler.addProcedure(addProcedureWindow.result[0])
			if addProcedureWindow.result[1] == True:
				self.addProcedure()
			self._updateAfterProcedureAction()
	
	def editProcedure(self):
		editProcedureWindow = EditProcedureWindow(self.master, title = "Uređivanje pretraga", dbHandler = self.dbHandler)
		self._updateAfterProcedureAction()
	
	def _reset(self):
		tempProc = self.dbHandler.getProceduresASProceduresList()
		self.procedures = None
		self.procedures = [[procedure, False, index] for index, procedure in enumerate(tempProc)]
		del self.chosenProcedures[:]
		self._updatePrices()
		self._updateListbox()
		self._populateChosenProcedures()
	
	def _getFactors(self):
		self.hzzobod = self.dbHandler.getHzzoBod()
		self.participation = self.dbHandler.getParticipationPercentage()
	
	def _addProcedureToList(self, event=None):
		lbIndex = int(self.listBox.curselection()[0])
		realIndex = self.listBoxIndexes[lbIndex]
		self.procedures[realIndex][1]=True
		self.chosenProcedures.append(self.procedures[realIndex][0].id)
		self._updatePrices()
		self._updateListbox()
		self._populateChosenProcedures()
	
	def _updateAfterProcedureAction(self):
		tempProc = self.dbHandler.getProceduresASProceduresList()
		self.procedures = []
		index=0
		for procedure in tempProc:
			if procedure.id in self.chosenProcedures:
				self.procedures.append([procedure, True, index])
			else:
				self.procedures.append([procedure, False, index])
			index+=1
		self._updatePrices()
		self._updateListbox()
		self._populateChosenProcedures()
			
	def __removeProcedureFromList(self, event=None, index=None):
		self.procedures[index][1]=False
		self._updatePrices()
		self._updateListbox()
		self._populateChosenProcedures()
	
	def _updateListbox(self):
		self.listBox.delete(0,"end")
		del self.listBoxIndexes[:]
		for procedure in self.procedures:
			if not procedure[1]:
				self.listBox.insert("end",procedure[0])
				self.listBoxIndexes.append(procedure[2])
	
	def _populateChosenProcedures(self):
		index = 0
		for widget in self.chosenFrame.winfo_children():
			widget.destroy()
		for procedure in self.procedures:
			if procedure[1]:
				tk.Label(self.chosenFrame, text = "{0: <30}".format(procedure[0].name[:30])).grid(row=index, column=0, sticky="nw")
				tk.Label(self.chosenFrame, text = ("{0:.2f} kn").format(procedure[0].price)).grid(row=index, column=1, sticky="ne")
				def _removeProcedureFromList(event, self=self, index=procedure[2]): #To be able to give index to callback method
					return self.__removeProcedureFromList(event,index)
				w = tk.Label(self.chosenFrame, text = "Obriši", foreground="blue", cursor="hand2")
				w.grid(row=index, column=2, sticky="ne")
				w.bind("<Button-1>", _removeProcedureFromList) #bind to internal method
				index+=1
	
	def __calculatePrices(self):
		priceHospital = 0
		priceHzzo = 0
		priceHzzoParticipation = 0
		for procedure in self.procedures:
			if procedure[1]:
				priceHospital+=procedure[0].price
				priceHzzo+=(self.hzzobod*procedure[0].hzzobod)
		priceHzzoParticipation = priceHzzo * (self.participation/100)
		return [priceHzzo, priceHzzoParticipation, priceHospital]
		
	def _updatePrices(self):
		prices = self.__calculatePrices()
		self.priceHzzo.set("{0:.2f} kn".format(prices[0]))
		self.priceParticipation.set("{0:.2f} kn".format(prices[1]))
		self.priceHospital.set("{0:.2f} kn".format(prices[2]))