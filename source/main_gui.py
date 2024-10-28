from tkinter import Tk

from source.components import MenuBar as mb
from source.components import Modes

from source.data.SystemData import SystemData

class GUI:
    """
    The GUI class represents the main interface of the application, 'Imageination'.
    It initializes and sets up the main window, menu bar, and modes of the application.

    Attributes:
        data (SystemData): An instance of the SystemData class, which stores application data 
                           like file names and switch data.
    """
    data: SystemData

    def __init__(self):
        """
        Initialize the graphical user interface of the application.
        """
        root = Tk()
        self.data = SystemData()
        root.title("Imageination")
        root.option_add('*tearOff', False)
        root.wm_minsize(width=400, height=300)

        menubar = mb.MenuBar(root)
        modes = Modes.Modes(root, self.data)

        root.mainloop()


