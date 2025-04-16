import tkinter as tk
from tkinter import messagebox
from components.logic import check_winner, check_draw
from components.ai import get_ai_move
from components.sound import play_click, play_win, play_draw
from components.theme import LIGHT_THEME, DARK_THEME
from components.timer import TurnTimer


class TicTacToeBoard:
    def __init__(self, master):
        self.master = master
        self.theme = LIGHT_THEME  # starting with light theme
        self.is_one_player = True  # one-player mode by default
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.scores = {"X": 0, "O": 0}
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.apply_theme()
        self.timer = TurnTimer(master, 10, self.timer_expired, self.timer_label)
        self.timer.start()

    def create_widgets(self):
        # Create board buttons
        frame = tk.Frame(self.master)
        frame.pack(pady=10)
        for row in range(3):
            for col in range(3):
                btn = tk.Button(frame, text="", font=("Helvetica", 32), width=5, height=2,
                                command=lambda r=row, c=col: self.handle_click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = btn

        # Status label
        self.status = tk.Label(self.master, text="Player X's turn", font=("Helvetica", 18))
        self.status.pack()

        # Timer label
        self.timer_label = tk.Label(self.master, text="", font=("Helvetica", 16))
        self.timer_label.pack(pady=5)

        # Score label
        self.score_label = tk.Label(self.master, text=self.get_score_text(), font=("Helvetica", 14))
        self.score_label.pack(pady=5)

        # Control buttons
        controls = tk.Frame(self.master)
        controls.pack(pady=10)
        self.restart_btn = tk.Button(controls, text="Restart Game", command=self.restart_game)
        self.restart_btn.grid(row=0, column=0, padx=5)
        self.theme_btn = tk.Button(controls, text="Switch Theme", command=self.switch_theme)
        self.theme_btn.grid(row=0, column=1, padx=5)
        self.mode_btn = tk.Button(controls, text="Toggle Mode (1P/2P)", command=self.toggle_mode)
        self.mode_btn.grid(row=0, column=2, padx=5)

    def apply_theme(self):
        # Apply theme colors to master and widgets
        self.master.configure(bg=self.theme["bg"])
        for widget in [self.status, self.score_label, self.restart_btn, self.theme_btn, self.mode_btn,
                       self.timer_label]:
            widget.configure(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        for row in self.buttons:
            for btn in row:
                btn.configure(bg="white", fg=self.theme["btn_fg"])

    def get_score_text(self):
        return f"Score - X: {self.scores['X']} | O: {self.scores['O']}"

    def handle_click(self, row, col):
        if self.board[row][col] != "" or check_winner(self.board):
            return

        self.make_move(row, col)
        # If one-player mode and it's now AI's turn, let AI make a move
        if self.is_one_player and self.current_player == "O":
            self.master.after(500, self.ai_move)

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(
            text=self.current_player,
            fg=(self.theme["x_color"] if self.current_player == "X" else self.theme["o_color"])
        )
        play_click()
        winner = check_winner(self.board)
        if winner:
            # If winner is a list, extract the symbol from one of the winning cells.
            if isinstance(winner, list):
                winning_symbol = self.board[winner[0][0]][winner[0][1]]
            else:
                winning_symbol = winner

            self.end_game(winning_symbol)
        elif check_draw(self.board):
            self.end_game("Draw")
        else:
            self.switch_turn()

    def ai_move(self):
        move = get_ai_move(self.board)
        if move:
            self.make_move(*move)

    def switch_turn(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status.config(text=f"Player {self.current_player}'s turn")
        self.timer.start()

    def timer_expired(self):
        # If timer expires, switch turn automatically
        self.status.config(text="Time up! Switching turn...")
        self.switch_turn()

    def end_game(self, result):
        self.timer.cancel()
        if result == "Draw":
            self.status.config(text="It's a Draw!")
            play_draw()
        else:
            self.status.config(text=f"🎉 Player {result} Wins!")
            play_win()
            self.scores[result] += 1
            self.score_label.config(text=self.get_score_text())
        messagebox.showinfo("Game Over", self.status.cget("text"))

    def restart_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.status.config(text="Player X's turn")
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", bg="white")
        self.timer.start()

    def switch_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        self.apply_theme()

    def toggle_mode(self):
        self.is_one_player = not self.is_one_player
        mode_text = "One Player" if self.is_one_player else "Two Player"
        self.status.config(text=f"Mode switched to: {mode_text}")
        # Optionally restart game after mode change
        self.restart_game()
