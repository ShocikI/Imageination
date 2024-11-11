from tkinter.ttk import Combobox, Treeview
from tkinter import filedialog
from PIL import Image
import os

from source.data.SwitchData import SwitchData


class SystemData():
    """
    The SystemData class holds all the essential data for the application's state, 
    including selected file names, color switch data, and the file selection combobox.

    Attributes:
        file_names (list[str]): A list of selected file paths.
        switch_data (list[SwitchData]): A list storing color switch configurations.
        file_list (Combobox | None): A Tkinter Combobox widget for displaying selected files.
        mean_tree: (Treeview | None): A Tkinter Treeview widget for displaying selected files and their weight in mean image operation.
        mean_data: (dict): A dictionary of selected file path with file weight.
    """
    file_names: list[str]
    switch_data: list[SwitchData]
    file_list: Combobox | None
    mean_tree: Treeview | None
    mean_data: dict

    def __init__(self):
        """
        Initializes an empty SystemData object with no selected files, no color switch data,
        and no assigned Combobox or Treeview widget.
        """
        self.file_names = []
        self.switch_data = []
        self.file_list = None
        self.mean_tree = None
        self.mean_data = {}

    # FrameSelectFile methods
    def select_files(self) -> None:
        """
        Opens a file dialog for the user to select image files (.png, .jpg, .jpeg).
        Adds the selected files to the file_names list and updates mean_data with file metadata.
        """
        file = filedialog.askopenfilenames()
        if file == "":
            return
        
        file_list = list(file)
        for f in file_list:
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                self.file_names.append(f)
        print(self.file_list)

        if len(self.file_names) > 0:
            for file in self.file_names:
                if file not in self.mean_data.keys():
                    image = Image.open(file)
                    self.mean_data[file] = {
                        "weight": 1, 
                        "height": image.height,
                        "width": image.width,
                        "mode": image.mode
                    }
            self.update_files_data()

    def select_folder(self) -> None:
        """
        Opens a directory dialog for the user to select a folder containing image files (.png, .jpg, .jpeg).
        Adds all image files in the folder to the file_names list and updates mean_data with file metadata.
        """
        folder_name = filedialog.askdirectory().replace("/", "\\")
        if folder_name == "":
            return

        os.chdir(folder_name)
        for f in list(os.listdir()):
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                self.file_names.append(os.path.join(folder_name, f))

        if len(self.file_names) > 0:  
            for file in self.file_names:
                if file not in self.mean_data.keys():
                    image = Image.open(file)
                    self.mean_data[file] = {
                        "weight": 1, 
                        "height": image.height,
                        "width": image.width,
                        "mode": image.mode
                    }
            self.update_files_data()

    def remove_selected_in_select_file_combobox(self) -> None:
        """
        Removes the currently selected file in the file_list Combobox from the file_names list.
        """
        name = self.file_list.get()
        if name != '':        
            self.remove_file(name)

    def remove_selected_in_mean_image_tree(self) -> None:
        """
        Removes the files currently selected in the mean_tree Treeview from the file_names list.
        """
        selected_files = [
            self.mean_tree.item(item)['values'][0] 
            for item in self.mean_tree.selection()
        ]
        
        if len(selected_files):
            for file in selected_files:
                self.remove_file(file)

    def remove_file(self, file_name: str) -> None:
        """
        Removes the specified file from the file_names list and updates the mean_data dictionary 
        to remove associated metadata. Refreshes the Tkinter widgets displaying file data.

        Args:
            file_name (str): The file path to be removed from the file_names list.
        """
        index = self.file_names.index(file_name)
        self.file_names.pop(index)
        
        for key in reversed(self.mean_data.keys()):
            if key not in self.file_names:
                self.mean_data.pop(key)
                break

        self.update_files_data()     

    def clear_selection(self) -> None:
        """
        Clears the list of selected files and the mean_data dictionary, 
        and updates the Tkinter widgets to reflect the empty list.
        """
        self.file_names = []
        self.mean_data = {}
        self.update_files_data()
        print("List has been cleared.")

    def update_files_data(self):
        """
        Updates the file_list Combobox and mean_tree Treeview with current data 
        from file_names and mean_data, respectively. Clears and redraws the treeview items.
        """
        self.file_list['values'] = self.file_names
        self.file_list.set("")

        # Clear tree
        for item in self.mean_tree.get_children():
            self.mean_tree.delete(item)
        
        # Draw tree
        if len(self.mean_data):
            for data in self.mean_data.keys():
                item = self.mean_data[data]
                self.mean_tree.insert("", 'end', values=(data, item['weight'], item['height'], item['width'], item['mode']))
        
    def remove_switch_data(self, frame: SwitchData):
        """
        Removes the specified SwitchData frame from the switch_data list and from the GUI display.

        Args:
            frame (SwitchData): The SwitchData frame to be removed.
        """
        frame.grid_remove()
        self.switch_data.remove(frame)