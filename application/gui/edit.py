import tkinter as tk
import os

from tkinter import messagebox
from .dialog import SimpleDialog

from ..jsondb.model import Procedure

class EditProcedureWindow(SimpleDialog):
	def __init__(self, parent, title=None):
		SimpleDialog.__init__(self, parent, title)
		
	def createButtons(self):
		buttonBox = tk.Frame(self)
		w = tk.Button(buttonBox, text="Zatvori", width=12, command=self.cancel)
		w.pack(side="right", padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		buttonBox.pack()
	
	def body(self, master):
		pass
	
	def validate(self):
		pass
	
	def apply(self):
		pass