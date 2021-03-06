from xoboard import *
from xomoves import *

'''
board = xoBoard([[2,0,1],[2,1,0],[1,0,2]])
print(board.GetBoard())
print(board.WinningPos(1))
print(board.WinningPos(2))
print(board.HasWon(1))
print(board.HasWon(2))

board.FlipState(2,0,2)
print(board.GetBoard())
print(board.HasWon(1))
print(board.HasWon(2))

board.FlipState(2,0,0)
print(board.GetBoard())

board = xoBoard([[0,1,2],[0,1,0],[0,2,0]])
print(board.GetBoard())

##onepass = NextMoveProvider(1,2)
##print(onepass.GetMove(board))

twopass = NextMoveProvider(2, 2)
print(twopass.GetMove(board))
'''

#board = xoBoard([[2,0,1],[1,1,2],[2,0,0]])
#abalg = AlphaBeta(10, 1)

#print(fullminimax.minimax(board, 1, True))
#print(abalg.minimaxAlpha(board, 0, -110, -101))
board = xoBoard([[2,0,1],[0,0,0],[0,0,0]])
mm = MinmaxFull(2, 1)
print(mm.minimax(board, 3, True, True))
ab = AlphaBeta(2,1)
print(ab.alphaBeta(board, 3, -100, 100, True, True))
