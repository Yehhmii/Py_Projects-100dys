from tkinter import ttk
import tkinter as tk
from gui_components import ConversionTab
from morse_core import MorseTranslator, MorsePlayer
import tkinter.messagebox as messagebox


class TextToMorseTab(ConversionTab):
    def create_widgets(self):
        # Input section
        self.text_input = self.create_input_section("Enter Text:")

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Convert button
        convert_btn = ttk.Button(button_frame, text="Convert to Morse",
                                 command=self.convert_text_to_morse)
        convert_btn.pack(side=tk.LEFT, padx=5)

        # Play sound button
        play_btn = ttk.Button(button_frame, text="Play Sound",
                              command=self.play_morse_sound)
        play_btn.pack(side=tk.LEFT, padx=5)

        # Output section
        self.morse_output = self.create_output_section("Morse Code:")

        # Copy button
        self.create_button("Copy to Clipboard", self.copy_morse)

    def convert_text_to_morse(self):
        text = self.text_input.get("1.0", tk.END).strip().upper()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to convert")
            return

        morse_result = MorseTranslator.text_to_morse(text)
        self.update_output(self.morse_output, morse_result)

    def play_morse_sound(self):
        morse_code = self.morse_output.get("1.0", tk.END).strip()
        if not morse_code:
            messagebox.showwarning("Warning", "No Morse code to play")
            return
        MorsePlayer.play_morse_code(morse_code)

    def copy_morse(self):
        morse_code = self.morse_output.get("1.0", tk.END).strip()
        if morse_code:
            self.clipboard_clear()
            self.clipboard_append(morse_code)
            messagebox.showinfo("Copied", "Morse code copied to clipboard")

    def update_output(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)