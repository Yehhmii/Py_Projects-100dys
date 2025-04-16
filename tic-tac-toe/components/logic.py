def check_winner(board):
    # Rows, columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return [(i, 0), (i, 1), (i, 2)]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return [(0, i), (1, i), (2, i)]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return [(0, 2), (1, 1), (2, 0)]

    return None


def check_draw(board):
    return all(cell != "" for row in board for cell in row)
