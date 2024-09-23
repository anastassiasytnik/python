from typing import *
from random import choice
from RankMatrix import *

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

MEN_PREFIX : Final = "M";
WOMEN_PREFIX: Final = "W";

class MatchState:
    """ Contains everything you need to save a point in matching process to be able to continue the process.
        This class has following attributes:
          menPreferences - contains personal rankings of all participating women for each participating man.
          womenPreferences - contains personal rankings of all participating men for each participating woman.
    """

    def __getRandomPreferences(self, owners: list, choices: list) -> dict:
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
    
    def __init__(self, size: int) -> None:
        if (2 > size):
            raise ValueError("There isn't enough participants to make matching a problem");
        self.men: list = getOrderedLabels(size, MEN_PREFIX);
        self.women: list = getOrderedLabels(size, WOMEN_PREFIX);
        self.menPreferences: dict = self.__getRandomPreferences(self.men, self.women)
        self.womenPreferences: dict = self.__getRandomPreferences(self.women, self.men)
        self.rankMatrix: dict = RankMatrix(self.women, self.men, self.womenPreferences, self.menPreferences)
        
if __name__ == "__main__":
    boo = MatchState(5)
    for man, preferences in boo.menPreferences.items():
        print(f"{man} = {preferences}")
    print("-------------------------")
    for woman, preferences in boo.womenPreferences.items():
        print(f"{woman} = {preferences}")
    matrix = boo.rankMatrix
    for line in matrix.getTableLines():
        print(line)