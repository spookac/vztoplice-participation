import os, sys
from application.gui import Gui

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative)
	return os.path.join(relative)
	
filename = "procedures.json"
data_dir = "db"

mydatafile = resource_path(os.path.join(data_dir, filename))

gui = Gui("640", "480")
gui.startApplication(mydatafile)