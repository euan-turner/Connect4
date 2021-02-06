import numpy as np, time

class Game():

    def __init__(self):
        ##0 represents empty place
        ##rows represent columns in the board, columns represent rows
        ##Top row is left column, bottom is right
        ##Pieces 'fall' to the end of the row
        self.state = np.zeros((7,6),dtype=int)
        self.turns = 0

    def output(self):
        print("------------------------------")
        for row in self.state.T:
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
                return token
        
        ##Check columns
        for row in state.T:
            if self.check_four(row,token):
                ##Win occurs
                return token

        ##Check diagonals
        for offset in range(-3,3):
            for_diag = np.diagonal(state, offset=offset)
            back_diag = np.diagonal(np.fliplr(state),offset=offset)
            if self.check_four(for_diag,token) or self.check_four(back_diag,token):
                ##Win occurs
                return token

        return 0

    ##Check an array for a sequence of four identical values
    def check_four(self, arr : np.ndarray, token : int) -> bool:
        inds = np.where(arr==token)[0]
        return any(i==j-1 and j==k-1 and k==l-1 for i,j,k,l in zip(inds,inds[1:],inds[2:],inds[3:]))

    def turn(self):
        self.output()
        if self.turns % 2 == 0:
            token = 1
            ##choice = self.find_best_move(token)
        else:
            ##Human plays second
            token = -1

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
                
        ##Choice is the row in self.state to update
        ##Find the column, filling from end of row
        ##np.count_nonzero returns number of non-zero elements in array
        new_row = 5 - np.count_nonzero(self.state[choice]) 
        self.state[choice][new_row] = token
        status = self.check_win(token, self.state)
        self.turns += 1
        if status != 0:
            self.output()
            if token == 1:
                print("Player 1 wins")
            elif token == -1:
                print("Player 2 wins")
            self.reset()
        elif 0 not in self.state:
            print("Game is drawn")
            self.reset()
    
    ##Returns the column choice
    def find_best_move(self, ai_token : int) -> int:
        best_move = None
        best_eval = -10000

        ##Search valid moves
        for col in range(7):
            if self.heights[col] < 6:
                self.state[5-self.heights[col]][col] = ai_token
                self.heights[col] += 1
                ##Depth->0 is the the start of the game. Depth->42 is the end
                curr_depth = len(np.where(self.state!=0)[0])
                ##Initial alpha = -1000 , beta = 1000
                move_eval = self.minimax(curr_depth, False, ai_token, -1000, 1000)
                

                if move_eval > best_eval:
                    best_eval = move_eval
                    best_move = col

                self.heights[col] -= 1
                self.state[5-self.heights[col]][col] = 0
        
        return best_move
    
    def minimax(self, depth : int, is_max : bool, ai_token : int, alpha : int, beta : int) -> int:
        print(self.state)
        ##AI win
        if is_max and self.check_win(ai_token):
            return 100
        ##Opponent win
        elif not is_max and self.check_win(- ai_token):
            return -100
        ##Draw
        elif 0 not in self.state:
            return 0

        ##Maximsing player -> AI
        if is_max:
            best_eval = -10000

            ##Search valid mvoes
            for col in range(7):
                if self.heights[col]  < 6:

                    self.state[5-self.heights[col]][col] = ai_token
                    self.heights[col] += 1
                    move_eval = self.minimax(depth+1,not is_max, ai_token, alpha, beta)
                    self.heights[col] -= 1
                    self.state[5-self.heights[col]][col] = 0

                    best_eval = max(best_eval, move_eval)
                    alpha = max(alpha, best_eval)

                    if beta <= alpha:
                        break
            return best_eval

        ##Minimising player -> Human
        elif not is_max:
            best_eval = 10000

            ##Search valid moves
            for col in range(7):
                if self.heights[col] < 6:

                    self.state[5-self.heights[col]][col] = - ai_token
                    self.heights[col] += 1
                    move_eval = self.minimax(depth+1, not is_max, ai_token, alpha, beta)
                    self.heights[col] -= 1
                    self.state[5-self.heights[col]][col] = 0

                    best_eval = min(best_eval, move_eval)
                    beta = min(beta, best_eval)

                    if beta <= alpha:
                        break
            return best_eval
        

game = Game()
while True:
    
    game.turn()