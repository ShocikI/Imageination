from tkinter import colorchooser

def select_target_color(item):
    color = colorchooser.askcolor(initialcolor='#ff0808')
    item.color_list.append(color)
    item.box_switches.insert(len(item.color_list)+1, color[1])

def remove_selected_color(data):
    indices = data.box_switches.curselection()
    for index in indices:
        data.box_switches.delete(index)

def remove_frame(frame):
    print("Remove frame")

def generate_images(props):
    print("generate images")
