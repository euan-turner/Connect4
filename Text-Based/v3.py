import numpy as np
from prettytable import PrettyTable
import random
from itertools import cycle
from dataclasses import dataclass
from math import inf

PLAYER = 1
AI = -1
EMPTY = 0

@dataclass
class Move:
    row : int
    col : int

def shuffle(arr):
    random.shuffle(arr)
    return arr

class Board():
    """Monitors the board state, and provides functions to 
    interact with the current state.
    """    

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
    
    def add_row(self, move):
        """Find and add the row index to a move descriptor

        Args:
            move (Move): A move with col, but no row

        Returns:
            Move: A move with col and row
        """        
        for row in range(5, -1,-1):
            if self.state[row][move.col] == EMPTY:
                move.row = row
                return move
    
    def make_move(self, move, token):
        """Play a move in the board state

        Args:
            move (Move): Row and col of move
            token (int): Piece to play
        """        
        self.state[move.row][move.col] = token
    
    def undo_move(self, move):
        """Undo a move, for use in minimax

        Args:
            move (Move): Row and col to undo
        """        
        self.state[move.row][move.col] = EMPTY
    
    def valid_moves(self):
        """Gets a list of all valid moves in the position

        Returns:
            Move[]: Array of Move instances without rows
        """        
        moves = []
        for col in range(7):
            if self.state[0][col] == EMPTY:
                move = Move(None, col)
                moves.append(move)
        return moves
    
    def find_runs(self, token, length):
        """Finds the number of runs of a given length
        in a board state. Calls count_runs on a series
        of sub-arrays of self.state.

        Args:
            token (int): Piece to look for
            length (int): Length to look for

        Returns:
            int: Number of runs
        """        
        total = 0

        for row in self.state:
            total += self.count_runs(row, token, length)
        for col in self.state.T:
            total += self.count_runs(col, token, length)
        
        for offset in range(-5,7):
            ##Forward diagonals
            total += self.count_runs(
                np.diagonal(self.state, offset = offset),
                token, length)
            ##Backward diagonals
            total += self.count_runs(
                np.diagonal(np.fliplr(self.state),
                offset = offset), token, length)
        return total
    
    def count_runs(self, arr, token, length):
        """Count the number of runs in a sub-array

        Args:
            arr (int[]): Sub-array of state to search
            token (int): Piece to search for
            length (int): Length to look for

        Returns:
            int: Number of runs in sub-array
        """        
        if len(arr) < length:
            return 0
        else:
            total = 0
            for i in range(0, len(arr)-length+1):
                run = arr[i:i+length]
                if len(np.where(run==token)[0]) == length:
                    total += 1
        return total
    
    def check_win(self):
        """Check if the board is won

        Returns:
            bool
        """        
        if self.find_runs(PLAYER, 4) or self.find_runs(AI, 4):
            return True
        else:
            return False
    
    def game_over(self):
        """Check if board is terminal

        Returns:
            int: 1 = won, 0 = drawn, -1 = not terminal
        """        
        won = self.check_win()
        full = len(np.where(self.state == EMPTY)[0])
        if won:
            return 1
        elif full == 0:
            return 0
        else:
            return -1



class Game():

    def __init__(self):
        self.board = Board()
        self.players = cycle(shuffle([PLAYER,AI]))
        self.current = next(self.players)
        self.MAX_SEARCH_DEPTH = 5
    
    def turn(self):
        """Either take player input, or call AI, for a move
        """        
        self.board.output()
        
        move = None

        if self.current == AI:
            move = self.find_best_move()

        else:
            valid = self.board.valid_moves()
            while move not in valid:
                choice = int(input("Enter column (1-7): ")) - 1
                move = Move(None, choice)
            move = self.board.add_row(move)
        
        self.board.make_move(move, self.current)
        self.board.turns += 1

        status = self.board.game_over()
        if status == 0:
            print("Game is drawn")
            self.board.output()
            self.board.reset()
        elif status == 1:
            print("Game is won")
            self.board.output()
            self.board.reset()

        self.current = next(self.players)
    
    def find_best_move(self):
        """AI player, calls minimax function to evaluate moves

        Returns:
            Move: Best move according to evaluation
        """        
        best_move = None
        best_eval = -inf

        for move in shuffle(self.board.valid_moves()):
            move = self.board.add_row(move)

            self.board.make_move(move, AI)
            move_eval = self.minimax(0, -inf, inf, False)
            print(move, move_eval)
            self.board.undo_move(move)

            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        
        return best_move

    def minimax(self, depth, alpha, beta, isMax):
        """Minimax evaluation for AI agent.
        Uses alpha-beta pruning to shrink search tree

        Args:
            depth (int): Current search depth
            alpha (int): Best eval so far
            beta (int): Worst eval so far
            isMax (bool): Player is maximiser (AI)

        Returns:
            int: Best move eval from position
        """        
        status = self.board.game_over()
        if status == 0:
            return 0
        elif status == 1:
            if isMax:
                return -1000000 + depth
            else:
                return 1000000 + depth
        elif depth == self.MAX_SEARCH_DEPTH:
            return self.evaluate()
        
        if isMax:
            best = -inf
            for move in shuffle(self.board.valid_moves()):
                move = self.board.add_row(move)

                self.board.make_move(move, AI)
                best = max(best, self.minimax(depth+1, alpha, beta, False))
                self.board.undo_move(move)

                if best >= beta:
                    break
                alpha = max(alpha, best)
            return best
        else:
            best = inf
            for move in shuffle(self.board.valid_moves()):
                move = self.board.add_row(move)

                self.board.make_move(move, PLAYER)
                best = min(best, self.minimax(depth+1, alpha, beta, True))
                self.board.undo_move(move)

                if best <= alpha:
                    break
                beta = min(beta, best)
            return best

    def evaluate(self):
        """Heuristic evaluation of board state.
        Calculated using number of runs for each player

        Returns:
            int: Evaluation score
        """        
        ai_twos = self.board.find_runs(AI, 2)
        ai_threes = self.board.find_runs(AI, 3)
        opp_twos = self.board.find_runs(PLAYER, 2)
        opp_threes = self.board.find_runs(PLAYER, 3)

        score = (ai_threes * 1000 - opp_threes * 1000 +
                 ai_twos * 100 - opp_twos * 100)
        return score
    
    def main(self):
        while True:
            self.turn()

game = Game()
game.main()
