from tkinter import filedialog
from tkinter.ttk import Button, Label, Frame, Labelframe, Combobox, Separator
from gui.ops import FrameSelectFileOperators as ops

class FrameSelectFile(Frame):
    select_frame = None
    remove_frame = None
    get_img_button = None
    folder_img_button = None
    reset_button = None
    file_list = None
    remove_button = None

    def __init__(self, root, props):
        Frame.__init__(self, root)
        self.create(root, props)

    def create(self, root, props):
        self['padding'] = (10, 5)

        self.select_frame = Labelframe(self, text="Select files")
        self.get_img_button = Button(
            self.select_frame, text="Select images", 
            command=lambda: ops.select_files(self.file_list, props)
        )
        self.folder_img_button = Button(
            self.select_frame, text="Select folder", 
            command=lambda: ops.select_folder(self.file_list, props)
        )

        self.remove_frame = Labelframe(self, text="Remove one image")
        self.remove_button = Button(
            self.remove_frame, text="Remove button", 
            command=lambda: ops.remove_file(self.file_list, props)
        )
        self.file_list = Combobox(self.remove_frame, values=props['file_names'], justify='right', xscrollcommand=True)
        self.reset_button = Button(
            self.remove_frame, text="Clear selection", 
            command=lambda: ops.clear_selection(self.file_list, props)
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
