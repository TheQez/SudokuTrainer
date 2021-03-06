from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy


class TrivialPenciling(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        highlightedEntries = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
        removedEntries = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                if not sudoku.isInLargeMode[i][j]:
                    for num in sudoku.entries[i][j]:
                        if (SudokuTactic.isInRow(sudoku, num, i) or
                                SudokuTactic.isInColumn(sudoku, num, j) or
                                SudokuTactic.isInBox(sudoku, num, i, j)):
                            newSudoku.entries[i][j].remove(num)
                            removedEntries[i][j].add(num)
        explanation = 'Removed all pencilling that shared a box, column or row with the same numbered entry.'
        return newSudoku, highlightedEntries, removedEntries, explanation
