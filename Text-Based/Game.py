import numpy as np, time

class Game():

    def __init__(self):
        ##0 represents empty place
        ##state[0] is top row, last to be filled
        ##pieces fall to state[6]
        self.state = np.zeros((6,7),dtype=int)
        self.heights = np.zeros(7,dtype=int)
        self.turns = 0

    def output(self):
        print("------------------------------")
        for row in self.state:
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
    def check_win(self,token : int) -> bool:
        ##Check rows
        for row in self.state:
            if self.check_four(row,token):
                ##Win occurs
                return True
        
        ##Check columns
        for col in self.state.T:
            if self.check_four(col,token):
                ##Win occurs
                return True

        ##Check diagonals
        for offset in range(-2,4):
            for_diag = np.diagonal(self.state, offset=offset)
            back_diag = np.diagonal(np.fliplr(self.state),offset=offset)
            if self.check_four(for_diag,token) or self.check_four(back_diag,token):
                ##Win occurs
                return True
        
        return False

    ##Check an array for a sequence of four identical values
    def check_four(self, arr : np.ndarray, token : int) -> bool:
        inds = np.where(arr==token)[0]
        return any(i==j-1 and j==k-1 and k==l-1 for i,j,k,l in zip(inds,inds[1:],inds[2:],inds[3:]))

    def turn(self):
        if self.turns % 2 == 0:
            token = 1
        else:
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
            elif self.heights[choice] == 6:
                print("Column full")
                continue
            break
        
        self.state[5-self.heights[choice]][choice] = token
        self.heights[choice] += 1
        self.turns += 1

        status = self.check_win(token)
        if status:
            self.output()
            if token == 1:
                print("Player 1 wins")
            elif token == 2:
                print("Player 2 wins")
            self.reset()
        elif 0 not in self.state:
            print("Game is drawn")
            self.reset()

game = Game()
while True:
    game.output()
    game.turn()