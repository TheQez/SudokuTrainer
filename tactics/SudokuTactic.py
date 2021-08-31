from abc import ABC, abstractmethod

class SudokuTactic(ABC):

    @abstractmethod
    def apply(self, sudoku):
        pass

    @staticmethod
    def isInRow(sudoku, number, row):
        for i in range(0, 9):
            if sudoku.isInLargeMode[row][i]:
                if sudoku.entries[row][i] == str(number):
                    return True
        return False

    @staticmethod
    def isInColumn(sudoku, number, column):
        for i in range(0, 9):
            if sudoku.isInLargeMode[i][column]:
                if sudoku.entries[i][column] == str(number):
                    return True
        return False

    # Checks if number appears in same box as (x, y)
    @staticmethod
    def isInBox(sudoku, number, x, y):
        for i in range(0, 3):
            for j in range(0, 3):
                if sudoku.isInLargeMode[x-(x%3)+i][y-(y%3)+j]:
                    if sudoku.entries[x-(x%3)+i][y-(y%3)+j] == str(number):
                        return True
        return False
