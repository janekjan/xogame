import pygame
from pygame.locals import *
from sys import exit

from xoboard import *
from xomoves import *

#SETTINGS
PREDICTION_DEPTH = 3
PLAYER_SYMBOL = 2
I_START = True

if PLAYER_SYMBOL==1: MY_SYMBOL = 2
else: MY_SYMBOL = 1

class Field():
    state = 0
    x, y = 0, 0

    def __init__(self, x, y):
        self.x = 205*x
        self.y = 205*y

    def change(self, newstate):
        if newstate>2 or newstate <0:
            raise RuntimeError("Wrong state: must be 0, 1 or 2")
        self.state = newstate

    def update(self):
        if self.state==0:
            screen.blit(empty_image, (self.x, self.y))
        elif self.state==1:
            screen.blit(x_image, (self.x, self.y))
        elif self.state==2:
            screen.blit(o_image, (self.x, self.y))

    def checkState(self):
        return self.state

def onmouse():
    (cx, cy) = pygame.mouse.get_pos()
    bx, by = -1, -1
    if (cx<190): bx = 0
    elif (cx>410): bx = 2
    else: bx = 1
    if (cy<190): by = 0
    elif (cy>410): by = 2
    else: by = 1
    if gameboard[bx][by].checkState() != 0:
        return
    gameboard[bx][by].change(PLAYER_SYMBOL)
    board.FlipState(bx, by, PLAYER_SYMBOL)
    gameboard[bx][by].update()
    pygame.display.update()
    (newx, newy) = mover.GetMove(board)
    gameboard[newx][newy].change(MY_SYMBOL)
    board.FlipState(newx, newy, MY_SYMBOL)
    
pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Gra O i X')

#mover = MinmaxFull(PREDICTION_DEPTH, MY_SYMBOL)
mover = NextMoveProvider(PREDICTION_DEPTH, MY_SYMBOL)
#mover = AlphaBeta(PREDICTION_DEPTH, MY_SYMBOL)

#prepare gameboard
board = xoBoard()
gameboard = [[0,0,0],[0,0,0],[0,0,0]]
for i in range(3):
    for j in range(3):
        gameboard[i][j] = Field(i, j)


empty_image = pygame.image.load('empty.png').convert()
x_image = pygame.image.load('x.png').convert()
o_image = pygame.image.load('o.png').convert()
board_image = pygame.image.load('board.png').convert()

if not I_START:
    (newx, newy) = mover.GetMove(board)
    gameboard[newx][newy].change(MY_SYMBOL)
    board.FlipState(newx, newy, MY_SYMBOL)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        if event.type==pygame.MOUSEBUTTONUP:
            onmouse()
    screen.fill((255,255,255))
    screen.blit(board_image, (0,0))
    for i in range(3):
        for j in range(3):
            gameboard[i][j].update()
    pygame.display.update()
    clock.tick(30)
