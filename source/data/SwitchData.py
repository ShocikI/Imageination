from tkinter.ttk import Button, Frame, Label, Labelframe, Combobox, Spinbox
from tkinter import BooleanVar, Listbox, Checkbutton, IntVar

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
        check_tolerance (Checkbox | None): A Checkbox to choose a usage of tolerance.
        tolerance_type (dict): A 
        tolerance (int): A 
        b_add (Button | None): A button to open a color chooser for selecting target colors.
        b_remove (Button | None): A button to remove the selected color from the list.
        b_remove_frame (Button | None): A button to remove the entire color switch frame.
    """
    rgb_color: tuple
    hex_color: str
    color_list: list[str]
    box_color: Listbox | None = None
    box_switches: Listbox | None = None
    tolerance_type = {"Cubic", "Sphere"}
    tolerance_value: int
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
        self.tolerance = 0
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

        self.use_tolerance = BooleanVar(self, value=False, name="Use tolerance")
        self.tolerance_value = IntVar()
        self.check_tolerance = Checkbutton(self, text="Use tolerance", variable=self.use_tolerance, onvalue=True, offvalue=False, command=self.toggle_tolerance_option, width=20)
        self.label_box = Label(self, text="Tolerance type: ")
        self.box_tolerance = Combobox(self, values=["Cubic", "Spherical"], justify='left', width=9)
        self.label_spin = Label(self, text="Tolerance value: ")
        self.spin_tolerance = Spinbox(self, from_=0, to=128, textvariable=self.tolerance_value, width=4)

        self.b_add = Button(self, text="Select target color", command=lambda: ops.select_target_color(self) )
        self.b_add['padding'] = (10, 5)

        self.b_remove = Button(self, text="Remove selected color", command=lambda: ops.remove_selected_color(self) )
        self.b_remove['padding'] = (10, 5)

        self.b_remove_frame = Button(self, text="Remove this frame", command=lambda: ops.remove_frame(self, data) )


    def grid_up(self, column, row):
        """
        Places the frame and its components in the specified grid layout of the parent widget.

        Args:
            column (int): The column position in the grid layout.
            row (int): The row position in the grid layout.
        """
        self.columnconfigure([1,3], weight=1)
        self.grid(column=column, row=row, columnspan=3)
        self.box_color.grid(column=1, row=1, columnspan=3, pady=5, sticky="we", padx=10)
        self.box_switches.grid(column=1, row=2, columnspan=3, rowspan=2, sticky="we", padx=10)

        self.check_tolerance.grid(column=1, row=4, columnspan=3, sticky='w')

        self.b_add.grid(column=5, row=1, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove.grid(column=5, row=2, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove_frame.grid(column=5, row=3, columnspan=3, padx=5, pady=5, ipady=5, sticky='we')

    def toggle_tolerance_option(self):
        if self.use_tolerance.get():
            self.label_box.grid(column=1, row=5, padx=5, columnspan=2, sticky="w")
            self.box_tolerance.grid(column=3, row=5, padx=(0,10), pady=5, sticky="w")
            self.label_spin.grid(column=1, row=6, padx=5, columnspan=2, sticky="w")
            self.spin_tolerance.grid(column=3, row=6, sticky="w")
        else:
            self.label_box.grid_forget()
            self.box_tolerance.grid_forget()
            self.label_spin.grid_forget()
            self.spin_tolerance.grid_forget()