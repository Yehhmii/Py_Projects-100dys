import tkinter as tk
from tkinter import scrolledtext, messagebox
import random, time
from components.passages import SAMPLES
from components.test_logic import calculate_wpm, calculate_accuracy
from components.highscore import save_score, load_scores
from components.stats import plot_stats
from components.sound import play_start, play_end, play_key
from components.theme import LIGHT, DARK

class TypingTestUI:
    def __init__(self, root):
        self.root = root
        self.root.title('HitHub Typing Test')
        self.theme = LIGHT
        self.sample_text = ''
        self.mode = 'Completion'
        self.difficulty = 'Easy'
        self.start_time = None
        self.end_time = None
        self.timer_id = None
        self.target_time = None
        self._build_ui()

    def _build_ui(self):
        self.root.configure(bg=self.theme['bg'])
        # Controls frame
        ctrl = tk.Frame(self.root, bg=self.theme['bg'])
        ctrl.pack(pady=5)
        # Difficulty
        tk.Label(ctrl, text='Difficulty:', bg=self.theme['bg'], fg=self.theme['fg']).grid(row=0, column=0)
        self.diff_var = tk.StringVar(value='Easy')
        tk.OptionMenu(ctrl, self.diff_var, *SAMPLES.keys()).grid(row=0, column=1)
        # Mode
        tk.Label(ctrl, text='Mode:', bg=self.theme['bg'], fg=self.theme['fg']).grid(row=0, column=2)
        self.mode_var = tk.StringVar(value='Completion')
        tk.OptionMenu(ctrl, self.mode_var, 'Completion', 'Timed (60s)').grid(row=0, column=3)
        # Theme Toggle
        tk.Button(ctrl, text='Toggle Theme', command=self._toggle_theme,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=4, padx=5)
        # Stats Button
        tk.Button(ctrl, text='View Stats', command=plot_stats,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=5, padx=5)

        # Timer display
        self.timer_label = tk.Label(self.root, text='Time: 0s', font=('Arial', 14),
                                    bg=self.theme['bg'], fg=self.theme['fg'])
        self.timer_label.pack()
        # Live accuracy
        self.live_acc = tk.Label(self.root, text='Accuracy: 0%', font=('Arial', 12),
                                 bg=self.theme['bg'], fg=self.theme['fg'])
        self.live_acc.pack(pady=2)

        # Sample text
        self.sample_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=5,
                                                    bg=self.theme['entry_bg'], fg=self.theme['fg'], font=('Arial',12))
        self.sample_box.pack(padx=10, pady=5)
        self.sample_box.configure(state='disabled')

        # Entry box
        self.entry_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=5,
                                                   bg=self.theme['entry_bg'], fg=self.theme['fg'], font=('Arial',12), state='disabled')
        self.entry_box.pack(padx=10, pady=5)
        self.entry_box.bind('<KeyPress>', lambda e: play_key())
        self.entry_box.bind('<KeyRelease>', lambda e: self._update_live())

        # Buttons
        btnf = tk.Frame(self.root, bg=self.theme['bg'])
        btnf.pack(pady=5)
        tk.Button(btnf, text='Start', command=self.start_test,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=0, padx=5)
        tk.Button(btnf, text='End', command=self.end_test,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=1, padx=5)
        tk.Button(btnf, text='Reset', command=self.reset_test,
                  bg=self.theme['btn_bg'], fg=self.theme['btn_fg']).grid(row=0, column=2, padx=5)

    def start_test(self):
        # Initialize test
        play_start()
        self.difficulty = self.diff_var.get()
        self.mode = self.mode_var.get()
        self.sample_text = random.choice(SAMPLES[self.difficulty])
        self.sample_box.configure(state='normal')
        self.sample_box.delete('1.0', tk.END)
        self.sample_box.insert(tk.END, self.sample_text)
        self.sample_box.configure(state='disabled')
        self.entry_box.configure(state='normal')
        self.entry_box.delete('1.0', tk.END)
        self.start_time = time.time()
        self.end_time = None
        # Timed mode setup
        if self.mode.startswith('Timed'):
            self.target_time = int(self.mode.split('(')[1].rstrip('s)'))
            self.root.after(self.target_time * 1000, self.end_test)
        self._update_timer()

    def _update_timer(self):
        if not self.start_time: return
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.timer_id = self.root.after(1000, self._update_timer)

    def _update_live(self):
        typed = self.entry_box.get('1.0', tk.END).strip()
        acc = calculate_accuracy(self.sample_text, typed)
        self.live_acc.config(text=f"Accuracy: {acc:.1f}%")

    def end_test(self):
        if not self.start_time: return
        # stop timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.end_time = time.time()
        typed = self.entry_box.get('1.0', tk.END).strip()
        char_count = len(typed)
        wpm = calculate_wpm(self.start_time, self.end_time, char_count)
        acc = calculate_accuracy(self.sample_text, typed)
        save_score(self.mode, self.difficulty, wpm)
        best = load_scores().get(f"{self.mode}-{self.difficulty}", 0)
        play_end()
        messagebox.showinfo("Results", f"WPM: {wpm:.2f}\nAccuracy: {acc:.2f}%\nBest: {best:.2f} WPM")
        self.start_time = None

    def reset_test(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.start_time = None
        self.timer_label.config(text='Time: 0s')
        self.live_acc.config(text='Accuracy: 0%')
        self.sample_box.configure(state='normal')
        self.sample_box.delete('1.0', tk.END)
        self.sample_box.configure(state='disabled')
        self.entry_box.delete('1.0', tk.END)
        self.entry_box.configure(state='disabled')

    def _toggle_theme(self):
        self.theme = DARK if self.theme == LIGHT else LIGHT
        # rebuild UI
        for w in self.root.winfo_children(): w.destroy()
        self._build_ui()
