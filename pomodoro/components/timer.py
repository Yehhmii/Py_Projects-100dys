import tkinter as tk
from tkinter import ttk
import math
from components.sound import play_check, play_break


class PomodoroTimer:
    def __init__(self, root, update_ui, config):
        self.root = root
        self.update_ui = update_ui
        self.config = config
        self.reps = 0
        self._timer_id = None
        self.remaining = 0
        self.paused = False

    def start(self):
        self.reps += 1
        w, s, l = self.config['work'], self.config['short'], self.config['long']
        if self.reps % 4 == 0:
            self._count_down(l * 60)
            play_break()
        elif self.reps % 2 == 0:
            self._count_down(s * 60)
            play_break()
        else:
            self._count_down(w * 60)
        self.paused = False

    def pause(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
            self.paused = True

    def resume(self):
        if self.paused:
            self._count_down(self.remaining)
            self.paused = False

    def reset(self):
        if self._timer_id:
            self.root.after_cancel(self._timer_id)
        self.reps = 0
        self.remaining = 0
        self.paused = False

    def _count_down(self, count):
        self.remaining = count
        mins = math.floor(count/60)
        secs = count % 60
        self.update_ui(mins, secs, count)
        if count > 0:
            self._timer_id = self.root.after(1000, self._count_down, count-1)
        else:
            play_check()
            self.start()
