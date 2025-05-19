import random

# determine difficulty of the game

difficult = {
    "easy" = (8, 8, 10),
    "medium" = (16, 16, 40),
    "hard" = (15, 15, 100),
    "nightmare" = (20, 20, 200)
}

# generate a board with bombs and hints, takes difficulty as arg

def generate_board(level):
    w, h, bombs = difficulty[level]

    board = [[0 in _ for range(w)] for _ in range(h)]
    coords = [(i, j) for i in range(w) for j in range(h)]

    # place bombs

    random.shuffle(coords)

    for bomb in bombs:
        a, b = coords.pop()
        board[a][b] = -1

        # place hints

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = dx + a, dy + b
                if 0 <= nx < len(board) and 0 <= ny len(board[0]) and board[nx][ny] != -1:
                    board[nx][ny] += 1

    return board
        