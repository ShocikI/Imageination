from tkinter import Menu


class MenuBar(Menu):
    def __init__(self, root):
        Menu.__init__(self, root)
        root['menu'] = self
        self.menu_file = Menu(self)
        self.menu_edit = Menu(self)
        self.menu_modes = Menu(self)

        self.add_cascade(menu=self.menu_file, label="File")
        self.add_cascade(menu=self.menu_edit, label="Edit")
        self.add_cascade(menu=self.menu_modes, label="Modes")
        
        self.menu_file.add_command(label="file", command=lambda:print("file"))
        self.menu_edit.add_command(label="edit", command=lambda:print("edit"))
        self.menu_modes.add_command(label="edit", command=lambda:print("modes"))

    