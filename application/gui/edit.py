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
		if dbHandler:
			self.procedures = dbHandler.getProceduresASProceduresList()
		SimpleDialog.__init__(self, parent, title) 
		
	def createButtons(self):
		buttonBox = tk.Frame(self)
		w = tk.Button(buttonBox, text="Spremi", width=13, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(buttonBox, text="Spremi i zatvori", width=13, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(buttonBox, text="Odustani i zatvori", width=13, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		buttonBox.pack(side="right")
	
	def body(self, master):
		#Create and pack listbox
		mainFrame = tk.Frame(self)
		tk.Label(mainFrame, text = "Kliknite dvaput na pretragu kako bi se prikazali svi podaci", foreground = "red").grid(row = 0, column = 0, sticky = "w", columnspan=3)
		self.lstBox = tk.Listbox(mainFrame, width=40)
		#self.lstBox.pack(side="left", fill = "both", expand = 1)
		self.lstBox.bind("<Double-Button-1>", self.openProcedure)
		for procedure in self.procedures:
			self.lstBox.insert("end", procedure)
		self.lstBox.grid(row = 1, column = 0, rowspan = 10)
		#Listbox
		#Create and pack entries
		#entriesFrame = tk.Frame(mainFrame)
		tk.Label(mainFrame, text = "Šifra pretrage (*):").grid(row = 1, column = 1, sticky = "w")
		tk.Label(mainFrame, text = "Ime pretrage (*):").grid(row = 2, column = 1, sticky = "w")
		tk.Label(mainFrame, text = "HZZO bodovi (*):").grid(row = 3, column = 1, sticky = "w")
		tk.Label(mainFrame, text = "Cijena za privatno plaćanje (*):").grid(row = 4, column = 1, sticky = "w")
		tk.Label(mainFrame, text = "Kategorija:").grid(row = 5, column = 1, sticky = "w")
		self.sifra = tk.Entry(mainFrame, textvariable=self.id)
		self.sifra.grid(row = 1, column = 2)
		self.ime = tk.Entry(mainFrame, textvariable=self.name)
		self.ime.grid(row = 2, column = 2)
		self.hzzobod = tk.Entry(mainFrame, textvariable=self.hzzoscore)
		self.hzzobod.grid(row = 3, column = 2)
		self.privatno = tk.Entry(mainFrame, textvariable=self.price)
		self.privatno.grid(row = 4, column = 2)
		self.category = tk.Entry(mainFrame, textvariable=self.cat)
		self.category.grid(row = 5, column = 2)
		#entriesFrame.pack()
		mainFrame.pack(padx=5, pady=5)
		#entriesFrame.grid(row = 0, column = 1)
		
	
	def validate(self):
		pass
	
	def apply(self):
		pass
	
	def openProcedure(self, event=None):
		self.currentSelection = self.lstBox.curselection()[0]
		self.id.set(self.procedures[self.currentSelection].id)
		self.name.set(self.procedures[self.currentSelection].name)
		self.hzzoscore.set(self.procedures[self.currentSelection].hzzobod)
		self.price.set(self.procedures[self.currentSelection].price)
		self.cat.set(self.procedures[self.currentSelection].category)