from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy

class HiddenSingle(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        for i in range(0, 9):
            for j in range(0, 9):
                if not sudoku.isInLargeMode[i][j]:
                    for num in sudoku.entries[i][j]:
                        if SudokuTactic.numInRow(sudoku, num, i) == 1 or SudokuTactic.numInColumn(sudoku, num, j) == 1 or SudokuTactic.numInBox(sudoku, num, i, j) == 1:
                            newSudoku.isInLargeMode[i][j] = True
                            newSudoku.entries[i][j] = str(num)
                            break
        return newSudoku


