from tkinter.ttk import Button, Frame, Labelframe, Scrollbar
from tkinter import Listbox

from source.ops import FrameSwitchColorOperators as ops
from source.ops import sys_operators as sops


class SwitchData(Labelframe):
    rgb_color: tuple
    hex_color: str
    color_list: list[str]
    box_color: Listbox
    box_switches: Listbox
    b_add: Button
    b_remove: Button
    b_remove_frame: Button

    def __init__(self, parent, props, rgb, hex=None):
        self.rgb_color = rgb
        if hex:
            self.hex_color = hex
        else:
            self.hex_color = sops.RGB_to_hex(self.rgb_color)
    
        self.color_list = []
        Labelframe.__init__(self, parent, text=self.hex_color)
        self.create(props)

    def create(self, props):
        # Layout
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
            command=lambda: ops.remove_frame(self, props)
        )


    def grid_up(self, column, row):
        self.grid(column=column, row=row, columnspan=3)
        self.box_color.grid(column=1, row=1, columnspan=3, pady=5, sticky='nwe')
        self.box_switches.grid(column=1, row=2, columnspan=3, rowspan=2)

        self.b_add.grid(column=4, row=1, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove.grid(column=4, row=2, columnspan=3, padx=5, pady=5, sticky='nswe')
        self.b_remove_frame.grid(column=4, row=3, columnspan=3, padx=5, pady=5, ipady=5, sticky='we')
