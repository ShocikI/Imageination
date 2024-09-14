from tkinter.ttk import Notebook, Frame, Label

class Modes(Notebook):
    def __init__(self, root):
        Notebook.__init__(self, root)
        self.grid(column=1, row=1)
        
        f1 = Frame(self)
        f1.grid(column=1, row=1)
        f2 = Frame(self)
        f2.grid(column=1, row=1)
        self.add(f1, text="Select files")
        self.add(f2, text="Change colors")
        label1 = Label(f1, text="frame 1")
        label1.grid(column=1, row=1)
        
        label2 = Label(f2, text="frame 2")
        label2.grid(column=1, row=1)