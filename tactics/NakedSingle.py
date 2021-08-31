from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy

class NakedSingle(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        for i in range(0, 9):
            for j in range(0, 9):
                if not sudoku.isInLargeMode[i][j] and len(sudoku.entries[i][j]) == 1:
                    newSudoku.isInLargeMode[i][j] = True
                    newSudoku.entries[i][j] = str(sudoku.entries[i][j][0])
        return newSudoku