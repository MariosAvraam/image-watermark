from tkinter import ttk, Tk, Label, Entry, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Watermark Application")
        
        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", font=('Arial', 10))
        
        # Create and place widgets
        self.upload_button = ttk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.image_label = Label(root, text="Image will be displayed here.")
        self.image_label.pack(pady=20)

        self.watermark_entry = Entry(root, width=30)
        self.watermark_entry.pack(pady=20)
        self.watermark_entry.insert(0, "Enter watermark text")

        self.color_label = tk.Label(root, text="Select Watermark Color:")
        self.color_label.pack(pady=(20,0))
        self.color_combobox = ttk.Combobox(root, values=["white", "black", "red", "blue", "green", "yellow"], state="readonly")
        self.color_combobox.pack(pady=(0,20))
        self.color_combobox.set("white")  # default value

        self.apply_button = ttk.Button(root, text="Apply Watermark", command=self.apply_watermark)
        self.apply_button.pack(pady=20)

        self.save_button = ttk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=20)

        # Variables to hold image data
        self.image = None
        self.watermarked_image = None


    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path)
        self.display_image(self.image)


    def display_image(self, image):
        max_width = 400
        max_height = 400

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

        self.watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)

        # Set watermark properties
        font = ImageFont.truetype("arial.ttf", 30)
        text = self.watermark_entry.get()
        color = self.color_combobox.get()
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position watermark at the bottom right corner
        x = self.watermarked_image.width - text_width - 30
        y = self.watermarked_image.height - text_height - 30
        draw.text((x, y), text, font=font, fill=color)

        self.display_image(self.watermarked_image)


    def save_image(self):
        if not self.watermarked_image:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not file_path:
            return

        self.watermarked_image.save(file_path)


root = Tk()
app = WatermarkApp(root)
root.mainloop()
