"""This module creates a mainwindow to run the application."""
# from os import system
# from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QListWidget, QListWidgetItem, QLineEdit
# from PyQt5.QtGui import QPixmap, QIcon
# from .productwindow import prod_window

from clips import Environment, Symbol
from random import randint
from Tile import Tile
from grid import Grid
from factutil import *

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
                x, y = getFlaggedCoord(strfact, grid)
                if not grid.grid[x][y].isFlagged():
                    grid.grid[x][y].setFlag()
                    clips_bomb_count += 1
            elif isFactOpened(strfact):
                x, y = getOpenedCoord(strfact, grid)
                if not grid.grid[x][y].isOpened():
                    grid.openTile(x, y)
            break
        break

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
