from tkinter import ttk, Tk, Label, Entry, filedialog, PanedWindow, Frame, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Watermark Application")
        self.root.state('zoomed')  # Open app in fullscreen mode

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", font=('Arial', 10))

        # Create a split view using PanedWindow
        self.paned_window = PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Left side for image upload and display
        self.left_frame = Frame(self.paned_window, bg='gray')
        self.upload_button = ttk.Button(self.left_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)
        self.image_label = Label(self.left_frame, text="Image will be displayed here.", bg='gray')
        self.image_label.pack(pady=20, padx=20)
        self.paned_window.add(self.left_frame)


        # Right side for watermark properties
        self.right_frame = Frame(self.paned_window)

        # Add a button to upload image as watermark
        self.upload_watermark_button = ttk.Button(self.right_frame, text="Upload Image as Watermark", command=self.upload_watermark_image)
        self.upload_watermark_button.pack(pady=10)
        
        # Add a label to show the path of the uploaded watermark image
        self.watermark_image_label = Label(self.right_frame, text="", wraplength=200)
        self.watermark_image_label.pack(pady=10)

        # Add a label to display the uploaded watermark image
        self.watermark_display_label = Label(self.right_frame, bg='gray')
        self.watermark_display_label.pack(pady=5)


        self.remove_watermark_image_button = ttk.Button(self.right_frame, text="Remove Image Watermark", command=self.remove_watermark_image)
        self.remove_watermark_image_button.pack(pady=10)

        
        self.watermark_entry = Entry(self.right_frame, width=30)
        self.watermark_entry.pack(pady=10)
        self.watermark_entry.insert(0, "Enter watermark text")

        self.color_label = tk.Label(self.right_frame, text="Select Watermark Color:")
        self.color_label.pack(pady=5)
        self.color_combobox = ttk.Combobox(self.right_frame, values=["white", "black", "red", "blue", "green", "yellow"], state="readonly")
        self.color_combobox.pack(pady=5)
        self.color_combobox.set("white")  # default value

        # Dropdown for font selection
        self.font_var = tk.StringVar(self.right_frame)
        available_fonts = [f[:-4] for f in os.listdir('fonts') if f.endswith('.otf')]
        if available_fonts:
            self.font_var.set(available_fonts[0])  # set default value to the first font
            self.font_dropdown = tk.OptionMenu(self.right_frame, self.font_var, *available_fonts)
            self.font_dropdown.pack(pady=10)

        self.opacity_label = tk.Label(self.right_frame, text="Watermark Opacity:")
        self.opacity_label.pack(pady=5)
        self.opacity_scale = tk.Scale(self.right_frame, from_=10, to=100, orient="horizontal", sliderlength=30, length=250)
        self.opacity_scale.pack(pady=5)
        self.opacity_scale.set(50)  # default value

        self.position_var = tk.StringVar(self.right_frame)
        self.position_var.set("Bottom-Right")  # default value
        self.position_options = ["Top-Left", "Top-Right", "Center", "Bottom-Left", "Bottom-Right"]
        self.position_dropdown = tk.OptionMenu(self.right_frame, self.position_var, *self.position_options)
        self.position_dropdown.pack(pady=10)

        self.apply_button = ttk.Button(self.right_frame, text="Apply Watermark", command=self.apply_watermark)
        self.apply_button.pack(pady=10)

        self.save_button = ttk.Button(self.right_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

        self.paned_window.add(self.right_frame)
        self.root.update()  # Force the window to update its dimensions
        self.paned_window.sash_place(0, self.root.winfo_width() // 2, 0)


        # Variables to hold image data
        self.image = None
        self.watermarked_image = None

    
    def upload_watermark_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.watermark_image = Image.open(file_path)

        # Ensure the watermark image has an alpha channel (transparency)
        if self.watermark_image.mode != 'RGBA':
            self.watermark_image = self.watermark_image.convert('RGBA')

        # Display the uploaded watermark image in the label
        max_width = 150
        max_height = 150
        # Check if the image needs to be resized
        if self.watermark_image.width > max_width or self.watermark_image.height > max_height:
            # Calculate the aspect ratio
            aspect_ratio = self.watermark_image.width / self.watermark_image.height
            if aspect_ratio > 1:
                # Image is wider than it is tall
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                # Image is taller than it is wide
                new_height = max_height
                new_width = int(max_height * aspect_ratio)

            # Resize the image
            self.watermark_image = self.watermark_image.resize((new_width, new_height), Image.LANCZOS)

        tk_watermark_image = ImageTk.PhotoImage(self.watermark_image)
        self.watermark_display_label.config(image=tk_watermark_image)
        self.watermark_display_label.image = tk_watermark_image

        # Disable the watermark text entry when an image is used
        self.watermark_entry.config(state=tk.DISABLED)


    
    def validate_input(self):
        """
        Validates user input before applying watermark.
        """
        if not self.image:
            messagebox.showerror("Error", "Please upload an image first!")
            return False
        
        if not self.watermark_entry.get().strip() and not self.watermarked_image:
            messagebox.showerror("Error", "Please enter a watermark text or choose an image as a watermark!")
            return False

        return True


    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path)
        self.display_image(self.image)


    def display_image(self, image):
        max_width = 600
        max_height = 600

        # Check if the image needs to be resized
        if image.width > max_width or image.height > max_height:
            # Calculate the aspect ratio
            aspect_ratio = image.width / image.height
            if aspect_ratio > 1:
                # Image is wider than it is tall
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                # Image is taller than it is wide
                new_height = max_height
                new_width = int(max_height * aspect_ratio)

            # Resize the image
            image = image.resize((new_width, new_height), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tk_image, text="")
        self.image_label.image = tk_image


    def apply_watermark(self):
        if not self.image:
            return

        # Check for necessary validations
        if not self.validate_input():
            return

        self.watermarked_image = self.image.copy()

        # If a watermark image is provided
        if self.watermark_image:
            # Resize the watermark image to be 1/5th the width of the original image, 
            # and make sure to keep the alpha channel
            base_width_ratio = 0.2
            base_width = int(self.image.width * base_width_ratio)
            aspect_ratio = self.watermark_image.width / self.watermark_image.height
            new_width = base_width
            new_height = int(base_width / aspect_ratio)
            self.watermark_image = self.watermark_image.resize((new_width, new_height), Image.LANCZOS).convert('RGBA')

            # Calculate position based on user's choice
            position = self.position_var.get()
            if position == "Top-Left":
                x, y = 30, 30
            elif position == "Top-Right":
                x, y = self.watermarked_image.width - self.watermark_image.width - 30, 30
            elif position == "Center":
                x = (self.watermarked_image.width - self.watermark_image.width) / 2
                y = (self.watermarked_image.height - self.watermark_image.height) / 2
            elif position == "Bottom-Left":
                x, y = 30, self.watermarked_image.height - self.watermark_image.height - 30
            else:  # Bottom-Right
                x, y = self.watermarked_image.width - self.watermark_image.width - 30, self.watermarked_image.height - self.watermark_image.height - 30
            
            # Create a mask using the alpha channel of the watermark image
            mask = self.watermark_image.split()[3]

            # Place the watermark image using the mask
            position = (int(x), int(y))
            self.watermarked_image.paste(self.watermark_image, position, mask)
        else:
            # Use the text watermark
            draw = ImageDraw.Draw(self.watermarked_image)

            # Set watermark properties
            selected_font = self.font_var.get() + ".otf"
            font_path = os.path.join('fonts', selected_font)
            font = ImageFont.truetype(font_path, 30)

            text = self.watermark_entry.get()
            color_name = self.color_combobox.get()
            alpha = int(self.opacity_scale.get() * 2.55)  # converting percentage to [0, 255] scale
            color = self.get_rgba(color_name, alpha)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Determine the position based on user's choice
            position = self.position_var.get()
            if position == "Top-Left":
                x, y = 30, 30
            elif position == "Top-Right":
                x, y = self.watermarked_image.width - text_width - 30, 30
            elif position == "Center":
                x = (self.watermarked_image.width - text_width) / 2
                y = (self.watermarked_image.height - text_height) / 2
            elif position == "Bottom-Left":
                x, y = 30, self.watermarked_image.height - text_height - 30
            else:  # Bottom-Right
                x, y = self.watermarked_image.width - text_width - 30, self.watermarked_image.height - text_height - 30

            draw.text((x, y), text, font=font, fill=color)

        self.display_image(self.watermarked_image)



    def save_image(self):
        if not self.validate_input():
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not file_path:
            return

        self.watermarked_image.save(file_path)

    
    def get_rgba(self, color_name, alpha=255):
        color_dict = {
            "white": (255, 255, 255, alpha),
            "black": (0, 0, 0, alpha),
            "red": (255, 0, 0, alpha),
            "blue": (0, 0, 255, alpha),
            "green": (0, 255, 0, alpha),
            "yellow": (255, 255, 0, alpha)
        }
        return color_dict.get(color_name, (255, 255, 255, alpha))
    

    def remove_watermark_image(self):
        self.watermark_image = None
        # Clear the displayed watermark image
        self.watermark_display_label.config(image=None)
        self.watermark_display_label.image = None  # This line is essential to free up the memory used by the PhotoImage
        # Enable the watermark text entry
        self.watermark_entry.config(state=tk.NORMAL)
        tk.messagebox.showinfo("Info", "Watermark image removed. You can now use text.")


root = Tk()
app = WatermarkApp(root)
root.mainloop()
