import tkinter as tk
import os

from tkinter import messagebox
from tkinter import StringVar
from .dialog import SimpleDialog

class HZZOBodWindow(SimpleDialog):
	
	def __init__(self, parent, title=None, hzzoFactor=0):
		self.hzzobod = StringVar()
		self.hzzobod.set(hzzoFactor)
		SimpleDialog.__init__(self, parent, title)
	
	def createButtons(self):
		box = tk.Frame(self)

		w = tk.Button(box, text="Prihvati", width=10, command=self.ok, default="active")
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(box, text="Odustani", width=10, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	
	def body(self, master):
		tk.Label(master, text = "HZZO Bod:").grid(row = 0, column = 0)
		self.bod = tk.Entry(master, textvariable=self.hzzobod)
		self.bod.grid(row = 0, column = 1) #Put it in grid after the value is assigned, otherwise it will be None
	
	
	def validate(self):
		try:
			correctScore = float(self.bod.get())
			return 1
		except ValueError:
			tk.messagebox.showwarning(
				"Nepravilan format boda", 
				"Unsesni format boda nije ispravan. Molim koristiti samo brojke te tocku (.) ako je rijec o decimalnom broju"
			)
			return 0
	
	
	def apply(self):
		self.result = float(self.bod.get())