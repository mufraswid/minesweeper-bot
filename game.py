"""This module creates a mainwindow to run the application."""
# from os import system
# from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QListWidget, QListWidgetItem, QLineEdit
# from PyQt5.QtGui import QPixmap, QIcon
# from .productwindow import prod_window

from clips import Environment, Symbol, Facts
from random import randint
from Tile import Tile

### CLASSES ###
# Grid to model the field
class Grid:
    def __init__(self, size):
        '''
        Konstruktor
        '''
        self.size = size
        self.grid = [ [Tile(n + self.size * i) for n in range(size)] for i in range(size)]

    def generateRandomBombs(self, count):
        '''
        Generate random bombs on the field
        '''
        for n in range(count):
            while (True):
                x = randint(0, self.size-1)
                y = randint(0, self.size-1)
                if x > 0 and y > 0 and self.grid[x][y].bomb == False:
                    self.grid[x][y].bomb = True
                    break

    def inputBombs(self, count):
        '''
        Take input to set the bombs in the field
        '''
        for n in range(count):
            while(True):
                x, y =  map(int, input('Koordinat bomb %d: '%(n+1)).split(','))
                if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size) or ((x == 0) and (y == 0)):
                    print("Out of bounds!")
                else:
                    if self.grid[x][y].bomb == False and not((x == 0) and (y == 0)):
                        self.grid[x][y].bomb = True
                        break
                    else:
                        print("Koordinat sudah terisi bomb!")

    def inbounds(self, x, y):
        '''
        Check if x and y is within the field
        '''
        return (0 <= x and x < self.size and 0 <= y and y < self.size) 

    def getLabel(self, x, y):
        '''
        Get value of a Tile from its surroundings
        '''
        s = 0
        for (dx, dy) in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            if self.inbounds(x+dx, y+dy) and self.grid[x+dx][y+dy].isBomb():
                s += 1
        return s
    
    def printBombs(self):
        '''
        Print bombs in the field
        '''
        for i in range(self.size):
            print("=== ", end='')
        print()
        for i in range(self.size):
            for j in range(self.size):
                if(self.grid[j][i].isBomb()):
                    print(" B  ", end = '')
                else:
                    print("[ ] ", end = '')
            print()
        for i in range(self.size):
            print("=== ", end='')
        print()

    def printField(self):
        '''
        Print the board with all tiles opened
        '''
        for i in range(self.size):
            print("=== ", end='')
        print()
        for y in range(self.size):
            for x in range(self.size):
                currTile = self.grid[x][y]
                if (currTile.isBomb()):
                    print(" B  ", end='')
                else:
                    print("[" + str(self.getLabel(x,y)) + "] ", end='')
            print()
        for i in range(self.size):
            print("=== ", end='')
        print()

    def printBoard(self):
        '''
        Print the board as it is
        '''
        for i in range(self.size):
            print("=== ", end='')
        print()
        for y in range(self.size):
            for x in range(self.size):
                currTile = self.grid[x][y]
                if (currTile.isOpened()):
                    if (currTile.isBomb()):
                        print(" B  ", end='')
                    else:
                        print(" " + self.getLabel(x,y) + "  ", end='')
                elif (currTile.isFlagged()):
                    print("[F] ", end = '')
                else:
                    print("[ ] ", end = '')
            print()
        for i in range(self.size):
            print("=== ", end='')
        print()

    
    def openAdjacent(self, id):
        '''
        Open adjacent safe tiles, recursively
        '''
        surr = self.getSurroundings(id)
        for tile in surr:
            x, y = tile % self.size, tile // self.size
            if self.getLabel(x,y) == 0:
                self.grid[x][y].open()
                self.openAdjacent(tile)          
    
    def getSurroundings(self, id):
        '''
        Get surrounding tiles' ids
        '''
        surr = []
        x = id % self.size 
        y = id / self.size 
        for (dx, dy) in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
            if self.inbounds(x+dx, y+dy):
                nx = x + dx
                ny = y + dy
                surr.append(nx + ny * self.size)
        return surr


# Fact utils
def isFactSquare(str):
    return str[1:7] == 'square'

def isFactFlagged(str):
    return str[1:8] == 'flagged'

def getFlaggedCoord(str):
    '''
    get flagged coord of surrounding, coord is id
    '''
    raw = str[10:]
    id = 0
    # raw is (xx)
    if (raw.length == 4):
        id = int(raw[1:2])
    # raw is (x)
    else:
        id = int(raw[1])
    return id

def getFlaggedCoord(str, size):
    '''
    get flagged coord of surrounding, coord is (x,y)
    '''
    raw = str[10:]
    id = 0
    # raw is (xx)
    if (raw.length > 2):
        id = int(raw[1:2])
    # raw is (x)
    else:
        id = int(raw[1])
    return (id % size, id // size)

def isFactOpened(str):
    # return true if fact is opened
    return str[1:7] == 'opened'

def getOpenedCoord(str):
    '''
    get opened coord of surrounding, coord is id
    '''
    raw = str[9:]
    id = 0
    # raw is (xx)
    if (raw.length > 2):
        id = int(raw[1:2])
    # raw is (x)
    else:
        id = int(raw[2])
    return id

def getOpenedCoord(str, size):
    '''
    get opened coord of surrounding, coord is (x,y)
    '''
    raw = str[9:]
    id = 0
    # raw is (xx)
    if (raw.length > 2):
        id = int(raw[1:2])
    # raw is (x)
    else:
        id = int(raw[2])
    return (id % size, id // size)

def main():
    '''
    Main function
    '''
    size = 0
    while(True):
        size = int(input("Masukkan ukuran papan (4 <= n <= 10): "))
        if (4 <= size and size <= 10):
            break
        else:
            print("Invalid size!")
    
    bombCount = 0
    while(True):
        bombCount = int(input("Masukkan jumlah bomb dalam papan: "))
        if (1 <= bombCount and bombCount <= (size*size-1)):
            break
        else:
            print("Invalid amount!")
    
    grid = Grid(size)

    while (True):
        case = input("Apakah bomb diinput secara random? (y/n)")
        if (case == "y"):
            grid.generateRandomBombs(bombCount)
            break
        elif (case == "n"):
            grid.inputBombs(bombCount)
            break
    grid.printBombs()
    grid.printField()
    grid.printBoard()

    ### SOLVER PART ###
    # init clps environment, load mines.clp
    env = Environment()
    env.load('mines.clp')
    
    clips_bomb_count = 0
    
    while clips_bomb_count < bombCount:
        for fact in env.facts():
            strfact = str(fact)
            if isFactSquare(strfact):
                # Retract because the fact is outdated
                env.build(f'retract {strfact}')
            elif isFactFlagged(strfact):
                # Ensure the flag has never been checked before
                clips_bomb_count += 1
            elif isFactOpened(strfact):

                pass
            # Count every possibility of adjacent squares      
            # Push fact to clips using assert
            # env.run()

def init(size):
    ''' 
    Init game aspects
    '''
    size = int(input("Masukkan ukuran papan (4 <= n <= 10): "))
    bombCount = int(input("Masukkan jumlah bomb dalam papan: "))

    grid = Grid(size)

    while (True):
        case = input("Apakah bomb diinput secara random? (y/n)")
        if (case == "y"):
            grid.generateRandomBombs(bombCount)
            break
        elif (case == "n"):
            grid.inputBombs(bombCount)
            break
    grid.print()
    

if __name__ == "__main__":
    main()
