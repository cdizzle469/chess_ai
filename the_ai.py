import chess


chess_board = chess.Board()




piece_values = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 100000}





def get_move(board):
    move = list(board.legal_moves)[0]
    best_move, _, _, _ = minimax(board.copy(), 3, float('inf'), float('-inf'), move)
    return best_move
    
board= chess.Board()

pieces = board.piece_map()

for square, piece in pieces.items():
    print(str(chess.square_name(square)))
    print(square)

for i in pieces:
    print(i)

def evaluate(board):
    eval = 0
    pieces = board.piece_map()
    if board.is_checkmate():
        if board.turn:
            return float('-inf')
        else:
            return float('inf')
    for square, piece in pieces.items():
        piece_type = piece.piece_type
        if piece.color == chess.WHITE:
            if len(pieces.items())<10:
                eval+=piece_values.get(piece_type)
            if piece.piece_type == chess.PAWN:
                eval += int(str(chess.square_name(square))[1])/20
            
        else:
            
            if piece.piece_type == chess.PAWN:
                if len(pieces.items())<10:
                    eval += int(str(chess.square_name(square))[1])/20
            eval-=piece_values.get(piece_type)
        
        piece = board.piece_at(square)
        if piece.piece_type == chess.KING:
            if piece.color:
                eval+=len([move for move in board.legal_moves if move.from_square == square])
            else:
                eval-=len([move for move in board.legal_moves if move.from_square == square])
    if board.turn:
        for move in board.legal_moves:
            eval+=0.01
    else:
        for move in board.legal_moves:
            eval-=0.01
    
    if board.is_stalemate():
        return 0
    return eval


def minimax(board, depth, alpha, beta, best_move):
    moves = list(board.legal_moves)
   
    if board.is_checkmate() or depth==0:
        return best_move, evaluate(board), alpha, beta
    if board.turn:
        best_eval = float('-inf')
        for move in moves:
                
            board.push(move)
            _, val, alpha, beta = minimax(board, depth-1, alpha, beta, best_move)
            
            if val>best_eval:
                best_eval = val
                best_move = move
                
            board.pop()
            if beta>alpha:
                break
        
        alpha = max(alpha, best_eval)
        
        return best_move, best_eval, alpha, beta

    else:
       
        best_eval = float('inf')
        for move in moves:
            board.push(move)
            _, val, alpha, beta = minimax(board, depth-1, alpha, beta, best_move)
            if val<best_eval:
                best_eval = val
                best_move = move
            board.pop()
            
            if alpha<beta:
                break
        beta = min(beta, best_eval)
        return best_move, best_eval, alpha, beta
        

   
   
   
# move = get_move(chess_board)
# print(move)


print(get_move(chess_board))