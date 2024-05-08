
# Imports
import pygame, sys, random, ast, os
from pygame.locals import *

# Basic global variables
# Set up the size of the window and board
FPS = 30
WINDOWWIDTH = 480
WINDOWHEIGHT = 640
BOARDWIDTH = 3
BOARDHEIGHT = 3
SQUARESIZE = 150
XMARGIN = 15
YMARGIN = 100

# Set up basic colors to be used
BGCOLOR = (100, 100, 100)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
TEXTCOLOR   = (  0,  50, 255)
TEXTBGCOLOR = (255, 255, 255)

# Set up the starting buttons
BUTTONWIDTH = 200
BUTTONHEIGHT = 50
BUTTONCOLOR = (100, 100, 100)
BUTTONHOVERCOLOR = (150, 150, 150)
BUTTONTEXTCOLOR = WHITE
BUTTON1_X = (WINDOWWIDTH - BUTTONWIDTH) // 2
BUTTON1_Y = 200
BUTTON2_X = (WINDOWWIDTH - BUTTONWIDTH) // 2
BUTTON2_Y = 300
BUTTON3_X = (WINDOWWIDTH - BUTTONWIDTH) // 2
BUTTON3_Y = 400

# Set up the board variables
X = [1]
O = [-1]

# Set up some variables to be used for dictionary training
CURRENTDIRECTORY = os.path.dirname(os.path.abspath(__file__))
WINVALUE = 10
LOSSVALUE = -10
TIEVALUE = 0




def Intro(): # The beginning function that allows the user to choose the mode

    # Begin the pygame instance
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('Tic-Tac-Toe')

    # The beginning loop that lets the user choose the mode
    while True:

        # Fill in the background and then set up the buttons
        DISPLAYSURF.fill(BLACK)
        pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, (BUTTON1_X, BUTTON1_Y, BUTTONWIDTH, BUTTONHEIGHT))
        pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, (BUTTON2_X, BUTTON2_Y, BUTTONWIDTH, BUTTONHEIGHT))
        pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, (BUTTON3_X, BUTTON3_Y, BUTTONWIDTH, BUTTONHEIGHT))

        # When the button is hovered over, it highlights into a different color
        mousex, mousey = pygame.mouse.get_pos()
        if BUTTON1_X < mousex < BUTTON1_X + BUTTONWIDTH and BUTTON1_Y < mousey < BUTTON1_Y + BUTTONHEIGHT:
            pygame.draw.rect(DISPLAYSURF, BUTTONHOVERCOLOR, (BUTTON1_X, BUTTON1_Y, BUTTONWIDTH, BUTTONHEIGHT))
        if BUTTON2_X < mousex < BUTTON2_X + BUTTONWIDTH and BUTTON2_Y < mousey < BUTTON2_Y + BUTTONHEIGHT:
            pygame.draw.rect(DISPLAYSURF, BUTTONHOVERCOLOR, (BUTTON2_X, BUTTON2_Y, BUTTONWIDTH, BUTTONHEIGHT))
        if BUTTON3_X < mousex < BUTTON3_X + BUTTONWIDTH and BUTTON3_Y < mousey < BUTTON3_Y + BUTTONHEIGHT:
            pygame.draw.rect(DISPLAYSURF, BUTTONHOVERCOLOR, (BUTTON3_X, BUTTON3_Y, BUTTONWIDTH, BUTTONHEIGHT))
        
        # Adds text to the buttons
        buttonText("P vs P", FONT, BUTTONTEXTCOLOR, DISPLAYSURF, BUTTON1_X + BUTTONWIDTH // 2, BUTTON1_Y + BUTTONHEIGHT // 2)
        buttonText("P vs AI", FONT, BUTTONTEXTCOLOR, DISPLAYSURF, BUTTON2_X + BUTTONWIDTH // 2, BUTTON2_Y + BUTTONHEIGHT // 2)
        buttonText("AI vs AI", FONT, BUTTONTEXTCOLOR, DISPLAYSURF, BUTTON3_X + BUTTONWIDTH // 2, BUTTON3_Y + BUTTONHEIGHT // 2)
        
        # Let the user choose the mode:
        # PVP: Both sides chosen by human
        # PVAI: X chosen by human, O chosen by AI
        # AIVAI: Both sides chosen by AI
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if BUTTON1_X < mousex < BUTTON1_X + BUTTONWIDTH and BUTTON1_Y < mousey < BUTTON1_Y + BUTTONHEIGHT:
                    main('PVP')
                elif BUTTON2_X < mousex < BUTTON2_X + BUTTONWIDTH and BUTTON2_Y < mousey < BUTTON2_Y + BUTTONHEIGHT:
                    main('PVAI')
                elif BUTTON3_X < mousex < BUTTON3_X + BUTTONWIDTH and BUTTON3_Y < mousey < BUTTON3_Y + BUTTONHEIGHT:
                    main('AIVAI')

        # Update the screen each frame
        pygame.display.update()
        FPSCLOCK.tick(FPS)
            
def main(gameType): # The main gameplay function

    # Set some more global variables
    global FPSCLOCK, DISPLAYSURF
    FONT = pygame.font.Font('freesansbold.ttf', 20)

    # Initialize the some variables, including the board and taken squares
    mousex = 0
    mousey = 0
    xTurn = True
    mainBoard = initializeBoard()
    takenSquares = startStatus(False)
    oGameBoards = []
    xGameBoards = []

    # Depending on user choice, defines some variables for input later
    if gameType == 'PVP':
        playerX = 'Human'
        playerO = 'Human'
    elif gameType == 'PVAI':
        playerX = 'Human'
        playerO = 'AI'
    elif gameType == 'AIVAI':
        playerX = 'AI'
        playerO = 'AI'

    # Main loop for gameplay
    while True:

        # Initialize the mouseclick and some board information
        mouseClicked = False
        DISPLAYSURF.fill(BLACK)

        # Draw the board
        drawGrid()
        drawBoard(mainBoard, takenSquares)

        # Check to see if game is being quit, or if the mouse has been pressed
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        # Logic for the X player (X always goes first)
        if xTurn == True:
            # If the X player is human, get mouse input to determine which space
            if playerX == 'Human':
                squarex, squarey = getSquareAtPixel(mousex, mousey)
                if squarex != None and squarey != None and mouseClicked:
                    if not takenSquares[squarex][squarey]:
                        takenSquares[squarex][squarey] = True
                        mainBoard[squarex][squarey] = [1]
                        xTurn = False
            # If the X player is an AI, get a move based on the AIX logic
            elif playerX == 'AI':
                squarex, squarey = getAIXMove(mainBoard)
                if not takenSquares[squarex][squarey]:
                    takenSquares[squarex][squarey] = True
                    mainBoard[squarex][squarey] = [1]
                    xTurn = False

            # Creates a list of the current values in the board that can be put into a board file later
            # Currently not being used
            boardState = []
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    if mainBoard[x][y] == [1]:
                        boardState.append(1)
                    elif mainBoard[x][y] == [-1]:
                        boardState.append(-1)
                    elif mainBoard[x][y] == [0]:
                        boardState.append(0)
            xGameBoards.append([boardState, 0])

        # Logic for O player
        elif xTurn == False:
            # If the O player is human, get mouse input to determine which space
            if playerO == 'Human':
                squarex, squarey = getSquareAtPixel(mousex, mousey)
                if squarex != None and squarey != None and mouseClicked:
                    if not takenSquares[squarex][squarey]:
                        takenSquares[squarex][squarey] = True
                        mainBoard[squarex][squarey] = [-1]
                        xTurn = True
            # If the O player is an AI, use the board logic to choose a move
            elif playerO == 'AI':
                squarex, squarey = getAIOMove(mainBoard)
                if not takenSquares[squarex][squarey]:
                    takenSquares[squarex][squarey] = True
                    mainBoard[squarex][squarey] = [-1]
                    xTurn = True

            # Creates a list of the boards that can be used to write to the dictionary file
            boardState = []
            for x in range(BOARDWIDTH):
                for y in range(BOARDHEIGHT):
                    if mainBoard[x][y] == [1]:
                        boardState.append(1)
                    elif mainBoard[x][y] == [-1]:
                        boardState.append(-1)
                    elif mainBoard[x][y] == [0]:
                        boardState.append(0)
            oGameBoards.append([boardState, 0])

        # Check for a win or tie
        boardData = []
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if mainBoard[x][y] == [1]:
                    boardData.append(1)
                elif mainBoard[x][y] == [-1]:
                    boardData.append(-1)
                elif mainBoard[x][y] == [0]:
                    boardData.append(0)
        checkWin = checkForWin(boardData)
        # If there is a win or tie, end the game and write the result on the screen
        if checkWin != False:
            if checkWin == 'X':
                winText = 'X Wins!'
                # Update the values of the board dictionary based on the result
                if playerO == 'AI':
                    for i in range(len(oGameBoards)):
                        oGameBoards[i][1] = LOSSVALUE
            elif checkWin == 'O':
                winText = 'O Wins!'
                if playerO == 'AI':
                    for i in range(len(oGameBoards)):
                        oGameBoards[i][1] = WINVALUE
            elif checkWin == 'Tie':
                winText = 'It\'s a Tie!'
                if playerO == 'AI':
                    for i in range(len(oGameBoards)):
                        oGameBoards[i][1] = TIEVALUE

            # Write the board dictionary to the file and update the values, then reset the dictionary
            writeOBoardsToFile(oGameBoards)
            oGameBoards = []

            # Draw the result to the screen
            textSurf = FONT.render(winText, True, WHITE, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = (int(WINDOWWIDTH / 2), int(YMARGIN / 2))
            DISPLAYSURF.blit(textSurf, textRect)
            drawBoard(mainBoard, takenSquares)
            pygame.display.update()

            # If both players are AI, don't wait so training is sped up
            if playerX != 'AI' or playerO != 'AI':
                pygame.time.wait(1000)
            # Reset everything and start over
            mainBoard = initializeBoard()
            takenSquares = startStatus(False)
            xTurn = True

        # Update display each frame
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def initializeBoard(): # Sets up the board with blanks in each space
    mainBoard = []
    for _ in range(BOARDWIDTH):
        column = []
        for _ in range(BOARDHEIGHT):
            column.append([0])
        mainBoard.append(column)
    return mainBoard

def startStatus(val): # Sets up the list of taken squares where each is not taken
    takenSquares = []
    for _ in range(BOARDWIDTH):
        takenSquares.append([val] * BOARDHEIGHT)
    return takenSquares

def drawGrid(): # Draws the grid on the board
    for x in range(BOARDWIDTH + 1):
        pygame.draw.line(DISPLAYSURF, WHITE, (XMARGIN + (SQUARESIZE * (x)), YMARGIN), (XMARGIN + (SQUARESIZE * (x)), YMARGIN + (SQUARESIZE * BOARDHEIGHT)), 3)
    for y in range(BOARDHEIGHT + 1):
        pygame.draw.line(DISPLAYSURF, WHITE, (XMARGIN, YMARGIN + (SQUARESIZE * (y))), (XMARGIN + (SQUARESIZE * BOARDWIDTH), YMARGIN + (SQUARESIZE * (y))), 3)
    return

def drawBoard(mainBoard, takenSquares): # Draws the shape on each of the appropriate spaces
    for squarex in range(BOARDWIDTH):
        for squarey in range(BOARDHEIGHT):
            if takenSquares[squarex][squarey]:
                shape = getShape(mainBoard, squarex, squarey)
                drawShape(shape, squarex, squarey)

def getShape(board, squarex, squarey): # Returns the shape at each space
    return board[squarex][squarey]

def drawShape(shape, squarex, squarey): # Draws the actual shape at the appropriate space
    left, top = leftTopCoordsOfSquare(squarex, squarey)

    if shape == X:
        pygame.draw.line(DISPLAYSURF, WHITE, (left+5, top+5), (left+145, top+145), 5)
        pygame.draw.line(DISPLAYSURF, WHITE, (left+145, top+5), (left+5, top+145), 5)
    if shape == O:
        pygame.draw.circle(DISPLAYSURF, WHITE, (left+75, top+75), 70)
        pygame.draw.circle(DISPLAYSURF, BLACK, (left+75, top+75), 65)

def leftTopCoordsOfSquare(squarex, squarey): # Returns the upper left corner of the requested square
    left = squarex * (SQUARESIZE) + XMARGIN
    top = squarey * (SQUARESIZE) + YMARGIN
    return (left, top)

def getSquareAtPixel(x, y): # Returns which square is at the provided pixel
    for squarex in range(BOARDWIDTH):
        for squarey in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfSquare(squarex, squarey)
            squareRect = pygame.Rect(left, top, SQUARESIZE, SQUARESIZE)
            if squareRect.collidepoint(x, y):
                return (squarex, squarey)
    return (None, None)

def checkForWin(board): # Determines if the game has been won by a player, or if the game is a tie

    # Gets the values of each row, column, and diagonal of the board
    boardTotal = totalBoard(board)

    # If any of the values is 3 or -3, then that row/column/diagonal is either all X or all O, so that player wins
    for x in range(len(boardTotal)):
        if boardTotal[x] == 3:
            return 'X'
        elif boardTotal[x] == -3:
            return 'O'

    # If every spacec on the board has a symbol on it and there isn't a winner, the game is a tie        
    board_total = 0
    for x in range(len(board)):
        if board[x] != 0:
            board_total += 1
    if board_total == 9:
        return 'Tie'
    
    return False

def totalBoard(board): # Totals the value of each row/column/diagonal

    boardTotal = []

    # Checks each column
    boardTotal.append(board[0] + board[1] + board[2])
    boardTotal.append(board[3] + board[4] + board[5])
    boardTotal.append(board[6] + board[7] + board[8])
    # Checks each row
    boardTotal.append(board[0] + board[3] + board[6])
    boardTotal.append(board[1] + board[4] + board[7])
    boardTotal.append(board[2] + board[5] + board[8])
    # Checks the diagonals
    boardTotal.append(board[0] + board[4] + board[8])
    boardTotal.append(board[2] + board[4] + board[6])

    return boardTotal

def buttonText(text, font, color, surface, x, y): # Writes the text to the intro buttons
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def getRandomMove(board): # Returns a random move of the available spaces

    randomMove = []
    for x in range(BOARDHEIGHT):
        for y in range(BOARDWIDTH):
            if board[x][y] == [0]:
                randomMove.append((x, y))
    return random.choice(randomMove)

def getAIXMove(board): # Returns a move based on simple choices similar to a human

    # Creates a list of the current values in each space
    boardData = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == [1]:
                boardData.append(1)
            elif board[x][y] == [-1]:
                boardData.append(-1)
            elif board[x][y] == [0]:
                boardData.append(0)

    # Create a value list of potential moves
    moveChoice = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(boardData)):
        # If the space is taken, it is effectively removed
        if boardData[i] != 0:
            moveChoice[i] = -100000000
        else: 
            # If the space would create a win, take that space
            boardData[i] = 1
            checkWin = checkForWin(boardData)
            if checkWin == 'X':
                moveChoice[i] = 100000000
            # If the space would let the opponent win, take that space to block
            boardData[i] = -1
            checkWin = checkForWin(boardData)
            if checkWin == 'O' and moveChoice[i] == 0:
                moveChoice[i] = 10000
            boardData[i] = 0

    # If there is no guaranteed win or block, return a random empty space
    if max(moveChoice) == 0:
        return getRandomMove(board)
    # Otherwise pick the best space
    else:
        bestMove = moveChoice.index(max(moveChoice))

    # Return the coordinates rather than just the list index
    if bestMove < 3:
        return (0, bestMove)
    elif bestMove < 6:
        return (1, bestMove - 3)
    else:
        return (2, bestMove - 6)

def getAIOMove(board): # Returns a move based on the external data file

    # Creates a list of the current values for each space
    boardData = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDWIDTH):
            if board[x][y] == [1]:
                boardData.append(1)
            elif board[x][y] == [-1]:
                boardData.append(-1)
            elif board[x][y] == [0]:
                boardData.append(0)

    # Opens the appropriate data file that holds all the potential moves
    oFile = 'oBoards.txt'
    file_path = os.path.join(CURRENTDIRECTORY, oFile)

    # Creates a dictionary of board states that have a key of a board state and a value of how good it is
    boardFile = open(file_path, 'r')
    boardDictionary = ast.literal_eval(boardFile.read())

    # Create a value list of potential moves
    moveChoice = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(boardData)):
        # If the space is already taken, effectively remove it from the list
        if boardData[i] == 1 or boardData[i] == -1:
            moveChoice[i] = -100000000
        else:
            # For each potential move, find the associated dictionary value and insert it into the potential moves
            boardData[i] = -1
            moveChoice[i] = boardDictionary.get(str(boardData))
            if moveChoice[i] == None:
                moveChoice[i] = 0
            boardData[i] = 0

    # If there is no guaranteed win or block, return a random empty space
    if max(moveChoice) == 0:
        return getRandomMove(board)
    # Otherwise pick the best space
    else:
        bestMove = moveChoice.index(max(moveChoice))

    # Return the coordinates rather than just the list index
    if bestMove < 3:
        return (0, bestMove)
    elif bestMove < 6:
        return (1, bestMove - 3)
    else:
        return (2, bestMove - 6)
    
def writeOBoardsToFile(oGameBoards): # Writes the boards of each game to the board dictionary

    # Opens and creates a dictionary from the list of boards
    oFile = 'oBoards.txt'
    file_path = os.path.join(CURRENTDIRECTORY, oFile)
    boardFile = open(file_path, 'r+')
    boardDictionary = ast.literal_eval(boardFile.read())

    # Adds the boards from current game into the dictionary
    for i in range(len(oGameBoards)):
        # If the board is already found, just add the value
        if str(oGameBoards[i][0]) in boardDictionary:
            boardDictionary[str(oGameBoards[i][0])] = boardDictionary[str(oGameBoards[i][0])] + oGameBoards[i][1]
        # Otherwise add the board to the dictionary
        else:
            boardDictionary[str(oGameBoards[i][0])] = oGameBoards[i][1]

    # Write the new dictionary to the file and close it
    boardFile.seek(0)
    boardFile.truncate()
    boardFile.write(str(boardDictionary))
    boardFile.close()

    return False




if __name__ == '__main__':
    Intro()