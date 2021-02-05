import pygame, random
pygame.init()

##Colours
red = (128,0,0)
blue = (0,0,128)
green = (0,128,0)
yellow = (255,223,0)
orange = (204, 102, 0)

##Window
(w,h) = (750,750)
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Connect 4")
screen.fill(yellow)
pygame.display.flip()

##Variables
boardStatus = [0,0,0,0,0,0,0]

##Player class
class player():

    def __init__(self,colour, name, turnVal):
        self.colour = colour
        self.name = name
        self.turnVal = turnVal
        self.wins = 0
        
##Make an empty board with column labels
def makeBoard(screen):
    ##Making the circles
    circles = []
    for row in range(1,7):
        for column in range(1,8):
            circle = [(255,255,255),((column*100)-25, row*100+50),(50)]
            circles.append(circle)

    for circle in circles:
        pygame.draw.circle(screen, circle[0], circle[1], circle[2])

    ##Making the column labels
    for i in range(1,8):
        logo = pygame.font.SysFont('rockwell', 50)
        textSurface = logo.render(str(i), False, (0,0,0))
        screen.blit(textSurface, (i*100-40, 40))
    pygame.display.flip()

##Recieving a user's go
def recieveGo(boardStatus):
    ##Validate column choice
    while True:
        try:
            choice = int(input("Which column would you like to go in: "))-1
        except:
            continue
        
        if choice < 0 or choice > 6:
            print("Choice should be in the range 1-7, try again")
            continue
        elif boardStatus[choice] == 6:
            print("\nColumn " + str(choice+1) + " is full, try a different column\n")
            continue
        break
    print("\n")
    boardStatus[choice] += 1
    return choice, boardStatus

##Making the token for the player's turn
def makeToken(columnChoice, gameBoard, turnVal, boardStatus):
    ##Make token
    row  = boardStatus[columnChoice]-1
    token = (player.colour,((columnChoice+1)*100-25,-100*(row+1)+750), 45)
    
    ##Draw token
    pygame.draw.circle(screen, token[0], token[1], token[2])
    
    ##Update gameBoard to show the positions of a player's counters
    gameBoard[row][columnChoice] = turnVal

    ##Turn values are actual indexes for the gameBoard
    turn = (row, columnChoice)
    return turn, gameBoard

##Check if a player has won according to their board state list
def fourCheck(gameBoard, rowCol, turnVal):
    row, column = rowCol[0], rowCol[1]
    ##Check row
    rowCheck = gameBoard[row]
    
    if checkWin(rowCheck, turnVal):
        return True
    
    ##Check column
    columnCheck = []
    for i in gameBoard:
        columnCheck.append(i[column])
    
    if checkWin(columnCheck, turnVal):
        return True
    
    ##Check positive diagonal, make front half first, then back half
    posCheck = []
    posCheck.append(gameBoard[row][column])
    ##Append all turns to the bottom left
    for count in range(1,6):
        if row-count >= 0 and column-count >= 0:
            posCheck.append(gameBoard[row-count][column-count])
        else:
            break
    
    posCheck = list(reversed(posCheck))

    ##Append all turns to the top right
    for count in range(1,6):
        try:
            posCheck.append(gameBoard[row+count][column+count])
        except:
            break

    
    if checkWin(posCheck, turnVal):
        return True
    
    ##Check negative diagonal
    negCheck = []
    negCheck.append(gameBoard[row][column])
    
    ##Append all turns to the bottom right
    for count in range(1,6):
        try:
            negCheck.append(gameBoard[row-count][column+count])
        except:
            break

    negCheck = list(reversed(negCheck))

    ##Append all turns to the top left
    for count in range(1,6):
        try:
            negCheck.append(gameBoard[row+count][column-count])
        except:
            break

    
    if checkWin(negCheck, turnVal):
        return True
                    
    return False
    
##Check the win condition for a list
def checkWin(checkList, turnVal):
    contQ = False
    contQ = checkTurns(checkList, turnVal)
    if contQ and any(i==j and j==k and k==l for i,j,k,l in zip(checkList, checkList[1:], checkList[2:], checkList[3:])):
        return True
    else:
        return False

##Check a player has more than four turns in a list
def checkTurns(lst, turnVal):
    total = 0
    for i in lst:
        if i == turnVal:
            total += 1
    if total > 3:
        return True
    else:
        return False

##Make a list to represent the game board
def makeGameBoard():
    gameBoard = []
    for i in range(0,6):
        row = []
        for _ in range(0,7):
            row.append('.')
        gameBoard.append(row)
    return gameBoard

##Minimax algorithm to calculate the next move for the computer
def minimax(gameBoard, startQ, boardStatus, nextMoves):
    ##Giving a win away can be tested in the function, but wouldn't permanently remove the move.
    

    ##Removing all full columns from next moves
    for i in nextMoves:
        if boardStatus[i] == 6:
            nextMoves.remove(i)

    ##Creating minimax
    ##Temporary variables for testing
    testBoard = gameBoard
    testStatus = boardStatus
    testMoves = nextMoves

    ##Create a game tree of depth 6-ply (3 turns for each player)
    ##Depth will be the ply
    ##Start with neutral score values for each column
    colEvalScore = [0,0,0,0,0,0,0]
    for ply in range(6):
        ##If Computer turn
        if ply % 2 == 0:
            ##Establish max values for board evalutation for this turn
            maxVal = -100
            maxTurn = (-1,-1)
            
            ##Find the best next move for the Computer - i.e. results in the greatest positive value
            for testCol in testMoves:
                
                ##Simulate a move in each column
                testRow = testStatus[testCol]
                testBoard[testRow][testCol] = True

                ##Use evalBoard function to evaluate board position
                evalScore = evalBoard(True, testBoard, (testRow, testCol))

                ##Compare evaluation score to maximum values for this turn
                if evalScore > maxVal:
                    maxVal = evalScore
                    maxTurn = (testRow, testCol)

                ##Revert testBoard for next test
                testBoard[testRow][testCol] = '.'

            ##Update testBoard with maximum move for this turn (max for the computer)
            testBoard[maxTurn[0]][maxTurn[1]] = True
            testStatus[testCol] += 1

            ##Check maxVal for a win, so node is a leaf

            ##If this move fills a column, remove from testMoves
            if testStatus[testCol] == 6:
                testMoves.remove(testCol)
                

        ##Else if Player turn
        elif ply % 2 == 1:
            ##Establish min values for board evaluation for this turn
            minVal = 100
            minTurn = (-1,-1)
            
            ##Find the best next move for the player - i.e results in the lowest negative value
            for testCol in testMoves:

                ##Simulate a move in each column
                testRow = testStatus[testCol]
                testBoard[testRow][testCol] = False

                ##Use evalBoard to evaluate the board position
                evalScore = evalBoard(False, testBoard, (testRow, testCol))

                ##Compare evalution score to minimum values for this turn
                if evalScore < minVal:
                    minVal = evalScore
                    minTurn = (testRow, testCol)

                ##Revert testBoard for next test
                testBoard[testRow][testCol] = '.'

            ##Update testBoard with minimum move for this turn (max for the player)
            testBoard[minTurn[0]][minTurn[1]] = False
            testStatus[testCol] += 1

            ##Check minVal for a win, so node is a leaf

            ##If this move fills a column, remove from testMoves
            if testStatus[testCol] == 6:
                testMoves.remove(testCol)
    
    turn = random.randint(0,6)
    while turn not in nextMoves:
        turn = random.randint(0,6)

        
    return nextMoves [0], nextMoves

##Evaluates the board in any position using a set of heuristics - Positive result is a good position for computer, negative result is a good position for the player
def evalBoard(turnVal, testBoard, rowCol):
    ##Check for a win, which overrides all other heuristics
    pass


    
    

##Creating players for PvP
redPlayer = player(red, 'Red', True)
bluePlayer = player(blue, 'Blue', False)
players1 = [redPlayer, bluePlayer]
random.shuffle(players1)

##Creating players for PvAI
greenPlayer = player(green, 'Green', False)
compPlayer = player(orange, 'Computer', True)
players2 = [greenPlayer, compPlayer]
random.shuffle(players2)


        
play = True
while play:
    gameMode = input("Would you like to:\n1) Play against an opponent\n2) Play against an AI\n3) Quit\n")
    while gameMode not in {'1', '2', '3'}:
        gameMode = input("Would you like to:\n1) Play against an opponent\n2) Play against an AI\n3) Quit\n")
        

    ##Play against an opponent
    if gameMode == '1':
        
        ##Make board on screen
        makeBoard(screen)

        ##Game board
        gameBoard = makeGameBoard()
            

        ##Game condition
        finished = False

        ##Gameloop
        while not finished:
            pygame.event.get()
            for player in players1:
                print(player.name + " turn\n\n")
                
                choice, boardStatus = recieveGo(boardStatus)
                rowCol, gameBoard = makeToken(choice, gameBoard, player.turnVal, boardStatus)

                finishQ = fourCheck(gameBoard, rowCol, player.turnVal)

                pygame.display.flip()
                pygame.event.get()
                
                ##If game is over
                if finishQ:
                    print(player.name + " has won\n\n\n")
                    player.wins += 1
                    print("Wins\n" + redPlayer.name + ":", redPlayer.wins , "\n" + bluePlayer.name + ":" , bluePlayer.wins, "\n\n")
                    finished = True

                    ##Reset all variables to create blank slate for new game
                    random.shuffle(players1)
                    boardStatus = [0,0,0,0,0,0,0]
                    gameBoard = []

                    ##Erase tokens from screen
                    screen.fill(yellow)
                    break

    elif gameMode == '2':
        ##Make board on screen
        makeBoard(screen)

        ##Game board
        gameBoard = makeGameBoard()

        ##Is the AI starting?
        if players2[0] == redPlayer:
            startQ = False
        else:
            startQ = True

        ##Next possible moves for AI
        nextMoves = [0,1,2,3,4,5,6]

        
        ##Game condition
        finished = False

        ##Gameloop
        while not finished:
            pygame.event.get()
            for player in players2:
                print(player.name + " turn")
                ##If the player's turn
                if player.name == 'Green':
                    
                    choice, boardStatus = recieveGo(boardStatus)
                    rowCol, gameBoard = makeToken(choice, gameBoard, player.turnVal, boardStatus)

                    finishQ = fourCheck(gameBoard, rowCol, player.turnVal)

                    pygame.display.flip()
                    pygame.event.get()

                ##Else if the computer's turn
                elif player.name == 'Computer':
                    
                    ##Use minimax function to calculate turns

                    turn, nextMoves = minimax(gameBoard, startQ, boardStatus, nextMoves)

                    print(nextMoves)
                    
                    boardStatus[turn] += 1
                    rowCol, gameBoard = makeToken(turn, gameBoard, player.turnVal, boardStatus)

                    finishQ = fourCheck(gameBoard, rowCol, player.turnVal)

                    pygame.display.flip()
                    pygame.event.get()

                if finishQ:
                    print(player.name + " has won\n\n\n")
                    player.wins += 1
                    print("Wins\n" + greenPlayer.name + ":", greenPlayer.wins , "\n" + compPlayer.name + ":" , compPlayer.wins, "\n\n")
                    finished = True

                    ##Reset all variables to create blank slate for new game
                    random.shuffle(players2)
                    boardStatus = [0,0,0,0,0,0,0]
                    gameBoard = []

                    ##Erase tokens from screen
                    screen.fill(yellow)
                    break
                    

    elif gameMode == '3':
        exit

    else:
        print("Invalid entry")

##FinishQ for the player is not working, and need to fix update restricted moves for opponent winning positions

                
                
