from tkinter import Tk

from gui.components import MenuBar as mb
from gui.components import Modes
from gui.components.frames import FrameSelectFile as fsf

class GUI:
    props = {
        "file_names": [],
    }
    # Prepare interface
    def __init__(self):
        root = Tk()
        root.title("Imageination")
        root.option_add('*tearOff', False)
        root.wm_minsize(width=400, height=300)
        root.wm_maxsize(width=600, height=400)

        menubar = mb.MenuBar(root)
        modes = Modes.Modes(root, self.props)

        root.mainloop()


