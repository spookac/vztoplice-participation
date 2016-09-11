import tkinter as tk
import os

from tkinter import messagebox
from .dialog import SimpleDialog

class NewProcedureWindow(SimpleDialog):

	def __init__(self, parent, title=None):
		SimpleDialog.__init__(self, parent, title)
		self.sifra=None
		self.ime=None
		self.hzzobod=None
		self.privatno=None
		self.category=None
	
	def createButtons(self):
		box = tk.Frame(self)
		
		w = tk.Button(box, text="Spremi i zatvori", width=12, command=self.ok, default="active")
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(box, text="Spremi i novi", width=12, command=self.applyandnew)
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(box, text="Odustani", width=12, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)
		
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		
		box.pack()
		
	def body(self, master):
		tk.Label(master, text = "Šifra pretrage (*):").grid(row = 0, column = 0, sticky = "w")
		tk.Label(master, text = "Ime pretrage (*):").grid(row = 1, column = 0, sticky = "w")
		tk.Label(master, text = "HZZO bodovi (*):").grid(row = 2, column = 0, sticky = "w")
		tk.Label(master, text = "Cijena za privatno plaćanje (*):").grid(row = 3, column = 0, sticky = "w")
		tk.Label(master, text = "Kategorija:").grid(row = 4, column = 0, sticky = "w")
		tk.Label(master, text = "Unosi označeni sa zvijezdicom (*) su obavezni", foreground = "red").grid(row = 5, sticky = "w", columnspan = 2)
		self.sifra = tk.Entry(master)
		self.sifra.grid(row = 0, column = 1)
		self.ime = tk.Entry(master)
		self.ime.grid(row = 1, column = 1)
		self.hzzobod = tk.Entry(master)
		self.hzzobod.grid(row = 2, column = 1)
		self.privatno = tk.Entry(master)
		self.privatno.grid(row = 3, column = 1)
		self.category = tk.Entry(master)
		self.category.grid(row = 4, column = 1)
	
	def validate(self):
		if self.sifra.index("end") == 0 or self.ime.index("end") == 0 or self.hzzobod.index("end") == 0 or self.privatno.index("end") == 0:
			tk.messagebox.showwarning(
				"Nisu popunjeni svi podaci",
				"Molim popuniti barem sljedeće podatke: 'Šifra pretrage', 'Ime pretrage', 'HZZO bodovi' i 'Cijena za privatno plaćanje'."
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
		
	def applyandnew(self):
		pass