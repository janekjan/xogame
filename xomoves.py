
from xoboard import xoBoard, verboseLog
from copy import deepcopy

WEIGHT_OF_WIN = 5

class MinmaxFull:
    def __init__(self, depth, player):
        if depth <= 0:
            raise RuntimeError("Depth must be positive")
        self.depth = depth
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

    def minimax_old(self, board, player, returnmove=False):
        #print("Hello, Minimax: ", player, board)
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
        if returnmove: moves = []
        for i in emptyPositions:
            board.FlipState(i[0], i[1], player)
            minimaxValues.append(self.minimax(board, opponent))
            if returnmove:
                moves.append(deepcopy(board))
            board.FlipState(i[0], i[1], 0)
        #Returns
        # returnmove==True means 'root' level
        if player==self.player:
            if returnmove:
                besti = 0
                for i in range(len(minimaxValues)):
                    if minimaxValues[i]>minimaxValues[besti]:
                        besti = i
                return [minimaxValues[besti], moves[besti]]
            #print("returning ", max(minimaxValues))
            return max(minimaxValues)
        if player==self.opponent:
            if returnmove:
                worsti = 0
                for i in range(len(minimaxValues)):
                    if minimaxValues[i]<minimaxValues[worsti]:
                        worsti = i
                return [minimaxValues[worsti], moves[worsti]]
            #print('returning ', min(minimaxValues))
            return min(minimaxValues)
        raise RuntimeError("Something went wrong!")
    
    def CalculateWeight(self, board):
        verboseLog("calculating weight for", board)
        if board.HasWon(self.opponent):
            return [1, board]
        if board.HasWon(self.player):
            return [5, board]
        if board.WinningPos(self.opponent) != []:
            return [2, board]
        if board.WinningPos(self.player) != []:
            return [4, board]
        return [3, board]

    def minimax(self, board, depth, isItMe):
        if depth==0:
            verboseLog('minimax weight==0')
            pom = self.CalculateWeight(board)
            return pom[0]
        if (not isItMe) and board.WinningPos(self.player):
            return WEIGHT_OF_WIN
        if isItMe and board.WinningPos(self.opponent):
            return -WEIGHT_OF_WIN
        
        if isItMe:
            best = -WEIGHT_OF_WIN
            children = board.GetChildren(self.player)
            for child in children:
                pom = self.minimax(child, depth-1, False)
                best = max(best, pom)
            return best
        else:
            best = WEIGHT_OF_WIN
            children = board.GetChildren(self.opponent)
            for child in children:
                pom = self.minimax(child, depth-1, True)
                verboseLog('minimax best ', best)
                verboseLog('minimax pom ', pom)
                best = min(best, pom)
            return best
        raise RuntimeError("Something Went Wrong with recursion!")
            
        
    def GetMove(self, board):
        return self.minimax(board, self.depth, True)
    
class AlphaBeta:
    def __init__(self, depth, player):
        if depth <= 0:
            raise RuntimeError("Depth must be positive")
        self.depth = depth
        self.player = player
        if player==1: self.opponent = 2
        elif player==2: self.opponent = 1
        else:
            raise RuntimeError("Player must be 1 or 2")

    def weight(self, board):
        if board.HasWon(self.opponent):
            return -WEIGHT_OF_WIN
        if board.HasWon(self.player):
            return WEIGHT_OF_WIN
        if board.WinningPos(self.opponent) != []:
            return -50
        if board.WinningPos(self.player) != []:
            return 40
        return 0

    def minimaxAlpha(self, board, depth, alpha, beta):
        emptys = board.GetEmptyPos()
        if emptys==[]:
            if board.HasWon(self.player):
                return WEIGHT_OF_WIN
            elif board.HasWon(self.opponent):
                return -WEIGHT_OF_WIN
            else:
                return 0
            
        if depth==self.depth:
            return self.weight(board)

        for i in emptys:
            board.FlipState(i[0],i[1], self.player)
            alpha = max(alpha, self.minimaxBeta(board, depth+1, alpha, beta))
            board.FlipState(i[0], i[1], 0)
            if alpha >= beta:
                return beta
        return alpha

    def minimaxBeta(self, board, depth, alpha, beta):
        emptys = board.GetEmptyPos()
        if emptys==[]:
            if board.HasWon(self.player):
                return WEIGHT_OF_WIN
            elif board.HasWon(self.opponent):
                return -WEIGHT_OF_WIN
            else:
                return 0

        if depth==self.depth:
            return self.weight(board)

        for i in emptys:
            board.FlipState(i[0], i[1], self.opponent)
            beta = min(alpha, self.minimaxAlpha(board, depth+1, alpha, beta))
            if beta <= alpha:
                return alpha
        return beta

    def GetMove(self, board):
        pass
