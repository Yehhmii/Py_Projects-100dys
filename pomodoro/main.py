from tkinter import *
import math
import sys
import os
from tkinter import PhotoImage

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 60
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

if getattr(sys, 'frozen', False):
    # Running as a bundled exe
    image_path = os.path.join(sys._MEIPASS, 'bg_hit.png')
else:
    # Running as a normal script
    image_path = 'bg_hit.png'

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 4 == 0:
        count_down(long_break_sec)
        label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("HitHub Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# Label
label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 45))
label.grid(row=0, column=1)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=image_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)


# Button
btn_start = Button(text="Start", padx=20, command=start_timer)
btn_start.grid(row=2, column=0)
# Button2
btn_set = Button(text="Pause", padx=20, command=pause_timer)
btn_set.grid(row=2, column=1)
# Button3
btn_reset = Button(text="Reset", padx=20, command=reset_timer)
btn_reset.grid(row=2, column=2)

# Label✔✔
check_marks = Label( fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
check_marks.grid(row=3, column=1)


window.mainloop()
