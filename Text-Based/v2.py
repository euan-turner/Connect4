import numpy as np
from prettytable import PrettyTable
import math

PLAYER1= 1
PLAYER2 = -1

class Board():

    def __init__(self):
        self.state = np.zeros((6,7), dtype = int)
        self.turns = 0
    
    def output(self):
        table = PrettyTable()
        table.header = False
        table.hrules = True

        for row in self.state:
            r = []
            for col in row:
                if col == 1:
                    r.append('@')
                elif col == -1:
                    r.append('#')
                else:
                    r.append(' ')
            table.add_row(r)
        print(table)
    
    def reset(self):
        self.__init__()

    def make_move(self, state, col, token):
        """Make a move for a player in a board state

        Args:
            state (np.ndarray): Current board state
            col (int): Column to move in
            token (int): Piece to play
        """

        temp = state.copy()
        for row in range(5,-1,-1):
            if temp[row][col] == 0:
                temp[row][col] = token
                return temp

    def get_valid_moves(self, state):
        valid_moves = []
        for col in range(0,7):
            if state[0][col] == 0:
                valid_moves.append(col)
        return valid_moves

    
    def find_runs(self, state, token, length):
        """Finds the number of occurrences of a run of a given length,
        for a player in a board state.

        Args:
            state (np.ndarray): Current board state
            token (int): Player's token to look for runs with
            length (int): Length of run to search for
        """    
        
        total_runs = 0

        ##Check for horizontal runs
        for row in state:
            total_runs += self.count_runs(row,token,length)
        
        ##Check for vertical runs
        for col in state.T:
            total_runs += self.count_runs(col,token,length)
        
        ##Check for diagonal runs
        for offset in range(-5,7):
            ##Backward diagonals
            total_runs += self.count_runs(np.diagonal(state, offset = offset), token, length)
            ##Forward diagonals
            total_runs += self.count_runs(np.diagonal(np.fliplr(state), offset = offset), token, length)
        
        return total_runs
    
    def count_runs(self, arr, token, length):
        """Counts the number of runs of a given length in a 1D array for a player.

        Args:
            arr (np.ndarray): 1D array to search
            token (int): Player's token to look for
            length (int): Minimum length of run to look for
        """        
        if len(arr) < length:
            return 0
        else:
            total = 0
            for i in range(0,len(arr)-length+1):
                run = arr[i:i+length]
                if len(np.where(run==token)[0]) == length:
                    total += 1
        
        return total
    
    def check_game_over(self, state, token):
        check_win = self.find_runs(state, token, 4)
        full = len(np.where(state!=0)[0])
        if check_win >= 1 or full == 42:
            return True
        else:
            return False


class Game():

    def __init__(self):
        self.board = Board()


    def turn(self):
        self.board.output()
        if self.board.turns%2 == 0:
            token = PLAYER1

            ##Validate column choice
            while True:
                try:
                    choice = int(input("Enter column (1-7): ")) -1
                except:
                    print("Invalid entry")
                if choice not in self.board.get_valid_moves(self.board.state):
                    print("Invalid move")
                    continue
                break

        else:
            token = PLAYER2
            minimax = Minimax(self.board, token)
            choice,score = minimax.find_best_move(5)
            print(f'Move: {choice}, Score: {score}')
        
        

        self.board.state = self.board.make_move(self.board.state, choice, token)
        self.board.turns += 1
        
        if self.board.check_game_over(self.board.state, token):
            print("Won")
            self.board.output()
            self.board.reset()
        elif self.board.turns == 42:
            print("Draw")
            self.board.reset()
    
    def main(self):
        while True:
            self.turn()
    
    

class Minimax():
    
    def __init__(self,board, token):
        self.board = board
        self.base_state = self.board.state.copy()
        self.token = token
    
    def find_best_move(self,depth):

        legal_moves = {}
        for move in self.board.get_valid_moves(self.base_state):
            temp_state = self.board.make_move(self.base_state, move, self.token)
            legal_moves[move] = -self.search(depth-1, temp_state, -self.token)
        
        best_score = -math.inf
        best_move = None
        moves = legal_moves.items()
        for move,score in moves:
            if score > best_score:
                best_score = score
                best_move = move
            
        return best_move, best_score
    
    def search(self, depth, state, token):
        ##Check if node is terminal
        if depth == 0 or self.board.check_game_over(state,token):
            return self.evaluate(state, token)

        legal_moves = []
        for move in self.board.get_valid_moves(state):
            temp_state = self.board.make_move(state, move, token)
            legal_moves.append(temp_state)

        alpha = -math.inf
        for new_state in legal_moves:
            alpha = max(alpha, -self.search(depth-1, new_state, -token))
        
        return alpha
    
    def evaluate(self, state, token):
        opp_fours = self.board.find_runs(state,-token,4)
        if opp_fours > 0:
            return -1000000
        p_fours = self.board.find_runs(state,token,4)
        p_threes = self.board.find_runs(state,token,3)
        p_twos = self.board.find_runs(state,token,2)
        return p_fours*1000000 + p_threes*1000 + p_twos

game = Game()
game.main()
