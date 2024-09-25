from typing import *
from random import choice
from RankMatrix import *
from copy import deepcopy

MEN_PREFIX : Final = "M";
WOMEN_PREFIX: Final = "W";

def getOrderedLabels(amount: int, prefix: str) -> list:
    """ produces list of ordered labels all of which start with a prefix and 
        continued with consecutive numbers starting from 0. Numbers smaller than 10 have 1 leading zero.
        Arguments:
           amount - non-negative integer - how many labels you need
           prefix - common part of all the labels
        Example: getOrderedLabels(5, "obj") will produce ["obj00", "obj01", "obj02", "obj03", "obj04"]
    """
    if (0 > amount):
        raise ValueError("function getOrderedLabels requires a positive integer as a value of argument 'amount'");
    result = []
    for i in range(amount):
        result.append(prefix + ("0" if 10 > i else "") + str(i))
    return result;

def getRandomPreferences(owners: list, choices: list) -> dict:
    # could do arg check, but meh
    result: dict = {}
    for owner in owners:
        preferences = []
        for i in range(len(choices)):
            newChoice = choice(choices)
            while newChoice in preferences:
                newChoice = choice(choices)
            preferences.append(newChoice)
        result[owner] = preferences
    return result

def generate(size: int):
    if (2 > size):
        raise ValueError("There isn't enough participants to make matching a problem");
    men: list = getOrderedLabels(size, MEN_PREFIX);
    women: list = getOrderedLabels(size, WOMEN_PREFIX);
    menPreferences: dict = getRandomPreferences(men, women)
    womenPreferences: dict = getRandomPreferences(women, men)
    rankMatrix: dict = fromPreferences(women, men, womenPreferences, menPreferences)
    # store already matched tuples here
    offsets = rankMatrix.getOffsetIdx()
    return MatchState(size, men, women, menPreferences, womenPreferences, rankMatrix, [])

class MatchState:
    """ Contains everything you need to save a point in matching process to be able to continue the process.
        This class has following attributes:
          menPreferences - contains personal rankings of all participating women for each participating man.
          womenPreferences - contains personal rankings of all participating men for each participating woman.
    """
    
    def __init__(self, size, men, women, menPref, womenPref, rankMatrix, matched):
        self.size = size
        self.men = men
        self.women = women
        self.menPreferences = menPref
        self.womenPreferences = womenPref
        self.rankMatrix = rankMatrix
        self.matched = matched

    def match(self, woman, man):
        newSize = self.size - 1
        newMen = self.men[:].remove(man)
        newWomen = self.women[:].remove(woman)
        matchRank = self.rankMatrix.getRanks(woman, man)
        # if not a perfect match we shouldn't allow to match more desired side partners
        # with less desired candidates
        sureMatch = (0 == matchRank[0]) and (0 == matchRank[1])
        print("SURE MATCH? ", sureMatch, matchRank)
        restrictedMen = []
        restrictedWomen = []
        if (not sureMatch):
            print(">>> making restricted men")
            for i in range(matchRank[0]):
                restrictedMen.append(self.womenPreferences[woman][i])
            for i in range(matchRank[1]):
                restrictedWomen.append(self.menPreferences[man][i])

        newMenPref = {}
        for person, pref in self.menPreferences.items():
            if man == person:
                continue
            if person in restrictedMen:
                print("found restricted person: ", person)
                truncateIdx = pref.index(woman)
                newMenPref[person] = pref[:truncateIdx]
                if len(newMenPref[person]) == 0:
                    print(f"{woman} and {person} would rather be with each other than with {man} and any other unmatched woman")
                    raise DeadEndException(woman, man)
            else:
                newMenPref[person] = pref[:]
                newMenPref[person].remove(woman)

        newWomenPref = {}
        for person, pref in self.womenPreferences.items():
            if woman == person:
                continue
            if person in restrictedWomen:
                truncateIdx = pref.index(man)
                newWomenPref[person] = pref[:truncateIdx]
                if (len(newMenPref) == 0):
                    print(f"{man} and {person} would rather be with each other than with {woman} or any unmatched man")
                    raise DeadEndException(woman, man)
            else:
                newWomenPref[person] = pref[:]
                newWomenPref[person].remove(man)
        newMatched = self.matched[:].append((woman, man))
        newMatrix = self.rankMatrix.delete(woman, man, newWomenPref, newMenPref)
        return MatchState(newSize, newMen, newWomen, newMenPref, newWomenPref, newMatrix, newMatched)

        
if __name__ == "__main__":
    boo: MatchState = generate(5)
    for man, preferences in boo.menPreferences.items():
        print(f"{man} = {preferences}")
    print("-------------------------")
    for woman, preferences in boo.womenPreferences.items():
        print(f"{woman} = {preferences}")
    matrix = boo.rankMatrix
    for line in matrix.getTableLines():
        print(line)
    offsets = matrix.getOffsetIdx()
    for offset in sorted(offsets):
        print(f"offset: {offset}; members: {offsets[offset]}")
    pair = input("Enter labels of a pair separated by space: ")
    print("*" * 30)
    answer = pair.split()
    hoo = boo.match(answer[0], answer[1])
    for man, preferences in hoo.menPreferences.items():
        print(f"{man} = {preferences}")
    print("-------------------------")
    for woman, preferences in hoo.womenPreferences.items():
        print(f"{woman} = {preferences}")
    matrix = hoo.rankMatrix
    for line in matrix.getTableLines():
        print(line)
    offsets = matrix.getOffsetIdx()
    for offset in sorted(offsets):
        print(f"offset: {offset}; members: {offsets[offset]}")
