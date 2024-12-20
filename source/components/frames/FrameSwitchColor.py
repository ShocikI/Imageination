from tkinter.ttk import Frame, Button, Scrollbar, Notebook
from tkinter import Toplevel, Canvas, messagebox, Event
from PIL import Image, ImageTk

from source.ops import FrameSwitchColorOperators as ops
from source.data.SystemData import SystemData, SwitchData


class FrameSwitchColor(Frame):
    """
    FrameSwitchColor creates a GUI frame for color switch operations within a scrollable canvas.
    It handles user interactions for selecting and switching colors from images, as well as generating output images.
    """
    canvas: Canvas | None = None
    scrollbar: Scrollbar | None = None
    scr_frame: Frame | None = None
    b_pop_up: Button | None = None
    b_generate: Button | None = None
    pop_up: Toplevel | None = None
    zoom_window: Toplevel | None = None
    
    ZOOM_FACTOR: int = 15
    ZOOM_AREA_SIZE: int = 10 

    def __init__(self, parent: Notebook, data: SystemData):
        """
        Initializes the FrameSwitchColor.

        Args:
            parent (Notebook): The parent Notebook widget.
            data (SystemData): An instance of SystemData holding information related to switches and image data.
        """
        Frame.__init__(self, parent)
        self.create(data)

    def create(self, data: SystemData):
        """
        Initializes the FrameSwitchColor.

        Args:
            parent (Notebook): The parent Notebook widget.
            data (SystemData): An instance of SystemData holding information related to switches and image data.
        """
        self['padding'] = (10, 5)
        # Create Canvas in Frame to make Scrollable Frame
        # self > Canvas > Frame
        self.canvas = Canvas(self, highlightthickness=0, bd=0)
        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scr_frame = Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.scr_frame, anchor="nw")

        self.b_pop_up = Button(self.scr_frame, text="Select color to switch", command=lambda: self.draw_pop_up(data))
        self.b_pop_up['padding'] = (15, 5)

        for item in data.switch_data:
            self.create_switch_frame(item.color_hex)

        self.b_generate = Button(
            self.scr_frame, text="Generate images",
            command=lambda: (ops.generate_images(data), self.update_grid(data))
        )
        self.b_generate['padding'] = (15, 5)

        # Grid
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(fill="both", expand=True)

        self.b_pop_up.grid(column=2, row=1, sticky='we')
        # Bind mouse wheel scrolling to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)  # For macOS scroll up
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)  # For macOS scroll down
        self.scr_frame.bind("<Configure>", self.on_frame_configure)

    def _on_mouse_wheel(self, event):
        """
        Handles mouse wheel scrolling for Windows, Linux, and macOS.

        Args:
            event (Event): The event object containing details of the mouse scroll.
        """
        if event.num == 4:  # macOS scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # macOS scroll down
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")  # Windows/Linux scroll

    def on_frame_configure(self, event=None):
        """
        Updates the canvas scrolling region based on the size of the frame.

        Args:
            event (Event, optional): The event object. Defaults to None.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_scrollbar_when_needed(self):
        """
        Shows or hides the scrollbar depending on the size of the content in the canvas.
        """
        if self.canvas.bbox("all")[3] > self.canvas.winfo_height():
            self.scrollbar.pack(side='right', fill="y")
        else:
            self.scrollbar.pack_forget()

    def update_grid(self, data: SystemData):
        """
        Updates the grid layout within the scrollable frame, regenerating it based on current switch data.

        Args:
            data (SystemData): The data structure holding switch data for color switching.
        """
        for widget in self.grid_slaves():
            widget.grid_forget()

        self.b_pop_up.grid(column=2, row=1, sticky='we')
        row = 2
        # Chcek data in switch_data
        if len(data.switch_data) > 0:
            for item in data.switch_data:
                item.grid_up(1, row)
                row += 3
            
            self.b_generate.grid(column=2, row=row, sticky='we')
            self.b_generate.grid()
        else:
            self.b_generate.grid_remove()

    def draw_pop_up(self, data: SystemData):
        """
        Draws a pop-up window to allow the user to select a pixel from the image for color switching.

        Args:
            data (SystemData): The data structure holding image and switch data.
        """
        if len(data.file_names) != 1:
            messagebox.showinfo(message='Select 1 image in "File selection".')
            return None
        image_data = Image.open(data.file_names[0])
        color_mode = image_data.mode
        if color_mode is 'RGB':
            messagebox.showinfo(message='This operation is possible only for RGB images.')
            return None

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
        zoom_canvas = Canvas(self.zoom_window, width=self.ZOOM_AREA_SIZE * self.ZOOM_FACTOR, height=self.ZOOM_AREA_SIZE * self.ZOOM_FACTOR)
        zoom_canvas.pack(side="right")

        canvas.bind("<Button-1>", lambda event: self.get_pixel_color(event, image_data, 1, data))
        canvas.bind("<Button-3>", lambda event: (
            self.zoom_window.deiconify(), 
            self.show_zoom(event, image_data, zoom_canvas, data)
        ))

    def show_zoom(self, event: Event, image_data: Image, zoom_canvas: Canvas, data: SystemData):
        """
        Displays a zoomed-in section of the image near the selected pixel.

        Args:
            event (Event): The event object containing the mouse click position.
            image_data (Image): The image object being zoomed in.
            zoom_canvas (Canvas): The canvas displaying the zoomed-in image.
            data (SystemData): The data structure holding system and switch data.
        """
        x, y = event.x, event.y
        
        half_area = self.ZOOM_AREA_SIZE  // 2
        box = (x - half_area, y - half_area, x + half_area, y + half_area)
        
        if box[0] < 0 or box[1] < 0 or box[2] > image_data.width or box[3] > image_data.height:
            return
        
        cropped_image = image_data.crop(box)
        zoomed_image = cropped_image.resize(
            (self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR, self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR), 
            Image.NEAREST
        )
        
        tk_zoomed_image = ImageTk.PhotoImage(zoomed_image)
        zoom_canvas.create_image(0, 0, anchor='nw', image=tk_zoomed_image)
        zoom_canvas.image = tk_zoomed_image 
        
        self.zoom_window.geometry(f"+{event.x_root - self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR // 2}+{event.y_root - self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR // 2}")
        self.zoom_window.lift()
        self.zoom_window.attributes("-topmost", True)

        zoom_canvas.delete("border")
        zoom_canvas.create_rectangle(0, 0, self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR, self.ZOOM_AREA_SIZE  * self.ZOOM_FACTOR, outline="black", width=3, tags="border")

        zoom_canvas.bind("<Button-1>", lambda new_event: self.get_pixel_color(new_event, cropped_image, self.ZOOM_FACTOR, data))

    def get_pixel_color(self, event: Event, image_data: Image, multiplier: float, data: SystemData):
        """
        Captures the RGB value of the pixel the user clicked and updates the switch data if it's a new color.

        Args:
            event (Event): The event object containing the mouse click position.
            image_data (Image): The image from which the pixel color is selected.
            multiplier (float): Scaling factor for zooming purposes.
            data (SystemData): The data structure holding switch data and image information.
        """
        x, y = int(event.x / multiplier), int(event.y / multiplier)
        rgb_pixel = image_data.getpixel((x, y))

        is_new = True
        if len(data.switch_data):
            for image_data in data.switch_data:
                if list(image_data.rgb_color) == list(rgb_pixel):
                    is_new = False

        self.zoom_window.destroy()
        self.pop_up.destroy()

        if is_new:
            data.switch_data.append(SwitchData(self.scr_frame, data, rgb_pixel))
            self.update_grid(data)
