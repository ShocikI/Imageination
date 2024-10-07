from tkinter.ttk import Button, Frame, Combobox, Notebook, Spinbox, Separator
from tkinter import IntVar

from source.data.SystemData import SystemData

class FrameMeanImage(Frame):

    def __init__ (self, parent: Notebook, data: SystemData) -> None:
        Frame.__init__(self, parent)
        self.create(data)
    
    def create(self, data: SystemData) -> None:
        self['padding'] = (10, 5)

        self.image_weight = IntVar(self, value=1)

        self.combo_images = Combobox(self, values=data.file_list, width=30, xscrollcommand=True, justify='right')
        self.spin_weight = Spinbox(self, from_=1, to= 100, justify='right', width=4)
        self.button_change_weight = Button(self, command=lambda _:print("button_change_width"), text="button_change_width")
        self.button_remove_image = Button(self, command=lambda _:print("button_remove_image"), text="button_remove_image")
        self.separator = Separator(self, orient='horizontal')
        self.button_generate = Button(self, command=lambda _:print("button_generate"), text="button_generate")

        # Grid
        self.columnconfigure(1, weight=1)
        self.columnconfigure(5, weight=1)
        self.combo_images.grid(column=2, row=1, columnspan=3, sticky='nwe')

        self.spin_weight.grid(column=2, row=2, sticky='w')
        self.button_change_weight.grid(column=3, row=2, columnspan=2, padx=(5, 0), pady=(5, 0), sticky='we')
        self.button_change_weight['padding']= (15, 5)

        self.button_remove_image.grid(column=3, row=3, columnspan=2, padx=(5, 0), pady=(5, 0), sticky='we')
        self.button_remove_image['padding']= (15, 5)

        self.separator.grid(column=1, row=4, columnspan=5, sticky='we', pady=(10,10))

        self.button_generate.grid(column=2, row=5, columnspan=3, sticky='nwe')
        self.button_generate['padding']= (15, 5)



