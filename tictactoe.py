
# Imports
import pygame, sys, random, ast, os
from pygame.locals import *

# Basic global variables
# Set up the size of the window and board
FPS = 30
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640
BOARD_WIDTH = 3
BOARD_HEIGHT = 3
SQUARE_SIZE = 150
X_MARGIN = 15
Y_MARGIN = 100

# Set up basic colors to be used
BG_COLOR = (100, 100, 100)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
TEXT_COLOR   = (  0,  50, 255)
TEXT_BG_COLOR = (255, 255, 255)

# Set up the starting buttons
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = WHITE
BUTTON1_X = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
BUTTON1_Y = 200
BUTTON2_X = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
BUTTON2_Y = 300
BUTTON3_X = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
BUTTON3_Y = 400

# Set up the board variables
X = [1]
O = [-1]

# Set up some variables to be used for dictionary training
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WIN_VALUE = 10
LOSS_VALUE = -10
TIE_VALUE = 0




def intro(): # The beginning function that allows the user to choose the mode

    # Begin the pygame instance
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('Tic-Tac-Toe')

    # The beginning loop that lets the user choose the mode
    while True:

        # Fill in the background and then set up the buttons
        DISPLAY_SURF.fill(BLACK)
        pygame.draw.rect(DISPLAY_SURF, BUTTON_COLOR, (BUTTON1_X, BUTTON1_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(DISPLAY_SURF, BUTTON_COLOR, (BUTTON2_X, BUTTON2_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(DISPLAY_SURF, BUTTON_COLOR, (BUTTON3_X, BUTTON3_Y, BUTTON_WIDTH, BUTTON_HEIGHT))

        # When the button is hovered over, it highlights into a different color
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if BUTTON1_X < mouse_x < BUTTON1_X + BUTTON_WIDTH and BUTTON1_Y < mouse_y < BUTTON1_Y + BUTTON_HEIGHT:
            pygame.draw.rect(DISPLAY_SURF, BUTTON_HOVER_COLOR, (BUTTON1_X, BUTTON1_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        if BUTTON2_X < mouse_x < BUTTON2_X + BUTTON_WIDTH and BUTTON2_Y < mouse_y < BUTTON2_Y + BUTTON_HEIGHT:
            pygame.draw.rect(DISPLAY_SURF, BUTTON_HOVER_COLOR, (BUTTON2_X, BUTTON2_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        if BUTTON3_X < mouse_x < BUTTON3_X + BUTTON_WIDTH and BUTTON3_Y < mouse_y < BUTTON3_Y + BUTTON_HEIGHT:
            pygame.draw.rect(DISPLAY_SURF, BUTTON_HOVER_COLOR, (BUTTON3_X, BUTTON3_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Adds text to the buttons
        button_text("P vs P", FONT, BUTTON_TEXT_COLOR, DISPLAY_SURF, BUTTON1_X + BUTTON_WIDTH // 2, BUTTON1_Y + BUTTON_HEIGHT // 2)
        button_text("P vs AI", FONT, BUTTON_TEXT_COLOR, DISPLAY_SURF, BUTTON2_X + BUTTON_WIDTH // 2, BUTTON2_Y + BUTTON_HEIGHT // 2)
        button_text("AI vs AI", FONT, BUTTON_TEXT_COLOR, DISPLAY_SURF, BUTTON3_X + BUTTON_WIDTH // 2, BUTTON3_Y + BUTTON_HEIGHT // 2)
        
        # Let the user choose the mode:
        # PVP: Both sides chosen by human
        # PVAI: X chosen by human, O chosen by AI
        # AIVAI: Both sides chosen by AI
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if BUTTON1_X < mouse_x < BUTTON1_X + BUTTON_WIDTH and BUTTON1_Y < mouse_y < BUTTON1_Y + BUTTON_HEIGHT:
                    main('PVP')
                elif BUTTON2_X < mouse_x < BUTTON2_X + BUTTON_WIDTH and BUTTON2_Y < mouse_y < BUTTON2_Y + BUTTON_HEIGHT:
                    main('PVAI')
                elif BUTTON3_X < mouse_x < BUTTON3_X + BUTTON_WIDTH and BUTTON3_Y < mouse_y < BUTTON3_Y + BUTTON_HEIGHT:
                    main('AIVAI')

        # Update the screen each frame
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
            
def main(game_type): # The main gameplay function

    # Set some more global variables
    global FPS_CLOCK, DISPLAY_SURF
    FONT = pygame.font.Font('freesansbold.ttf', 20)

    # Initialize the some variables, including the board and taken squares
    mouse_x = 0
    mouse_y = 0
    x_turn = True
    main_board = initialize_board()
    taken_squares = start_status(False)
    o_game_boards = []
    x_game_boards = []

    # Depending on user choice, defines some variables for input later
    if game_type == 'PVP':
        player_x = 'Human'
        player_o = 'Human'
    elif game_type == 'PVAI':
        player_x = 'Human'
        player_o = 'AI'
    elif game_type == 'AIVAI':
        player_x = 'AI'
        player_o = 'AI'

    # Main loop for gameplay
    while True:

        # Initialize the mouseclick and some board information
        mouse_clicked = False
        DISPLAY_SURF.fill(BLACK)

        # Draw the board
        draw_grid()
        draw_board(main_board, taken_squares)

        # Check to see if game is being quit, or if the mouse has been pressed
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        # Logic for the X player (X always goes first)
        if x_turn == True:
            # If the X player is human, get mouse input to determine which space
            if player_x == 'Human':
                square_x, square_y = get_square_at_pixel(mouse_x, mouse_y)
                if square_x != None and square_y != None and mouse_clicked:
                    if not taken_squares[square_x][square_y]:
                        taken_squares[square_x][square_y] = True
                        main_board[square_x][square_y] = [1]
                        x_turn = False
            # If the X player is an AI, get a move based on the AIX logic
            elif player_x == 'AI':
                square_x, square_y = get_ai_x_move(main_board)
                if not taken_squares[square_x][square_y]:
                    taken_squares[square_x][square_y] = True
                    main_board[square_x][square_y] = [1]
                    x_turn = False

            # Creates a list of the current values in the board that can be put into a board file later
            # Currently not being used
            board_state = []
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    if main_board[x][y] == [1]:
                        board_state.append(1)
                    elif main_board[x][y] == [-1]:
                        board_state.append(-1)
                    elif main_board[x][y] == [0]:
                        board_state.append(0)
            x_game_boards.append([board_state, 0])

        # Logic for O player
        elif x_turn == False:
            # If the O player is human, get mouse input to determine which space
            if player_o == 'Human':
                square_x, square_y = get_square_at_pixel(mouse_x, mouse_y)
                if square_x != None and square_y != None and mouse_clicked:
                    if not taken_squares[square_x][square_y]:
                        taken_squares[square_x][square_y] = True
                        main_board[square_x][square_y] = [-1]
                        x_turn = True
            # If the O player is an AI, use the board logic to choose a move
            elif player_o == 'AI':
                square_x, square_y = get_ai_o_move(main_board)
                if not taken_squares[square_x][square_y]:
                    taken_squares[square_x][square_y] = True
                    main_board[square_x][square_y] = [-1]
                    x_turn = True

            # Creates a list of the boards that can be used to write to the dictionary file
            board_state = []
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    if main_board[x][y] == [1]:
                        board_state.append(1)
                    elif main_board[x][y] == [-1]:
                        board_state.append(-1)
                    elif main_board[x][y] == [0]:
                        board_state.append(0)
            o_game_boards.append([board_state, 0])

        # Check for a win or tie
        board_data = []
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                if main_board[x][y] == [1]:
                    board_data.append(1)
                elif main_board[x][y] == [-1]:
                    board_data.append(-1)
                elif main_board[x][y] == [0]:
                    board_data.append(0)
        check_win = check_for_win(board_data)
        # If there is a win or tie, end the game and write the result on the screen
        if check_win != False:
            if check_win == 'X':
                win_text = 'X Wins!'
                # Update the values of the board dictionary based on the result
                if player_o == 'AI':
                    for i in range(len(o_game_boards)):
                        o_game_boards[i][1] = LOSS_VALUE
            elif check_win == 'O':
                win_text = 'O Wins!'
                if player_o == 'AI':
                    for i in range(len(o_game_boards)):
                        o_game_boards[i][1] = WIN_VALUE
            elif check_win == 'Tie':
                win_text = 'It\'s a Tie!'
                if player_o == 'AI':
                    for i in range(len(o_game_boards)):
                        o_game_boards[i][1] = TIE_VALUE

            # Write the board dictionary to the file and update the values, then reset the dictionary
            write_o_boards_to_file(o_game_boards)
            o_game_boards = []

            # Draw the result to the screen
            text_surf = FONT.render(win_text, True, WHITE, BLACK)
            text_rect = text_surf.get_rect()
            text_rect.center = (int(WINDOW_WIDTH / 2), int(Y_MARGIN / 2))
            DISPLAY_SURF.blit(text_surf, text_rect)
            draw_board(main_board, taken_squares)
            pygame.display.update()

            # If both players are AI, don't wait so training is sped up
            if player_x != 'AI' or player_o != 'AI':
                pygame.time.wait(1000)
            # Reset everything and start over
            main_board = initialize_board()
            taken_squares = start_status(False)
            x_turn = True

        # Update display each frame
        pygame.display.update()
        FPS_CLOCK.tick(FPS)




def initialize_board(): # Sets up the board with blanks in each space
    main_board = []
    for _ in range(BOARD_WIDTH):
        column = []
        for _ in range(BOARD_HEIGHT):
            column.append([0])
        main_board.append(column)
    return main_board

def start_status(val): # Sets up the list of taken squares where each is not taken
    taken_squares = []
    for _ in range(BOARD_WIDTH):
        taken_squares.append([val] * BOARD_HEIGHT)
    return taken_squares

def draw_grid(): # Draws the grid on the board
    for x in range(BOARD_WIDTH + 1):
        pygame.draw.line(DISPLAY_SURF, WHITE, (X_MARGIN + (SQUARE_SIZE * (x)), Y_MARGIN), (X_MARGIN + (SQUARE_SIZE * (x)), Y_MARGIN + (SQUARE_SIZE * BOARD_HEIGHT)), 3)
    for y in range(BOARD_HEIGHT + 1):
        pygame.draw.line(DISPLAY_SURF, WHITE, (X_MARGIN, Y_MARGIN + (SQUARE_SIZE * (y))), (X_MARGIN + (SQUARE_SIZE * BOARD_WIDTH), Y_MARGIN + (SQUARE_SIZE * (y))), 3)
    return

def draw_board(main_board, taken_squares): # Draws the shape on each of the appropriate spaces
    for square_x in range(BOARD_WIDTH):
        for square_y in range(BOARD_HEIGHT):
            if taken_squares[square_x][square_y]:
                shape = get_shape(main_board, square_x, square_y)
                draw_shape(shape, square_x, square_y)

def get_shape(board, square_x, square_y): # Returns the shape at each space
    return board[square_x][square_y]

def draw_shape(shape, square_x, square_y): # Draws the actual shape at the appropriate space
    left, top = left_top_coords_of_square(square_x, square_y)

    if shape == X:
        pygame.draw.line(DISPLAY_SURF, WHITE, (left+5, top+5), (left+145, top+145), 5)
        pygame.draw.line(DISPLAY_SURF, WHITE, (left+145, top+5), (left+5, top+145), 5)
    if shape == O:
        pygame.draw.circle(DISPLAY_SURF, WHITE, (left+75, top+75), 70)
        pygame.draw.circle(DISPLAY_SURF, BLACK, (left+75, top+75), 65)

def left_top_coords_of_square(square_x, square_y): # Returns the upper left corner of the requested square
    left = square_x * (SQUARE_SIZE) + X_MARGIN
    top = square_y * (SQUARE_SIZE) + Y_MARGIN
    return (left, top)

def get_square_at_pixel(x, y): # Returns which square is at the provided pixel
    for square_x in range(BOARD_WIDTH):
        for square_y in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_square(square_x, square_y)
            square_rect = pygame.Rect(left, top, SQUARE_SIZE, SQUARE_SIZE)
            if square_rect.collidepoint(x, y):
                return (square_x, square_y)
    return (None, None)

def check_for_win(board): # Determines if the game has been won by a player, or if the game is a tie

    # Gets the values of each row, column, and diagonal of the board
    board_total = total_board(board)

    # If any of the values is 3 or -3, then that row/column/diagonal is either all X or all O, so that player wins
    for x in range(len(board_total)):
        if board_total[x] == 3:
            return 'X'
        elif board_total[x] == -3:
            return 'O'

    # If every spacec on the board has a symbol on it and there isn't a winner, the game is a tie        
    board_total = 0
    for x in range(len(board)):
        if board[x] != 0:
            board_total += 1
    if board_total == 9:
        return 'Tie'
    
    return False

def total_board(board): # Totals the value of each row/column/diagonal

    board_total = []

    # Checks each column
    board_total.append(board[0] + board[1] + board[2])
    board_total.append(board[3] + board[4] + board[5])
    board_total.append(board[6] + board[7] + board[8])
    # Checks each row
    board_total.append(board[0] + board[3] + board[6])
    board_total.append(board[1] + board[4] + board[7])
    board_total.append(board[2] + board[5] + board[8])
    # Checks the diagonals
    board_total.append(board[0] + board[4] + board[8])
    board_total.append(board[2] + board[4] + board[6])

    return board_total

def button_text(text, font, color, surface, x, y): # Writes the text to the intro buttons
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def get_random_move(board): # Returns a random move of the available spaces

    random_move = []
    for x in range(BOARD_HEIGHT):
        for y in range(BOARD_WIDTH):
            if board[x][y] == [0]:
                random_move.append((x, y))
    return random.choice(random_move)

def get_ai_x_move(board): # Returns a move based on simple choices similar to a human

    # Creates a list of the current values in each space
    board_data = []

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == [1]:
                board_data.append(1)
            elif board[x][y] == [-1]:
                board_data.append(-1)
            elif board[x][y] == [0]:
                board_data.append(0)

    # Create a value list of potential moves
    move_choice = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(board_data)):
        # If the space is taken, it is effectively removed
        if board_data[i] != 0:
            move_choice[i] = -100000000
        else: 
            # If the space would create a win, take that space
            board_data[i] = 1
            check_win = check_for_win(board_data)
            if check_win == 'X':
                move_choice[i] = 100000000
            # If the space would let the opponent win, take that space to block
            board_data[i] = -1
            check_win = check_for_win(board_data)
            if check_win == 'O' and move_choice[i] == 0:
                move_choice[i] = 10000
            board_data[i] = 0

    # If there is no guaranteed win or block, return a random empty space
    if max(move_choice) == 0:
        return get_random_move(board)
    # Otherwise pick the best space
    else:
        best_move = move_choice.index(max(move_choice))

    # Return the coordinates rather than just the list index
    if best_move < 3:
        return (0, best_move)
    elif best_move < 6:
        return (1, best_move - 3)
    else:
        return (2, best_move - 6)

def get_ai_o_move(board): # Returns a move based on the external data file

    # Creates a list of the current values for each space
    board_data = []

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_WIDTH):
            if board[x][y] == [1]:
                board_data.append(1)
            elif board[x][y] == [-1]:
                board_data.append(-1)
            elif board[x][y] == [0]:
                board_data.append(0)

    # Opens the appropriate data file that holds all the potential moves
    o_file = 'oBoards.txt'
    file_path = os.path.join(CURRENT_DIRECTORY, o_file)

    # Creates a dictionary of board states that have a key of a board state and a value of how good it is
    board_file = open(file_path, 'r')
    board_dictionary = ast.literal_eval(board_file.read())

    # Create a value list of potential moves
    move_choice = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(board_data)):
        # If the space is already taken, effectively remove it from the list
        if board_data[i] == 1 or board_data[i] == -1:
            move_choice[i] = -100000000
        else:
            # For each potential move, find the associated dictionary value and insert it into the potential moves
            board_data[i] = -1
            move_choice[i] = board_dictionary.get(str(board_data))
            if move_choice[i] == None:
                move_choice[i] = 0
            board_data[i] = 0

    # If there is no guaranteed win or block, return a random empty space
    if max(move_choice) == 0:
        return get_random_move(board)
    # Otherwise pick the best space
    else:
        best_move = move_choice.index(max(move_choice))

    # Return the coordinates rather than just the list index
    if best_move < 3:
        return (0, best_move)
    elif best_move < 6:
        return (1, best_move - 3)
    else:
        return (2, best_move - 6)
    
def write_o_boards_to_file(o_game_boards): # Writes the boards of each game to the board dictionary

    # Opens and creates a dictionary from the list of boards
    o_file = 'oBoards.txt'
    file_path = os.path.join(CURRENT_DIRECTORY, o_file)
    board_file = open(file_path, 'r+')
    board_dictionary = ast.literal_eval(board_file.read())

    # Adds the boards from current game into the dictionary
    for i in range(len(o_game_boards)):
        # If the board is already found, just add the value
        if str(o_game_boards[i][0]) in board_dictionary:
            board_dictionary[str(o_game_boards[i][0])] = board_dictionary[str(o_game_boards[i][0])] + o_game_boards[i][1]
        # Otherwise add the board to the dictionary
        else:
            board_dictionary[str(o_game_boards[i][0])] = o_game_boards[i][1]

    # Write the new dictionary to the file and close it
    board_file.seek(0)
    board_file.truncate()
    board_file.write(str(board_dictionary))
    board_file.close()

    return False




if __name__ == '__main__':
    intro()