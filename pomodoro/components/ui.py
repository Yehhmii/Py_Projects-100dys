import tkinter as tk
from tkinter import ttk, PhotoImage
import sys, os
from components.theme import LIGHT, DARK
from components.settings import open_settings
from components.timer import PomodoroTimer
from components.sound import _resource_path

class PomodoroUI:
    def __init__(self, root):
        self.root = root
        self.root.title('HitHub Pomodoro')
        self.config = {'work': 25, 'short': 5, 'long': 15}
        self.theme = LIGHT
        # Instantiate timer before building UI
        self.timer = PomodoroTimer(root, self._update_timer, self.config)
        self._build()

    def _build(self):
        self.root.configure(bg=self.theme['bg'])
        top = tk.Frame(self.root, bg=self.theme['bg'])
        top.pack(pady=10)

        self.label = tk.Label(top, text='Timer', font=('Courier', 36),
                              bg=self.theme['bg'], fg=self.theme['fg'])
        self.label.pack()

        mid = tk.Frame(self.root, bg=self.theme['bg'])
        mid.pack(pady=10)
        self.canvas = tk.Canvas(mid, width=500, height=224,
                                bg=self.theme['bg'], highlightthickness=0)
        self.canvas.pack()
        # Add tomato background image
        img_path = _resource_path(os.path.join('assets', 'tomato.png'))
        self.bg_img = PhotoImage(file=img_path)
        self.canvas.create_image(250, 112, image=self.bg_img)
        # Timer text on top
        self.timer_text = self.canvas.create_text(250, 130, text='00:00',
                                                  fill=self.theme['fg'], font=('Courier', 32, 'bold'))

        self.progress = ttk.Progressbar(self.root, length=200, mode='determinate')
        self.progress.pack(pady=5)

        # Checkmarks Label to indicate sessions completed
        self.check_marks = tk.Label(self.root, text="", font=('Courier', 20),
                                    bg=self.theme['bg'], fg=self.theme['fg'])
        self.check_marks.pack(pady=5)  # CHANGED: Added checkmarks display

        bot = tk.Frame(self.root, bg=self.theme['bg'])
        bot.pack(pady=10)
        self.btn_start = tk.Button(bot, text='Start', command=self.timer.start,
                                   bg=self.theme['btn_bg'], fg=self.theme['btn_fg'])
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(bot, text='Pause', command=self._toggle_pause,
                                   bg=self.theme['btn_bg'], fg=self.theme['btn_fg'])
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(bot, text='Reset', command=self.timer.reset,
                                   bg=self.theme['btn_bg'], fg=self.theme['btn_fg'])
        self.btn_reset.grid(row=0, column=2, padx=5)

        opt = tk.Frame(self.root, bg=self.theme['bg'])
        opt.pack(pady=10)
        tk.Button(opt, text='Settings', command=lambda: open_settings(self.root, self.config, self._apply_settings),
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=0, padx=5)
        tk.Button(opt, text='Toggle Theme', command=self._toggle_theme,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=1, padx=5)

    def _update_timer(self, mins, secs, total):
        # Update label text based on session type
        if self.timer.reps % 2 == 0:
            self.label.config(text='Break')  # CHANGED
        else:
            self.label.config(text='Work')   # CHANGED

        text = f"{mins:02d}:{secs:02d}"
        self.canvas.itemconfig(self.timer_text, text=text, fill=self.theme['fg'])

        # update progress
        session_length = (
            self.config['work']*60 if self.timer.reps % 2 != 0 else
            self.config['short']*60 if self.timer.reps % 4 == 0 else
            self.config['long']*60
        )
        percent = ((session_length - total) / session_length) * 100
        self.progress['value'] = percent

        # Update checkmarks when a cycle completes
        if mins == 0 and secs == 0:
            marks = '✔' * (self.timer.reps // 2)
            self.check_marks.config(text=marks)  # CHANGED

    def _toggle_pause(self):
        if self.timer.paused:
            self.timer.resume()
            self.btn_pause.config(text='Pause')
        else:
            self.timer.pause()
            self.btn_pause.config(text='Resume')

    def _toggle_theme(self):
        self.theme = DARK if self.theme == LIGHT else LIGHT
        self._reapply_theme()

    def _reapply_theme(self):
        for widget in self.root.winfo_children(): widget.destroy()
        # Re-instantiate timer with same state
        self.timer = PomodoroTimer(self.root, self._update_timer, self.config)
        self._build()

    def _apply_settings(self, new_conf):
        self.config.update(new_conf)
        self.timer.reset()
