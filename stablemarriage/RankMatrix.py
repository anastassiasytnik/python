from typing import *
from copy import deepcopy

TABLE_ZERO_ZERO: Final = "Col headers: "
TABLE_HEADER: Final = "Rank Matrix"

class DeadEndException(RuntimeError):
    def __init__(self, rowLabel, colLabel):
        self.rowLabel = rowLabel
        self.colLabel = colLabel
    def __str__(self):
        return f"Reached dead end trying to match {self.rowLabel} with {self.colLabel}"
    

def fromPreferences(rowLabelLst: list, colLabelLst: list, rowPreferences: dict, colPreferences: dict):
    matrix: dict = {}
    matrix[TABLE_ZERO_ZERO] = colLabelLst[:]
    offsets: dict = {}
    # this will have keys - members of labelLst2 and values - their index in the original provided list
    colIdxLookup = {}
    # this one will be reversed
    colLblLookup = {}
    idx: int = 0
    for label in colLabelLst:
        colIdxLookup[label] = idx
        colLblLookup[idx] = label
        idx += 1
    rowLblLookup = {}
    idx = 0
    for label in rowLabelLst:
        rowLblLookup[idx] = label
        idx += 1

    # now that lookup dicts are there - fill the matrix.
    # fill up preferences1 first
    for rowLabel in rowLabelLst:
        row = [(0, 0)] * len(colLabelLst)
        place = 0
        for colLabel in rowPreferences[rowLabel]:
            colIdx = colIdxLookup[colLabel]
            row[colIdx] = (place, 0)
            place += 1
        matrix[rowLabel] = row
    # now fill out values from preferences2 and group similarly offset relationships
    colIdx = 0
    for colLabel in colLabelLst:
        place = 0
        for rowLabel in colPreferences[colLabel]:
            prevValue: tuple = matrix[rowLabel][colIdx]
            matrix[rowLabel][colIdx] = (prevValue[0], place)
            # fill out offset index
            totalOffset = place + prevValue[0]
            dictPairs = offsets.get(totalOffset, {})
            best = min(prevValue[0], place)
            pairLst = dictPairs.get(best, [])
            pairLst.append((rowLabel, colLabel))
            dictPairs[best] = pairLst
            offsets[totalOffset] = dictPairs
            place += 1
        colIdx += 1
    return RankMatrix(matrix, offsets, rowLblLookup, colLblLookup, colIdxLookup)

class RankMatrix:
    """ 
        This class has following private attributes:
           __colIdxLookup - allows to find the column index in the matrix by the provided label
           __rowLblLookup, __colLblLookup - allows to find the label by the provided index
           __matrix - the ranking matrix.
           __offsets: - lists possible pairs in order of their ranking filed by ranking and min distance from most desired
    """

    def __init__(self, matrix: dict, offset: dict, rowLblLookup: dict, colLblLookup: dict, colIdxLookup: dict):
        self.__matrix = matrix
        self.__offsets = offset
        self.__colIdxLookup = colIdxLookup
        self.__colLblLookup = colLblLookup
        self.__rowLblLookup = rowLblLookup


    def getOffsetIdx(self) -> dict:
        return deepcopy(self.__offsets)
        
    def getTableLines(self) -> list:
        # TODO handle labels of different lengths (for real names)
        # calculate length of col headers row and regular matrix row
        # pick bigger of the above and the TABLE_HEADER line to be the width of the table
        # to which we pad all the rows for nice representation.
        colLblLen = len(self.__colLblLookup[0])
        rowLblLen = len(self.__rowLblLookup[0])
        # separate row headers from values by " | " and values from each other by a single space unless col headers are long
        # value itself will be displayed as (##:##) - 7 characters total
        colCount = len(self.__matrix[TABLE_ZERO_ZERO])
        rowLen = rowLblLen + 3 + colCount * 8
        colHeaderLen = rowLblLen + 3 + (colLblLen + 1) * colCount
        tableHeaderLen = len(TABLE_HEADER)
        lineLen = max(tableHeaderLen, rowLen, colHeaderLen)

        result: list = []
        # Add table header
        outputLn: str = TABLE_HEADER + "\n"
        if tableHeaderLen < lineLen:
            margin = (lineLen - tableHeaderLen) // 2
            outputLn = " " * margin + TABLE_HEADER + " " * (lineLen - tableHeaderLen - margin) + "\n"
        result.append(outputLn)

        # add column headers
        marginL = 0
        marginR = 1
        if colLblLen < 7:
            marginL = (7 - colLblLen) // 2
            marginR = 7 - colLblLen - marginL + 1 # + 1 = space between colheaders
        outputLn = " " * (rowLblLen + 3)
        for colHeader in self.__matrix[TABLE_ZERO_ZERO]:
            outputLn += (" " * marginL) + colHeader + (" " * marginR)
        outputLn += "\n"
        result.append(outputLn);

        # add rows
        marginL = 0
        marginR = 1
        if (7 < colLblLen):
            marginL = (colLblLen - 7) // 2
            marginR = colLblLen - 7 - marginL + 1
        CELL_TEMPLATE = (" " * marginL) + "({}:{})" + (" " * marginR)
        NULL_TEMPLATE = (" " * marginL) + "  NIL  " + (" " * marginR)
        for idx in sorted(self.__rowLblLookup):
            rowHeader = self.__rowLblLookup[idx]
            outputLn = rowHeader + " | "
            for ranks in self.__matrix[rowHeader]:
                if ranks is not None:
                    outputLn += CELL_TEMPLATE.format(
                        (ranks[0] if ranks[0] > 9 else "0" + str(ranks[0])),
                        (ranks[1] if ranks[1] > 9 else "0" + str(ranks[1])))
                else:
                    outputLn += NULL_TEMPLATE
            outputLn  += "\n"
            result.append(outputLn)
        return result

    def getRanks(self, rowLabel, colLabel) -> tuple:
        colIdx = self.__colIdxLookup[colLabel]
        return self.__matrix[rowLabel][colIdx]

    def delete(self, rowLabel, colLabel, rowPref, colPref):
        delColIdx = self.__colIdxLookup[colLabel]
        delRowIdx = list(filter(lambda x: (self.__rowLblLookup[x] == rowLabel), self.__rowLblLookup))[0]
        deletedRank = self.__matrix[rowLabel][delColIdx]
        sureMatch = (0 == deletedRank[0] and 0 == deletedRank[1])
        deletedRow = self.__matrix[rowLabel]

        newRowLblLookup = {}
        for i in range(len(self.__rowLblLookup) - 1):
            if i < delRowIdx:
                newRowLblLookup[i] = self.__rowLblLookup[i]
            elif i >= delRowIdx:
                newRowLblLookup[i] = self.__rowLblLookup[i + 1]

        newColLblLookup = {}
        newColIdxLookup = {}
        for i in range(len(self.__colLblLookup) - 1):
            if i < delColIdx:
                newColLblLookup[i] = self.__colLblLookup[i]
                newColIdxLookup[self.__colLblLookup[i]] = i
            elif i >= delColIdx:
                newColLblLookup[i] = self.__colLblLookup[i + 1]
                newColIdxLookup[self.__colLblLookup[i + 1]] = i
        newColHeaders = self.__matrix[TABLE_ZERO_ZERO][:]
        newColHeaders.remove(colLabel)
        newMatrix = {TABLE_ZERO_ZERO: newColHeaders}
        newOffset = {}
        for curRowLabel, ranks in self.__matrix.items():
            if rowLabel == curRowLabel or curRowLabel == TABLE_ZERO_ZERO:
                continue
            # adjust?
            print("WTF: ", curRowLabel, ranks)
            newRow = []
            colIdx = 0
            delColValue = ranks[delColIdx]
            for rank in ranks:

                # TODO should the index of ppl AFTER "-1" person be adjusted?
                if colIdx == delColIdx:
                    print("skipping col being deleted: ", colIdx, colLabel)
                    colIdx += 1
                    continue
                # all ranks that are higher than with the deleted labels stays untouched
                # but ranks that are lower than with the deleted labels improved for sure match, but removed for others
                newRRank = 0
                newCRank = 0
                print(f"Processing column {colIdx} with rank {rank}. For {curRowLabel} rank with DELETED {colLabel} was {delColValue}.")
                if (rank is None):
                    newRRank = -1
                elif (delColValue is None):
                    newRRank = rank[0]
                elif (rank[0] < delColValue[0]):
                    # this row liked this column better than this row liked the deleted column
                    newRRank = rank[0]
                elif (sureMatch or deletedRank[1] < delColValue[1]):
                    # either the deleted pair not gonna stray cause they like each other BEST of all
                    # OR deleted column liked the deleted row better than deleted column liked this row
                    # so this pair doesn't threaten match that was just made
                    newRRank = rank[0] - 1
                else:
                    # match of this row with this column would be a threat that the deleted column and THIS row
                    # might prefer each other to their matches
                    newRRank = -1
                print(f"new row rank is : {newRRank}")
                print(f"for column {colIdx} rank with DELETED {rowLabel} was {deletedRow[colIdx]}. Considering rank {rank}")
                if (rank is None):
                    newCRank = -1
                elif (deletedRow[colIdx] is None):
                    newCRank = rank[1]
                elif (rank[1] < deletedRow[colIdx][1]):
                    # this column liked this row better than this column liked the deleted row
                    newCRank = rank[1]
                elif (sureMatch or deletedRank[0] < deletedRow[colIdx][0]):
                    # either the deleted pair not gonna stray cause they like each other BEST of all (remaining)
                    # OR deleted row liked deleted column better than deleted row liked this colum
                    newCRank = rank[1] - 1
                else:
                    # match of this row with this column would be a threat that the deleted row and this column
                    # might prefer each other to their matches
                    newCRank = -1
                print(f"new column rank is {newCRank}")
                if (-1 == newRRank or -1 == newCRank):
                    newRow.append(None)
                else:
                    newRow.append((newRRank, newCRank))
                    totalOffset = newRRank + newCRank
                    dictPairs = newOffset.get(totalOffset, {})
                    best = min(newRRank, newCRank)
                    pairLst = dictPairs.get(best,[])
                    pairLst.append((curRowLabel, self.__colLblLookup[colIdx]))
                    dictPairs[best] = pairLst
                    newOffset[totalOffset] = dictPairs
                print("newRow is now " , newRow)
                colIdx += 1
            newMatrix[curRowLabel] = newRow
            print(">>>>> NEW MATRIX ROW>>>>: ", newRow)
            input("press enter")
        return RankMatrix(newMatrix, newOffset, newRowLblLookup, newColLblLookup, newColIdxLookup)
