from tkinter import Menu


class MenuBar(Menu):
    """
    The MenuBar class creates a menu bar for the root window of the application,
    including "File", "Edit", and "Modes" menus. Each menu can contain various commands.

    Inherits from:
        Menu: A Tkinter widget that represents a menu bar.

    Attributes:
        root (Tk): The root window to which the menu bar is attached.
        menu_file (Menu | None): The "File" menu with associated commands.
        menu_edit (Menu | None): The "Edit" menu with associated commands.
        menu_modes (Menu | None): The "Modes" menu with associated commands.
    """
    menu_file: Menu | None = None
    menu_edit: Menu | None = None
    menu_modes: Menu | None = None

    def __init__(self, root):
        """
        Initializes the MenuBar by creating three main menus: "File", "Edit", and "Modes",
        and attaching them to the root window's menu bar.

        Args:
            root (Tk): The main window where the menu bar will be added.
        """
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

    