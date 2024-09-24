from tkinter import colorchooser, messagebox, filedialog
from PIL import Image
import numpy as np
from itertools import product
import os



def select_target_color(item) -> None:
    """
    Opens a color chooser dialog to select a color and adds the selected color
    to the given item's color list and updates the color switches.

    Args:
        item (SwitchData): An object that contains the color list and box switches for the color selection.
    """
    color = colorchooser.askcolor(initialcolor='#ff0808')
    if color[0] not in item.color_list:    
        item.color_list.append(color[0])
        item.box_switches.insert(len(item.color_list)+1, color[1])

def remove_selected_color(data) -> None:
    """
    Removes the selected color from the box_switches list in the given data object.

    Args:
        data (SwitchData): An object containing the list of box switches where the selected color is stored.
    """
    index = data.box_switches.curselection()
    if index:
        data.box_switches.delete(index)

def remove_frame(frame, data) -> None:
    """
    Removes the specified frame from the GUI grid and removes the frame's data from switch_data.

    Args:
        frame (SwitchData): The frame to be removed from the grid.
        data (SystemData): An object that contains switch_data, which stores information about the frames.
    """
    frame.grid_remove()
    data.switch_data.remove(frame)

def generate_images(data) -> None:
    """
    Generates new image files by applying color transformations to the selected file 
    based on the user's color choices. After the images are generated, the program is reset.

    Args:
        data (SystemData): An object containing the image file names and the user's selected switch_data (color transformations).
    """
    # Clear empty colors
    for item in reversed(data.switch_data):
        if item.box_switches.size() < 1:
            data.switch_data.remove(item)
    
    if validate_data(data):
        return None
    
    # Get target folder
    target_folder = filedialog.askdirectory()
    if target_folder == "":
        return None
    os.chdir(target_folder)

    # Prepare file
    image = Image.open(data.file_names[0])
    matrix = np.array(image)
    look_up_table = make_look_up_table(matrix, data.switch_data)

    # Make all combinations of color switches
    if len(data.switch_data) > 1:
        colors = ()
        for item in data.switch_data:
            colors = colors + ([(color, item.hex_color) for color in item.color_list], )
        combos = product(*colors)
    else:
        item = data.switch_data[0]
        combos = ([(color, item.hex_color)] for color in item.color_list)
    
    # Generate every combo
    for index, combo in enumerate(combos):
        generate_file(matrix, look_up_table, combo, index)

    # Reset program
    for frame in props.switch_data:
        remove_frame(frame, props)

    data.file_names = []

    print("Finished!")

def validate_data(data) -> bool:
    """
    Validates the data by checking if an image is selected and if color switches are present.

    Args:
        data (SystemData): An object that contains file_names and switch_data (colors and transformations).
    
    Returns:
        bool: True if validation fails, otherwise False.
    """
    # Check if there is any file
    if len(data.file_names) != 1:
        messagebox.showinfo(message='Select 1 image in "File selection".')
        return True

    # Check if there is any color
    if len(data.switch_data) < 1:
        messagebox.showinfo(message='Select at least 1 color to switch.')
        return True

    return False

def make_look_up_table(matrix: np.array, data: list) -> dict:
    """
    Creates a lookup table that maps color hex values to the corresponding pixel coordinates
    in the image matrix where the colors are found.

    Args:
        matrix (np.array): A 2D array representing the pixel data of the image.
        data (list): A list of items that contain the colors to be looked up.

    Returns:
        dict: A dictionary mapping hex color values to the pixel coordinates in the matrix.
    """
    table = {}
    for item in data:
        table[item.hex_color] = []

    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            for item in data:
                if list(item.rgb_color) == list(matrix[row][column]):
                    table[item.hex_color].append((row, column))

    return table

def generate_file(matrix: np.array, table: dict, combination: list[tuple], index: int):
    """
    Generates a new image by applying the color transformations based on the given combination 
    and saves the new image file.

    Args:
        matrix (np.array): A 2D array representing the pixel data of the image.
        table (dict): A lookup table mapping color hex values to pixel coordinates.
        combination (list[tuple]): A list of color transformations (RGB and target color).
        index (int): The index used to name the generated image file.
    """
    for rgb, target in combination:
        for row, column in table[target]:
            matrix[row, column] = list(rgb)
    
    new_image = Image.fromarray(matrix)

    new_image.save(f"combination_{index}.jpg")
