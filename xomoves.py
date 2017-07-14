
from xoboard import xoBoard
from copy import deepcopy

WEIGHT_OF_WIN = 100

class MinmaxFull:
    def __init__(self, depth, player):
        if depth <= 0:
            raise RuntimeError("Depth must be positive")
        #self.depth = depth
        self.player = player
        if player==1: self.opponent = 2
        elif player==2: self.opponent = 1
        else:
            raise RuntimeError("Player must be 1 or 2")

    def LocalOpponent(self, localplayer):
        if localplayer==1: return 2
        elif localplayer==2: return 1
        else:
            raise RuntimeError("Player must be 1 or 2")

    def minimax(self, board, player):
        opponent = self.LocalOpponent(player)
        #If final state, return usefulness
        if board.HasWon(player):
            return WEIGHT_OF_WIN
        if board.HasWon(opponent):
            return -WEIGHT_OF_WIN
        emptyPositions = board.GetEmptyPos()
        if emptyPositions == []:
            return 0
        #For each state, get its minimax
        minimaxValues = []
        for i in emptyPositions:
            board.FlipState(i[0], i[1], player)
            minimaxValues.append(self.minimax(board, opponent))
            board.FlipState(i[0], i[1], 0)
        #Returns
        if player==self.player:
            return max(minimaxValues)
        if player==self.opponent:
            return min(minimaxValues)
        raise RuntimeError("Something went wrong!")

    def GetMove(self, board):
        pass
    
