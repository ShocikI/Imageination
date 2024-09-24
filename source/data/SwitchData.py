from tkinter.ttk import Button, Frame, Labelframe
from tkinter import Listbox

import source.ops.FrameSwitchColorOperators as ops
import source.ops.sys_operators as sops


class SwitchData(Labelframe):
    """
    The SwitchData class represents a labeled frame in the GUI, which stores information 
    about a specific color and allows users to select target colors for switching.
    
    Attributes:
        rgb_color (tuple): The RGB value of the original color.
        hex_color (str): The hexadecimal representation of the original color.
        color_list (list[str]): A list of target colors to switch to.
        box_color (Listbox | None): A Listbox displaying the current color in hex format.
        box_switches (Listbox | None): A Listbox displaying the selected target colors.
        b_add (Button | None): A button to open a color chooser for selecting target colors.
        b_remove (Button | None): A button to remove the selected color from the list.
        b_remove_frame (Button | None): A button to remove the entire color switch frame.
    """
    rgb_color: tuple
    hex_color: str
    color_list: list[str]
    box_color: Listbox | None = None
    box_switches: Listbox | None = None
    b_add: Button | None = None
    b_remove: Button | None = None
    b_remove_frame: Button | None = None

    def __init__(self, parent: Frame, data, rgb: tuple, hex: str | None = None):
        """
        Initializes a new SwitchData frame with a given RGB color and optional hex value.

        Args:
            parent (Frame): The parent widget in which this frame is placed.
            data (SystemData): Application properties passed for additional operations (e.g., removing frames).
            rgb (tuple): The RGB color to switch from.
            hex (str | None): Optional hexadecimal representation of the color. If not provided,
                              the hex value is computed from the RGB color.
        """
        self.rgb_color = rgb
        if hex:
            self.hex_color = hex
        else:
            self.hex_color = sops.RGB_to_hex(self.rgb_color)
    
        self.color_list = []
        Labelframe.__init__(self, parent, text=self.hex_color)
        self.create(data)

    def create(self, data):
        """
        Creates and arranges the widgets inside the frame, including the color display listbox, 
        target color listbox, and buttons for adding/removing colors and removing the frame.

        Args:
            data (SystemData): Application properties used for certain operations, such as removing the frame.
        """
        self.box_color = Listbox(self, height=1)
        self.box_color.insert(1, self.hex_color)
        self.box_color['state'] = "disable"

        self.box_switches = Listbox(self, height=5)

        self.b_add = Button(
            self, text="Select target color",
            command=lambda: ops.select_target_color(self)
        )
        self.b_add['padding'] = (10, 5)

        self.b_remove = Button(
            self, text="Remove selected color",
            command=lambda: ops.remove_selected_color(self)
        )
        self.b_remove['padding'] = (10, 5)

        self.b_remove_frame = Button(
            self, text="Remove this frame",
            command=lambda: ops.remove_frame(self, data)
        )


    def grid_up(self, column, row):
        """
        Places the frame and its components in the specified grid layout of the parent widget.

        Args:
            column (int): The column position in the grid layout.
            row (int): The row position in the grid layout.
        """
        self.grid(column=column, row=row, columnspan=3)
        self.box_color.grid(column=1, row=1, columnspan=3, pady=5, sticky='nwe')
        self.box_switches.grid(column=1, row=2, columnspan=3, rowspan=2)

        self.b_add.grid(column=4, row=1, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove.grid(column=4, row=2, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove_frame.grid(column=4, row=3, columnspan=3, padx=5, pady=5, ipady=5, sticky='we')
