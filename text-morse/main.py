import tkinter as tk
from tkinter import ttk
from text_to_morse_tab import TextToMorseTab
from morse_to_text_tab import MorseToTextTab


class MorseCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Morse Code Converter")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        # self.root.configure(bg="#2d2d2d")
        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Main background color
        self.root.configure(bg="#2d2d2d")

        # Notebook style
        self.style.configure('TNotebook', background="#2d2d2d")
        self.style.configure('TNotebook.Tab',
                             background="#3d3d3d",
                             foreground="#ffffff",
                             padding=[10, 5])
        self.style.map('TNotebook.Tab',
                       background=[('selected', "#4CAF50")])

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        text_to_morse_tab = TextToMorseTab(notebook)
        morse_to_text_tab = MorseToTextTab(notebook)

        notebook.add(text_to_morse_tab, text="Text to Morse")
        notebook.add(morse_to_text_tab, text="Morse to Text")


if __name__ == "__main__":
    root = tk.Tk()
    app = MorseCodeApp(root)
    root.mainloop()