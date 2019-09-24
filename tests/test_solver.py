import unittest
import sudoku
import numpy as np

# easy
puzzle_easy = np.asarray([[4, 1, 0, 2, 7, 0, 8, 0, 5],
                          [0, 8, 5, 1, 4, 6, 0, 9, 7],
                          [0, 7, 0, 5, 8, 0, 0, 4, 0],
                          [9, 2, 7, 4, 5, 1, 3, 8, 6],
                          [5, 3, 8, 6, 9, 7, 4, 1, 2],
                          [1, 6, 4, 3, 2, 8, 7, 5, 9],
                          [8, 5, 2, 7, 0, 4, 9, 0, 0],
                          [0, 9, 0, 8, 0, 2, 5, 7, 4],
                          [7, 4, 0, 9, 6, 5, 0, 2, 8]])

# medium
puzzle_medium = np.asarray([[0, 0, 0, 8, 0, 0, 0, 0, 0],
                            [4, 0, 0, 0, 1, 5, 0, 3, 0],
                            [0, 2, 9, 0, 4, 0, 5, 1, 8],
                            [0, 4, 0, 0, 0, 0, 1, 2, 0],
                            [0, 0, 0, 6, 0, 2, 0, 0, 0],
                            [0, 3, 2, 0, 0, 0, 0, 9, 0],
                            [6, 9, 3, 0, 5, 0, 8, 7, 0],
                            [0, 5, 0, 4, 8, 0, 0, 0, 1],
                            [0, 0, 0, 0, 0, 3, 0, 0, 0]])

# hard
puzzle_hard = np.asarray([[4, 0, 0, 0, 0, 0, 8, 0, 5],
                          [0, 3, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 7, 0, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0, 0, 6, 0],
                          [0, 0, 0, 0, 8, 0, 4, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 6, 0, 3, 0, 7, 0],
                          [5, 0, 0, 2, 0, 0, 0, 0, 0],
                          [1, 0, 4, 0, 0, 0, 0, 0, 0]])


puzzle_easy_solved = np.asarray([[4, 1, 6, 2, 7, 9, 8, 3, 5],
                                 [3, 8, 5, 1, 4, 6, 2, 9, 7],
                                 [2, 7, 9, 5, 8, 3, 6, 4, 1],
                                 [9, 2, 7, 4, 5, 1, 3, 8, 6],
                                 [5, 3, 8, 6, 9, 7, 4, 1, 2],
                                 [1, 6, 4, 3, 2, 8, 7, 5, 9],
                                 [8, 5, 2, 7, 1, 4, 9, 6, 3],
                                 [6, 9, 1, 8, 3, 2, 5, 7, 4],
                                 [7, 4, 3, 9, 6, 5, 1, 2, 8]])

puzzle_easy_non_valid1 = np.asarray([[4, 1, 6, 2, 7, 9, 8, 3, 5],
                                     [3, 8, 5, 1, 4, 6, 2, 9, 7],
                                     [2, 2, 9, 5, 8, 3, 6, 4, 1],
                                     [9, 7, 7, 4, 5, 1, 3, 8, 6],
                                     [5, 3, 8, 6, 9, 7, 4, 1, 2],
                                     [1, 6, 4, 3, 2, 8, 7, 5, 9],
                                     [8, 5, 2, 7, 1, 4, 9, 6, 3],
                                     [6, 9, 1, 8, 3, 2, 5, 7, 4],
                                     [7, 4, 3, 9, 6, 5, 1, 2, 8]])

puzzle_easy_non_valid2 = np.asarray([[4, 1, 6, 2, 7, 9, 8, 3, 5],
                                     [3, 8, 5, 1, 4, 6, 2, 9, 7],
                                     [2, 7, 9, 5, 8, 3, 6, 4, 1],
                                     [9, 2, 7, 4, 5, 1, 3, 8, 6],
                                     [5, 3, 8, 6, 0, 7, 4, 1, 2],
                                     [1, 6, 4, 3, 2, 8, 7, 5, 9],
                                     [8, 5, 2, 7, 1, 4, 9, 6, 3],
                                     [6, 9, 1, 8, 3, 2, 5, 7, 4],
                                     [7, 4, 3, 9, 6, 5, 1, 2, 8]])


class TestSolver(unittest.TestCase):

    def test_validate(self):
        self.assertTrue(sudoku.validate(puzzle_easy_solved))
        self.assertFalse(sudoku.validate(puzzle_easy_non_valid1))
        self.assertFalse(sudoku.validate(puzzle_easy_non_valid2))

    def test_find_empty(self):
        puzzle1_empty = {(0, 2): {9, 3, 6}, (0, 5): {9, 3}, (0, 7): {3, 6}, (1, 0): {2, 3}, (1, 6): {2}, (2, 0): {2, 3, 6}, (2, 2): {9, 3, 6}, (2, 5): {9, 3}, (2, 6): {1, 2, 6}, (2, 8): {1, 3}, (6, 4): {1, 3}, (6, 7): {3, 6}, (6, 8): {1, 3}, (7, 0): {3, 6}, (7, 2): {1, 3, 6}, (7, 4): {1, 3}, (8, 2): {1, 3}, (8, 6): {1}}
        self.assertEqual(sudoku.find_empty_cells(puzzle_easy), puzzle1_empty)

    def test_easy_solve(self):
        self.assertTrue(sudoku.validate(sudoku.solve(puzzle_easy.copy())))

    def test_medium_solve(self):
        self.assertTrue(sudoku.validate(sudoku.solve(puzzle_medium.copy())))

    def test_hard_solve(self):
        self.assertTrue(sudoku.validate(sudoku.solve(puzzle_hard.copy())))


if __name__ == '__main__':
    unittest.main()
