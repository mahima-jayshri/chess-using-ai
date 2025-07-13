import chess
import math
#import random

# Assign piece values for evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000
}

# Evaluate the board: positive if White is better, negative if Black
def evaluate_board(board):
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Piece values
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Piece-square tables for white (mirrored for black)
    pawn_table = [
         0,  5,  5, -10, -10,  5,  5,  0,
         0, 10, -5,  0,  0, -5, 10,  0,
         0, 10, 10, 20, 20, 10, 10,  0,
         5, 15, 20, 25, 25, 20, 15,  5,
         5, 10, 10, 20, 20, 10, 10,  5,
         0,  5, 10, 10, 10, 10,  5,  0,
         0,  0,  0,  0,  0,  0,  0,  0,
         0,  0,  0,  0,  0,  0,  0,  0
    ]

    knight_table = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ]

    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values.get(piece.piece_type, 0)

            # Add positional value
            if piece.piece_type == chess.PAWN:
                positional = pawn_table[square if piece.color == chess.WHITE else chess.square_mirror(square)]
            elif piece.piece_type == chess.KNIGHT:
                positional = knight_table[square if piece.color == chess.WHITE else chess.square_mirror(square)]
            else:
                positional = 0  # You can add more tables later

            total_piece_value = value + positional

            if piece.color == chess.WHITE:
                score += total_piece_value
            else:
                score -= total_piece_value

    # Add mobility
    mobility = len(list(board.legal_moves))
    board.push(chess.Move.null())  # Pass turn to opponent
    opp_mobility = len(list(board.legal_moves))
    board.pop()

    score += 0.1 * (mobility - opp_mobility)

    return score

     

# Minimax with depth limit
def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            print(move, evaluate_board(board))
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move



# Public function to get the best move for AI (Black)
def get_ai_move(board, depth=2):
    if board.turn == chess.BLACK:
        _, best_move = minimax(board, depth, -math.inf, math.inf, False)
        return best_move
    return None
