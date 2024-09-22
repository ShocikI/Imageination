from tkinter import Tk

from source.components import MenuBar as mb
from source.components import Modes
from source.components.frames import FrameSelectFile as fsf

from source.data import SwitchData as sd

class GUI:
    props = {
        "file_names": [],
        "switch_data": []
    }
    # Prepare interface
    def __init__(self):
        root = Tk()
        root.title("Imageination")
        root.option_add('*tearOff', False)
        root.wm_minsize(width=400, height=300)

        menubar = mb.MenuBar(root)
        modes = Modes.Modes(root, self.props)

        root.mainloop()


