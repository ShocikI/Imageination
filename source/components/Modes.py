from tkinter.ttk import Notebook, Frame, Label
from source.components.frames import FrameSelectFile as fsf
from source.components.frames import FrameSwitchColor as fsc

class Modes(Notebook):
    def __init__(self, root, props):
        Notebook.__init__(self, root)
        self.pack(expand=True, fill='both', padx=10, pady=10)
        
        f1 = fsf.FrameSelectFile(self, props)
        self.add(f1, text="Files selection")

        f2 = fsc.FrameSwitchColor(self, props)
        self.add(f2, text="Switch colors")

        