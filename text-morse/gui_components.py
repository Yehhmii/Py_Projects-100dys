import tkinter as tk
from tkinter import ttk


class TabFrame(ttk.Frame):
    """Base class for tab frames"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.style = ttk.Style()
        self.configure_style()

    def configure_style(self):
        # Configure styles with fallback values
        bg_color = "#2d2d2d"  # Default background color
        try:
            # Try to get the master's background if it exists
            if hasattr(self.master, 'cget') and 'background' in self.master.keys():
                bg_color = self.master.cget('background')
        except tk.TclError:
            pass

        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel',
                             background=bg_color,
                             foreground="#ffffff",
                             font=('Segoe UI', 10))
        self.style.configure('TButton',
                             background="#4CAF50",
                             foreground="#eed54f",
                             font=('Segoe UI', 10, 'bold'))


class ConversionTab(TabFrame):
    """Base class for conversion tabs"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # To be implemented by subclasses
        pass

    def create_input_section(self, label_text):
        """Create labeled input section"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        label = ttk.Label(frame, text=label_text, font=('Segoe UI', 11))
        label.pack(anchor=tk.W)

        input_widget = tk.Text(frame, height=5, bg="#3d3d3d", fg="#ffffff",
                               insertbackground="white", font=('Segoe UI', 10), wrap=tk.WORD)
        input_widget.pack(fill=tk.X)

        return input_widget

    def create_output_section(self, label_text):
        """Create labeled output section"""
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        label = ttk.Label(frame, text=label_text, font=('Segoe UI', 11))
        label.pack(anchor=tk.W)

        output_widget = tk.Text(frame, height=5, bg="#3d3d3d", fg="#ffffff",
                                font=('Segoe UI', 10), state=tk.DISABLED)
        output_widget.pack(fill=tk.X)

        return output_widget

    def create_button(self, text, command):
        """Create a styled button"""
        button = ttk.Button(self, text=text, command=command)
        button.pack(pady=5)
        return button