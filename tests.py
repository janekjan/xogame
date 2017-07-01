from xoboard import *

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

onepass = NextMoveProvider(1,2)
print(onepass.GetMove(board))
