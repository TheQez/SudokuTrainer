from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy

class TrivialPenciling(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        highlightedEntries = [[set() for i in range(0, 9)] for j in range(0, 9)]
        removedEntries = [[set() for i in range(0, 9)] for j in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                if not sudoku.isInLargeMode[i][j]:
                    for num in sudoku.entries[i][j]:
                        if SudokuTactic.isInRow(sudoku, num, i) or SudokuTactic.isInColumn(sudoku, num, j) or SudokuTactic.isInBox(sudoku, num, i, j):
                            newSudoku.entries[i][j].remove(num)
                            removedEntries[i][j].add(num)
        return newSudoku, highlightedEntries, removedEntries
