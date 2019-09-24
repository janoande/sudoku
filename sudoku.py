import numpy as np
import copy

EMPTY = 0

# puzzles for testing purposes
# easy
puzzle1 = np.asarray([[4, 1, 0, 2, 7, 0, 8, 0, 5],
                      [0, 8, 5, 1, 4, 6, 0, 9, 7],
                      [0, 7, 0, 5, 8, 0, 0, 4, 0],
                      [9, 2, 7, 4, 5, 1, 3, 8, 6],
                      [5, 3, 8, 6, 9, 7, 4, 1, 2],
                      [1, 6, 4, 3, 2, 8, 7, 5, 9],
                      [8, 5, 2, 7, 0, 4, 9, 0, 0],
                      [0, 9, 0, 8, 0, 2, 5, 7, 4],
                      [7, 4, 0, 9, 6, 5, 0, 2, 8]])

# medium
puzzle2 = np.asarray([[0, 0, 0, 8, 0, 0, 0, 0, 0],
                      [4, 0, 0, 0, 1, 5, 0, 3, 0],
                      [0, 2, 9, 0, 4, 0, 5, 1, 8],
                      [0, 4, 0, 0, 0, 0, 1, 2, 0],
                      [0, 0, 0, 6, 0, 2, 0, 0, 0],
                      [0, 3, 2, 0, 0, 0, 0, 9, 0],
                      [6, 9, 3, 0, 5, 0, 8, 7, 0],
                      [0, 5, 0, 4, 8, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 3, 0, 0, 0]])

# hard
puzzle3 = np.asarray([[4, 0, 0, 0, 0, 0, 8, 0, 5],
                      [0, 3, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 7, 0, 0, 0, 0, 0],
                      [0, 2, 0, 0, 0, 0, 0, 6, 0],
                      [0, 0, 0, 0, 8, 0, 4, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 6, 0, 3, 0, 7, 0],
                      [5, 0, 0, 2, 0, 0, 0, 0, 0],
                      [1, 0, 4, 0, 0, 0, 0, 0, 0]])


def validate(sudoku):
    def valid_rows(sudoku):
        return all([set(row) == set(range(1, 10)) for row in sudoku])

    def valid_blocks(sudoku):
        for y in range(0, 3):
            for x in range(0, 3):
                block = sudoku[3*x:3*(x+1), 3*y:3*(y+1)]
                if set(block.flatten()) != set(range(1, 10)):
                    return False
        return True

    sudoku = np.asarray(sudoku)
    return not np.isin(0, sudoku) and valid_rows(sudoku) and valid_rows(sudoku.T) and valid_blocks(sudoku)


# update possible values in empty cells
def update_empty_cells(board, cell, value, empty_cells):
    for i in range(9):
        # update row
        if board[cell[0], i] == EMPTY:
            empty_cells[(cell[0], i)].discard(value)
        # update col
        if board[i, cell[1]] == EMPTY:
            empty_cells[(i, cell[1])].discard(value)
    # update block
    for blockx in [cell[0]//3 * 3 + x for x in range(3)]:
        for blocky in [cell[1]//3 * 3 + y for y in range(3)]:
            if board[blockx, blocky] == EMPTY:
                empty_cells[(blockx, blocky)].discard(value)


def find_empty(board):
    empty_cells = {}
    for i in range(9):
        available_row_nums = set(range(10)) - set(board[i])
        for j in range(9):
            if board[i, j] == EMPTY:
                block_nums = set(board[i//3 * 3:(i+3)//3 * 3,
                                       j//3 * 3:(j+3)//3 * 3].flatten())
                column_nums = set(board[:, j])
                available_nums = available_row_nums - column_nums - block_nums
                empty_cells[(i, j)] = available_nums
    return empty_cells


def solve_trivial(board, empty_cells):
    updated = True
    while updated:
        updated = False
        for cell, nums in empty_cells.copy().items():
            if len(nums) == 1:
                updated = True
                single_avail_num = tuple(nums)[0]
                board[cell] = single_avail_num
                update_empty_cells(board, cell, single_avail_num, empty_cells)
                empty_cells.pop(cell)


def search(board, empty_cells):
    if len(empty_cells) == 0:
        print("Success!")
        return True
    min_cell, min_nums = min(empty_cells.items(), key=lambda x: len(x[1]))
    # print(f"Search on cell {min_cell}, with nums {min_nums}")
    for num in min_nums:
        # print(f"Now trying {num}")
        board[min_cell] = num
        # need to store copy of empty_cells
        orig_empty_cells = copy.deepcopy(empty_cells)
        update_empty_cells(board, min_cell, num, empty_cells)
        empty_cells.pop(min_cell)
        if search(board, empty_cells):
            return True
        # undo
        empty_cells = orig_empty_cells
        board[min_cell] = 0
    return False


def solve(board):
    # Pass 1:
    # - precompute the availabre numbers for each empty cell
    # - store empty arary positions (tuple) in hash-table
    empty_cells = find_empty(board)

    # Pass 2:
    # Fill in as many of the cells who have only 1 number of choices
    # Repeat until no more trivial cell values remains
    solve_trivial(board, empty_cells)

    # Pass 3:
    # trial-and-error -> backtrack
    search(board, empty_cells)

    return board


solve(puzzle3)
