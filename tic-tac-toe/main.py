import tkinter as tk
from components.board import TicTacToeBoard


def main():
    root = tk.Tk()
    root.title("Tic Tac Toe - Enhanced")
    TicTacToeBoard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
