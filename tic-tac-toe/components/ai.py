import random

def get_ai_move(board):
    """
    Choose a random empty cell from the board.
    board: 2D list (3x3), where each cell is 'X', 'O', or ''.
    Returns a tuple (row, col) for AI's move.
    """
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if empty_cells:
        return random.choice(empty_cells)
    return None
