
from xoboard import xoBoard, verboseLog
from copy import deepcopy

WEIGHT_OF_WIN = 5
INFINITY = 1000000009


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

    def minimax(self, board, depth, isItMe, chBoard = False):
        verboseLog('minimax depth ', depth)
        if depth==0:
            verboseLog('minimax weight==0')
            pom = self.CalculateWeight(board)
            return pom
        '''
        if (not isItMe) and board.WinningPos(self.player):
            return [WEIGHT_OF_WIN, board]
        if isItMe and board.WinningPos(self.opponent):
            return [-WEIGHT_OF_WIN, board]
        '''
        if isItMe:
            best = [-WEIGHT_OF_WIN,'error']
            children = board.GetChildren(self.player)
            for child in children:
                pom = self.minimax(child, depth-1, False)
                if pom[0]>=best[0]:
                    best = deepcopy(pom)
            if not chBoard:
                best[1] = board   #deepcopy?
            return best
        else:
            best = [WEIGHT_OF_WIN, 'error']
            children = board.GetChildren(self.opponent)
            for child in children:
                pom = self.minimax(child, depth-1, True)
                #verboseLog('minimax best ', best)
                #verboseLog('minimax pom ', pom)
                if pom[0]<=best[0]:
                    best = deepcopy(pom)
            if not chBoard:
                best[1] = board  #Deepcopy?
            return best
        raise RuntimeError("Something Went Wrong with recursion!")
            
        
    def GetMove(self, board):
        resboard =  self.minimax(board, self.depth, True, True)
        verboseLog('GetMove resboard ', resboard)
        x, y = -1, -1
        newboard = resboard[1].GetBoard()
        oldboard = board.GetBoard()
        for i in range(3):
            for j in range(3):
                if (oldboard[i][j]==0) and (newboard[i][j]==self.player):
                    return (i, j)
        raise RuntimeError("Something went wrong, no move found")
        
    
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
    '''
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
    '''
    def alphaBeta(self, board, depth, alpha, beta, isItMe, chBoard=False):
        if depth==0:
            pom = self.CalculateWeight(board)
            return pom
        if isItMe:
            best = [-INFINITY, 'error']
            children = board.GetChildren(self.player)
            for child in children:
                pom = self.alphaBeta(child, depth-1, alpha, beta, False)
                if pom[0] >= best[0]:
                    best = deepcopy(pom)
                if pom[0] >= alpha:
                    alpha = pom[0]
                if beta <= alpha:
                    break
            if not chBoard:
                best[1] = board
            return best
        else:
            best = [INFINITY, 'error']
            children = board.GetChildren(self.opponent)
            for child in children:
                pom = self.alphaBeta(child, depth-1, alpha, beta, True)
                if best[0] >= pom[0]:
                    best = deepcopy(pom)
                if beta >= pom[0]:
                    beta = pom[0]
                if beta <= alpha:
                    break
            if not chBoard:
                best[1] = board
            return best
        raise RuntimeError("Something Went Wrong with AlphaBeta recursion")
            

    def GetMove(self, board):
        resboard =  self.alphaBeta(board, self.depth, -INFINITY, INFINITY, True, True)
        print('GetMove resboard ', resboard)
        x, y = -1, -1
        newboard = resboard[1].GetBoard()
        oldboard = board.GetBoard()
        for i in range(3):
            for j in range(3):
                if (oldboard[i][j]==0) and (newboard[i][j]==self.player):
                    return (i, j)
        raise RuntimeError("Something went wrong, no move found")
