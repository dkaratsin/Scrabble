# -*- encoding: utf-8 -*-
import itertools
import json
import random
import letters

class SakClass:
    def __init__(self):
        self.lettersInSak = letters.lettersInSak[:]
        self.lettersRemaining = 102

    def getLetters(self, n=5):
        gotLetters = []
        if( n <= self.lettersRemaining):
            for x in range(n):
                pickRandomly = random.randint(0,self.lettersRemaining-1)
                gotLetters.append(self.lettersInSak.pop(pickRandomly))
                self.lettersRemaining -= 1
            return gotLetters
        else:
            return False
        
    def putBackLetters(self, lettersReturned):
        for i in lettersReturned:
            self.lettersInSak.append(i)
            self.lettersRemaining += 1
            
    def randomizeSak(self):
        random.shuffle(self.lettersInSak)
            
    

class Player:
    def getLettersFromSak(self, sak, n=7):
        if(n <= sak.lettersRemaining):
            self.playerLetters.extend(sak.getLetters(n))
            return True
        else: return False
        
    def __init__(self, sak, name = 'Adam' , score = 0,):
        self.playerLetters = []
        self.getLettersFromSak(sak)
        self.name = name
        self.score = score
   
    def __repr__(self):
        return f"Player(name='{self.name}', score={self.score})"
   
    def returnLettersToSak(self, sak, listOfLetters):
        sak.putBackLetters(listOfLetters)
        self.playerLetters = [letter for letter in self.playerLetters if not letter in listOfLetters or listOfLetters.remove(letter)]
        self.getLettersFromSak(sak, 7 - len(self.playerLetters))
        
    def playWord(self, word, game, sak):
        if(len(word)>7 or len(word)<2):
            print('word length must be between 2 and 7 letters. Try again:')
            return False
        if all(self.playerLetters.count(char) >= word.count(char) for char in word ):
            if word in game.lexiko:
                gainedScore = game.lexiko.get(word)
                self.score += gainedScore
                print(self.name + ' gained '+ str(gainedScore) + ' points \t Total Score = ' + str(self.score))
   
                for letter in word:
                    self.playerLetters.remove(letter)
                #IF SAK CANT PROVIDE NEW LETTERS -> GAME OVER
                if(not self.getLettersFromSak(sak, 7-len(self.playerLetters))):
                    game.gameOver = True
                print("'Enter' to continue...")
                input()

                return True;
            else:
                print('Invalid word. Try again...')
        else: 
            print('Available letters do not match the given word. Try again...')
        return False;
    
    def play(self, game, sak):
        while True:
            print("******************************************************************************\n")
            print("Letters remaining in sak = " + str(sak.lettersRemaining))
            print('Player: ' + self.name)
            print("Score: \t" + str(self.score))
            output = ''
            for letter in self.playerLetters:
                output += str(letter) + '( ' + str(game.lets[letter][1]) + ' )'
            print('Available letters(value):  ' + output)
            print('-> Write a valid word with your letters or\n'
                  '-> Type "p" to pass and swap any number of letters\n'
                  '-> Type "q" to end the game')
            print('word:' ,end = ' ')
            word = input()
            if word == 'q':
                game.gameOver = True
                break;
            elif word == 'p': 
                print('type letters to swap:')
                lettersToSwap = input()
                lettersReturned = []
                for letter in lettersToSwap:
                    lettersReturned.append(letter)
                self.getLettersFromSak(sak, len(lettersReturned))
                self.returnLettersToSak(sak, lettersReturned)
                break
            else:
                if(self.playWord(word,game,sak)): break
   
class Human(Player):
    def __init__(self, sak, name='Dimitris', score=0):
        super().__init__(sak, name, score)

class Computer(Player):
    def __init__(self, sak, algo='smart', name='Computer', score=0):
        super().__init__(sak, name, score)
        self.algo = algo
        
    def playWord(self, word, game, sak):
        output = ''
        for letter in self.playerLetters:
            output += str(letter) + '( ' + str(game.lets[letter][1]) + ' )'
        print('Available letters(value):  ' + output)
        print('Word played: ' + word)
        super().playWord(word, game, sak)
        
    def generatePossibleWords(self, game, permSize):
        possibleWords = []
        for i in itertools.permutations(self.playerLetters, permSize):
            word = ''.join([str(letter) for letter in i])
            if(word in game.lexiko):
                possibleWords.append(word)
        return possibleWords

    def play(self, game, sak):
        print("******************************************************************************\n")
        print('Player: ' + self.name)
        print("Score: \t" + str(self.score))
        
        #del sort
        #MIN LETTERS
        if(self.algo == 'min'): 
            for n in range(2,8):
                possibleWords = self.generatePossibleWords(game,n)
                if(possibleWords):
                    self.playWord(possibleWords[0], game, sak)
                    break
                     
        #MAX LETTERS
        elif(self.algo == 'max'): 
            for n in range(7,1,-1):
                possibleWords = self.generatePossibleWords(game,n)
                if(possibleWords):
                    self.playWord(possibleWords[0], game, sak)
                    break
        
        #SMART
        elif(self.algo == 'smart'):  
            possibleWords = []
            for n in range(2,8):
                possibleWords.extend( self.generatePossibleWords(game,n) )
            if(possibleWords):
                maxKey = max(possibleWords, key=lambda k: game.lexiko.get(k))
                self.playWord(maxKey, game, sak)
                
                
        if(len(possibleWords)==0):
            if(sak.lettersRemaining>7):
                self.returnLettersToSak(sak, self.playerLetters)
            elif(sak.lettersRemaining>0):
                self.returnLettersToSak(sak, [self.playerLetters[x] for x in range(sak.lettersRemaining)])
            else:
                game.gameOver = True
                    
    

class Game:
    def calcWordScore(self, word):
        scoreCounter = 0
        lets = letters.lets
        for letter in word:
            scoreCounter += lets[letter][1]
        return scoreCounter
    
    def saveMatchToJson(self, data):
        try:
            with open("data.json", 'x') as json_file:
                matchHistory = []
                matchHistory.append(data)
                json.dump(matchHistory, json_file)
                return
        except:
            pass
        with open("data.json", 'r+') as json_file:
            try:
                matchHistory = json.load(json_file)
            except json.JSONDecodeError:
                matchHistory = []
            matchHistory.append(data)
            json_file.seek(0)
            json.dump(matchHistory, json_file)
            json_file.truncate()
        
            
    def printMatchHistory():
        try:
            with open("data.json", 'r+') as json_file:
                try:
                    matchHistory = json.load(json_file)
                except json.JSONDecodeError:
                    matchHistory = []
                for x in matchHistory:
                    print(x[0] + '( ' + str(x[1]) +  ' ) vs ( ' + str(x[2]) + ' )'  + x[3])
        except:
            print('no match history found')
            
            
         
    def __init__(self, name, algo= 'smart'):
        self.lexiko = {}
        self.lets = letters.lets
        self.gameOver = False
        self.sak = SakClass()
        self.player = Human(self.sak, name)
        self.computer = Computer(self.sak, algo)
            
    def __repr__(self):
        return 'Game between player: ' + self.player.name + ' and ' + self.computer.name
    
    def setup(self):
        with open('greek7.txt','r',encoding="utf-8") as f7:
            words = f7.readlines()
            words = [s.strip() for s in words]
            self.lexiko = {word: self.calcWordScore(word) for word in words}
        
            
    def run(self):
        playerTurn = True
        while not self.gameOver:
            if(playerTurn): self.player.play(self, self.sak)
            else:           self.computer.play(self, self.sak)
            playerTurn = not playerTurn
        self.end()

    def end(self):
        print("******************************************************************************\n")
        print("Game Over")
        print(self.player.name + ' vs ' + self.computer.name)
        print("Score")
        print(str(self.player.score) + ' ' + str(self.computer.score))
        
        if(self.player.score == self.computer.score): 
            print("Tie")
        else: 
            print("Winner -> " + str(self.player.name) if self.player.score > self.computer.score else str(self.computer.name))
            
        match = [ self.player.name , self.player.score , self.computer.score, self.computer.algo, self.sak.lettersRemaining ] 
        self.saveMatchToJson(match)
        
        
        
    
