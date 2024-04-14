from config import *
from typing import *
from piece import *

def get_square(number, letter) -> Tuple[int, int]:
  row = BOARD_ROWS - number
  col = ord(letter) - ord('a')
  
  return (row, col)

def check_square_empty(pieces : List[Piece], row : int, col : int) -> bool:
  for piece in pieces:
    if piece.row == row and piece.col == col:
      return False
  
  return True

def remove_piece_empty(pieces : List[Piece], row : int, col : int) -> None:
  for piece in pieces:
    if piece.row == row and piece.col == col:
      pieces.remove(piece)
      break
    
def create_pieces() -> List[Piece]:
  
  # base textures for all pieces
  w_pawn_base = Piece_sprite("assets\\pieces\\white\\wp.png")
  b_pawn_base = Piece_sprite("assets\\pieces\\black\\bp.png")

  w_rook_base = Piece_sprite("assets\\pieces\\white\\wr.png")
  b_rook_base = Piece_sprite("assets\\pieces\\black\\br.png")

  w_knight_base = Piece_sprite("assets\\pieces\\white\\wn.png")
  b_knight_base = Piece_sprite("assets\\pieces\\black\\bn.png")
  
  w_bishop_base = Piece_sprite("assets\\pieces\\white\\wb.png")
  b_bishop_base = Piece_sprite("assets\\pieces\\black\\bb.png")
  
  w_queen_base = Piece_sprite("assets\\pieces\\white\\wq.png")
  b_queen_base = Piece_sprite("assets\\pieces\\black\\bq.png")

  w_king_base = Piece_sprite("assets\\pieces\\white\\wk.png")
  b_king_base = Piece_sprite("assets\\pieces\\black\\bk.png")
  
  pieces = []

  # adding the white pawns 
  for c in LETTERS:
    row, col = get_square(2, c)
    pieces.append(Pawn(w_pawn_base, col, row))
  
  # adding the white rooks 
  row, col = get_square(1, 'a')
  pieces.append(Rook(w_rook_base, col, row))
  row, col = get_square(1, 'h')
  pieces.append(Rook(w_rook_base, col, row))
  
  # adding the white knights 
  row, col = get_square(1, 'b')
  pieces.append(Knight(w_knight_base, col, row))
  row, col = get_square(1, 'g')
  pieces.append(Knight(w_knight_base, col, row))
  
  # adding the white bishops 
  row, col = get_square(1, 'c')
  pieces.append(Bishop(w_bishop_base, col, row))
  row, col = get_square(1, 'f')
  pieces.append(Bishop(w_bishop_base, col, row))
  
  # adding the white queen 
  row, col = get_square(1, 'd')
  pieces.append(Queen(w_queen_base, col, row))
  
  # adding the white king 
  row, col = get_square(1, 'e')
  pieces.append(King(w_king_base, col, row))
  
  #
  # ADDING BLACK PIECES
  #
  
  
  # adding the black pawns 
  for c in LETTERS:
    row, col = get_square(7, c)
    pieces.append(Pawn(b_pawn_base, col, row, 2))
  
  # adding the black rooks 
  row, col = get_square(8, 'a')
  pieces.append(Rook(b_rook_base, col, row, 2))
  row, col = get_square(8, 'h')
  pieces.append(Rook(b_rook_base, col, row, 2))
  
  # adding the black knights 
  row, col = get_square(8, 'b')
  pieces.append(Knight(b_knight_base, col, row, 2))
  row, col = get_square(8, 'g')
  pieces.append(Knight(b_knight_base, col, row, 2))
  
  # adding the black bishops 
  row, col = get_square(8, 'c')
  pieces.append(Bishop(b_bishop_base, col, row, 2))
  row, col = get_square(8, 'f')
  pieces.append(Bishop(b_bishop_base, col, row, 2))
  
  # adding the black queen 
  row, col = get_square(8, 'd')
  pieces.append(Queen(b_queen_base, col, row, 2))
  
  # adding the black king 
  row, col = get_square(8, 'e')
  pieces.append(King(b_king_base, col, row, 2))
  
  return pieces