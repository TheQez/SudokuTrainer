from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy

class NakedSingle(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        highlightedEntries = [[set() for i in range(0, 9)] for j in range(0, 9)]
        removedEntries = [[set() for i in range(0, 9)] for j in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                if not sudoku.isInLargeMode[i][j] and len(sudoku.entries[i][j]) == 1:
                    newSudoku.isInLargeMode[i][j] = True
                    (element, ) = sudoku.entries[i][j]
                    newSudoku.entries[i][j] = element
                    highlightedEntries[i][j].add(element)
        return newSudoku, highlightedEntries, removedEntries