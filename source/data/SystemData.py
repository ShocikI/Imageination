from tkinter.ttk import Combobox
from source.data.SwitchData import SwitchData

class SystemData():
    """
    The SystemData class holds all the essential data for the application's state, 
    including selected file names, color switch data, and the file selection combobox.

    Attributes:
        file_names (list[str]): A list of selected file paths.
        switch_data (list[SwitchData]): A list storing color switch configurations.
        file_list (Combobox | None): A Tkinter Combobox widget for displaying selected files.
    """
    file_names: list[str]
    switch_data: list[SwitchData]
    file_list: Combobox | None = None

    def __init__(self):
        """
        Initializes an empty SystemData object with no selected files, no color switch data,
        and no assigned Combobox widget.
        """
        self.file_names = []
        self.switch_data = []
        self.file_list = None