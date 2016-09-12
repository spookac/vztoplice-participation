import tkinter as tk

from .main import MainWindow

class Gui:
	
	def __init__(self, width, height):
		self.applicationRoot = None	
		self.jsonData = None
		self.size = str(width) + 'x' + str(height)
	
	def startApplication(self):
		self.applicationRoot = tk.Tk()
		self.applicationRoot.title("Specijalna bolnica za medicinsku rehabilitaciju Varazdinske Toplice")
		self.applicationRoot.geometry(self.size)
		self.applicationRoot.resizable(False, False)
		window = MainWindow(self.applicationRoot)
		self.applicationRoot.mainloop()
	
	def provideData(self, jsonData):
		#TODO: Implementation
		pass