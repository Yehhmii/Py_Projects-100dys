import tkinter as tk
from tkinter import simpledialog

def open_settings(root, config, apply_callback):
    """
    Opens a dialog to set WORK, SHORT_BREAK, LONG_BREAK durations.
    config: dict with keys 'work', 'short', 'long'
    apply_callback: called with updated config when saved
    """
    dialog = tk.Toplevel(root)
    dialog.title('Settings')
    dialog.grab_set()

    tk.Label(dialog, text='Work (min):').grid(row=0, column=0, pady=5, sticky='e')
    e_work = tk.Entry(dialog)
    e_work.insert(0, str(config['work']))
    e_work.grid(row=0, column=1)

    tk.Label(dialog, text='Short Break (min):').grid(row=1, column=0, pady=5, sticky='e')
    e_short = tk.Entry(dialog)
    e_short.insert(0, str(config['short']))
    e_short.grid(row=1, column=1)

    tk.Label(dialog, text='Long Break (min):').grid(row=2, column=0, pady=5, sticky='e')
    e_long = tk.Entry(dialog)
    e_long.insert(0, str(config['long']))
    e_long.grid(row=2, column=1)

    def save():
        try:
            new_conf = {
                'work': int(e_work.get()),
                'short': int(e_short.get()),
                'long': int(e_long.get())
            }
        except ValueError:
            return
        apply_callback(new_conf)
        dialog.destroy()

    tk.Button(dialog, text='Save', command=save).grid(row=3, column=0, columnspan=2, pady=10)
