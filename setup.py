from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
 
setup(
    windows = ['application.py','application/gui/main.py','application/gui/add.py','application/gui/edit.py','application/gui/numberedit.py'],
    zipfile = None,
)