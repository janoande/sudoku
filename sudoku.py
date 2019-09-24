import numpy as np
import copy

EMPTY = 0


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
    return not np.isin(0, sudoku) \
        and valid_rows(sudoku) \
        and valid_rows(sudoku.T) \
        and valid_blocks(sudoku)


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


def find_empty_cells(board):
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


def search(board, empty_cells):
    if len(empty_cells) == 0:
        return True
    min_cell, min_nums = min(empty_cells.items(), key=lambda x: len(x[1]))
    for num in min_nums:
        board[min_cell] = num
        # need to store copy of empty_cells state in case of backtrack
        orig_empty_cells = copy.deepcopy(empty_cells)
        update_empty_cells(board, min_cell, num, empty_cells)
        empty_cells.pop(min_cell)
        if search(board, empty_cells):
            return True
        empty_cells = orig_empty_cells
        board[min_cell] = 0
    return False


def solve(board):
    assert search(board, find_empty_cells(board)), \
           f"failed to solve puzzle\n{board}"
    return board
