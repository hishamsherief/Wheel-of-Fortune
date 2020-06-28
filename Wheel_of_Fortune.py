class WOFPlayer:
    
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []
    
    # To add the prize money to the user balance    
    def addMoney(self,amt):
        self.prizeMoney += amt
    
    # To clear the balance of the user    
    def goBankrupt(self):
        self.prizeMoney = 0
    
    # To add the Prize to the user collection    
    def addPrize(self,prize):
        self.prizes.append(prize)
        
    def __str__(self):
        return '{} (${})'.format(self.name, self.prizeMoney)

class WOFHumanPlayer(WOFPlayer):
        
    def getMove(self, category, obscuredPhrase, guessed):
        prompt = prompt = "{} has ${}\n\nCategory: {}\nPhrase:  {}\nGuessed: {}\n\nGuess a letter, phrase, or type 'exit' or 'pass':".format(self.name, self.prizeMoney, category, obscuredPhrase, guessed)
        guess = input(prompt)
        return guess
    
class WOFComputerPlayer(WOFPlayer):
    
    # Alphabets sorted according to the probabilty to appear in a word
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    
    def __init__(self, name, difficulty):
        WOFPlayer.__init__(self, name)
        self.difficulty = difficulty

    # Probability to return true increases for increase in difficulty
    def smartCoinFlip(self):
        num = random.randint(1, 10)
        if num > self.difficulty:
            return True
        else:
            return False
    
    # To get the possible charectors that can be guessed
    def getPossibleLetters(self, guessed):
        possible_letters = []
        for c in LETTERS:
            if c not in guessed:
                if c in VOWELS and self.prizeMoney < VOWEL_COST:
                    continue
                possible_letters.append(c)
        return possible_letters
    
    # To get input from the computer player
    def getMove(self,category, obscuredPhrase, guessed):
        possible_chars = list(self.getPossibleLetters(guessed))
        free_chars = [s for s in possible_chars if s not in VOWELS]
        if free_chars == [] and self.prizeMoney < VOWEL_COST:
            return 'pass'
        
        # To return most probable letter (Probability increases as difficulty increases)
        if self.smartCoinFlip == True:
            for e in self.SORTED_FREQUENCIES[::-1]:
                if e in possible_chars:
                    break
            return e
        # To return a random letter
        else:
            return random.choice(possible_chars)



import sys
sys.setrecursionlimit(600000)

import json
import random
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS  = 'AEIOU'
VOWEL_COST  = 250

# Repeatedly asks the user for a number between min & max (inclusive)
def getNumberBetween(prompt, min, max):
    userinp = input(prompt)

    while True:
        try:
            n = int(userinp)
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError: # The user didn't enter a number
            errmessage = '{} is not a number.'.format(userinp)

        # If we haven't gotten a number yet, add the error message and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# Spins the wheel of fortune wheel to give a random prize
def spinWheel():
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase to guess
def getRandomCategoryAndPhrase():
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return (category, phrase.upper())

# Given a phrase and a list of guessed letters, returns an obscured version
def obscurePhrase(phrase, guessed):
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Returns a string representing the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    return """
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

print('='*15)
print('WHEEL OF FORTUNE')
print('='*15)
print('')

num_human = getNumberBetween('How many human players?', 0, 10)

# Create the human player instances
human_players = [WOFHumanPlayer(input('Enter the name for human player #{}'.format(i+1))) for i in range(num_human)]

num_computer = getNumberBetween('How many computer players?', 0, 10)

# If there are computer players, ask how difficult they should be
if num_computer >= 1:
    difficulty = getNumberBetween('What difficulty for the computers? (1-10)', 1, 10)

# Create the computer player instances
computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), difficulty) for i in range(num_computer)]

players = human_players + computer_players

# No players
if len(players) == 0:
    print('We need players to play!')
    raise Exception('Not enough players')

category, phrase = getRandomCategoryAndPhrase()
guessed = []

# playerIndex keeps track of the index of the player whose turn it is
playerIndex = 0

winner = False

def requestPlayerMove(player, category, guessed):
    while True:
        time.sleep(0.1)

        move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
        move = move.upper()
        if move == 'EXIT' or move == 'PASS':
            return move
        elif len(move) == 1:
            if move not in LETTERS:
                print('Guesses should be letters. Try again.')
                continue
            elif move in guessed:
                print('{} has already been guessed. Try again.'.format(move))
                continue
            elif move in VOWELS and player.prizeMoney < VOWEL_COST: # if it's a vowel, and the player doesn't have enough money
                    print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
                    continue
            else:
                return move
        #if player guessed phrase
        else:
            return move


while True:
    player = players[playerIndex]
    wheelPrize = spinWheel()

    print('')
    print('-'*15)
    print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
    print('')
    print('{} spins...'.format(player.name))
    time.sleep(2)
    print('{}!'.format(wheelPrize['text']))
    time.sleep(1)

    if wheelPrize['type'] == 'bankrupt':
        player.goBankrupt()
    elif wheelPrize['type'] == 'loseturn':
        pass
    elif wheelPrize['type'] == 'cash':
        move = requestPlayerMove(player, category, guessed)
        if move == 'EXIT':
            print('Until next time!')
            break
        elif move == 'PASS':
            print('{} passes'.format(player.name))
        elif len(move) == 1: # they guessed a letter
            guessed.append(move)

            print('{} guesses "{}"'.format(player.name, move))

            if move in VOWELS:
                player.prizeMoney -= VOWEL_COST

            count = phrase.count(move)
            if count > 0:
                if count == 1:
                    print("There is one {}".format(move))
                else:
                    print("There are {} {}'s".format(count, move))

                player.addMoney(count * wheelPrize['value'])
                if wheelPrize['prize']:
                    player.addPrize(wheelPrize['prize'])

                # all of the letters have been guessed
                if obscurePhrase(phrase, guessed) == phrase:
                    winner = player
                    break

                continue

            elif count == 0:
                print("There is no {}".format(move))
        else:
            if move == phrase: # they guessed the full phrase correctly
                winner = player

                player.addMoney(wheelPrize['value'])
                if wheelPrize['prize']:
                    player.addPrize(wheelPrize['prize'])

                break
            else:
                print('{} was not the phrase'.format(move))

    # Move on to the next player (or go back to player[0] if we reached the end)
    playerIndex = (playerIndex + 1) % len(players)

if winner:
    print('{} wins! The phrase was {}'.format(winner.name, phrase))
    print('{} won ${}'.format(winner.name, winner.prizeMoney))
    if len(winner.prizes) > 0:
        print('{} also won:'.format(winner.name))
        for prize in winner.prizes:
            print('    - {}'.format(prize))
else:
    print('Nobody won. The phrase was {}'.format(phrase))