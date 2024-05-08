# -*- encoding: utf-8 -*-
import classes
def guidelines():
    return '''Scrabble Game Documentation
Introduction:
This Python program implements a simplified version of the Scrabble board game, where a human player competes against a computer player. The game includes functionality for drawing and swapping letters, forming words, and calculating scores based on the value of each letter.

Classes:
    SakClass:
        Represents the tile sack from which players draw letters.
        Provides methods for drawing letters, returning letters, and shuffling the sack.
    Player:
        Base class for both human and computer players.
        Handles actions related to playing words, returning letters and getting new ones.
    Human:
        Subclass of Player representing a human player.
        Inherits methods from Player class and provides a method for interacting with the user.
    Computer:
        Subclass of Player representing a computer player.
        Inherits methods from Player class and implements AI algorithms for word selection:
            'min': 
                Prioritizes playing the shortest valid word available.
            'max':
                Prioritizes playing the longest valid word available.
            'smart': 
                Prioritizes playing the highest-scoring valid word available.
        Extends __init__, playWord, play methods and defines the generatePossibleWords method.  
    Game:
        Manages the flow of the game, including setup, running the game loop, and determining the winner.
        Utilizes dictionaries for letter values and word scores.
        Provides functionality for saving match history to a JSON file.
Other files:
    letters.py:
        lets:
            Dictionary that contains the Capital greek letters as keys and their value and number of instances un the sak at start.
            (Used to calculate value of words and display letter scores)
        lettersInSak:
            Starting list of letters for an instance of SakClass 
    data.json:
        
'''

print("******************************************************************************\n")
print("Hello player. This is Scrabble in Greek." )
name = 'player'
while True:
    print("******************************************************************************\n")
    print("Name: " + name)
    print("Menu\n'p'-> play \n'c'-> change name\n'h'-> match history\n'q'-> quit\n'help(guidelines)'-> docstring\n")
    print("******************************************************************************")
    x = input()
    if( x == 'p'):
        while True:
            print("******************************************************************************\n")
            print("Input 'q' to exit")
            print("Choose AI algorithm to start game.")
            print("Available algorithms:\n\t\t *->min"
                                         "\n\t\t *->max"
                                        "\n\t\t *->smart" )
            print("Type the name of the algorithm here: " ,end='')
            x = input()
            if(x == 'min' or x == 'max' or x == 'smart'):
                game = classes.Game(name, x)
                game.setup()
                game.run()
            elif(x == 'q'):
                break
            else:
                print('Invalid algorithm name. Make sure to input the name of one of the available algorithms correctly')
    elif( x == 'c'):
        print("******************************************************************************\n")
        print("Enter name:" ,end='')
        name = input()
    elif( x == 'h'):
        classes.Game.printMatchHistory()
    elif( x == 'q'):
        break;
    elif( x == 'help(guidelines)'):
        print(guidelines())

             
        
