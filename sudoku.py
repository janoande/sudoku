import numpy as np
import copy
import random

EMPTY = 0


def valid(sudoku):
    def valid_rows(sudoku):
        for row in sudoku:
            non_zero_row = row[[n > 0 for n in row]]
            if len(set(non_zero_row)) != len(non_zero_row):
                return False
        return True

    def valid_blocks(sudoku):
        for y in range(0, 3):
            for x in range(0, 3):
                block = sudoku[3*x:3*(x+1), 3*y:3*(y+1)].flatten()
                non_zero_block = block[[n > 0 for n in block]]
                if len(set(non_zero_block)) != len(non_zero_block):
                    return False
        return True
    return valid_rows(sudoku) \
        and valid_rows(sudoku.T) \
        and valid_blocks(sudoku)


def complete(sudoku):
    return not np.isin(0, sudoku) and valid(sudoku)


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


# Note: does not guarantee unique solution
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
    if not valid(board):
        raise Exception("This board is invalid and cannot be solved.")
    if not search(board, find_empty_cells(board)):
        raise Exception("Failed to find a solution.")
    return board


def generate(blanks):
    board = np.zeros((9, 9), dtype=int)
    board[0] = list(range(1, 10))
    random.shuffle(board[0])
    # Note: solve will generate the same board for the same initial permutation
    board = solve(board)
    for i in range(blanks):
        board[random.randint(0, 8), random.randint(0, 8)] = 0
    return board
