from xoboard import *

board = xoBoard()
#board.FlipState(1,1,2)
#...
#.o.
#...
fourpass = NextMoveProvider(4, 1)
print(fourpass.GetMove(board))
