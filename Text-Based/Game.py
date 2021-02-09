import numpy as np, time

class Game():

    def __init__(self):
        ##0 represents empty place
        ##rows represent columns in the board, columns represent rows
        ##Top row is left column, bottom is right
        ##Pieces 'fall' to the end of the row
        self.state = np.zeros((7,6),dtype=int)
        self.turns = 0

    def output(self, state):
        print("------------------------------")
        for row in state.T:
            print(end = "|")
            for col in row:
                if col == 1:
                    char = ' # '
                elif col == -1:
                    char = ' @ '
                else:
                    char = '   '
                print(char, end = "|")
            print("\n------------------------------")
        
    def reset(self):
        time.sleep(1)
        self.__init__()

    ##Check for four in a row -> win condition 
    ##State has shape (7,6)
    def check_win(self,token : int, state : np.ndarray) -> bool:
        ##Check rows
        for col in state:
            if self.check_four(col,token):
                ##Win occurs
                return True
        
        ##Check columns
        for row in state.T:
            if self.check_four(row,token):
                ##Win occurs
                return True

        ##Check diagonals
        for offset in range(-3,3):
            for_diag = np.diagonal(state, offset=offset)
            back_diag = np.diagonal(np.fliplr(state),offset=offset)
            if self.check_four(for_diag,token) or self.check_four(back_diag,token):
                ##Win occurs
                return True

        return False

    ##Check an array for a sequence of four identical values
    def check_four(self, arr : np.ndarray, token : int) -> bool:
        for i in range(len(arr)-3):
            if (arr[i] == token) and (arr[i+1] == token) and \
               (arr[i+2] == token) and (arr[i+3] == token):
               return True
        return False

    ##Returns all valid moves for  a board state
    def valid_moves(self, curr_state : np.ndarray):
        moves = []
        for col in curr_state:
            if col[0] == 0:
                moves.append(col)
        return moves
    
    ##Token is placed in specified column of state
    def make_move(self, token, col, state):
        new_row = 5-np.count_nonzero(state[col])
        state[col][new_row] = token
        self.turns += 1
        return new_row

    def turn(self):
        self.output(self.state)
        if self.turns % 2 == 0:
            token = 1
            
        else:
            token = -1
            ##choice = self.find_best_move(token)

        ##Validate column choice
        while True:
            try:
                choice = int(input("Enter column (1-7): ")) -1
            except:
                print("Invalid choice")
                continue
                            
            if choice < 0 or choice > 6:
                print("Invalid choice")
                continue
            elif self.state[choice][0] != 0:
                print("Column full")
                continue
            break
        
        self.make_move(token, choice, self.state)

        status = self.check_win(token, self.state)
        if status:
            self.output(self.state)
            if token == 1:
                print("Player 1 wins")
            elif token == -1:
                print("Player 2 wins")
            self.reset()
        elif self.turns == 42:
            print("Game is drawn")
            self.reset()
            

    ##Returns the column choice
    def find_best_move(self, ai_token : int) -> int:
        opp_token = - ai_token

        best_move = None
        best_eval = -10000

        eval_state = self.state.copy()


        ##Search valid moves
        for move in valid_moves(eval_state):
            row = self.make_move(ai_token, move, eval_state)
            move_eval = self.minimax(eval_state, self.turns+1, False, ai_token, -10000, 10000)
            ##Undo move from state
            eval_state[move][row] = 0
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move

        # for col in range(7):
        #     ##Column is not full
        #     if eval_state[col][0] == 0:
        #         row = 5 - np.count_nonzero(eval_state[col])
        #         eval_state[col][row] = ai_token
        #         ##Depth -> 0 - start, Depth -> 42 - end
        #         curr_depth = np.count_nonzero(eval_state)
        #         ##Inital alpha -> -10000, Initial beta -> 10000
        #         move_eval = self.minimax(eval_state, curr_depth, False, ai_token, -10000, 10000)
        #         eval_state[col][row] = 0

        #         if move_eval > best_eval:
        #             best_eval = move_eval
        #             best_move = col

        return best_move

    def minimax(self, eval_state : np.ndarray, depth : int, is_max : bool, ai_token : int, alpha : int, beta : int) -> int:
        
        ##AI win
        if is_max and self.check_win(ai_token,eval_state) == ai_token:
            return 100
        ##Opponent win
        elif not is_max and self.check_win(- ai_token, eval_state) == -(ai_token):
            return -100
        ##Draw
        elif 0 not in eval_state:
            return 0

        ##Maximising player -> AI
        if is_max:
            best_eval = -10000

            ##Search valid moves
            for col in range(7):
                ##Column is not full
                if eval_state[col][0] == 0:
                    row = 5 - np.count_nonzero(eval_state[col])
                    eval_state[col][row] = ai_token
                    move_eval = self.minimax(eval_state, depth+1, not is_max, ai_token, alpha, beta)
                    eval_state[col][row] = 0

                    best_eval = max(best_eval, move_eval)
                    alpha = max(alpha, best_eval)

                    if beta <= alpha:
                        break

        ##Minimising player -> Human
        elif not is_max:
            best_eval = 10000

            ##Search valid moves
            for col in range(7):
                ##Column is not full
                if eval_state[col][0] == 0:
                    row = 5 - np.count_nonzero(eval_state[col])
                    eval_state[col][row] = -(ai_token)
                    move_eval = self.minimax(eval_state, depth+1, not is_max, ai_token, alpha, beta)
                    eval_state[col][row] = 0

                    best_eval = min(best_eval, move_eval)
                    beta = min(beta, move_eval)

                    if beta <= alpha:
                        break
        ##self.output(eval_state)
        ##print(best_eval)
        return best_eval

game = Game()
while True:
    
    game.turn()