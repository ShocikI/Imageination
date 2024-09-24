from tkinter import filedialog
import os

from source.data.SystemData import SystemData


def select_files(data: SystemData) -> None:
    """
    Opens a file dialog for the user to select image files (.png, .jpg, .jpeg).
    The selected files are added to the file_names list in the provided SystemData object.

    Args:
        data (SystemData): An object that contains the list of file names (file_names)
                           and a Tkinter widget to display the selected files (file_list).
    """
    file = filedialog.askopenfilenames()
    if file == "":
        return
    
    file_list = list(file)
    for f in file_list:
        if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
            data.file_names.append(f)

    if len(data.file_names) > 0:
        data.file_list['values'] = data.file_names
        data.file_list.set("")

def select_folder(data: SystemData) -> None:
    """
    Opens a directory dialog for the user to select a folder containing image files (.png, .jpg, .jpeg).
    All image files in the folder are added to the file_names list in the provided SystemData object.

    Args:
        data (SystemData): An object that contains the list of file names (file_names)
                           and a Tkinter widget to display the selected files (file_list).
    """
    folder_name = filedialog.askdirectory().replace("/", "\\")
    if folder_name == "":
        return

    os.chdir(folder_name)
    for f in list(os.listdir()):
        if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
            data.file_names.append(os.path.join(folder_name, f))

    if len(data.file_names) > 0:
        data.file_list['values'] = data.file_names
        data.file_list.set("")

def remove_file(data: SystemData) -> None:
    """
    Removes the selected file from the file_names list in the provided SystemData object
    and updates the Tkinter widget displaying the list of files.

    Args:
        data (SystemData): An object that contains the list of file names (file_names)
                           and a Tkinter widget to display the selected files (file_list).
    """
    name = data.file_list.get()
    if name != '':
        index = data.file_names.index(name)
        data.file_names.pop(index)
        data.file_list['values'] = data.file_names
        data.file_list.set("")

def clear_selection(data: SystemData) -> None:
    """
    Clears the list of selected files in the provided SystemData object and updates
    the Tkinter widget to reflect the empty list.

    Args:
        data (SystemData): An object that contains the list of file names (file_names)
                           and a Tkinter widget to display the selected files (file_list).
    """
    data.file_names = []
    data.file_list['values'] = data.file_names
    data.file_list.set("")
    print("List has been cleared.")