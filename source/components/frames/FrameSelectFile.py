from tkinter.ttk import Button, Frame, Labelframe, Combobox, Notebook

from source.data.SystemData import SystemData


class FrameSelectFile(Frame):
    """
    The FrameSelectFile class represents the UI component for selecting and removing image files.
    It allows the user to either select individual images or choose a folder containing images, 
    and also provides options to remove selected images or clear the selection.

    Inherits from:
        Frame: A Tkinter Frame widget that acts as a container for other widgets.

    Attributes:
        select_frame (Labelframe | None): Frame containing file selection buttons.
        remove_frame (Labelframe | None): Frame containing file removal options.
        get_img_button (Button | None): Button to select individual image files.
        folder_img_button (Button | None): Button to select a folder containing images.
        reset_button (Button | None): Button to clear all selected images.
        remove_button (Button | None): Button to remove a selected image from the list.
    """
    select_frame: Labelframe | None = None
    remove_frame: Labelframe | None = None
    get_img_button: Button | None = None
    folder_img_button: Button | None = None
    reset_button: Button | None = None
    remove_button: Button | None = None

    def __init__(self, parent: Notebook, data: SystemData) -> None:
        """
        Initializes the FrameSelectFile UI component.

        Args:
            parent (Notebook): The parent widget, typically a Notebook tab.
            data (SystemData): System-wide data structure holding file and color switch information.
        """
        Frame.__init__(self, parent)
        self.create(data)

    def create(self, data: SystemData) -> None:
        """
        Creates and configures the layout of the file selection and removal components.

        Args:
            data (SystemData): The data object that manages file selection and list of files.
        """
        self['padding'] = (10, 5)

        self.select_frame = Labelframe(self, text="Select files")
        self.get_img_button = Button(self.select_frame, text="Select images", command=lambda: data.select_files())
        self.folder_img_button = Button(self.select_frame, text="Select folder", command=lambda: data.select_folder())

        self.remove_frame = Labelframe(self, text="Remove one image")
        self.remove_button = Button(self.remove_frame, text="Remove selected", command=lambda: data.remove_file())
        data.file_list = Combobox(self.remove_frame, values=data.file_names, justify='right', xscrollcommand=True)
        self.reset_button = Button(self.remove_frame, text="Clear selection", command=lambda: data.clear_selection())

        # Grid
        self.select_frame.grid(column=2, row=1)
        self.select_frame['padding'] = (10, 5)
        self.remove_frame.grid(column=2, row=2, sticky=("N", "S", "W", "E"))
        self.remove_frame['padding'] = (10, 5)

        self.get_img_button.grid(column=2, row=2, columnspan=4, padx=(0, 5), pady=(0, 5), sticky=("W", "E"))
        self.get_img_button['padding'] = (10,5)
        self.folder_img_button.grid(column=7, row=2, columnspan=4, padx=(5, 0), pady=(0, 5), sticky=("W", "E"))
        self.folder_img_button['padding'] = (10,5)
        data.file_list.grid(column=1, row=2, columnspan=10, sticky=("W", "E"))
        self.remove_button.grid(column=2, row=4, columnspan=4, padx=(0, 5), pady=(5), sticky=("W", "E"))
        self.remove_button['padding'] = (10,5)
        self.reset_button.grid(column=7, row=4, columnspan=4, padx=(5, 0), pady=(5), sticky=("W", "E"))
        self.reset_button['padding'] = (10,5)

    