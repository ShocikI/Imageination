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
        and no assigned Combobox widget.
        """
        self.file_names = []
        self.switch_data = []
        self.file_list = None
        self.mean_tree = None
        self.mean_data = {}

    def select_files(self) -> None:
        """
        Opens a file dialog for the user to select image files (.png, .jpg, .jpeg).
        The selected files are added to the file_names list in the provided SystemData object.
        """
        file = filedialog.askopenfilenames()
        if file == "":
            return
        
        file_list = list(file)
        for f in file_list:
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                self.file_names.append(f)

        if len(self.file_names) > 0:
            for file in self.file_names:
                if file not in self.mean_data.keys():
                    image = Image.open(file)
                    self.mean_data[file] = (1, image.height, image.width, image.mode)
            self.update_files_data()


    def select_folder(self) -> None:
        """
        Opens a directory dialog for the user to select a folder containing image files (.png, .jpg, .jpeg).
        All image files in the folder are added to the file_names list in the provided SystemData object.
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
                    self.mean_data[file] = (1, image.height, image.width, image.mode)
            self.update_files_data()


    def remove_selected_in_select_file_combobox(self) -> None:
        name = self.file_list.get()
        if name != '':        
            self.remove_file(name)


    def remove_selected_in_mean_image_tree(self) -> None:
        selected_files = [
            self.mean_tree.item(item)['values'][0] 
            for item in self.mean_tree.selection()
        ]
        
        if len(selected_files):
            for file in selected_files:
                self.remove_file(file)


    def remove_file(self, file_name: str) -> None:
        """
        Removes the selected file from the file_names list in the provided SystemData object
        and updates the Tkinter widget displaying the list of files.
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
        Clears the list of selected files in the provided SystemData object and updates
        the Tkinter widget to reflect the empty list.
        """
        self.file_names = []
        self.mean_data = {}
        self.update_files_data()
        print("List has been cleared.")


    def update_files_data(self):
        self.file_list['values'] = self.file_names
        self.file_list.set("")

        # Clear tree
        for item in self.mean_tree.get_children():
            self.mean_tree.delete(item)
        
        # Draw tree
        if len(self.mean_data):
            for data in self.mean_data.keys():
                weight, width, height, mode = self.mean_data[data]
                self.mean_tree.insert("", 'end', values=(data, weight, height, width, mode))
    