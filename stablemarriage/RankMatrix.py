from typing import *

class RankMatrix:
    """ 
        This class has following private attributes:
           __idxLookup1, __idxLookup2 - allows to find the index in the matrix by the provided label
           __lblLookup1, __lblLookup2 - allows to find the label by the provided index
           __matrix - the ranking matrix.
    """
    TABLE_ZERO_ZERO: Final = "Col headers: "
    TABLE_HEADER: Final = "Rank Matrix"

    def __init__(self, labelLst1: list, labelLst2: list, preferences1: dict, preferences2: dict) -> None:
        self.__matrix: dict = {}
        self.__matrix[self.TABLE_ZERO_ZERO] = labelLst2[:]
        self.__offsets: dict = {}
        # this will have keys - members of labelLst2 and values - their index in the original provided list
        self.__idxLookup2 = {}
        # this one will be reversed
        self.__lblLookup2 = {}
        idx: int = 0
        for label in labelLst2:
            self.__idxLookup2[label] = idx
            self.__lblLookup2[idx] = label
            idx += 1
        self.__idxLookup1 = {}
        self.__lblLookup1 = {}
        idx = 0
        for label in labelLst1:
            self.__idxLookup1[label] = idx
            self.__lblLookup1[idx] = label
            idx += 1

        # now that lookup dicts are there - fill the matrix.
        # fill up preferences1 first
        for rowLabel in labelLst1:
            row = [(0, 0)] * len(labelLst2)
            place = 0
            for colLabel in preferences1[rowLabel]:
                colIdx = self.__idxLookup2[colLabel]
                row[colIdx] = (place, 0)
                place += 1
            self.__matrix[rowLabel] = row
        # now fill out values from preferences2 and group similarly offset relationships
        colIdx = 0
        for colLabel in labelLst2:
            place = 0
            for rowLabel in preferences2[colLabel]:
                prevValue: tuple = self.__matrix[rowLabel][colIdx]
                self.__matrix[rowLabel][colIdx] = (prevValue[0], place)
                place += 1
            colIdx += 1

        
        
    def getTableLines(self) -> list:
        # TODO handle labels of different lengths (for real names)
        # calculate length of col headers row and regular matrix row
        # pick bigger of the above and the TABLE_HEADER line to be the width of the table
        # to which we pad all the rows for nice representation.
        colLblLen = len(self.__lblLookup2[0])
        rowLblLen = len(self.__lblLookup1[0])
        # separate row headers from values by " | " and values from each other by a single space unless col headers are long
        # value itself will be displayed as (##:##) - 7 characters total
        colCount = len(self.__matrix[self.TABLE_ZERO_ZERO])
        rowLen = rowLblLen + 3 + colCount * 8
        colHeaderLen = rowLblLen + 3 + (colLblLen + 1) * colCount
        tableHeaderLen = len(self.TABLE_HEADER)
        lineLen = max(tableHeaderLen, rowLen, colHeaderLen)

        result: list = []
        # Add table header
        outputLn: str = self.TABLE_HEADER + "\n"
        if tableHeaderLen < lineLen:
            margin = (lineLen - tableHeaderLen) // 2
            outputLn = " " * margin + self.TABLE_HEADER + " " * (lineLen - tableHeaderLen - margin) + "\n"
        result.append(outputLn)

        # add column headers
        marginL = 0
        marginR = 1
        if colLblLen < 7:
            marginL = (7 - colLblLen) // 2
            marginR = 7 - colLblLen - marginL + 1 # + 1 = space between colheaders
        outputLn = " " * (rowLblLen + 3)
        for colHeader in self.__matrix[self.TABLE_ZERO_ZERO]:
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
        for idx in sorted(self.__lblLookup1):
            rowHeader = self.__lblLookup1[idx]
            outputLn = rowHeader + " | "
            for ranks in self.__matrix[rowHeader]:
                outputLn += CELL_TEMPLATE.format(
                    (ranks[0] if ranks[0] > 9 else "0" + str(ranks[0])),
                    (ranks[1] if ranks[1] > 9 else "0" + str(ranks[1])))
            outputLn  += "\n"
            result.append(outputLn)
        return result