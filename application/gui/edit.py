# -*- coding: utf-8 -*-

import tkinter as tk
import os

from tkinter import messagebox
from tkinter import StringVar
from .dialog import SimpleDialog

from ..jsondb.model import Procedure
from ..jsondb import jsondb

class EditProcedureWindow(SimpleDialog):
	def __init__(self, parent, title=None, dbHandler=None):
		self.procedures = None
		self.lstBox = None
		self.currentSelection = None
		self.id = StringVar()
		self.name = StringVar()
		self.hzzoscore = StringVar()
		self.price = StringVar()
		self.cat = StringVar()
		self.dbHandler = dbHandler
		if self.dbHandler:
			self.procedures = self.dbHandler.getProceduresASProceduresList()
		SimpleDialog.__init__(self, parent, title) 
		
	def createButtons(self):
		buttonBox = tk.Frame(self)
		w = tk.Button(buttonBox, text="Spremi", width=13, command=self.save)
		w.pack(side="left", padx=5, pady=5)
		#w = tk.Button(buttonBox, text="Spremi i zatvori", width=13, command=self.cancel)
		#w.pack(side="left", padx=5, pady=5)
		w = tk.Button(buttonBox, text="Odustani i zatvori", width=13, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		buttonBox.pack(side="right")
	
	def body(self, master):
		#Create and pack listbox
		mainFrame = tk.Frame(self)
		tk.Label(mainFrame, text = "Kliknite dvaput na pretragu kako bi se prikazali svi podaci", foreground = "red").grid(row = 0, column = 0, sticky = "w", columnspan=3)
		listboxFrame = tk.Frame(mainFrame)
		self.lstBox = tk.Listbox(listboxFrame, width=40, height=10)
		scrollBar = tk.Scrollbar(listboxFrame)
		scrollBar.grid(in_=listboxFrame, row=1, column=1, sticky="nsw")
		self.lstBox.bind("<Double-Button-1>", self.openProcedure)
		self.lstBox.grid(row = 1, column = 0)
		self.lstBox.config(yscrollcommand = scrollBar.set)
		scrollBar.config(command=self.lstBox.yview)
		listboxFrame.grid(row=1, column=0, sticky="w", rowspan=10)
		tk.Label(mainFrame, text = "Šifra pretrage (*):").grid(row = 1, column = 1, sticky = "w", padx=5)
		tk.Label(mainFrame, text = "Ime pretrage (*):").grid(row = 2, column = 1, sticky = "w", padx=5)
		tk.Label(mainFrame, text = "HZZO bodovi (*):").grid(row = 3, column = 1, sticky = "w", padx=5)
		tk.Label(mainFrame, text = "Cijena za privatno plaćanje (*):").grid(row = 4, column = 1, sticky = "w", padx=5)
		tk.Label(mainFrame, text = "Kategorija:").grid(row = 5, column = 1, sticky = "w", padx=5)
		self.sifra = tk.Entry(mainFrame, width=30, state="disabled", textvariable=self.id)
		self.sifra.grid(row = 1, column = 2)
		self.ime = tk.Entry(mainFrame, width=30, textvariable=self.name)
		self.ime.grid(row = 2, column = 2)
		self.hzzobod = tk.Entry(mainFrame, width=30, textvariable=self.hzzoscore)
		self.hzzobod.grid(row = 3, column = 2)
		self.privatno = tk.Entry(mainFrame, width=30, textvariable=self.price)
		self.privatno.grid(row = 4, column = 2)
		self.category = tk.Entry(mainFrame, width=30, textvariable=self.cat)
		self.category.grid(row = 5, column = 2)
		mainFrame.pack(padx=5, pady=5)
		
		#Populate procedures
		self._updateListbox()
		
	
	def validate(self):
		if self.sifra.index("end") == 0 or self.ime.index("end") == 0 or self.hzzobod.index("end") == 0 or self.privatno.index("end") == 0:
			tk.messagebox.showwarning(
				"Nisu popunjeni svi podaci",
				"Molim popuniti barem sljedeće podatke: 'Ime pretrage', 'HZZO bodovi' i 'Cijena za privatno plaćanje'."
			)
			return 0
		else:
			try:
				correctBodovi = float(self.hzzobod.get())
				correctPrivatno = float(self.privatno.get())
				return 1
			except ValueError:
				tk.messagebox.showwarning(
					"Nepravilan format brojeva", 
					"Unsesni format brojeva nije ispravan. Molim koristiti samo brojke te tocku (.) ako je rijec o decimalnom broju"
				)
				return 0
	
	def apply(self):
		pass
	
	def save(self):
		if not self.validate():
			return
		proc = Procedure(self.sifra.get(), self.ime.get(), float(self.hzzobod.get()), float(self.privatno.get()), self.category.get())
		self.procedures[self.currentSelection] = proc
		self.dbHandler.updateProcedure(proc)
		self._resetProcedure()
		self._updateListbox()
	
	def openProcedure(self, event=None):
		self.currentSelection = self.lstBox.curselection()[0]
		self.id.set(self.procedures[self.currentSelection].id)
		self.name.set(self.procedures[self.currentSelection].name)
		self.hzzoscore.set(self.procedures[self.currentSelection].hzzobod)
		self.price.set(self.procedures[self.currentSelection].price)
		self.cat.set(self.procedures[self.currentSelection].category)
		
	def _resetProcedure(self):
		self.id.set("")
		self.name.set("")
		self.hzzoscore.set("")
		self.price.set("")
		self.cat.set("")
		
	def _updateListbox(self):
		self.lstBox.delete(0,"end")
		for procedure in self.procedures:
			self.lstBox.insert("end", procedure)