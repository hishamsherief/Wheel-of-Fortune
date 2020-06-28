# Wheel-of-Fortune
#Text based Wheel of Fortune game

There are human players and computer players.
At the start of the game you should give the number of human and computer players.

Every player has some amount of money ($0 at the start of the game).
Every player has a set of prizes (none at the start of the game).

The goal is to guess a phrase within a category. For example:
Category: Artist & Song
Phrase: Whitney Houston’s I Will Always Love You

Players see the category and an obscured version of the phrase where every alphanumeric character in the phrase starts out as hidden:
Category: Artist & Song

Phrase: _______ _______'_ _ ____ ______ ____ ___

# "Note that the game is not case sensitive"

# During their turn, every player spins the wheel to determine the amount and may also contain a prize.
If the wheel lands on a cash square, players may do one of three actions:
Guess any letter that hasn’t been guessed by typing a letter (a-z)
Vowels (a, e, i, o, u) cost $250 to guess and can’t be guessed if the player doesn’t have enough money. All other letters are “free” to guess

The player can guess any letter that hasn’t been guessed and gets that cash amount for every time that letter appears in the phrase

If there is a prize, the user also gets that prize (in addition to any prizes they already had)

If the letter does appear in the phrase, the user keeps their turn. Otherwise, it’s the next player’s turn

# Example:
The user lands on $500 and guesses ‘W’
There are three W’s in the phrase, so the player wins $1500

Guess the complete phrase by typing a phrase
If they are correct, they win the game

If they are incorrect, it is the next player’s turn

Pass their turn by entering 'pass'

If the wheel lands on “lose a turn”, the player loses their turn and the game moves on to the next player

If the wheel lands on “bankrupt”, the player loses their turn and loses their money but they keep all of the prizes they have won so far.

The game continues until the entire phrase is revealed (or one player guesses the complete phrase)
