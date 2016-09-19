import tkinter as tk
import os

class SimpleDialog(tk.Toplevel):
	def __init__(self, parent, title=None):
		tk.Toplevel.__init__(self, parent) #Set this window as temporary window of its parent
		self.transient(parent)
		if title:
			self.title(title)
		self.parent = parent #Set parent to parent window
		self.result = None #Assign initial result of dialog window
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
	
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy() #Destroy Toplevel window
	
	def ok(self, event=None):
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		self.withdraw() #Hide the window
		self.update_idletasks() #Update all tasks
		self.apply() #Call apply method to set the result
		self.cancel() #Destroy window by calling cancel method
	
	def createButtons(self):
		pass #Virtual method, requires implementation
	
	def body(self, master):
		pass #Virtual method, requires implementation
	
	def validate(self):
		pass #Virtual method, requires implementation
	
	def apply(self):
		pass #Virtual method, requires implementation