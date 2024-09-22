from tkinter import filedialog
from tkinter.ttk import Button, Label, Frame, Labelframe, Combobox, Separator
import os

class FrameSelectFile(Frame):
    select_frame = None
    remove_frame = None
    get_img_button = None
    folder_img_button = None
    reset_button = None
    file_list = None
    remove_button = None

    def __init__(self, parent, props):
        Frame.__init__(self, parent)
        self.create(props)

    def create(self, props):
        self['padding'] = (10, 5)

        self.select_frame = Labelframe(self, text="Select files")
        self.get_img_button = Button(
            self.select_frame, text="Select images", 
            command=lambda: self.select_files(props)
        )
        self.folder_img_button = Button(
            self.select_frame, text="Select folder", 
            command=lambda: self.select_folder(props)
        )

        self.remove_frame = Labelframe(self, text="Remove one image")
        self.remove_button = Button(
            self.remove_frame, text="Remove selected", 
            command=lambda: self.remove_file(props)
        )
        self.file_list = Combobox(self.remove_frame, values=props['file_names'], justify='right', xscrollcommand=True)
        self.reset_button = Button(
            self.remove_frame, text="Clear selection", 
            command=lambda: self.clear_selection(props)
        )

        # Grid
        self.select_frame.grid(column=2, row=1)
        self.select_frame['padding'] = (10, 5)
        self.remove_frame.grid(column=2, row=2, sticky=("N", "S", "W", "E"))
        self.remove_frame['padding'] = (10, 5)

        self.get_img_button.grid(column=2, row=2, columnspan=4, padx=(0, 5), pady=(0, 5), sticky=("W", "E"))
        self.get_img_button['padding'] = (10,5)
        self.folder_img_button.grid(column=7, row=2, columnspan=4, padx=(5, 0), pady=(0, 5), sticky=("W", "E"))
        self.folder_img_button['padding'] = (10,5)
        self.file_list.grid(column=1, row=2, columnspan=10, sticky=("W", "E"))
        self.remove_button.grid(column=2, row=4, columnspan=4, padx=(0, 5), pady=(5), sticky=("W", "E"))
        self.remove_button['padding'] = (10,5)
        self.reset_button.grid(column=7, row=4, columnspan=4, padx=(5, 0), pady=(5), sticky=("W", "E"))
        self.reset_button['padding'] = (10,5)

    def select_files(self, props) -> None:
        file = filedialog.askopenfilenames()
        if file == "":
            return
        
        file_list = list(file)
        for f in file_list:
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                props['file_names'].append(f)

        if len(props['file_names']) > 0:
            self.file_list['values'] = props['file_names']
            self.file_list.set("")

    def select_folder(self, props) -> None:
        folder_name = filedialog.askdirectory().replace("/", "\\")
        if folder_name == "":
            return

        os.chdir(folder_name)
        for f in list(os.listdir()):
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"):
                props['file_names'].append(os.path.join(folder_name, f))
    
        if len(props['file_names']) > 0:
            self.file_list['values'] = props['file_names']
            self.file_list.set("")

    def remove_file(self, props) -> None:
        name = self.file_list.get()
        if name != '':
            index = props['file_names'].index(name)
            props['file_names'].pop(index)
            self.file_list['values'] = props['file_names']
            self.file_list.set("")

    def clear_selection(self, props) -> None:
        props['file_names'] = []
        self.file_list['values'] = props['file_names']
        self.file_list.set("")
        print("List has been cleared.")