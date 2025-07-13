
import pygame
import chess
import sys
from ai import get_ai_move
# Pygame setup
pygame.init()
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legal Chess Game (Player vs Player)")

# Colors
WHITE = (245, 245, 220)
BROWN = (139, 69, 19)

# Load piece images
def load_images():
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
    images = {}
    for piece in pieces:
        w_img = pygame.image.load(f'w{piece}.jpg')
        b_img = pygame.image.load(f'b{piece}.jpg')
        images[piece] = pygame.transform.scale(w_img, (SQUARE_SIZE, SQUARE_SIZE))
        images[piece.lower()] = pygame.transform.scale(b_img, (SQUARE_SIZE, SQUARE_SIZE))
    return images

piece_images = load_images()

# Draw the board and pieces
def draw_board(board):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            square = chess.square(col, 7 - row)  # translate pygame coords to chess square
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol()
                screen.blit(piece_images[symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Convert mouse position to a chess square
def get_square_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return chess.square(col, 7 - row)  # flip vertically

# Initialize the chess board
board = chess.Board()
selected_square = None
legal_moves = []

# Game loop
running = True
while running:
    draw_board(board)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if board.is_game_over():
            print("Game Over:", board.result())
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_square = get_square_from_mouse(event.pos)

            if selected_square is None:
                piece = board.piece_at(clicked_square)
                if piece and piece.color == board.turn:
                    selected_square = clicked_square
                    legal_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]
            else:
                move = chess.Move(selected_square, clicked_square)
                if move in board.legal_moves:
                    board.push(move)
                 # Call AI after player (white) moves
                 # Call AI after player (white) moves
                if not board.is_game_over() and not board.turn:  # AI's turn (Black)
                    ai_move = get_ai_move(board)
                    if ai_move:
                        board.push(ai_move)
                selected_square = None
                legal_moves = []
