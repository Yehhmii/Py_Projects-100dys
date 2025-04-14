from gui_components import ConversionTab
from morse_core import MorseTranslator
import tkinter.messagebox as messagebox
import tkinter as tk


class MorseToTextTab(ConversionTab):
    def create_widgets(self):
        # Input section
        self.morse_input = self.create_input_section("Enter Morse Code:")

        # Convert button
        self.create_button("Convert to Text", self.convert_morse_to_text)

        # Output section
        self.text_output = self.create_output_section("Decoded Text:")

        # Copy button
        self.create_button("Copy to Clipboard", self.copy_text)

    def convert_morse_to_text(self):
        morse_code = self.morse_input.get("1.0", tk.END).strip()
        if not morse_code:
            messagebox.showwarning("Warning", "Please enter Morse code to convert")
            return

        decoded_text = MorseTranslator.morse_to_text(morse_code)
        self.update_output(self.text_output, decoded_text)

    def copy_text(self):
        text = self.text_output.get("1.0", tk.END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copied", "Text copied to clipboard")

    def update_output(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)