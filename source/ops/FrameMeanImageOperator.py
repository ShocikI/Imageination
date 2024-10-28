from tkinter.ttk import Spinbox
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from os import chdir

from source.data.SystemData import SystemData

def change_weight_of_elements(spinbox: Spinbox, data: SystemData) -> None:
    """
    Updates the weight of selected image files based on the user input from the Spinbox.

    Args:
        spinbox (Spinbox): The widget from which to retrieve the new weight value.
        data (SystemData): The data structure containing the mean data for image manipulation.
    """
    try:
        new_weight = int(spinbox.get())
    except:
        return None

    selected_files = [
        data.mean_tree.item(item)['values'][0] 
        for item in data.mean_tree.selection()
    ]
    
    if len(selected_files):
        for file in selected_files:
            if file in data.mean_data.keys():
                item = data.mean_data[file]
                data.mean_data[file] = {
                        "weight": new_weight, 
                        "height": item['height'],
                        "width": item['width'],
                        "mode": item['mode']
                    }

    data.update_files_data()


def generate_mean_file(data: SystemData) -> None:
    """
    Generates a mean image file based on selected images and their respective weights. Saves the result as a new image.

    Args:
        data (SystemData): The data structure containing mean data and file paths for image averaging.
    """
    shape = validate_data_for_generate(data)
    if not shape:
        return None

    # Get target folder
    target_folder = filedialog.askdirectory()
    if target_folder == "":
        return None
    chdir(target_folder)

    # Make result matrix
    matrix = np.zeros(shape, dtype=int)
    weight_sum = 0
    for key in data.mean_data.keys():
        # Prepare values
        weight = data.mean_data[key]['weight']

        weight_sum += weight
        # Add image to prepared matrix
        image_matrix = np.array(Image.open(key), dtype=int)
        for _ in range(weight):
            matrix += image_matrix

    # Get mean value from the matrix
    matrix = matrix / weight_sum

    # Prepare to save as image
    matrix = np.array(matrix, dtype='uint8')
    new_image = Image.fromarray(matrix)

    new_image.save(f"mean_image_result.jpg")

    data.clear_selection()


def validate_data_for_generate(data: SystemData) -> tuple | None:
    """
    Validates the data to ensure that at least two images are selected and that they share the same resolution.

    Args:
        data (SystemData): The data structure containing mean data and image details for validation.

    Returns:
        tuple | None: The resolution of the images as (height, width, channels) if validation succeeds, else None.
    """
    # Check if in memory are more then 1 file
    if len(data.mean_data) < 2:
        messagebox.showinfo(message='Select at least 2 images in "File selection"')
        return None

    # Check if every images have this same resolution
    resolution = []
    if item['mode'] in ['L']:
        channels = 1
    elif item['mode'] in ['RGB']:
        channels = 3
    elif item['mode'] in ['RGBA']:
        channels = 4

    for item in data.mean_data.values():
        resolution.append((item['height'], item['width'], channels))

    if len(set(resolution)) != 1:
        messagebox.showinfo(message='Selected files have different resolutions.')
        return None

    return resolution[0]