import numpy as np
import math
import pygame
import sys
import random

ROWS = 6
COLS = 7

SQUARESIZE = 100

PLAYER = 1
AI = 2

WINDOW_LENGTH=4
EMPTY=0

WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
myfont = pygame.font.SysFont("monospace", 75)

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def draw_board(board):
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, 
                               (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    #if there is pieces in game state already
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, 
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                    int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, 
                                   (int(c * SQUARESIZE + SQUARESIZE / 2), 
                                    int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def draw_piece(board,row, col, turn, animate=False):
    color = RED if turn == PLAYER else YELLOW 
    
    # animation: gradually move the piece down
    if animate:
        for y in range(0, (row + 1) * SQUARESIZE, 5): 
            # redraw the board to prevent erasing existing pieces
            draw_board(board)
            
            # draw the dropping piece at the current y coordinate
            pygame.draw.circle(screen, color, 
                               (int(col * SQUARESIZE + SQUARESIZE / 2), 
                                int(y + SQUARESIZE / 2)), RADIUS)
            pygame.display.update()
            pygame.time.wait(30) 

    # draw the piece at its final position
    pygame.draw.circle(screen, color, 
                       (int(col * SQUARESIZE + SQUARESIZE / 2), 
                        int((row + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def draw_win_message(winner):
     # clear the top area
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE)) 
    text = f"{winner} WINS!!!"
    label = myfont.render(text, True, YELLOW if winner == "AI" else RED)
    #draw at top of screen
    screen.blit(label, (40, 10)) 
    pygame.display.update()
    pygame.time.wait(3000)

def highlight_column(col, color):
    pygame.draw.rect(screen, color, (col * SQUARESIZE, 0, SQUARESIZE, SQUARESIZE))
    pygame.display.update()

def visualize_move_evaluation(col, score):
    # highlight the column being evaluated
    highlight_column(col, (0, 255, 0))
    # display the score above the column
    label = myfont.render(str(score), True, (255, 255, 255))
    screen.blit(label, (col * SQUARESIZE + 10, 10))
    pygame.display.update()


def get_next_open_row_in_column(board, col_picked):
    # start from the bottom row, stops at 0(does not include -1), decrements by one
    for row in range(ROWS-1, -1, -1):  
        if board[row][col_picked] == 0: # check if the slot is empty
            return row  
    print("NO OPEN ROW AVAILABLE")
    return -1

def place_move(board, col_picked, turn):
   
    open_row = get_next_open_row_in_column(board, col_picked)
    if(open_row != -1):
        # record move on board (1 for player, 2 for AI)
        board[open_row][col_picked] = turn  
        # draw the piece on the board
        draw_piece(board,open_row, col_picked, turn, animate=False)
        return True # Move was successfully placed
    return False # Column is full, move not placed
    

#used by minimax to record a piece on the board without drawing the piece in the ui
def drop_move(board, col_picked, turn):
    open_row = get_next_open_row_in_column(board, col_picked)
    if(open_row != -1):
        board[open_row][col_picked] = turn  # Place the move (1 for player, 2 for AI)
        return True # move was successfully placed
    return False # column is full, move not placed

#checks to see if a piece can be placed in a column
def get_valid_columns(board):
    valid_columns = []
    for c in range(COLS):
        if(board[0][c] == 0):
            valid_columns.append(c)
    return valid_columns

def place_random_move(board, turn):
    valid_columns = get_valid_columns(board)
    rand_col_picked = random.choice(valid_columns)
    if place_move(board, rand_col_picked, turn): 
        print("Random move placed")
        return True
    else:
        print("Cant place random move")
        return False
        
def check_win_condition(board, turn):
    #check horizontal wins
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c]==turn and
                board[r][c+1]==turn and
                board[r][c+2] ==turn and
                board[r][c+3]== turn):
                return True
    #check vertical wins
    for r in range(ROWS-3):
        for c in range(COLS):
            if(board[r][c]==turn and
               board[r+1][c]==turn and
               board[r+2][c]== turn and
               board[r+3][c]== turn):
                return True
    #check for diagnial from bottom left to top right
    #start at 5,0 (bottom left of board) then (4,1) etc
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if(board[r][c] == turn and
               board[r+1][c+1]==turn and
               board[r+2][c+2]==turn and
               board[r+3][c+3]==turn):
                return True
    #check for diagnial from top left to bottom right
    # start at 5,6 (bottom right of board) then 
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if(board[r][c] == turn and
               board[r-1][c+1]==turn and
               board[r-2][c+2]==turn and
               board[r-3][c+3]==turn):
                return True
    return False

def switch_turn(turn):
    return AI if turn == PLAYER else PLAYER

def score_position(board, piece):
    score = 0

    # score centre column
    centre_array = [int(i) for i in list(board[:, COLS // 2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 3

    # score horizontal positions
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            # create a horizontal window of 4
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score vertical positions
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            # create a vertical window of 4
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score positive diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            # create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Ssore negative diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            # create a negative diagonal window of 4
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score
def evaluate_window(window, piece):
    score = 0
    # switch scoring based on turn
    opp_piece = PLAYER
    if piece == PLAYER:
        opp_piece = AI

    # prioritise a winning move
    if window.count(piece) == 4:
        score += 100
    # make connecting 3 second priority
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # make connecting 2 third priority
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    # prioritise blocking an opponent's winning move (but not over bot winning)
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def is_terminal_node(board):
    return check_win_condition(board, PLAYER) or check_win_condition(board, AI) or len(get_valid_columns(board)) == 0

# Implements the Minimax algorithm with Alpha-Beta pruning to determine the optimal move 
# for the AI in a Connect Four game.

# board: The current state of the game board.
# depth: The depth of the search tree (how many moves ahead we are considering).
# alpha: The best value that the maximizer can guarantee so far.
# beta: The best value that the minimizer can guarantee so far.
# maximisingPlayer: A boolean indicating whether we are maximizing or minimizing the score (True for maximizing, False for minimizing).

# returns the best column and score found

def minimax(board, depth, alpha, beta, maximisingPlayer):
    #get all columns that are not full
    valid_locations = get_valid_columns(board)

    #check if reached the end of game(terminal) or maximum search depth
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        #if the current state is terminal(meaning someone won or no valid moves left), then return a score based on the game outcome
        if is_terminal:
            # weight the bot winning really high
            if check_win_condition(board, AI):
                return (None, 9999999)
            # wight the human winning really low
            elif check_win_condition(board, PLAYER):
                return (None, -9999999)
            else:  # no more valid moves
                return (None, 0)
        # if it's not a terminal state but we reached the maximum depth, estimate the board's score
        # calls the score_position function to evaluate how good the board is for the AI.
        else:
            return (None, score_position(board, AI))

    #if it is the maximizing player's turn, the goal is to maximize the score:
    if maximisingPlayer:
        value = -9999999
        # randomise column to start
        column = random.choice(valid_locations)
        #iterates over each valid column, simulating a move.
        for col in valid_locations:
            # create a copy of the board
            b_copy = board.copy()
            # drop a piece in the temporary board and record score
            drop_move(b_copy, col, AI)

            #calls minimax recursively to evaluate the next state.
            #reduces the depth by 1.
            #switches to minimizing player for the next move.
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            #visualize_move_evaluation(col, new_score)  # Visualization
            #Update the best value and best column if the current move is better
            if new_score > value:
                value = new_score
                column = col
            #alpha is the best value the maximizer can achieve.
            #if alpha >= beta, it means that the minimizing player would not allow this branch to be chosen, so we can prune.
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # if it is the minimizing player's turn, the goal is to minimize the score
        value = 9999999
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            drop_move(b_copy, col, PLAYER)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            #visualize_move_evaluation(col, new_score)  # Visualization
            if new_score < value:
                value = new_score
                column = col
            #beta is the best value the minimizer can achieve.
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
def play_ai_move_using_minimax(board):
    # determine the best move using the minimax algorithm
    # depth = 7 is the most optimal. Decrease depth is ai speed is slow
    col, minimax_score = minimax(board, depth=6, alpha=-math.inf, beta=math.inf, maximisingPlayer=True)

    # if a valid column was found, place the move
    if col is not None and place_move(board, col, AI):
        print(f"AI placed move in column {col}")
        return True
    return False


def main():
    board = create_board()
    draw_board(board)
    game_over = False
    turn = PLAYER
    while not game_over: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(turn  == PLAYER):
                    posx = event.pos[0] # gets x coordinate
                    col = posx // SQUARESIZE #gets the col number from mouse click by floor division
                    if place_move(board, col, PLAYER):
                        print("Move Placed")
                        game_over = check_win_condition(board, PLAYER)
                        if(game_over):
                            print("PLAYER WINS!!!!!")
                            draw_win_message("Player")
                            break
                        else:
                            turn = AI
                    else: 
                        print("Column full")
                    if play_ai_move_using_minimax(board):
                        game_over = check_win_condition(board, AI)
                        if(game_over):
                            print(f"AI WINS!!!!!")
                            draw_win_message("AI")
                            break
                        else:
                            turn = PLAYER
    #show win screen
    if game_over:
        pygame.time.wait(3000)

        

if __name__ == "__main__":
    main()
