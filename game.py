"""This module creates a mainwindow to run the application."""
# from os import system
# from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QListWidget, QListWidgetItem, QLineEdit
# from PyQt5.QtGui import QPixmap, QIcon
# from .productwindow import prod_window

from clips import Environment, Symbol
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
    
    grid = Grid(size,bombCount)

    while (True):
        case = input("Apakah bomb diinput secara random? (y/n)")
        if (case == "y"):
            grid.generateRandomBombs(bombCount)
            break
        elif (case == "n"):
            grid.inputBombs(bombCount)
            break

    ### SOLVER PART ###
    # init clps environment, load mines.clp
    env = Environment()
    env.load('mines.clp')
    for rule in env.rules():
        rule.watch_firings = True
        # rule.matches()
    clips_bomb_count = 0
    print("We begin")

    # Init first move by opening tile(0,0)
    adj = set([])
    flag = set([])
    fact_arr = []
    grid.openTile(0,0)
    sqid = 0
    sqval = grid.getLabel(0,0)
    sqadj = "".join(adj)
    sqflag = len(flag)
    sqstring = "(square (no " + str(sqid) + ") (value " + str(sqval) + ") (adjacent " + str(sqadj) + ") (nflags " + str(sqflag) + "))"
    fact_arr.append(sqstring)
    print("Start!")

    win = True
    iterasi = 0
    
    while (clips_bomb_count < grid.bombCount) and win:
        iterasi += 1
        print("Iterasi ke-"+str(iterasi))
        for fact in fact_arr:
            strfact = str(fact)
            if isFactFlagged(strfact):
                print(f'read: {strfact}')
                # Ensure the flag has never been checked before
                id = getFlaggedCoord(strfact)
                x = id % grid.size
                y = id // grid.size 
                if not grid.grid[x][y].isFlagged():
                    grid.printBoard()
                    grid.grid[x][y].setFlag()
                    clips_bomb_count += 1
            elif isFactOpened(strfact):
                print(f'read: {strfact}')
                id = getOpenedCoord(strfact)
                x = id % grid.size
                y = id // grid.size
                if not grid.grid[x][y].isOpened():
                    grid.openTile(x, y)
                grid.printBoard()
                if (grid.checkBombOpened()):
                    win = False
                    break
        if not(win):
            break
    
        # print(f'BOMBCOUNT:{clips_bomb_count}')
        # Calculate probability to each adjacent unopened tiles
        # Format map = {id: probability}
        # grid.printBoard()
        adjDict = {}
        for x, y in grid.openedValuedTiles:
            arr = grid.getSurroundings(x, y)
            adj = set([])
            flag = set([])
            # for every unopened adjacent squares, increment probability from every adjacent valued tile
            for ax, ay in arr:
                id = ax + ay * grid.size
                if not grid.grid[ax][ay].isOpened() and not grid.grid[ax][ay].isFlagged():
                    if id not in adjDict:
                        adjDict[id] = 1 
                    else:
                        adjDict[id] += 1
                    adj.add(id)
                elif grid.grid[ax][ay].isFlagged():
                    flag.add(id)
            
            # cek surroundingnya ada yang belom kebuka
            # kalo belom, assert squarenya
            if (len(adj) > 0):
                sqid = x + y * grid.size
                sqval = grid.getLabel(x,y)
                sqadj = ""
                for val in adj:
                    sqadj += str(val)
                    sqadj += " "
                sqadj = sqadj[:len(sqadj)-1]
                sqflag = len(flag)
                sqstring = "(square (no " + str(sqid) + ") (value " + str(sqval) + ") (adjacent " + str(sqadj) + ") (nflags " + str(sqflag) + "))"
                # print(f'dis string {sqstring}')
                env.assert_string(sqstring)
                # f.assertit()

        for key in adjDict:
            # assert to clips
            probstring = "(prob (p " + str(adjDict[key]) + ") (id " + str(key) + "))"
            env.assert_string(probstring)
            # f.assertit()

        # Print Facts
        # for fact in env.facts():
        #     print(fact)
        # print("=========")
        env.run()
        fact_arr = []
        for fact in env.facts():
            s = str(fact)
            if s[:2] == 'f-':
                s = s.split('    ')[1]
            # print(s)
            fact_arr.append(s)
        
        env.reset()
    if (win):
        for y in range(grid.size):
            for x in range(grid.size):
                if (not(grid.grid[x][y].isBomb()) and not(grid.grid[x][y].isOpened())): 
                    grid.grid[x][y].open()
        print("Final Result:")
        grid.printBoard()
        print("AI won!")
    else:
        print("Final Result:")
        grid.printBoard()
        print("AI lost!")

def test():
    ''' 
    Testing the AI for 100 times
    '''
    wins = 0
    loses = 0
    size = int(input("Size= "))
    bombCount = int(input("Bombs= "))
    for i in range (100):
        grid = Grid(size,bombCount)
        grid.generateRandomBombs(bombCount)
        env = Environment()
        env.load('mines.clp')
        clips_bomb_count = 0
        print("We begin")

        # Init first move by opening tile(0,0)
        adj = set([])
        flag = set([])
        fact_arr = []
        grid.openTile(0,0)
        sqid = 0
        sqval = grid.getLabel(0,0)
        sqadj = "".join(adj)
        sqflag = len(flag)
        sqstring = "(square (no " + str(sqid) + ") (value " + str(sqval) + ") (adjacent " + str(sqadj) + ") (nflags " + str(sqflag) + "))"
        fact_arr.append(sqstring)
        print("Start!")

        win = True
        iterasi = 0
        
        while (clips_bomb_count < grid.bombCount) and win:
            iterasi += 1
            print("Iterasi ke-"+str(iterasi))
            for fact in fact_arr:
                strfact = str(fact)
                # print(f'read: {strfact}')
                if isFactFlagged(strfact):
                    # Ensure the flag has never been checked before
                    id = getFlaggedCoord(strfact)
                    x = id % grid.size
                    y = id // grid.size 
                    if not grid.grid[x][y].isFlagged():
                        grid.printBoard()
                        grid.grid[x][y].setFlag()
                        clips_bomb_count += 1
                elif isFactOpened(strfact):
                    id = getOpenedCoord(strfact)
                    x = id % grid.size
                    y = id // grid.size
                    if not grid.grid[x][y].isOpened():
                        grid.openTile(x, y)
                    grid.printBoard()
                    if (grid.checkBombOpened()):
                        win = False
                        break
            if not(win):
                break
        
            # print(f'BOMBCOUNT:{clips_bomb_count}')
            # Calculate probability to each adjacent unopened tiles
            # Format map = {id: probability}
            # grid.printBoard()
            adjDict = {}
            for x, y in grid.openedValuedTiles:
                arr = grid.getSurroundings(x, y)
                adj = set([])
                flag = set([])
                # for every unopened adjacent squares, increment probability from every adjacent valued tile
                for ax, ay in arr:
                    id = ax + ay * grid.size
                    if not grid.grid[ax][ay].isOpened() and not grid.grid[ax][ay].isFlagged():
                        if id not in adjDict:
                            adjDict[id] = 1 
                        else:
                            adjDict[id] += 1
                        adj.add(id)
                    elif grid.grid[ax][ay].isFlagged():
                        flag.add(id)
                
                # cek surroundingnya ada yang belom kebuka
                # kalo belom, assert squarenya
                if (len(adj) > 0):
                    sqid = x + y * grid.size
                    sqval = grid.getLabel(x,y)
                    sqadj = ""
                    for val in adj:
                        sqadj += str(val)
                        sqadj += " "
                    sqadj = sqadj[:len(sqadj)-1]
                    sqflag = len(flag)
                    sqstring = "(square (no " + str(sqid) + ") (value " + str(sqval) + ") (adjacent " + str(sqadj) + ") (nflags " + str(sqflag) + "))"
                    # print(f'dis string {sqstring}')
                    env.assert_string(sqstring)
                    # f.assertit()

            for key in adjDict:
                # assert to clips
                probstring = "(prob (p " + str(adjDict[key]) + ") (id " + str(key) + "))"
                env.assert_string(probstring)
                # f.assertit()

            # Print Facts
            # for fact in env.facts():
            #     print(fact)
            # print("=========")
            env.run()
            fact_arr = []
            for fact in env.facts():
                s = str(fact)
                if s[:2] == 'f-':
                    s = s.split('    ')[1]
                # print(s)
                fact_arr.append(s)
            
            env.reset()
        if (win):
            wins += 1
        else:
            loses += 1
    print("Size = " + str(size))
    print("Bombs = " + str(bombCount))
    print("Wins = " + str(wins))
    print("Loss = " + str(loses))



def game():
    '''
    Testing game by playing
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
    
    grid = Grid(size,bombCount)

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

    win = True
    while True:
        grid.printBoard()
        action = input("Action: ")
        if (isFactOpened(action)):
            id = getOpenedCoord(action)
            grid.openTile(id%grid.size, id//grid.size)
            if (grid.isOpenedBomb(id%grid.size, id//grid.size)):
                win = False
                break
        elif(isFactFlagged(action)):
            print("Action is flag")
            id = getFlaggedCoord(action)
            grid.flagTile(id%grid.size, id//grid.size)
        if (grid.isWin()):
            break
    if (win):
        print("You win!")
    else:
        print("You lose!")


if __name__ == "__main__":
    main()
    # test()
    # game()
