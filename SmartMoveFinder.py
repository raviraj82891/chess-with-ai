import random


pieceScore = {
    "K": 0,   
    "Q": 10,  
    "R": 5,   
    "B": 3,   
    "N": 3,   
    "p": 1    
}
CHECKMATE = 1000  
STALEMATE = 0     
DEPTH = 2

def findRandomMove(validMoves):

    if not validMoves:
        return None  
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMoves(gs, validMoves):
    if not validMoves:
        return None 

    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = -CHECKMATE  

    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves() 
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
       
            opponentMaxScore = -CHECKMATE  
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = turnMultiplier * scoreMaterial(gs.board)  

                if score > opponentMaxScore:
                    opponentMaxScore = score 
                gs.undoMove()  

           
            if opponentMaxScore > opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove

            gs.undoMove()  # Undo the player move

        return bestPlayerMove

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
                
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore 

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0 or not validMoves:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore    

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0 or len(validMoves) == 0:
        return turnMultiplier * scoreBoard(gs)
    
   
    # sortedMoves = sorted(validMoves, key=lambda move: 1 if gs.board[move.endRow][move.endCol] != '--' else 0, reverse=True)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore  

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':  # White piece
                score += pieceScore[square[1]]
            elif square[0] == 'b':  # Black piece
                score -= pieceScore[square[1]]
    return score
   
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':  # White piece
                score += pieceScore[square[1]]
            elif square[0] == 'b':  # Black piece
                score -= pieceScore[square[1]]
    return score