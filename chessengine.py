class GameState:
    def __init__(self):
       
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunction = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        self.enPassantPossibleLog = [self.enPassantPossible]

    def makeMove(self, move):
        """Execute a move on the board."""
        for log in self.castleRightsLog:
            print(log.wks, log.wqs, log.bks, log.bqs, end=", ")
        print()
        
        self.board[move.startRow][move.startCol] = "--"
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + move.promotionPiece
        else:
            self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantPossible = ()
            
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # kingside castling
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:  # queenside castling
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'
        
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        self.enPassantPossibleLog.append(self.enPassantPossible)

    def updateCastleRights(self, move):
        """Update castling rights based on king/rook movement or capture."""
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        # Handle rook capture
        if move.pieceCaptured == 'wR':
            if move.endRow == 7 and move.endCol == 0:
                self.currentCastlingRight.wqs = False
            elif move.endRow == 7 and move.endCol == 7:
                self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0 and move.endCol == 0:
                self.currentCastlingRight.bqs = False
            elif move.endRow == 0 and move.endCol == 7:
                self.currentCastlingRight.bks = False

    def undoMove(self):
        """Undo the last move made."""
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            self.castleRightsLog.pop()
            self.currentCastlingRight = self.castleRightsLog[-1]
            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]
            
            self.checkMate = False
            self.staleMate = False

    def squareUnderAttack(self, row, col):
        """Check if the square at (row, col) is under attack by the opponent."""
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        return any(move.endRow == row and move.endCol == col for move in opp_moves)

    def inCheck(self):
        """Check if the current player's king is in check."""
        king_loc = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        return self.squareUnderAttack(king_loc[0], king_loc[1])

    def getValidMoves(self):
        """Get all legal moves, filtering out those that leave the king in check."""
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def getAllPossibleMoves(self):
        """Generate all possible moves for the current player without legality check."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (self.whiteToMove and piece[0] == 'w') or (not self.whiteToMove and piece[0] == 'b'):
                    self.moveFunction[piece[1]](row, col, moves)
        return moves

    def getPawnMoves(self, row, col, moves):
        """Generate possible pawn moves, including en passant and promotions."""
        if self.whiteToMove:
            if row > 0 and self.board[row - 1][col] == "--":
                if row - 1 == 0:
                    for piece in ['Q', 'R', 'B', 'N']:
                        moves.append(Move((row, col), (row - 1, col), self.board, promotionPiece=piece))
                else:
                    moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col > 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    if row - 1 == 0:
                        for piece in ['Q', 'R', 'B', 'N']:
                            moves.append(Move((row, col), (row - 1, col - 1), self.board, promotionPiece=piece))
                    else:
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, isEnpassantMove=True))
            if col < 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    if row - 1 == 0:
                        for piece in ['Q', 'R', 'B', 'N']:
                            moves.append(Move((row, col), (row - 1, col + 1), self.board, promotionPiece=piece))
                    else:
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantMove=True))
        else:
            if row < 7 and self.board[row + 1][col] == "--":
                if row + 1 == 7:
                    for piece in ['Q', 'R', 'B', 'N']:
                        moves.append(Move((row, col), (row + 1, col), self.board, promotionPiece=piece))
                else:
                    moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col > 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if row + 1 == 7:
                        for piece in ['Q', 'R', 'B', 'N']:
                            moves.append(Move((row, col), (row + 1, col - 1), self.board, promotionPiece=piece))
                    else:
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, isEnpassantMove=True))
            if col < 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    if row + 1 == 7:
                        for piece in ['Q', 'R', 'B', 'N']:
                            moves.append(Move((row, col), (row + 1, col + 1), self.board, promotionPiece=piece))
                    else:
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, row, col, moves):
        """Generate possible rook moves."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for dr, dc in directions:
            for i in range(1, 8):
                endRow, endCol = row + dr * i, col + dc * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    piece = self.board[endRow][endCol]
                    if piece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, row, col, moves):
        """Generate possible knight moves."""
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for dr, dc in knight_moves:
            endRow, endCol = row + dr, col + dc
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = self.board[endRow][endCol]
                if piece == "--" or piece[0] == enemy_color:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        """Generate possible bishop moves."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for dr, dc in directions:
            for i in range(1, 8):
                endRow, endCol = row + dr * i, col + dc * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    piece = self.board[endRow][endCol]
                    if piece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, col, moves):
        """Generate possible queen moves (rook + bishop)."""
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        """Generate possible king moves."""
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for dr, dc in king_moves:
            endRow, endCol = row + dr, col + dc
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                piece = self.board[endRow][endCol]
                if piece == "--" or piece[0] == enemy_color:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getCastleMoves(self, row, col, moves):
        """Generate possible castling moves."""
        if self.squareUnderAttack(row, col):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row, col, moves):
        """Generate kingside castling moves."""
        if self.board[row][col + 1] == "--" and self.board[row][col + 2] == '--':
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, row, col, moves):
        """Generate queenside castling moves."""
        if (self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" and 
            self.board[row][col - 3] == "--"):
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove=True))

class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, promotionPiece=None, isCastleMove=False):
        """Initialize a move object."""
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.promotionPiece = promotionPiece if self.isPawnPromotion else None
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """Compare moves based on start, end, and promotion piece."""
        if isinstance(other, Move):
            return (self.startRow == other.startRow and
                    self.startCol == other.startCol and
                    self.endRow == other.endRow and
                    self.endCol == other.endCol and
                    self.promotionPiece == other.promotionPiece)
        return False

    def getChessNotation(self):
        """Return move in chess notation (e.g., 'e2e4')."""
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """Convert coordinates to chess notation."""
        return self.colsToFiles[c] + self.rowsToRanks[r]