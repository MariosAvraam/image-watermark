import os
import tkinter as tk
from tkinter import ttk, Tk, Label, Entry, PanedWindow, Frame, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Constants
MAX_IMAGE_DIMENSIONS = (600, 600)
MAX_WATERMARK_DIMENSIONS = (150, 150)
OFFSET = 30
FONT_DIR = 'fonts'
FONT_EXTENSION = '.otf'
AVAILABLE_COLORS = ["white", "black", "red", "blue", "green", "yellow"]
POSITIONS = ["Top-Left", "Top-Right", "Center", "Bottom-Left", "Bottom-Right"]


class WatermarkApp:
    """
    A GUI application for watermarking images with either text or another image.
    """

    def __init__(self, root):
        """
        Initialize the application with the main window (root).
        """
        self.root = root
        self._setup_ui()
        self._initialize_variables()

    def _setup_ui(self):
        """Configure UI components."""
        self._setup_main_window()
        self._setup_left_frame()
        self._setup_right_frame()

    def _setup_main_window(self):
        """Configure the main application window."""
        self.root.title("Modern Watermark Application")
        self.root.state('zoomed')
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", font=('Arial', 10))
        self.paned_window = PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

    def _setup_left_frame(self):
        """Set up the left frame for image upload and display."""
        self.left_frame = Frame(self.paned_window, bg='gray')

        self.upload_button = ttk.Button(self.left_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.image_label = Label(self.left_frame, text="Image will be displayed here.", bg='gray')
        self.image_label.pack(pady=20, padx=20)
        self.paned_window.add(self.left_frame)

    def _setup_right_frame(self):
        """Set up the right frame for watermark settings."""
        self.right_frame = Frame(self.paned_window)

        self.upload_watermark_button = ttk.Button(self.right_frame, text="Upload Image as Watermark", command=self.upload_watermark_image)
        self.upload_watermark_button.pack(pady=10)

        self.watermark_image_label = Label(self.right_frame, text="", wraplength=200)
        self.watermark_image_label.pack(pady=10)

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
        self.color_combobox.set("white")

        self.font_var = tk.StringVar(self.right_frame)
        available_fonts = [f[:-4] for f in os.listdir('fonts') if f.endswith('.otf')]
        if available_fonts:
            self.font_var.set(available_fonts[0])
            self.font_dropdown = tk.OptionMenu(self.right_frame, self.font_var, *available_fonts)
            self.font_dropdown.pack(pady=10)

        self.opacity_label = tk.Label(self.right_frame, text="Watermark Opacity:")
        self.opacity_label.pack(pady=5)
        self.opacity_scale = tk.Scale(self.right_frame, from_=10, to=100, orient="horizontal", sliderlength=30, length=250)
        self.opacity_scale.pack(pady=5)
        self.opacity_scale.set(50)

        self.position_var = tk.StringVar(self.right_frame)
        self.position_var.set("Bottom-Right")
        self.position_options = ["Top-Left", "Top-Right", "Center", "Bottom-Left", "Bottom-Right"]
        self.position_dropdown = tk.OptionMenu(self.right_frame, self.position_var, *self.position_options)
        self.position_dropdown.pack(pady=10)

        self.apply_button = ttk.Button(self.right_frame, text="Apply Watermark", command=self.apply_watermark)
        self.apply_button.pack(pady=10)

        self.save_button = ttk.Button(self.right_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

        self.paned_window.add(self.right_frame)
        self.root.update()
        self.paned_window.sash_place(0, self.root.winfo_width() // 2, 0)

    def _initialize_variables(self):
        """Initialize essential variables."""
        self.image = None
        self.watermarked_image = None

    def upload_image(self):
        """Load an image from file and display it in the app."""
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        self.image = Image.open(file_path)
        self.display_image(self.image)

    def display_image(self, image):
        """Display a given image in the left frame."""
        if image.width > MAX_IMAGE_DIMENSIONS[0] or image.height > MAX_IMAGE_DIMENSIONS[1]:
            aspect_ratio = image.width / image.height
            if aspect_ratio > 1:
                new_width = MAX_IMAGE_DIMENSIONS[0]
                new_height = int(MAX_IMAGE_DIMENSIONS[1] / aspect_ratio)
            else:
                new_height = MAX_IMAGE_DIMENSIONS[1]
                new_width = int(MAX_IMAGE_DIMENSIONS[1] * aspect_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tk_image, text="")
        self.image_label.image = tk_image

    def apply_watermark(self):
        """Apply the selected watermark to the image."""
        if not self.image:
            return
        if not self._validate_input():
            return
        self.watermarked_image = self.image.copy()
        
        # Apply image watermark if it exists
        if hasattr(self, 'watermark_image'):
            base_width_ratio = 0.2
            base_width = int(self.image.width * base_width_ratio)
            aspect_ratio = self.watermark_image.width / self.watermark_image.height
            new_width = base_width
            new_height = int(base_width / aspect_ratio)
            self.watermark_image = self.watermark_image.resize((new_width, new_height), Image.LANCZOS).convert('RGBA')

            position = self.position_var.get()

            if position == "Center":
                x = (self.watermarked_image.width - self.watermark_image.width) / 2
                y = (self.watermarked_image.height - self.watermark_image.height) / 2
            else:
                position_dict = {
                    "Top-Left": (OFFSET, OFFSET),
                    "Top-Right": (self.watermarked_image.width - self.watermark_image.width - OFFSET, OFFSET),
                    "Bottom-Left": (OFFSET, self.watermarked_image.height - self.watermark_image.height - OFFSET),
                    "Bottom-Right": (self.watermarked_image.width - self.watermark_image.width - OFFSET,
                                    self.watermarked_image.height - self.watermark_image.height - OFFSET)
                }
                x, y = position_dict.get(position, (0, 0))

            mask = self.watermark_image.split()[3]
            self.watermarked_image.paste(self.watermark_image, (int(x), int(y)), mask)

        # Apply text watermark if no image watermark exists
        else:
            draw = ImageDraw.Draw(self.watermarked_image)
            selected_font = self.font_var.get() + FONT_EXTENSION
            font_path = os.path.join(FONT_DIR, selected_font)
            font = ImageFont.truetype(font_path, 30)
            text = self.watermark_entry.get()
            color_name = self.color_combobox.get()
            alpha = int(self.opacity_scale.get() * 2.55)
            color = self.get_rgba(color_name, alpha)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            position = self.position_var.get()
            position_dict = {
                "Top-Left": (OFFSET, OFFSET),
                "Top-Right": (self.watermarked_image.width - text_width - OFFSET, OFFSET),
                "Center": ((self.watermarked_image.width - text_width) / 2,
                        (self.watermarked_image.height - text_height) / 2),
                "Bottom-Left": (OFFSET, self.watermarked_image.height - text_height - OFFSET),
                "Bottom-Right": (self.watermarked_image.width - text_width - OFFSET,
                                self.watermarked_image.height - text_height - OFFSET)
            }
            position_coords = position_dict.get(position, (0, 0))
            draw.text(position_coords, text, font=font, fill=color)
        
        self.display_image(self.watermarked_image)

    def save_image(self):
        """Save the watermarked image."""
        if not self._validate_input():
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                  filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not file_path:
            return

        self.watermarked_image.save(file_path)

    def get_rgba(self, color_name, alpha=255):
        """Return the RGBA value for a given color name and alpha value."""
        color_dict = {
            "white": (255, 255, 255, alpha),
            "black": (0, 0, 0, alpha),
            "red": (255, 0, 0, alpha),
            "blue": (0, 0, 255, alpha),
            "green": (0, 255, 0, alpha),
            "yellow": (255, 255, 0, alpha)
        }
        return color_dict.get(color_name, (255, 255, 255, alpha))

    def _validate_input(self):
        """Check if valid inputs for watermarking are provided by the user."""
        if not self.image:
            messagebox.showerror("Error", "Please upload an image first!")
            return False
        if not self.watermark_entry.get().strip() and not hasattr(self, 'watermark_image'):
            messagebox.showerror("Error", "Please enter a watermark text or choose an image as a watermark!")
            return False
        return True

    def upload_watermark_image(self):
        """Load a watermark image and display it in the app."""
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.watermark_image = Image.open(file_path)
        if self.watermark_image.mode != 'RGBA':
            self.watermark_image = self.watermark_image.convert('RGBA')

        if self.watermark_image.width > MAX_WATERMARK_DIMENSIONS[0] or self.watermark_image.height > MAX_WATERMARK_DIMENSIONS[1]:
            aspect_ratio = self.watermark_image.width / self.watermark_image.height
            if aspect_ratio > 1:
                new_width = MAX_WATERMARK_DIMENSIONS[0]
                new_height = int(MAX_WATERMARK_DIMENSIONS[1] / aspect_ratio)
            else:
                new_height = MAX_WATERMARK_DIMENSIONS[1]
                new_width = int(MAX_WATERMARK_DIMENSIONS[1] * aspect_ratio)
            self.watermark_image = self.watermark_image.resize((new_width, new_height), Image.LANCZOS)

        tk_watermark_image = ImageTk.PhotoImage(self.watermark_image)
        self.watermark_display_label.config(image=tk_watermark_image)
        self.watermark_display_label.image = tk_watermark_image
        self.watermark_entry.config(state=tk.DISABLED)

    def remove_watermark_image(self):
        """Remove the watermark image and re-enable text watermarking."""
        if hasattr(self, 'watermark_image'):
            del self.watermark_image
        self.watermark_display_label.config(image=None)
        self.watermark_display_label.image = None
        self.watermark_entry.config(state=tk.NORMAL)
        messagebox.showinfo("Info", "Watermark image removed. You can now use text.")


if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)
    root.mainloop()
