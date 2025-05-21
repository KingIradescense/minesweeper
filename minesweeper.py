import random
from collections import deque

# determine difficulty of the game

difficulty = {
    "easy" : (8, 8, 10),
    "medium" : (16, 16, 40),
    "hard" : (15, 15, 100),
    "nightmare" : (20, 20, 200)
}

# generate a board with bombs and hints, takes difficulty as arg. initially generates a blank board until first coord is clicked, then generates around
# to ensure the first click is not a bomb

def generate_board(level):
    w, h, bombs = difficulty[level]

    board = [[0 for _ in range(w)] for _ in range(h)]
    coords = [(i, j) for i in range(w) for j in range(h)]

    #? for testing purposes, a random initial click; bomb cannot be here
    rand_x = random.randint(0, w-1)
    rand_y = random.randint(0, h-1)

    # place bombs

    random.shuffle(coords)

    for _ in range(bombs):
        a, b = coords.pop()
        if (a, b) == (rand_x, rand_y):
            continue
        board[a][b] = -1

        # place hints

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = dx + a, dy + b
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] != -1:
                    board[nx][ny] += 1

    return board

# a little wrapped game logic

def handle_click(i, j, board, puzzle, flag_click):
    # player is trying to flag/unflag a tile. currently false until JS logic exists
    if flag_click:
        return toggle_flag(i, j, puzzle)
    # player marked it, don't let them click it
    if puzzle[i][j] == -1:
        return "flagged"
    # if they click on a bomb
    if board[i][j] == -1:
        return "lose"
    # if the tile is already revealed and is some value other than -1 or -2
    if puzzle[i][j] != -2:
        return "already revealed"
    
    # run flood fill if none of the previous passed
    flood_fill(i, j, board, puzzle)
    return "continue"

# wrapper for toggling flags

def toggle_flag(i, j, puzzle):
    if puzzle[i][j] == -2:
        puzzle[i][j] = -1
        return "flag placed"
    elif puzzle[i][j] == -1:
        puzzle[i][j] == -2
        return "flag removed"
    else:
        return "already revealed"
    


# flood fill; only called if given coord is definitely not a bomb so will not check
# puzzle is the 'current state' where uncovered tiles = 0 thru 8, flagged tiles are -1, unknown/covered tiles are -2
# true solution board is held in board and compred to determine end states
#! uses loops instead of recursion for BFS -> later JS animation

def flood_fill(i, j, board, puzzle):
    to_reveal = []
    queue = deque()
    queue.append((i, j))

    while queue:
        nx, ny = queue.popleft()

        # already revealed
        if puzzle[nx][ny] == -2:
            continue
        # flagged
        if puzzle[nx][ny] == -1:
            continue
    
        # reveal the next tile in queue
        puzzle[nx][ny] = board[nx][ny]
        to_reveal.append((nx, ny))

        # only queue neighbors if the current tile is blank/0
        if board[nx][ny] == 0:
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                cx, cy = nx + dx, ny + dy
                if 0 <= cx < len(board) and 0 <= cy < len(board[0]):
                    if puzzle[cx][cy] == -2:
                        queue.append((cx, cy))
    return to_reveal

def simulate_play(board, level):
    # -2 indicates covered tile. player board begins blank
    # puzzle = [[-2 for _ in range(len(board))] for _ in range(len(board[-2]))]
    # coords = [(i, j) for i in range(len(board)) for j in range(len(board[0]))]

    w, h, bombs = difficulty[level]

    puzzle = [[0 for _ in range(w)] for _ in range(h)]
    puzzle_coords = [(i, j) for i in range(w) for j in range(h)]

    random.shuffle(puzzle_coords)

    # only attempt 1000 times
    for _ in range(1000):
    
        x, y = puzzle_coords.pop()
        action = random.choices([False, True], weights = [0.75, 0.25])[0]

        result = handle_click(x, y, board, puzzle, action)

        if result == "lose":
            print("BOOM!")
            break
        elif result == "already revealed":
            puzzle_coords.append(x, y)
            continue
        elif result == "flagged" or result == "flag placed" or result == "flag removed":
            print_board(puzzle)
            puzzle_coords.append(x, y)
            continue
        else:
            print_board(puzzle)
            continue
    
        if not puzzle_coords:
            break


# print board for testing

def print_board(board):
    for row in board:
        for cell in row:
            print (cell, end = " ")
        print()
    print()

if __name__ == "__main__":
    level = random.choice(list(difficulty.keys()))
    board = generate_board(level)
    print_board(board)
    simulate_play(board, level)