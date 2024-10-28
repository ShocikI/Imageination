from tkinter.ttk import Button, Frame, Labelframe, Combobox, Notebook

from source.data.SystemData import SystemData


class FrameSelectFile(Frame):
    """
    The FrameSelectFile class represents a UI component for selecting and managing image files.
    This widget allows users to select individual images or an entire folder of images, and it
    provides options to remove selected images or clear the current selection.

    Inherits from:
        Frame: A Tkinter Frame widget that acts as a container for organizing other widgets.

    Attributes:
        select_frame (Labelframe | None): Frame containing buttons to select image files.
        remove_frame (Labelframe | None): Frame containing controls for removing selected files.
        get_img_button (Button | None): Button for selecting individual image files.
        folder_img_button (Button | None): Button for selecting an entire folder of images.
        reset_button (Button | None): Button for clearing the current selection of images.
        remove_button (Button | None): Button for removing a selected image from the list.
    """
    select_frame: Labelframe | None = None
    remove_frame: Labelframe | None = None
    get_img_button: Button | None = None
    folder_img_button: Button | None = None
    reset_button: Button | None = None
    remove_button: Button | None = None

    def __init__(self, parent: Notebook, data: SystemData) -> None:
        """
        Initializes the FrameSelectFile component and sets up the required UI structure.

        Args:
            parent (Notebook): The Notebook widget that acts as the parent container.
            data (SystemData): The data manager instance containing file list and related methods.
        """
        Frame.__init__(self, parent)
        self.create(data)

    def create(self, data: SystemData) -> None:
        """
        Creates and configures the file selection and removal layout within the FrameSelectFile component.

        This method sets up a Labelframe for selecting files and another for managing selected files. 
        It includes buttons for selecting individual images or folders, removing an image, and clearing 
        the selection.

        Args:
            data (SystemData): The data manager that stores file selection and provides associated actions.
        """
        self['padding'] = (10, 5)

        self.select_frame = Labelframe(self, text="Select files")
        self.get_img_button = Button(self.select_frame, text="Select images", command=data.select_files)
        self.folder_img_button = Button(self.select_frame, text="Select folder", command=data.select_folder)

        self.remove_frame = Labelframe(self, text="Remove one image")
        self.remove_button = Button(self.remove_frame, text="Remove selected", command=data.remove_selected_in_select_file_combobox)
        data.file_list = Combobox(self.remove_frame, values=data.file_names, justify='right', xscrollcommand=True)
        self.reset_button = Button(self.remove_frame, text="Clear selection", command=data.clear_selection)

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

    