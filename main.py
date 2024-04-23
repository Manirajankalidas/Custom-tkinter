##final app

import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import ttk
from tkinter import Canvas, PhotoImage
import os
from PIL import ImageGrab, Image
from pathlib import Path
import uuid


class WhiteboardApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title('Whiteboard')
        self.root.geometry('1920x1080')
        self.root.config(bg='#f2f3f5')

        # Initialize variables
        self.current_x = 0
        self.current_y = 0
        self.color = "black"
        self.is_eraser = False  # Flag to track whether eraser is selected
        self.lines = []

        # Create main Canvas for drawing
        self.canvas = Canvas(root, width=1370, height=700, background='white', cursor="hand2")
        self.canvas.place(x=155, y=10)
        self.canvas.bind('<Button-1>', self.locate_xy)
        self.canvas.bind('<B1-Motion>', self.addline)

        # Slider for line width
        self.current_value = tk.DoubleVar()
        self.slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=self.slider_changed,
                                variable=self.current_value)
        self.slider.place(x=30, y=600)

        # Label to display current line width
        self.value_label = ttk.Label(root, text=self.get_current_value())
        self.value_label.place(x=27, y=620)

        # Display color palette
        self.display_palette()

        # Add buttons for tools
        self.add_buttons()

    def locate_xy(self, event):
        # Update current coordinates when mouse is clicked
        self.current_x = event.x
        self.current_y = event.y

    def addline(self, event):
        # Draw a line based on mouse movement
        if self.is_eraser:
            # Draw white lines when eraser is selected
            line = self.canvas.create_line((self.current_x, self.current_y, event.x, event.y),
                                           width=self.get_current_value(), fill="white", capstyle=tk.ROUND, smooth=True)
            self.lines.append(line)
        else:
            # Draw lines with selected color
            line = self.canvas.create_line((self.current_x, self.current_y, event.x, event.y),
                                           width=self.get_current_value(), fill=self.color, capstyle=tk.ROUND, smooth=True)
            self.lines.append(line)
        self.current_x, self.current_y = event.x, event.y

    def display_palette(self):
        # Display color palette for selecting drawing color
        colors = Canvas(self.root, bg='#fff', width=37, height=300, bd=0)
        colors.place(x=35, y=25, width=60, height=260)

        def show_color(new_color):
            self.color = new_color

        def create_color_button(color, x, y):
            id = colors.create_rectangle((10, x, 50, y), fill=color)
            colors.tag_bind(id, '<Button-1>', lambda x: show_color(color))

        # Create color buttons
        create_color_button("black", 10, 40)
        create_color_button("red", 45, 75)
        create_color_button("orange", 80, 110)
        create_color_button("yellow", 115, 145)
        create_color_button("green3", 150, 180)
        create_color_button("blue", 185, 215)
        create_color_button("purple", 220, 250)

    def add_buttons(self):
        # Add buttons for tools
        button_positions = [
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\pencil.png", self.activate_pencil),
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\eraser.png", self.toggle_eraser),
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\clear.png", self.new_canvas),
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\imagefile.png", self.insert_image),
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\save.png", self.save_image),
            ("C:\\Users\\manir\\OneDrive\\Desktop\\mew technology\\project\\air paint\\finalApp\\background.png", self.change_color)
        ]
        for i, (icon_file, command) in enumerate(button_positions):
            button = self.create_button(icon_file, command)
            button.place(x=40, y=290 + i * 50)

    def create_button(self, icon_file, command):
        # Create a button with an icon
        icon = PhotoImage(file=icon_file)
        button = tk.Button(self.root, image=icon, bg='#f2f3f5', command=command)
        button.image = icon  # Prevent garbage collection of the image
        return button

    def activate_pencil(self):
        # Activate pencil tool
        self.is_eraser = False
        self.canvas["cursor"] = "arrow"

    def toggle_eraser(self):
        # Toggle eraser tool
        self.is_eraser = not self.is_eraser
        self.canvas["cursor"] = "dotbox" if self.is_eraser else "arrow"

    def new_canvas(self):
        # Clear the canvas
        self.canvas.delete('all')
        self.display_palette()

    def insert_image(self):
        global filename, f_img
        # Insert image onto the canvas
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image file",
                                              filetypes=(('PNG file', '*.png'), ('JPG file', '*.jpg'), ('All files', '*.*')))
        if not filename:
            return  # If no file selected, do nothing

         # Load the image file and create a PhotoImage object
        f_img = tk.PhotoImage(file=filename)

        # Get the size of the loaded image
        img_width = f_img.width()
        img_height = f_img.height()

        # Calculate the scaling factor to fit the image within the canvas
        scale_factor = min(1, self.canvas.winfo_width() / img_width, self.canvas.winfo_height() / img_height)
        
        # Resize the image to fit within the canvas
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        f_img = f_img.subsample(int(1 / scale_factor), int(1 / scale_factor))
        
        # Calculate the position to center the image on the canvas
        x = (self.canvas.winfo_width() - new_width) // 2
        y = (self.canvas.winfo_height() - new_height) // 2
        
        # Clear any existing items on the canvas
        self.canvas.delete("all")

        # Create image item on canvas
        my_img = self.canvas.create_image(x, y, image=f_img, anchor="nw")

    def save_image(self):
        # Save the canvas as an image
        x = self.root.winfo_rootx() + 200
        y = self.root.winfo_rooty() + 20
        img = ImageGrab.grab(bbox=(x, y, x + 1710, y + 840))

        # Paths for standard and OneDrive Desktop
        standard_desktop_path = Path.home() / "Desktop"
        onedrive_desktop_path = Path.home() / "OneDrive" / "Desktop"

        # Determine the correct Desktop path
        if onedrive_desktop_path.exists():
            desktop_path = onedrive_desktop_path
        else:
            desktop_path = standard_desktop_path


        # Define the "graffiti_image" folder path
        graffiti_image_path = desktop_path / "graffiti_image" 

        # Ensure the "graffiti_image" folder exists
        graffiti_image_path.mkdir(parents=True, exist_ok=True)  
        
        # Generate a random filename for the image
        filename = f"{uuid.uuid4()}.png"  
        full_path = graffiti_image_path / filename
        img.save(full_path)
        img.show()

    def get_current_value(self):
        # Get current value of the slider for line width
        return '{: .2f}'.format(self.current_value.get())

    def slider_changed(self, event):
        # Handle slider change event
        self.value_label.configure(text=self.get_current_value())

    def change_color(self):
        # Change drawing color
        color = colorchooser.askcolor()[1]  # Ask the user to choose a color and get the HEX value
        if color:
            self.canvas.config(bg=color)

    def run(self):
        # Run the Tkinter main loop
        self.root.mainloop()


if __name__ == "__main__":
    # Create and run the WhiteboardApp
    root = tk.Tk()
    whiteboard_app = WhiteboardApp(root)
    whiteboard_app.run()
