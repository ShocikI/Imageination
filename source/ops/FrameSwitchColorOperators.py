from tkinter import colorchooser, messagebox, filedialog
from PIL import Image
import numpy as np
from itertools import product
import os

def select_target_color(item) -> None:
    color = colorchooser.askcolor(initialcolor='#ff0808')
    item.color_list.append(color[0])
    item.box_switches.insert(len(item.color_list)+1, color[1])

def remove_selected_color(data) -> None:
    index = data.box_switches.curselection()
    data.box_switches.delete(index)

def remove_frame(frame, props) -> None:
    frame.grid_remove()
    props['switch_data'].remove(frame)

def generate_images(props) -> None:
    # Clear empty colors
    for item in reversed(props['switch_data']):
        if item.box_switches.size() < 1:
            props['switch_data'].remove(item)
    
    if validate_data(props):
        return None
    
    # Get target folder
    target_folder = filedialog.askdirectory()
    if target_folder == "":
        return None
    os.chdir(target_folder)

    # Prepare file
    image = Image.open(props['file_names'][0])
    matrix = np.array(image)
    look_up_table = make_look_up_table(matrix, props['switch_data'])

    # Make all combinations of color switches
    if len(props['switch_data']) > 1:
        colors = ()
        for item in props['switch_data']:
            colors = colors + ([(color, item.hex_color) for color in item.color_list], )
        combos = product(*colors)
    else:
        item = props['switch_data'][0]
        combos = ([(color, item.hex_color) for color in item.color_list], )
    
    # Generate every combo
    for index, combo in enumerate(combos):
        generate_file(matrix, look_up_table, combo, index)

    # Reset program
    for frame in props['switch_data']:
        remove_frame(frame, props)

    props['file_names'] = []

    print("Finished!")


def validate_data(props) -> bool:
    # Check if there is any file
    if len(props['file_names']) != 1:
        messagebox.showinfo(message='Select 1 image in "File selection".')
        return True

    # Check if there is any color
    if len(props['switch_data']) < 1:
        messagebox.showinfo(message='Select at least 1 color to switch.')
        return True

    return False

def make_look_up_table(matrix, data) -> dict:
    table = {}
    for item in data:
        table[item.hex_color] = []

    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            for item in data:
                if list(item.rgb_color) == list(matrix[row][column]):
                    table[item.hex_color].append((row, column))

    return table

def generate_file(matrix, table, combination, index):
    for rgb, target in combination:
        for row, column in table[target]:
            matrix[row, column] = list(rgb)
    
    new_image = Image.fromarray(matrix)

    new_image.save(f"combination_{index}.jpg")
