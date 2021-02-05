import pygame
pygame.init()

##Colours
RED = (128,0,0)
GREEN = (0,128,0)
BLUE = (0,0,128)
YELLOW = (255,223,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

class Display():

    def __init__(self, width, height, back_colour, board_colour):
        self.width = width
        self.height = height
        self.dims = (width,height)

        self.back_colour = back_colour
        self.board_colour = board_colour
    
        self.window = pygame.display.set_mode(self.dims)
        pygame.display.set_caption("Connect 4")
        self.window.fill(self.back_colour)
        self.draw_board()

    def draw_board(self):
        ##Draw circles
        for row in range(1,7):
            for column in range(1,8):
                pygame.draw.circle(self.window, WHITE, (column*100-25,row*100+50),50)
        
        ##Column labels
        for i in range(1,8):
            font = pygame.font.SysFont('rockwell', 50)
            text_surf = font.render(str(i), False, BLACK)
            self.window.blit(text_surf, (i*100-40, 40))
        pygame.display.flip()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                pygame.display.flip()

display = Display(750,750,YELLOW,WHITE)
display.main()
