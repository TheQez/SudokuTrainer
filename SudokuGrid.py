from itertools import product
import copy
import random
from typing import List, Union, Set

from tactics.TrivialPenciling import TrivialPenciling
from tactics.NakedSingle import NakedSingle
from tactics.HiddenSingle import HiddenSingle
from tactics.NakedDouble import NakedDouble


class SudokuGrid:
    def __init__(self, initState: List[List[Union[None, int, Set[int]]]] = [[None for _ in range(0, 9)] for _ in range(0, 9)]):
        self.tactics = []
        self.tactics.append(TrivialPenciling())
        self.tactics.append(NakedSingle())
        self.tactics.append(HiddenSingle())
        self.tactics.append(NakedDouble())
        self.entries = initState
        self.isInLargeMode = [[True for _ in range(0, 9)] for _ in range(0, 9)]

    # Does not check pencil markings
    def isNoDuplicates(self):
        # Rows
        for i in range(0, 9):
            row = []
            for j in range(0, 9):
                if self.isInLargeMode[i][j]:
                    if self.entries[i][j] in range(1, 10):
                        row.append(self.entries[i][j])
            if len(row) != len(set(row)):
                return False

        # Column
        for i in range(0, 9):
            column = []
            for j in range(0, 9):
                if self.isInLargeMode[j][i]:
                    if self.entries[j][i] in range(1, 10):
                        column.append(self.entries[j][i])
            if len(column) != len(set(column)):
                return False

        # Boxes
        for x1 in range(0, 3):
            for y1 in range(0, 3):
                box = []
                for x2 in range(0, 3):
                    for y2 in range(0, 3):
                        if self.isInLargeMode[3 * x1 + x2][3 * y1 + y2]:
                            if self.entries[3 * x1 + x2][3 * y1 + y2] in range(1, 10):
                                box.append(self.entries[3 * x1 + x2][3 * y1 + y2])
                if len(box) != len(set(box)):
                    return False

        return True

    def solutions(self, solutionsCutoff: int = 10, randomised: bool = False) -> List['SudokuGrid']:
        currentSudoku = copy.deepcopy(self)
        while True:
            if not currentSudoku.isNoDuplicates():
                return []
            nextSudoku = currentSudoku.getTactic()[0]
            if ((nextSudoku.isInLargeMode == currentSudoku.isInLargeMode) and
                    (nextSudoku.entries == currentSudoku.entries)):
                break
            currentSudoku = nextSudoku
        return currentSudoku.bruteForce(solutionsCutoff=solutionsCutoff, randomised=randomised)

    def bruteForce(self, solutionsCutoff: int = 10, randomised: bool = False) -> List['SudokuGrid']:
        # Find the next cell not filled
        x, y = None, None
        for i, j in product(range(0, 9), range(0, 9)):
            if not self.isInLargeMode[i][j] or self.entries[i][j] not in range(1, 10):
                x, y = i, j
                break

        # Base case, after sudoku completely filled
        if (x, y) == (None, None):
            if self.isNoDuplicates():
                return [self]
            else:
                return []

        if not self.isInLargeMode[x][y]:
            candidates = list(self.entries[x][y])
        else:
            candidates = [n for n in range(1, 10)]

        if randomised:
            random.shuffle(candidates)

        solutions = []
        for candidate in candidates:
            nextSudoku = copy.deepcopy(self)
            nextSudoku.isInLargeMode[x][y] = True
            nextSudoku.entries[x][y] = candidate
            if nextSudoku.isNoDuplicates():
                solutions += nextSudoku.bruteForce(solutionsCutoff=solutionsCutoff, randomised=randomised)
            if len(solutions) >= solutionsCutoff:
                break

        return solutions

    def addPenciling(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if ((self.isInLargeMode[i][j] and self.entries[i][j] not in range(1, 10)) or
                        (not self.isInLargeMode[i][j] and len(self.entries[i][j]) == 0)):
                    self.isInLargeMode[i][j] = False
                    self.entries[i][j] = set([n for n in range(1, 10)])

    def getTactic(self):
        self.addPenciling()
        for tactic in self.tactics:
            newSudoku, highlightedEntries, removedEntries = tactic.apply(self)
            if newSudoku.entries != self.entries:
                #print(tactic.__class__.__name__)
                return newSudoku, highlightedEntries, removedEntries, tactic.__class__
        return self, set(), set(), None

    def isValid(self):
        sols = self.solutions()
        if len(sols) == 1:
            return True
        else:
            return False

    def isSolved(self):
        for i, j in product(range(0, 9), range(0, 9)):
            if not self.isInLargeMode[i][j] or self.entries[i][j] not in range(1, 10):
                return False
        if not self.isNoDuplicates():
            return False
        return True
