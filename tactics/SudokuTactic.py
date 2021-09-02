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

    # Checks the number of pencil markings in a row
    @staticmethod
    def numInRow(sudoku, number, row):
        count = 0
        for i in range(0, 9):
            if not sudoku.isInLargeMode[row][i] and number in sudoku.entries[row][i]:
                count += 1
        return count

    @staticmethod
    def numInColumn(sudoku, number, column):
        count = 0
        for i in range(0, 9):
            if not sudoku.isInLargeMode[i][column] and number in sudoku.entries[i][column]:
                count += 1
        return count

    @staticmethod
    def numInBox(sudoku, number, x, y):
        count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if not sudoku.isInLargeMode[x-(x%3)+i][y-(y%3)+j]:
                    if number in sudoku.entries[x-(x%3)+i][y-(y%3)+j]:
                        count += 1
        return count

    @staticmethod
    def isConnected(x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return True

        # If in the same box
        if (x1 // 3 == x2 // 3) and (y1 // 3 == y2 // 3):
            return True

        return False