from tactics.SudokuTactic import SudokuTactic
from copy import deepcopy
from itertools import product


class NakedDouble(SudokuTactic):
    def apply(self, sudoku):
        newSudoku = deepcopy(sudoku)
        highlightedEntries = [[set() for _ in range(0, 9)] for _ in range(0, 9)]
        removedEntries = [[set() for _ in range(0, 9)] for _ in range(0, 9)]

        for x1, y1, x2, y2 in product(range(0, 9), range(0, 9), range(0, 9), range(0, 9)):
            if NakedDouble.isTacticViable(sudoku, x1, y1, x2, y2):
                tacticWorked = False
                elements = list(sudoku.entries[x1][y1])
                if (x1 == x2 and ((SudokuTactic.numInRow(sudoku, elements[0], x1) > 2) or
                                  (SudokuTactic.numInRow(sudoku, elements[1], x1) > 2))):
                    tacticWorked = True
                    for i in range(0, 9):
                        if not sudoku.isInLargeMode[x1][i] and i != y1 and i != y2:
                            if elements[0] in newSudoku.entries[x1][i]:
                                newSudoku.entries[x1][i].remove(elements[0])
                                removedEntries[x1][i].add(elements[0])
                            if elements[1] in newSudoku.entries[x1][i]:
                                newSudoku.entries[x1][i].remove(elements[1])
                                removedEntries[x1][i].add(elements[1])

                if (y1 == y2 and ((SudokuTactic.numInColumn(sudoku, elements[0], y1) > 2) or
                                  (SudokuTactic.numInColumn(sudoku, elements[1], y1) > 2))):
                    tacticWorked = True
                    for i in range(0, 9):
                        if not sudoku.isInLargeMode[i][y1] and i != x1 and i != x2:
                            if elements[0] in newSudoku.entries[i][y1]:
                                newSudoku.entries[i][y1].remove(elements[0])
                                removedEntries[i][y1].add(elements[0])
                            if elements[1] in newSudoku.entries[i][y1]:
                                newSudoku.entries[i][y1].remove(elements[1])
                                removedEntries[i][y1].add(elements[1])

                if (x1 // 3 == x2 // 3) and (y1 // 3 == y2 // 3):
                    if ((SudokuTactic.numInBox(sudoku, elements[0], x1, y1) > 2) or
                            (SudokuTactic.numInBox(sudoku, elements[1], x1, y1) > 2)):
                        tacticWorked = True
                        for i, j in product(range(0, 3), range(0, 3)):
                            x = (x1 // 3)*3 + i
                            y = (y1 // 3)*3 + j
                            if not sudoku.isInLargeMode[x][y] and (x, y) != (x1, y1) and (x, y) != (x2, y2):
                                if elements[0] in newSudoku.entries[x][y]:
                                    newSudoku.entries[x][y].remove(elements[0])
                                    removedEntries[x][y].add(elements[0])
                                if elements[1] in newSudoku.entries[x][y]:
                                    newSudoku.entries[x][y].remove(elements[1])
                                    removedEntries[x][y].add(elements[1])

                if tacticWorked:
                    highlightedEntries[x1][y1].add(elements[0])
                    highlightedEntries[x1][y1].add(elements[1])
                    highlightedEntries[x2][y2].add(elements[0])
                    highlightedEntries[x2][y2].add(elements[1])
                    explanation = 'Cells (' + str(x1) + ', ' + str(y1) + ') and (' + str(x2) + ', ' + str(y2) + ') '
                    explanation += 'both contain only ' + str(elements[0]) + ' and ' + str(elements[1]) + ' and see each other'
                    explanation += ', so any ' + str(elements[0]) + ' or ' + str(elements[1])
                    explanation += ' entries sharing a row, column or box with both can be removed.'
                    return newSudoku, highlightedEntries, removedEntries, explanation
        return sudoku, highlightedEntries, removedEntries, ''

    @staticmethod
    def isTacticViable(sudoku, x1, y1, x2, y2):
        if (x1 != x2) or (y1 != y2):
            if SudokuTactic.isConnected(x1, y1, x2, y2):
                if not sudoku.isInLargeMode[x1][y1] and not sudoku.isInLargeMode[x2][y2]:
                    if (len(sudoku.entries[x1][y1]) == 2 and len(sudoku.entries[x2][y2]) == 2 and
                            set(sudoku.entries[x1][y1]) == set(sudoku.entries[x2][y2])):
                        return True
        return False
