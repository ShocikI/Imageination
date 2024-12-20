from tkinter.ttk import Button, Frame, Combobox, Notebook, Spinbox, Separator, Treeview
from tkinter import IntVar

from source.ops import FrameMeanImageOperator as ops
from source.data.SystemData import SystemData

class FrameMeanImage(Frame):

    def __init__ (self, parent: Notebook, data: SystemData) -> None:
        Frame.__init__(self, parent)
        self.create(data)
    
    def create(self, data: SystemData) -> None:
        self['padding'] = (10, 5)

        self.image_weight = IntVar(self, value=1)

        data.mean_tree = Treeview(
            self, 
            columns=("file", "weight", "width", "height", 'mode'), 
            show='headings', 
            height=5
        )
        
        data.mean_tree.heading('file', text='File', anchor='w')
        data.mean_tree.heading('weight', text='Weight')
        data.mean_tree.heading('width', text='Width')
        data.mean_tree.heading('height', text='Height')
        data.mean_tree.heading('mode', text='Mode')

        data.mean_tree.column('weight', width=50, stretch=False, anchor='e')
        data.mean_tree.column('width', width=50, stretch=False, anchor='e')
        data.mean_tree.column('height', width=50, stretch=False, anchor='e')
        data.mean_tree.column('mode', width=75, stretch=False, anchor='e')
        
        self.spin_weight = Spinbox(self, from_=1, to=100, justify='right', width=4)
        self.button_change_weight = Button(
            self, 
            command=lambda: ops.change_weight_of_elements(self.spin_weight, data), 
            text="Change weight"
        )
        self.button_remove_image = Button(
            self, 
            command=data.remove_selected_in_mean_image_tree, 
            text="Remove selected"
        )
        self.separator = Separator(self, orient='horizontal')
        self.button_generate = Button(
            self, 
            command=lambda: ops.generate_mean_file(data), 
            text="Generate file"
        )

        # Grid
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(8, weight=1)
        self.columnconfigure(9, weight=1)
        data.mean_tree.grid(column=1, row=1, columnspan=9, sticky='nwe')

        self.spin_weight.grid(column=2, row=2, columnspan=2, sticky='w')
        self.button_change_weight.grid(column=4, row=2, columnspan=4, padx=(5, 0), pady=(5, 0), sticky='we')
        self.button_change_weight['padding']= (15, 5)

        self.button_remove_image.grid(column=4, row=3, columnspan=4, padx=(5, 0), pady=(5, 0), sticky='we')
        self.button_remove_image['padding']= (15, 5)

        self.separator.grid(column=1, row=4, columnspan=9, sticky='we', pady=(10,10))

        self.button_generate.grid(column=2, row=5, columnspan=7, sticky='nwe')
        self.button_generate['padding']= (15, 5)
