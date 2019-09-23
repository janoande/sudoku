from curses import wrapper
import curses
import sudoku
import numpy as np


BOARD_SIZE = 9*2 + 1 + 2*2  # 9 cells + spaces + 3 separators (+1 space)


def intchar(int):
    return chr(ord('0') + int)


def draw_board(board, screen, cur_pos):
    screen.move(0, 0)
    for i, row in enumerate(board):
        if max(1, i) % 3 == 0:
            screen.addstr("+".join(["-"*9]*3) + '\n')
        rowstr = np.vectorize(lambda x: f" {x if x != 0 else '.'} ")(row)
        if i == cur_pos[0]:
            rowstr[cur_pos[1]] = f">{rowstr[cur_pos[1]][1]}<"
        rowstr = ''.join(np.insert(rowstr,
                                   range(3, len(rowstr), 3),
                                   '|')) + '\n'
        screen.addstr(rowstr)


def loop(screen, board):
    cur_pos = [0, 0]
    while True:
        draw_board(board, screen, cur_pos)
        screen.refresh()
        key = screen.getkey()
        if key == 'q':
            break
        if key == 'S':
            board = sudoku.solve(board)
        # TODO: skip non-empty spots when moving
        if key == 'h':
            cur_pos[1] = max(0, cur_pos[1] - 1)
        if key == 't':
            cur_pos[0] = min(8, cur_pos[0] + 1)
        if key == 'n':
            cur_pos[0] = max(0, cur_pos[0] - 1)
        if key == 's':
            cur_pos[1] = min(8, cur_pos[1] + 1)
        if key.isdigit():
            # TODO: check for valid number
            board[tuple(cur_pos)] = key


def init(stdscr):
    stdscr.clear()
    sudokuwin = curses.newwin(BOARD_SIZE*2, BOARD_SIZE*2,
                              (curses.LINES - BOARD_SIZE)//2,
                              (curses.COLS - BOARD_SIZE)//2)
    # sudokuwin.border()
    curses.curs_set(0)  # hide cursor
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    stdscr.addstr("Sudoku ~ "
                  "move: [h,t,n,s]  "
                  "select number: [1-9]  "
                  "clear: 0   "
                  "solve: [S]  "
                  "new: [N]  "
                  "quit: [q]")
    stdscr.refresh()
    return sudokuwin


def main(stdscr):
    puzzle = sudoku.puzzle1
    sudokuwin = init(stdscr)
    loop(sudokuwin, puzzle)


wrapper(main)
