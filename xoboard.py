
class xoBoard:
    def __init__(self):
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
    def __init__(self, board):
        self.board = board

    def GetBoard(self):
        return self.board

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
    def __init__(self):
        pass

    
