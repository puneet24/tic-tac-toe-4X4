class TicTacToe():

    def __init__(self,verbose=False,n=4, depthLevel = 4):
        self.verbose=verbose
        self.n=n
        self.depthLevel = depthLevel
        self.instance=[]
        for i in range(n):
            self.instance.append([0]*n)

    def isLeaf(self):
        self.val=self.evaluate()
        if self.val == 1000 or self.val == -1000:
            return True;
        for row in range(self.n):
            for col in range(self.n):
                if (self.instance[row][col]==0):
                    return False
        return True;
        
    # Standarad heuisitic function for 4X4 tic tac toe, with some modifications, it can be made generic.
    def evaluate(self):
        if self.verbose:
            print self
            print self.val
        # Checking for Rows for X or O victory.
        evaluationMatrix = []

        for i in range(self.n):
            evaluationMatrix.append([[[0,0,0],[0,0,0]], [[0,0,0],[0,0,0]], [[0,0,0],[0,0,0]], [[0,0,0],[0,0,0]]])

        for row in range(0, self.n):
            for col in range(0, self.n):
                if self.instance[row][col] == 1:
                    evaluationMatrix[row][col] = [[1 + (evaluationMatrix[row][col-1][0][0] if col-1 >= 0 else 0), 1 + (evaluationMatrix[row-1][col][0][1] if row-1 >= 0 else 0), 1 + (evaluationMatrix[row-1][col-1][0][2] if col-1 >= 0 and row-1 >= 0 else 0)], [0,0,0]]
                    if evaluationMatrix[row][col][0][0] == 4 or evaluationMatrix[row][col][0][1] == 4 or evaluationMatrix[row][col][0][2] == 4:
                        return -1000
                elif self.instance[row][col] == -1:
                    evaluationMatrix[row][col] = [[0,0,0], [1 + (evaluationMatrix[row][col-1][1][0] if col-1 >= 0 else 0), 1 + (evaluationMatrix[row-1][col][1][1] if row-1 >= 0 else 0), 1 + (evaluationMatrix[row-1][col-1][1][2] if col-1 >= 0 and row-1 >= 0 else 0)]]
                    if evaluationMatrix[row][col][1][0] == 4 or evaluationMatrix[row][col][1][1] == 4 or evaluationMatrix[row][col][1][2] == 4:
                        return -1000
                else:
                    evaluationMatrix[row][col] = [[0,0,0], [0,0,0]]

        rightDiagonal = [[0,0], [0,0], [0,0], [0,0]]
        for row in range(0, self.n):
            if self.instance[row][self.n-1-row] == 1:
                rightDiagonal[row] = [1 + (rightDiagonal[row-1][0] if row-1 >= 0 else 0), 0]
            elif self.instance[row][self.n-1-row] == 1:
                rightDiagonal[row] = [0, 1 + (rightDiagonal[row-1][1] if row-1 >= 0 else 0)]
            else:
                rightDiagonal[row] = [0,0]

        if rightDiagonal[self.n-1][0] == 4:
            return 1000
        elif rightDiagonal[self.n-1][1] == 4:
            return -1000

        counters = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        for row in range(self.n):
            counters[rightDiagonal[row][0]][0] += 1
            counters[rightDiagonal[row][0]][1] += 1
            for col in range(self.n):
                counters[evaluationMatrix[row][col][0][0]][0] += 1
                counters[evaluationMatrix[row][col][0][1]][0] += 1
                counters[evaluationMatrix[row][col][0][2]][0] += 1
                counters[evaluationMatrix[row][col][1][0]][1] += 1
                counters[evaluationMatrix[row][col][1][1]][1] += 1
                counters[evaluationMatrix[row][col][1][2]][1] += 1

        finalScore = 6*counters[3][0] + 3*counters[2][0] + counters[1][0] - (6*counters[3][1] + 3*counters[2][1] + counters[1][1])

        return finalScore
  
    # Return all the legal moves
    def getLegalMoves(self):
        legal=[]
        for row in range(self.n):
            for col in range(self.n):
                if self.instance[row][col]==0:
                    legal.append([row,col])
        if self.verbose:
            print legal 
            print self
        return legal

    # make a move with particular value as per the player
    def makeMove(self,move,player):
        self.val=None
        self.instance[move[0]][move[1]]=player
        
    # unmake a move with particular value as per the player
    def unMakeMove(self,move):
        self.val=None
        self.makeMove(move,0);
    
    # cut off depth value is set to 3.
    # Standarad minimax with alpha beta pruning.
    def minimaxAlphaBeta(self, depth, player, alpha, beta):
        if self.isLeaf() or depth == self.depthLevel:
            return [self.evaluate(), [-1,-1]]
        allLegalMoves = self.getLegalMoves()
        bestMove = allLegalMoves[0]
        for move in allLegalMoves:
            self.makeMove(move,player)
            if player == 1:
                score = self.minimaxAlphaBeta(depth+1, -1, alpha, beta)[0]
                if score > alpha:
                    alpha = score
                    bestMove = move
            else:
                score = self.minimaxAlphaBeta(depth+1, 1, alpha, beta)[0]
                if score < beta:
                    beta = score
                    bestMove = move
            self.unMakeMove(move)
            
            if alpha >= beta:
                bestMove = move
                break

        return [alpha if player == 1 else beta, bestMove]

    def __str__(self):
        s=''
        for row in range(self.n):
            for col in range(self.n):
                if self.instance[row][col]==1:
                    s = s+' X '
                if self.instance[row][col]==-1:
                    s = s+' O '
                if self.instance[row][col]==0:
                    s=s+' - '
            s = s+"\n"
        return s

    def gamePlay(self, finalMoveStr = "", turn = True):
        while self.isLeaf() == False:
            soln = None
            player = None
            if turn == True:
                soln = self.minimaxAlphaBeta(0, 1, -float('inf'),float('inf'))
                self.makeMove(soln[1], 1)
                player = 'X'
            else:
                soln = self.minimaxAlphaBeta(0, -1, -float('inf'),float('inf'))
                self.makeMove(soln[1], -1)
                player = 'O'
            turn = True if turn == False else False 
            posn = soln[1][0]*self.n + soln[1][1] + 1
            finalMoveStr += (" -> " if len(finalMoveStr) > 0 else "") + player + str(posn)
        print finalMoveStr
        print self
        


def gamePlayScenarios(win = 1):
    if win == 1:
        problem=TicTacToe(False,4)
        problem.makeMove([1,1], 1)
        problem.makeMove([3,3], -1)
        problem.gamePlay("X6 -> O16", True)
    elif win == -1:
        problem=TicTacToe(False,4)
        problem.makeMove([3,3], 1)
        problem.makeMove([1,1], -1)
        problem.gamePlay("O6 -> X16", True)
    else:
        problem=TicTacToe(False,4)
        problem.gamePlay("", True)


# PROVE of FUTILE GAME, IF BOTH PLAYERS PLAY OPTIMALLY THEN GAME WILL DRAW
for row in range(4):
    for col in range(4):
        problem=TicTacToe(False,4)
        problem.makeMove([row, col], 1)
        problem.gamePlay("", False)

# # DRAW
# gamePlayScenarios(0)
# # PLAYER 1 WINS
# gamePlayScenarios(1)
# # PLAYER 2 WINS
# gamePlayScenarios(-1)

    

