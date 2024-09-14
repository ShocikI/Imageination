from tkinter import *
from tkinter import ttk

from gui.components import MenuBar as mb
from gui.components import Modes


class GUI:
    
    # Prepare interface
    def __init__(self):
        root = Tk()
        root.title("Imageination")
        root.option_add('*tearOff', FALSE)

        menubar = mb.MenuBar(root)
        modes = Modes.Modes(root)

        root.mainloop()

