
class xoBoard:
    def __init__(self):
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
    def __init__(self, board):
        self.board = board

    def GetBoard(self):
        return self.board

    def GetEmptyPos(self):
        retValue = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j]==0:
                    retValue.append([i,j])
        return retValue

    def WinningPos(self, player):
        if (player != 1) or (player != 2):
            raise RuntimeError("Player must be 1 or 2")
        retValue = []
        #across
        for j in range(3):
            count = [0,0,0]
            posOfZero = -1
            for i in range(3):
                count[self.board[j][i]] += 1
                if self.board[j][i]==0:
                    posOfZero = i
            if (count[0]==1) and (count[player]==2):
                retValue.append([j,posOfZero])
        #down
        for i in range(3):
            count = [0,0,0]
            posOfZero = -1
            for j in range(3):
                count[self.board[j][i]] += 1
                if self.board[j][i]==0:
                    posOfZero = i
            if (count[0]==1) and (count[player]==2):
                retValue.append([posOfZero, i])
        #'\' and '/'
        count = [0,0,0]
        posOfZero = -1
        for i in range(3):
            count[self.board[i][i]] += 1
            if self.board[i][i]==0:
                posOfZero = i
        if (count[0]==1) and (count[player]==2):
            retValue.append([posOfZero, posOfZero])
        count = [0,0,0]
        posOfZero = -1
        for i in range(3):
            count[self.board[2-i][i]] += 1
            if self.board[2-i][i]==0:
                posOfZero = i
        if (count[0]==1) and (count[player]==2):
            retValue.append([2 - posOfZero, posOfZero])
        return retValue
    
    def WinPossible(self, player):
        pass

    def HasWon(self, player):
        if (player != 1) or (player != 2):
            raise RuntimeError("Player must be 1 or 2")
        #across
        for j in range(3):
            count = [0,0,0]
            for i in range(3):
                count[self.board[j][i]] += 1
            if count[player]==3:
                return True
        #down
        for i in range(3):
            count = [0,0,0]
            for j in range(3):
                count[self.board[j][i]] += 1
            if count[player]==3:
                return True
        #'\' and '/'
        count = [0,0,0]
        for i in range(3):
            count[self.board[i][i]] += 1
        if count[player]==3:
            return True
        count = [0,0,0]
        for i in range(3):
            count[self.board[2-i][i]] += 1
        if count[player]==3:
            return True
        return False

    def FlipState(self, x, y, state):
        self.board[x][y] = state

class NextMoveProvider:
    def __init__(self, depth, player):
        if depth > 4:
            raise RuntimeError("Depth exceeding possible moves (4)")
        if depth <= 0:
            raise RuntimeError("Depth must be positive")
        self.depth = depth
        self.player = player
        if player==1: self.opponent = 2
        elif player==2: self.opponent = 1
        else:
            raise RuntimeError("Player must be 1 or 2")

    def CalculateWeight(self, board):
        if board.HasWon(self.opponent):
            return [1, board]
        if board.HasWon(self.player):
            return [5, board]
        if board.WinningPos(self.opponent) != []:
            return [2, board]
        if board.WinningPos(self.player) != []:
            return [4, board]
        return [3, board]

    def NextMove(self, board, depth):
        if depth==0:
            return self.CalculateWeight(board)
        #generate possibe self.player's moves
        #need to use deepcopy techinique so as to obtain a separate object
        boardTable = board.GetBoard()
        myMoves = []
        for i in range(3):
            for j in range(3):
                if boardTable[i][j]==0:
                    myMoves.append(xoBoard(boardTable))
                    myMoves[-1].FlipState(i, j, self.player)
                    #instant win
                    if myMoves[-1].HasWon(self.player):
                        return [5, myMoves[-1]]
        #for every possible move get opponent's assumed best move
        opponentsBestMoves = []
        for i in myMoves:
            opponentsBestMoves.append(self.OpponentsMove(i, depth))
        #calculate my best move
        highestWeight = 0
        for i in opponentsBestMoves:
            if i[0]>highestWeight:
                highestWeight = i[0]
                chosenMove = i
        return chosenMove
    
    def OpponentsMove(self, board, depth):
        boardTable = board.GetBoard()
        opponentMoves = []
        for i in range(3):
            for j in range(3):
                if boardTable[i][j]==0:
                    opponentMoves.append(xoBoard(boardTable))
                    opponentMoves[-1].FlipState(i, j, self.opponent)
                    #instant loose
                    if opponentMoves[-1].HasWon(self.opponent):
                        return [1, opponentMoves[-1]]
        # pass to my next move
        myNextMoves = []
        for i in opponentMoves:
            myNextMoves.append(self.NextMove(i, depth-1))
        #assume best possible opponent's move
        lowestWeight = 6
        for i in myNextMoves:
            if i[0]<lowestWeight:
                lowestWeight = i[0]
                chosenMove = i
        return chosenMove
    
                    

    
