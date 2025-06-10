import pygame as p
import chessengine, SmartMoveFinder

# Constants
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
colors = [p.Color("white"), p.Color("darkgreen")] 
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    try:
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(
                p.image.load("images/" + piece + ".png"),
                (SQ_SIZE, SQ_SIZE)
            )
    except FileNotFoundError as e:
        print(f"Error loading image: {e}")
        exit()

def highlightSquare(screen, gs, validMoves, sqSelected):
    """Highlight the selected square in blue and valid moves in yellow."""
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))  
            s.fill(p.Color('red'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawBoard(screen):
    """Draw the chessboard squares."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    """Draw the pieces on the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    """Draw the board, highlights, pieces, and game-over messages."""
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    
    # Display game-over states
    if gs.checkMate:
        font = p.font.SysFont("Helvitca", 32)
        text = font.render("Checkmate!", True, p.Color("Red"))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    elif gs.staleMate:
        font = p.font.SysFont("arial", 32)
        text = font.render("Stalemate!", True, p.Color("red"))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

def animateMove(move, screen, board, clock):
    """Animate the piece movement."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount
        drawBoard(screen)
        drawPieces(screen, board)
        # Draw the end square with board color
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # If captured piece, draw it
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Draw the moving piece at interpolated position
        screen.blit(IMAGES[move.pieceMoved], (c * SQ_SIZE, r * SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages()

    running = True
    sqSelected = ()  
    playerClicks = []  
    playerOne = True  # White is human
    PlayerTwo = False  # Black is AI

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and PlayerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
               
                if not (gs.checkMate or gs.staleMate) and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row, col):  
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        startSq = playerClicks[0]
                        endSq = playerClicks[1]
                        piece = gs.board[startSq[0]][startSq[1]]
                        if (piece == 'wp' and endSq[0] == 0) or (piece == 'bp' and endSq[0] == 7):
                            promotedPiece = input("Promote to Q, R, B, or N: ").upper()
                            while promotedPiece not in ['Q', 'R', 'B', 'N']:
                                promotedPiece = input("Invalid choice. Promote to Q, R, B, or N: ").upper()
                            move = chessengine.Move(startSq, endSq, gs.board, promotionPiece=promotedPiece)
                        else:
                            move = chessengine.Move(startSq, endSq, gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                break
                        if not moveMade:
                            playerClicks = [sqSelected]  

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  
                    gs.undoMove()
                    moveMade = True
                    sqSelected = ()  
                    playerClicks = []
                    animate = False
                if e.key == p.K_r:  
                    gs = chessengine.GameState()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    animate = False

        
        if not (gs.checkMate or gs.staleMate) and not humanTurn:
            AImove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AImove is None:
                AImove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        p.display.flip()
        clock.tick(MAX_FPS)

    p.quit()

if __name__ == "__main__":
    main()