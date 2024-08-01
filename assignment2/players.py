import random

VOWEL_COST = 250
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'

class WOFPlayer:
    """ Represents Wheel Of Fortune Player
        Player has name, money and prizes.
        and methods addMoney, goBankrupt and addPrize.
    """

    def __init__(self, name):
        """ Creates player with the provided name, 0 money and no prizes """
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def __str__(self):
        """ Outputs name and amount of money of the player. Example: 'Steve ($1800)'"""
        return f"{self.name} (${self.prizeMoney})"

    def addMoney(self, amt):
        """ Increases self.prizeMoney by amt """
        self.prizeMoney += amt

    def goBankrupt(self):
        """ Takes away all the money from the player (sets to 0) """
        self.prizeMoney = 0

    def addPrize(self, prize):
        """ Adds the specified prize to the player's prize list """
        self.prizes.append(prize)

class WOFHumanPlayer(WOFPlayer):
    """ adds a method to get human input for the turn """

    def getMove(self, category, obscuredPhrase, guessed):
        """ Asks user to provide their action for their turn and returns the answer as a result """
        line1 = f"{self.name} has ${self.prizeMoney}\n\n"
        line2 = f"Category: {category}\n"
        line3 = f"Phrase:   {obscuredPhrase}\n"
        line4 = f"Guessed:  {guessed}\n\n"
        line5 = "Guess a letter, phrase, or type 'exit' or 'pass':"
        prompt = line1 + line2 + line3 + line4 + line5
        result = input(prompt)
        return result

class WOFComputerPlayer(WOFPlayer):
    """ Represents computer player that has level.
        Player with higher level make a letter guess based on letter frequencies in language more often.
    """

    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    SORTED_CONSONANTES = "".join(x for x in SORTED_FREQUENCIES if x not in VOWELS)

    def __init__(self, name, level):
        super().__init__(name)
        self.level = level

    def smartCoinFlip(self):
        randNum = random.randint(1, 10)
        return randNum <= self.level

    def getPossibleLetters(self, guessed):
        choice = WOFComputerPlayer.SORTED_FREQUENCIES
        if (self.prizeMoney < 250):
            choice = WOFComputerPlayer.SORTED_CONSONANTES
        result = list(x for x in choice if x not in guessed)
        return result

    def getMove(self, category, obscuredPhrase, guessed):
        choice = self.getPossibleLetters(guessed)
        if (0 == len(choice)):
            return 'pass'
        if (self.smartCoinFlip):
            result = choice[len(choice) - 1]
            print(f"{self.name} makes smart choice {result} from {choice}")
            return result
        else:
            result = random.choice(choice)
            print(f"{self.name} makes bad choice {result} from {choice}")
            return result

test1 = WOFPlayer("Steve")
print(test1)
assert test1.prizeMoney == 0, "Initial amount of money supposed to be 0"
assert len(test1.prizes) == 0, "Initially list of prizes supposed to be empty"
test1.addMoney(900)
print(test1)
assert test1.prizeMoney == 900, f"Added 900 to player who had 0. expected total to be 900, but it is {test1.prizeMoney}"
test1.goBankrupt()
assert test1.prizeMoney == 0, f"Called goBankrupt, but player still have money {test1.prizeMoney}"

test2 = WOFHumanPlayer("Bob")
category = "The Sixties"
phrase = 'INDIANA JONES'
guessed = ['Z', 'J', 'Y', 'N', 'U', 'H', 'I', 'X']
obscuredPhrase = 'IN_I_N_ J_N__'
print(test2.getMove(category, obscuredPhrase, guessed))

test3 = WOFComputerPlayer("Mumba", 5)
print(WOFComputerPlayer.SORTED_FREQUENCIES)
print(WOFComputerPlayer.SORTED_CONSONANTES)
print(guessed)
possible = test3.getPossibleLetters(guessed)
print(possible)
for v in VOWELS:
    assert v not in possible, f"Mumba has no money, so vowels shouldn't be a valid choice, but {v} was found in possibilities"
test3.addMoney(300)
possible2 = test3.getPossibleLetters(guessed)
print(possible2)
vowCount = 0
for v in VOWELS:
    if v in possible2:
        vowCount += 1
assert vowCount > 0, f"Mumba has enough money, but not allowed to guess vowels"
test3.getMove(category, obscuredPhrase, guessed)

print("Testing Done")


