from tkinter.ttk import Notebook

from source.components.frames.FrameSelectFile import FrameSelectFile
from source.components.frames.FrameSwitchColor import FrameSwitchColor
from source.components.frames.FrameMeanImage import FrameMeanImage
from source.data.SystemData import SystemData


class Modes(Notebook):
    """
    The Modes class is a Notebook widget that organizes different functional modes 
    of the application into tabs. It allows users to switch between file selection 
    and color switch modes.

    Inherits from:
        Notebook: A Tkinter widget that provides a tabbed interface.
    """

    def __init__(self, root, data: SystemData):
        """
        Initializes the Modes notebook and adds two tabs: one for file selection 
        and one for switching colors.

        Args:
            root (Tk): The main window where the Notebook will be placed.
            data (SystemData): An instance of SystemData that stores application state 
                               such as selected files and color switch configurations.
        """
        Notebook.__init__(self, root)
        self.pack(expand=True, fill='both', padx=10, pady=10)
        
        f1 = FrameSelectFile(self, data)
        self.add(f1, text="Files selection")

        f2 = FrameSwitchColor(self, data)
        self.add(f2, text="Switch colors")

        f3 = FrameMeanImage(self, data)
        self.add(f3, text="Mean image")
