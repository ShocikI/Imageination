from tkinter.ttk import Notebook, Frame, Label
from gui.components.frames import FrameSelectFile as fsf

class Modes(Notebook):
    def __init__(self, root, props):
        Notebook.__init__(self, root)
        self.grid(column=1, row=1)
        
        f1 = fsf.FrameSelectFile(self, props)
        self.add(f1, text="Files selection")

        f2 = Frame(self)
        f2.grid(column=1, row=1)
        self.add(f2, text="Change colors")
        
        label2 = Label(f2, text="frame 2")
        label2.grid(column=1, row=1)