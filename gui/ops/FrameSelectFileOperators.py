from tkinter import filedialog
import os

def select_files(combo, props):
    file = filedialog.askopenfilenames()
    print(file)
    if file == "":
        return
    
    file_list = list(file)
    for f in file_list:
        if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
            props['file_names'].append(f)

    if len(props['file_names']) > 0:
        combo['values'] = props['file_names']
        combo.set("")


def select_folder(combo, props):
    folder_name = filedialog.askdirectory().replace("/", "\\")
    if folder_name == "":
        return

    os.chdir(folder_name)
    for f in list(os.listdir()):
        if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
            props['file_names'].append(os.path.join(folder_name, f))
    
    if len(props['file_names']) > 0:
        combo['values'] = props['file_names']
        combo.set("")


def remove_file(combo, props):
    name = combo.get()
    if name != '':
        index = props['file_names'].index(name)
        props['file_names'].pop(index)
        combo['values'] = props['file_names']
        combo.set("")

def clear_selection(combo, props):
    props['file_names'] = []
    combo['values'] = props['file_names']
    combo.set("")
    print("Images has been cleared.")