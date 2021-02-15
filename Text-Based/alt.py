import numpy as np
import random
import math

##Globals
ROW_COUNT = 6
COL_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2



def set_board():
    return np.zeros((ROW_COUNT, COL_COUNT))

def play_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_move(board, col):
    try:
        return board[ROW_COUNT -1][col] == EMPTY
    except:
        return False

def get_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == EMPTY:
            return row

def output(board):
    print("------------------------------")
    for row in np.flip(board,0):
        print(end = "|")
        for col in row:
            if col == AI_PIECE:
                char = ' # '
            elif col == PLAYER_PIECE:
                char = ' @ '
            else:
                char = '   '
            print(char, end = "|")
        print("\n------------------------------")    


def check_win(board, piece): ##Optimise later
    ##Check horizontal
    for col in range(COL_COUNT -3):
        for row in range(ROW_COUNT):
            if (board[row][col] == piece and
                board[row][col+1] == piece and
                board[row][col+2] == piece and
                board[row][col+3] == piece
            ):
                return True

    ##Check vertical
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT -3):
            if (board[row][col] == piece and
                board[row+1][col] == piece and
                board[row+2][col] == piece and
                board[row+3][col] == piece
            ):
                return True

    ##Check forward diagonals
    for col in range(COL_COUNT -3):
        for row in range(ROW_COUNT -3):
            if (board[row][col] == piece and
                board[row+1][col+1] == piece and
                board[row+2][col+2] == piece and
                board[row+3][col+3] == piece
            ): 
                return True

    ##Check backward diagonals
    for col in range(COL_COUNT -3):
        for row in range(3,ROW_COUNT):
            if (board[row][col] == piece and
                board[row-1][col+1] == piece and
                board[row-2][col+2] == piece and
                board[row-3][col+3] == piece
            ):
                return True

def heuristic_eval(board, piece): ##Optimise later
    score = 0 

    ##Score centre column -> preference for centre play
    centre_array = [int(i) for i in list(board[:, COL_COUNT//2])]
    centre_count = centre_array.count(piece)
    score += 100 * centre_count

    ##Score horizontals
    for row in range(ROW_COUNT):
        row = [int(i) for i in list(board[row, :])]
        for col in range(COL_COUNT -3):
            window = row[col : col+3]
            score += evaluate_window(window, piece)

    ##Score verticals
    for col in range(COL_COUNT):
        col = [int(i) for i in list(board[: ,col])]
        for row in range(ROW_COUNT -3):
            window = col[row : row+3]
            score += evaluate_window(window, piece)

    ##Score forward diagonals
    for row in range(ROW_COUNT -3):
        for col in range(COL_COUNT -3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)

    ##Score backward diagonals
    for row in range(ROW_COUNT -3):
        for col in range(COL_COUNT -3):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, curr_piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if curr_piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    
    ##Window contains a win for current player
    if window.count(curr_piece) == 4:
        score += 100
    ##3 pieces in window,1 empty
    elif window.count(curr_piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    ##2 pieces in window, 2 empty
    elif window.count(curr_piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    ##Opponent can win on their next turn
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score

def is_terminal_node(state):
    return (check_win(state, PLAYER_PIECE) or 
            check_win(state, AI_PIECE) or 
            len(get_valid_moves(state)) == 0
    )

def get_valid_moves(state):
    moves = []
    for col in range(COL_COUNT):
        if is_valid_move(state, col):
            moves.append(col)
    return moves

##Returns a (move, eval) tuple
def minimax(board, depth, alpha, beta, is_max):
    ##print(depth)
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            ##AI wins
            if check_win(board, AI_PIECE):
                return (None, 1000000-depth)
            ##Player wins
            elif check_win(board, PLAYER_PIECE):
                return (None, -1000000+depth)
            ##Game is drawn
            else:
                return (None, 0)
        ##Reached maximum search depth
        else:
            return (None, heuristic_eval(board, AI_PIECE))

    if is_max:
        best_eval = -math.inf
        best_move = random.choice(valid_moves)
        for col in valid_moves:
            row = get_row(board, col)
            copy = board.copy()
            play_piece(copy, row, col, AI_PIECE)
            move_eval = minimax(copy, depth-1, alpha, beta, False)[1]

            if move_eval > best_eval:
                best_eval = move_eval
                best_move = col
            
            alpha = max(alpha,best_eval)
            if beta <= alpha:
                break
        
        return (best_move, best_eval)
    
    elif not is_max:
        best_eval = math.inf
        best_move = random.choice(valid_moves)
        for col in valid_moves:
            row = get_row(board, col)
            copy = board.copy()
            play_piece(copy, row, col, PLAYER_PIECE)
            move_eval = minimax(copy, depth-1, alpha, beta, True)[1]

            if move_eval < best_eval:
                best_eval = move_eval
                best_move = col
            
            beta = min(beta, best_eval)
            if beta <= alpha:
                break
                
        return (best_move, best_eval)

def main():
    board = set_board()
    game_over = False
    turn = random.randint(PLAYER, AI)
    output(board)
    while not game_over:
        if turn == PLAYER:
            ##Validate column choice
            while True:
                try:
                    choice = int(input("Enter column (1-7): ")) -1
                except ValueError:
                    print("Enter a number")
                    continue

                if not is_valid_move(board, PLAYER_PIECE):
                    print("Enter a valid move")
                    continue
                break
            row = get_row(board, choice)
            play_piece(board, row, choice, PLAYER_PIECE)

            if check_win(board, PLAYER_PIECE):
                print("Player wins")
                game_over = True
            
            
            output(board)

            if check_win(board, PLAYER_PIECE):
                print("Player wins")
                game_over = True
                
            turn = AI

        elif turn == AI:
            col, move_eval = minimax(board, 6, -math.inf, math.inf, True)
            row = get_row(board, col)
            play_piece(board, row, col, AI_PIECE)

            output(board)

            if check_win(board, AI_PIECE):
                print("AI wins")
                game_over = True

            turn = PLAYER
main()
        

        

