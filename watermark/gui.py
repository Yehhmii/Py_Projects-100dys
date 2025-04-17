import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from watermark import apply_watermark

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarker")
        self.root.geometry("800x600")

        # State
        self.base_image = None
        self.watermark_image = None
        self.output_image = None

        # UI Elements
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        tk.Button(control_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Load Watermark", command=self.load_watermark).pack(side=tk.LEFT, padx=5)

        self.position_var = tk.StringVar(value="bottom-right")
        tk.OptionMenu(control_frame, self.position_var,
                      "top-left","top-right","bottom-left","bottom-right").pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Apply Watermark", command=self.apply).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save Image", command=self.save).pack(side=tk.LEFT, padx=5)

        # Preview area
        self.canvas = tk.Canvas(root, bg="gray", width=780, height=520)
        self.canvas.pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path: return
        self.base_image = Image.open(path)
        self.show_preview(self.base_image)

    def load_watermark(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not path: return
        self.watermark_image = Image.open(path)
        messagebox.showinfo("Watermark Loaded", f"Watermark loaded: {path}")

    def apply(self):
        if not self.base_image or not self.watermark_image:
            messagebox.showwarning("Missing Images", "Load both base image and watermark first.")
            return
        pos = self.position_var.get()
        self.output_image = apply_watermark(self.base_image, self.watermark_image, position=pos)
        self.show_preview(self.output_image)

    def save(self):
        if not self.output_image:
            messagebox.showwarning("No Output", "Apply watermark before saving.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPEG", "*.jpg"), ("PNG","*.png")])
        if path:
            self.output_image.save(path)
            messagebox.showinfo("Saved", f"Image saved to {path}")

    def show_preview(self, pil_img):
        # Resize preview to fit within canvas while preserving aspect ratio
        w, h = pil_img.size
        ratio = min(780 / w, 520 / h)
        new_size = (int(w * ratio), int(h * ratio))
        # Apply high-quality resampling
        resized = pil_img.resize(new_size, resample=Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.canvas.create_image(390, 260, image=self.tk_img)