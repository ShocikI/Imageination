from tkinter.ttk import Frame, Button, Labelframe, Scrollbar
from tkinter import Listbox, Toplevel, Canvas, messagebox, PhotoImage
from PIL import Image, ImageTk

from source.ops import FrameSwitchColorOperators as ops
from source.data import SwitchData as sd


class FrameSwitchColor(Frame):
    canvas = None
    window = None
    scrollbar = None
    scr_frame = None
    b_pop_up = None
    b_generate = None
    pop_up = None
    zoom_window = None
    
    zoom_factor = 15
    zoom_area_size = 10 

    def __init__(self, parent, props):
        Frame.__init__(self, parent)
        self.create(props)

    def create(self, props):
        self['padding'] = (10, 5)
        # Create Canvas in Frame to make Scrollable Frame
        # self > Canvas > Frame
        self.canvas = Canvas(self, highlightthickness=0, bd=0)
        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scr_frame = Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.window = self.canvas.create_window((0, 0), window=self.scr_frame, anchor="nw")

        self.b_pop_up = Button(
            self.scr_frame, text="Select color to switch", 
            command=lambda: self.draw_pop_up(props)
        )
        self.b_pop_up['padding'] = (15, 5)

        for data in props['switch_data']:
            self.create_switch_frame(color_hex)

        self.b_generate = Button(
            self.scr_frame, text="Generate images",
            command=lambda: (ops.generate_images(props), self.update_grid(props))
        )
        self.b_generate['padding'] = (15, 5)

        # Grid
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(fill="both", expand=True)

        self.b_pop_up.grid(column=2, row=1, sticky='we')

        self.scr_frame.bind("<Configure>", self.on_frame_configure)
    
    def on_frame_configure(self, event=None):
        """Funkcja wywoływana przy każdej zmianie rozmiaru frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def show_scrollbar_when_needed(self):
        if self.canvas.bbox("all")[3] > self.canvas.winfo_height():
            self.scrollbar.pack(side=tk.RIGHT, fill="y")
        else:
            self.scrollbar.pack_forget()

    def update_grid(self, props):
        for widget in self.grid_slaves():
            widget.grid_forget()

        self.b_pop_up.grid(column=2, row=1, sticky='we')
        row = 2
        # Sprawdź, czy są dane w switch_data
        print([name for name in props['file_names']])
        if len(props['switch_data']) > 0:
            for item in props['switch_data']:
                item.grid_up(1, row)
                row += 3
            
            self.b_generate.grid(column=2, row=row, sticky='we')
            self.b_generate.grid()
        else:
            self.b_generate.grid_remove()

    def draw_pop_up(self, props):
        if len(props['file_names']) != 1:
            messagebox.showinfo(message='Select 1 image in "File selection".')
            return None
        image_data = Image.open(props['file_names'][0])
        w, h = image_data.size
        image_to_display = ImageTk.PhotoImage(image_data)    

        self.pop_up = Toplevel(height=h, width=w)
        self.pop_up.title("Select one pixel")
        canvas = Canvas(self.pop_up, height=h, width=w)
        canvas.create_image(0, 0, anchor=('nw'), image=image_to_display)
        canvas.image_to_display = image_to_display
        canvas.pack()
        
        self.zoom_window = Toplevel(canvas)
        self.zoom_window.overrideredirect(True)
        self.zoom_window.attributes("-topmost", True)
        self.zoom_window.withdraw() 
        zoom_canvas = Canvas(
            self.zoom_window, 
            width=self.zoom_area_size * self.zoom_factor, 
            height=self.zoom_area_size * self.zoom_factor
        )
        zoom_canvas.pack(side="right")

        canvas.bind("<Button-1>", lambda event: self.get_pixel_color(event, image_data, 1, props))
        canvas.bind("<Button-3>", lambda event: (
            self.zoom_window.deiconify(), 
            self.show_zoom(event, image_data, zoom_canvas, props)
        ))

    def show_zoom(self, event, data, zoom_canvas, props):
        x, y = event.x, event.y
        
        half_area = self.zoom_area_size  // 2
        box = (x - half_area, y - half_area, x + half_area, y + half_area)
        
        if box[0] < 0 or box[1] < 0 or box[2] > data.width or box[3] > data.height:
            return
        
        cropped_image = data.crop(box)
        zoomed_image = cropped_image.resize(
            (self.zoom_area_size  * self.zoom_factor, self.zoom_area_size  * self.zoom_factor), 
            Image.NEAREST
        )
        
        tk_zoomed_image = ImageTk.PhotoImage(zoomed_image)
        zoom_canvas.create_image(0, 0, anchor='nw', image=tk_zoomed_image)
        zoom_canvas.image = tk_zoomed_image 
        
        self.zoom_window.geometry(f"+{event.x_root - self.zoom_area_size  * self.zoom_factor // 2}+{event.y_root - self.zoom_area_size  * self.zoom_factor // 2}")
        self.zoom_window.lift()
        self.zoom_window.attributes("-topmost", True)

        zoom_canvas.delete("border")
        zoom_canvas.create_rectangle(0, 0, self.zoom_area_size  * self.zoom_factor, self.zoom_area_size  * self.zoom_factor, outline="black", width=3, tags="border")

        zoom_canvas.bind("<Button-1>", lambda new_event: self.get_pixel_color(new_event, cropped_image, self.zoom_factor, props))

    def get_pixel_color(self, event, data, multiplier, props):
        x, y = int(event.x / multiplier), int(event.y / multiplier)
        rgb_pixel = data.getpixel((x, y))

        is_new = True
        if len(props['switch_data']):
            for data in props['switch_data']:
                if list(data.rgb_color) == list(data.rgb_color):
                    is_new = False

        self.zoom_window.destroy()
        self.pop_up.destroy()

        if is_new:
            props['switch_data'].append(sd.SwitchData(self.scr_frame, props, rgb_pixel))
            self.update_grid(props)
