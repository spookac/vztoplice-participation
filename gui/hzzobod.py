import tkinter as tk
from tkinter import messagebox
import os

class HZZOBodWindow(tk.Toplevel):
	
	def __init__(self, parent, title = None):
		tk.Toplevel.__init__(self, parent)
		self.transient(parent) #Set this window as temporary window of its parent
		if title:
			self.title(title)
		self.parent = parent
		self.result = None
		
		#Create body and set initial focus
		body = tk.Frame(self)
		self.initial_focus = self.body(body) #Set initial focus to the body of the window
		body.pack(padx=5, pady=5)
		
		self.createButtons() #Separately create buttons
		self.grab_set() #All events should be caught by this window

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel) #Proper way of handling cancelling dialog

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))

		self.initial_focus.focus_set()
		self.wait_window(self)
		
	
	def createButtons(self):
		box = tk.Frame(self)

		w = tk.Button(box, text="Prihvati", width=10, command=self.ok, default="active")
		w.pack(side="left", padx=5, pady=5)
		w = tk.Button(box, text="Odustani", width=10, command=self.cancel)
		w.pack(side="left", padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
		
	
	def ok(self, event=None):
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw() #Hide the window
		self.update_idletasks() #Update all tasks

		self.apply() #Call apply method to set the result

		self.cancel() #Destroy window by calling cancel method
	
	
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy() #Destroy Toplevel window
	
	
	def body(self, master):
		tk.Label(master, text = "HZZO Bod:").grid(row = 0, column = 0)
		self.bod = tk.Entry(master)
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