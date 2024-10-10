from tkinter.ttk import Spinbox
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from os import chdir
from skimage import io

from source.data.SystemData import SystemData

def change_weight_of_elements(spinbox: Spinbox, data: SystemData) -> None:
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
                _, height, width, mode = data.mean_data[file]
                data.mean_data[file] = (new_weight, height, width, mode)

    data.update_files_data()


def generate_mean_file(data: SystemData) -> None:
    # Check if in memory are more then 1 file
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
        weight, *_ = data.mean_data[key]
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
    # Check if in memory are more then 1 file
    if len(data.mean_data) < 2:
        messagebox.showinfo(message='Select at least 2 images in "File selection"')
        return None

    # Check if every images have this same resolution
    resolution = []
    for _, height, width, mode in data.mean_data.values():
        match mode:
            case '1':
                resolution.append((height, width, 1))
            case 'L':
                resolution.append((height, width, 1))
            case 'P':
                resolution.append((height, width, 1))
            case 'I':
                resolution.append((height, width, 1))
            case 'F':
                resolution.append((height, width, 1))
            case 'RGB':
                resolution.append((height, width, 3))
            case 'YCbCr':
                resolution.append((height, width, 3))
            case 'LAB':
                resolution.append((height, width, 3))
            case 'HSV':
                resolution.append((height, width, 3))
            case 'RGBA':
                resolution.append((height, width, 4))
            case 'CMYK':
                resolution.append((height, width, 4))
    
    if len(set(resolution)) != 1:
        messagebox.showinfo(message='Selected files have different resolutions.')
        return None

    return resolution[0]