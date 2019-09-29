import curses
import sudoku
import numpy as np
import textwrap


BOARD_WIDTH = 9*3 + 2  # 9 cells (+2 spaces) + 2 separators + newline
BOARD_HEIGHT = 9 + 3  # 9 cells + separators


def infowrite(win, text):
    win.clear()
    for n, line in enumerate(textwrap.wrap(text, width=BOARD_WIDTH)):
        win.addstr(n, 1, line)
    win.refresh()


def query(infowin, question, options):
    options_str = [f"{i}. {opt}"
                   for i, opt in enumerate(options.keys(), start=1)]
    infowin.clear()
    infowin.addstr(0, 1, question)
    for n, optstr in enumerate(options_str, start=1):
        infowin.addstr(n, 1, optstr)
    infowin.refresh()
    while True:
        key = infowin.getkey()
        if key == 'q':
            return None
        if not key.isdigit():
            continue
        key = int(key)
        if key > 0 and key <= len(options):
            return [optval
                    for i, optval in enumerate(options.values(), start=1)
                    if i == key][0]


def intchar(int):
    return chr(ord('0') + int)


def draw_board(board, screen, cur_pos):
    screen.move(0, 0)
    for i, row in enumerate(board):
        if max(1, i) % 3 == 0:
            screen.addstr("+".join(["-"*9]*3))
        rowstr = np.vectorize(lambda x: f" {x if x != 0 else '.'} ")(row)
        if i == cur_pos[0]:
            rowstr[cur_pos[1]] = f">{rowstr[cur_pos[1]][1]}<"
        rowstr = ''.join(np.insert(rowstr,
                                   range(3, len(rowstr), 3),
                                   '|'))
        screen.addstr(rowstr)


def loop(boardwin, infowin, board):
    cur_pos = [0, 0]
    infowrite(infowin, "Welcome! Hit [N]ew to generate a sudoku board.")
    while True:
        draw_board(board, boardwin, cur_pos)
        if sudoku.complete(board):
            infowrite(infowin, "Puzzle solved!")
        boardwin.refresh()
        key = boardwin.getkey()
        infowin.clear()
        infowin.refresh()
        if key == 'q':
            break
        if key == 'S':
            try:
                board = sudoku.solve(board)
            except Exception as err:
                infowrite(infowin, str(err))
        if key == 'N':
            difficulty = query(infowin, "Select difficulty", {"Easy": 25, "Medium": 40, "Hard": 60})
            if difficulty:
                board = sudoku.generate(difficulty)
            infowin.clear()
            infowin.refresh()
        if key == 'h':
            cur_pos[1] = max(0, cur_pos[1] - 1)
        if key == 't':
            cur_pos[0] = min(8, cur_pos[0] + 1)
        if key == 'n':
            cur_pos[0] = max(0, cur_pos[0] - 1)
        if key == 's':
            cur_pos[1] = min(8, cur_pos[1] + 1)
        if key.isdigit():
            board[tuple(cur_pos)] = key


def init(stdscr):
    stdscr.clear()
    sudokuwin = curses.newwin(BOARD_HEIGHT, BOARD_WIDTH,
                              (curses.LINES - BOARD_HEIGHT)//2,
                              (curses.COLS - BOARD_WIDTH)//2)
    # sudokuwin.border()
    infowin = curses.newwin(BOARD_HEIGHT, BOARD_WIDTH,
                            (curses.LINES - BOARD_HEIGHT)//2 + BOARD_HEIGHT,
                            (curses.COLS - BOARD_WIDTH)//2)
    curses.curs_set(0)  # hide cursor
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_BLUE, -1)
    stdscr.addstr("Sudoku ~ "
                  "Move: [h,t,n,s]  "
                  "Select number: [1-9]  "
                  "Clear: [0]  "
                  "Solve: [S]  "
                  "New: [N]  "
                  "Quit: [q]", curses.color_pair(2))
    stdscr.refresh()
    sudokuwin.refresh()
    return sudokuwin, infowin


def main(stdscr):
    empty_board = np.zeros((9, 9), dtype=int)
    boardwin, infowin = init(stdscr)
    loop(boardwin, infowin, empty_board)


curses.wrapper(main)
