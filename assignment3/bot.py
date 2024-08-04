from typing import *

class Letter:
    """ Represents a letter from the guess with a state of check

        When a word is guessed the game returns a list
        of letters where 2 flags assigned to each letter:
        whether the letter is in correct place
        (in_correct_place attribute)
        and whether the letter is present in the target word
        (in_word attribute)
        The assignment requires to write 2 getters:
        is_in_correct_place and is_in_word
    """

    def __init__(self, letter: str) -> None:
        """ initializes letter object with the provided letter and false values for attributes."""

        if (letter is None or len(letter) != 1):
            raise ValueError(f"Letter is a non-empty single-character string. {letter} was provided instead")
        self.letter = letter
        self.in_correct_place = False
        self.in_word = False
        self.idx = -1

    def is_in_correct_place(self) -> bool:
        """Returns True if it was determined that this letter was in the correct place in the guess made"""    

        return self.in_correct_place
    
    def is_in_word(self) -> bool:
        """Returns True if it was determined that this letter was in the target word from the guess made"""

        # apparently the game engine doesn't set in_word flag if it's in correct place.
        return self.in_word or self.in_correct_place

    def __str__(self):
        state: str = "absent"
        if (self.is_in_correct_place):
            state = "correct"
        elif (self.is_in_word):
            state = "present, but not in position"
        return f"{self.letter}({state})"

class Bot:
    """ Represents a bot that can play guess word game.

        The bot can make a guess by providing a word from the file "words.txt".
        The guess should take into account all the information received from the game from the previous guesses:
        The letters that were marked as "in word" should be present in the next guess
        The letters that were marked as "in correct place" should be present in the same position in the next guess
        The letters that were marked as not "in word" should not be present in the next guess.

        The bot should have 2 methods: make_guess and record_guess_results
    """

    def __init__(self, word_file: str):
        """ Reads the words from the file and creates a list of possible guesses """
        self.allWords = None
        with open(word_file, "r") as wFile:
            self.allWords: List[str] = list(x.strip().upper() for x in wFile.readlines())
        #make a copy, because we will be removing words that the previous guesses eliminates
        self.word_list: List[str] = self.allWords[:]
        self.absentLetters: List[str] = []
        self.presentLetters: List[str] = []
        # maps index of the letter in the target word to actual letter
        self.correctLetters: Mapping[int, str] = {}

    def make_guess(self) -> str:
        """ selects a word from list of words that haven't been disqualified yet by previous guesses"""

        print(f"Length is {len(self.word_list)}. First is {self.word_list[0]}")
        return self.word_list[0]
    
    def record_guess_results(self, guess: str, guess_results: List[Letter]) -> None:
        """ Updates the records and removes all leading "invalid" words from word_list
            until the very first word satisfies 
            This method assumes that guess_results argument contains letters 
            in the same order as they appear in guess argument.
            If the order wasn't preserve - the situation with multiple occurrences of same letter
            would not be resolved. - flaw of assignment design.
        """
        idx: int = 0
        for letter in guess_results:
            if (not letter.is_in_word()):
                self.absentLetters.append(letter.letter)
            elif (letter.is_in_correct_place()):
                self.correctLetters[idx] = letter.letter
            elif (letter.letter not in self.presentLetters):
                self.presentLetters.append(letter.letter)
            idx += 1

        print(f"Absent: {self.absentLetters}")
        print(f"Present: {self.presentLetters}")
        print(f"Correct: {self.correctLetters}")
        wordIdx: int = 0 #That was our last guess. It's not the word if we haven't got all 5 in self.correctLetters
        if (5 == len(self.correctLetters)):
            return #Nothing to do - we guessed the word.
        
        # Now if it wasn't a correct word - remove it
        del(self.word_list[0])
        print("Deleted previous guess")
        # TODO remove
        count = 0
        report: List[str] = []
        # Go through words, deleting invalid ones until we find 1st word that fits
        found: bool = False
        while not found:
            word = self.word_list[0]
            count += 1
            if (count % 20 == 0):
                print(f"These words have been rejected{report}")
                report = []
                boo = input("continue..")
            failed: bool = False
            # should contain all "correct" letters in their places
            for idx in self.correctLetters:
                if (word[idx] != self.correctLetters[idx]):
                    #doesn't have a letter we guessed already in a correct spot - remove
                    report.append(word)
                    del(self.word_list[wordIdx])
                    failed = True
                    break
            if failed: continue # get next word, as this was already disqualified and removed
            # should contain all present letters
            for ch in self.presentLetters:
                if (ch not in word):
                    report.append(word)
                    del(self.word_list[wordIdx])
                    failed = True
                    break
            if failed: continue # get next word, as this was already disqualified and removed
            # should NOT contain all absent letters
            for ch in self.absentLetters:
                if (ch in word):
                    report.append(word)
                    del(self.word_list[wordIdx])
                    failed = True
                    break
            if failed: continue # get next word, as this was already disqualified and removed
            # this word doesn't contradict all previous guesses validation - we found our next guess
            print(f"These words have been rejected: {report}")
            print(f"Found next guess: {word}")

            found = True
