from tkinter.ttk import Button, Frame, Label, Labelframe, Combobox, Spinbox
from tkinter import BooleanVar, Listbox, Checkbutton, IntVar

import source.ops.FrameSwitchColorOperators as ops
import source.ops.sys_operators as sops


class SwitchData(Labelframe):
    """
    The SwitchData class represents a labeled frame in the GUI for managing color switching operations.
    It allows users to select an original color and specify target colors to switch to, with options for 
    tolerance handling and various operations on the color data.

    Attributes:
        rgb_color (tuple): The RGB value of the original color (as a tuple of three integers).
        hex_color (str): The hexadecimal representation of the original color.
        color_list (list[str]): A list of target colors for switching, represented as hexadecimal strings.
        box_color (Listbox | None): A Listbox displaying the current color in hex format.
        box_switches (Listbox | None): A Listbox showing the list of selected target colors.
        check_tolerance (Checkbutton | None): A Checkbutton to enable or disable tolerance use for color switching.
        tolerance_type (set): A set of tolerance calculation methods, such as "Cubic" or "Sphere".
        tolerance_value (IntVar): An integer variable storing the tolerance value for color switching.
        use_tolerance (BooleanVar): An boolean variable storing user decision about tolerance usage.
        keep_difference (BooleanVar): An boolean variable storing user decision tp keep a difference between pixel
                                      values before and after color switching.
        b_add (Button | None): A button to open a color chooser for selecting target colors.
        b_remove (Button | None): A button to remove the selected color from the target color list.
        b_remove_frame (Button | None): A button to remove this frame from the parent widget.
        check_keep_diff (Checkbutton | None): A Checkbutton to enable or disable keeping a difference during color 
                                              switching.
    """
    rgb_color: tuple
    hex_color: str
    color_list: list[str]
    box_color: Listbox | None = None
    box_switches: Listbox | None = None
    check_tolerance: Checkbutton | None = None
    tolerance_type = {"Cubic", "Sphere"}
    tolerance_value: IntVar
    use_tolerance: BooleanVar
    keep_difference: BooleanVar
    b_add: Button | None = None
    b_remove: Button | None = None
    b_remove_frame: Button | None = None
    check_keep_diff: Checkbutton | None = None

    def __init__(self, parent: Frame, data, rgb: tuple, hex: str | None = None):
        """
        Initializes a new SwitchData frame with the specified RGB color and optional hexadecimal value.

        Args:
            parent (Frame): The parent widget in which this frame is placed.
            data (SystemData): Application data used for frame operations, such as managing other frames.
            rgb (tuple): The RGB color represented as a tuple of three integers.
            hex (str | None): Optional hexadecimal representation of the color. If not provided, it is
                              computed based on the RGB color.
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
        Creates and arranges the widgets inside the frame. This includes the original color display, 
        the target color list, buttons for adding/removing colors, and options for tolerance management.

        Args:
            data (SystemData): Application properties used for operations like removing this frame.
        """
        self.box_color = Listbox(self, height=1)
        self.box_color.insert(1, self.hex_color)
        self.box_color['state'] = "disable"

        self.box_switches = Listbox(self, height=5)

        self.use_tolerance = BooleanVar(self, value=False, name="Use tolerance")
        self.keep_difference = BooleanVar(self, value=False, name="Keep difference")
        self.tolerance_value = IntVar()
        self.check_tolerance = Checkbutton(self, text="Use tolerance", variable=self.use_tolerance, onvalue=True, offvalue=False, command=self.toggle_tolerance_option, width=20)
        self.label_box = Label(self, text="Tolerance type: ")
        self.box_tolerance = Combobox(self, values=["Cubic", "Spherical"], justify='left', width=9)
        self.label_spin = Label(self, text="Tolerance value: ")
        self.spin_tolerance = Spinbox(self, from_=0, to=128, textvariable=self.tolerance_value, width=4)
        self.check_keep_diff = Checkbutton(self, text="Keep difference", variable=self.keep_difference, onvalue=True, offvalue=False, width=20)

        self.b_add = Button(self, text="Select target color", command=lambda: ops.select_target_color(self) )
        self.b_add['padding'] = (10, 5)

        self.b_remove = Button(self, text="Remove selected color", command=lambda: ops.remove_selected_color(self) )
        self.b_remove['padding'] = (10, 5)

        self.b_remove_frame = Button(self, text="Remove this frame", command=lambda: ops.remove_frame(self, data) )


    def grid_up(self, column, row):
        """
        Places the SwitchData frame and its components in the specified grid layout of the parent widget.

        Args:
            column (int): The column position in the parent widget's grid layout.
            row (int): The row position in the parent widget's grid layout.
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
        """
        Toggles the visibility of the tolerance options (type and value) based on the state 
        of the 'Use tolerance' checkbox.
        """
        if self.use_tolerance.get():
            self.label_box.grid(column=1, row=5, padx=5, columnspan=2, sticky="w")
            self.box_tolerance.grid(column=3, row=5, padx=(0,10), pady=5, sticky="w")
            self.label_spin.grid(column=1, row=6, padx=5, columnspan=2, sticky="w")
            self.spin_tolerance.grid(column=3, row=6, sticky="w")
            self.check_keep_diff.grid(column=1, row=7, columnspan=3, sticky='w')
        else:
            self.label_box.grid_forget()
            self.box_tolerance.grid_forget()
            self.label_spin.grid_forget()
            self.spin_tolerance.grid_forget()
            self.check_keep_diff.grid_forget()