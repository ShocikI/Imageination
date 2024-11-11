from tkinter import colorchooser, messagebox, filedialog
from PIL import Image
import numpy as np
from itertools import product
import os
from math import sqrt

from source.data import SwitchData, SystemData


MIN_COLOR_VALUE = 0
MAX_COLOR_VALUE = 255

def select_target_color(item: SwitchData) -> None:
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

def remove_selected_color(data: SwitchData) -> None:
    """
    Removes the selected color from the box_switches list in the provided SwitchData object.

    Args:
        data (SwitchData): A SwitchData object containing the list of selected colors 
                           and box switches for color management.
    """
    index = data.box_switches.curselection()
    if index:
        data.box_switches.delete(index)

def generate_images(data: SystemData) -> None:
    """
    Generates and saves new image files by applying color transformations based on user color 
    preferences for selected images. Creates multiple image versions based on combinations 
    of user-defined color switches.

    Args:
        data (SystemData): A SystemData object containing:
            - file_names (list[str]): A list of image file paths to process.
            - switch_data (list[SwitchData]): List of SwitchData objects containing 
              user-defined color transformations.

    Workflow:
        1. Removes any empty SwitchData entries with no colors selected.
        2. Validates if `switch_data` has required color transformation info.
        3. Asks the user to select a directory to save generated images.
        4. Applies color transformations to each selected image:
            - Uses a lookup table to map original colors to user-selected colors.
            - Generates all possible combinations of transformations if multiple colors are selected.
        5. Saves each new image in the target directory.
        6. Resets color selections and clears file data after generation.

    Returns:
        None: This function performs operations but returns no value.
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
    for frame in data.switch_data:
        data.remove_frame(frame)

    data.file_names = []
    data.mean_data = {}

    print("Finished!")

def validate_data(data: SystemData) -> bool:
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

def make_look_up_table(matrix: np.array, data: list[SwitchData]) -> dict:
    """
    Creates a lookup table mapping hex color values to pixel coordinates in the image matrix.
    Supports exact color matching and tolerance-based matching (cubic or spherical) for approximate color matches.

    Args:
        matrix (np.array): 3D array representing image pixel data (rows, columns, RGB values).
        data (list[SwitchData]): List of SwitchData objects containing color and tolerance settings.

    Returns:
        dict: A dictionary where keys are hex color values and values are lists of pixel coordinates (row, column).
    """
    # Create look up table
    table = {}
    for item in data:
        table[item.hex_color] = []
    # Check tolerance usage
    for item in data:
        keep_diff = item.keep_difference
        if item.use_tolerance:
            tolerance_type = item.box_tolerance.get()
            tol_value = item.tolerance_value.get()

            if tolerance_type == 'Cubic' and tol_value > 0:
                for row in range(len(matrix)):
                    for column in range(len(matrix[row])):
                        r = int(matrix[row][column][0]) - item.rgb_color[0] 
                        g = int(matrix[row][column][1]) - item.rgb_color[1] 
                        b = int(matrix[row][column][2]) - item.rgb_color[2] 
                        if abs(r) < tol_value and abs(g) < tol_value and abs(b) < tol_value:
                            table[item.hex_color].append((row, column, keep_diff, r, g, b))

            elif tolerance_type == "Spherical" and tol_value > 0:
                for row in range(len(matrix)):
                    for column in range(len(matrix[row])):
                        r = int(matrix[row][column][0]) - item.rgb_color[0]
                        g = int(matrix[row][column][1]) - item.rgb_color[1]
                        b = int(matrix[row][column][2]) - item.rgb_color[2]
                        if sqrt(r*r + g*g + b*b) < tol_value:
                            table[item.hex_color].append((row, column, keep_diff, r, g, b))

            else:
                for row in range(len(matrix)):
                    for column in range(len(matrix[row])):
                        if list(item.rgb_color) == list(matrix[row][column]):
                            table[item.hex_color].append((row, column, keep_diff, 0, 0, 0))

        else:
            for row in range(len(matrix)):
                for column in range(len(matrix[row])):
                    if list(item.rgb_color) == list(matrix[row][column]):
                        table[item.hex_color].append((row, column, keep_diff, 0, 0, 0))
    
    return table

def generate_file(matrix: np.array, table: dict, combination: list[tuple], index: int):
    """
    Applies color transformations from a combination list to a given image matrix 
    and saves the modified image as a new file.

    Args:
        matrix (np.array): Array representing the image's pixel data.
        table (dict): A lookup table mapping color hex values to pixel coordinates.
        combination (list[tuple]): List of color transformations (RGB values and target colors).
        index (int): Index used to uniquely name each generated image file.
    """
    for rgb, target in combination:
        for row, column, keep_diff, r, g, b in table[target]:
            if keep_diff:
                new_r = list(rgb)[0] + r
                if new_r < MIN_COLOR_VALUE: new_r = MIN_COLOR_VALUE
                elif new_r > MAX_COLOR_VALUE: new_r = MAX_COLOR_VALUE

                new_g = list(rgb)[1] + g
                if new_g < MIN_COLOR_VALUE: new_g = MIN_COLOR_VALUE
                elif new_g > MAX_COLOR_VALUE: new_g = MAX_COLOR_VALUE

                new_b = list(rgb)[2] + b
                if new_b < MIN_COLOR_VALUE: new_b = MIN_COLOR_VALUE
                elif new_b > MAX_COLOR_VALUE: new_b = MAX_COLOR_VALUE

            else:
                new_r, new_g, new_b = list(rgb)
            matrix[row][column] = [new_r, new_g, new_b]

    new_image = Image.fromarray(matrix)

    new_image.save(f"combination_{index}.jpg")
