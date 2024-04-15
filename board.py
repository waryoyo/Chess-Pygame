from util import *
from piece import Piece_Type
import itertools

class Board:
  def __init__(self) -> None:
    self.board_map = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    self.pa_1_king_map = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]
    self.pa_2_king_map = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]

    self.pieces = create_pieces()
    self.selected_piece = None
    self.checked = False
    self.checked_lines = []

    # self.selected_piece_valid_moves = []

  
  def get_moves_after_blocked(self, moves : List[Tuple[int, int]], keep_first = False):
    valid_moves = []
    for move in moves:
      if not self.check_square_empty(move[0], move[1]):
        if keep_first:
          valid_moves.append(move)
        break
      
      valid_moves.append(move)

    return valid_moves
  
  def get_moves_after_blocked_player(self, moves : List[Tuple[int, int]], player : int):
    valid_moves = []
    for move in moves:
      if not self.check_square_empty(move[0], move[1]) and self.check_same_player(move[0], move[1], player):
        break
      
      valid_moves.append(move)

    return valid_moves
    
  def calculate_valid_moves(self, piece : Piece):
    
    # TODO: Prevent 2 kings from touching each other by removing intersections between them.
    
    other_king_map = self.pa_1_king_map if piece.player == 2 else self.pa_2_king_map
    
    direction = -1 if piece.player == 1 else 1
    
    if piece.get_type == Piece_Type.PAWN:
      valid_moves = piece.valid_moves()
      valid_moves = self.get_moves_after_blocked(valid_moves)
    
      if check_square_valid(piece.row + 1, piece.col + (1 * direction)):
        other_king_map[piece.col + (1 * direction)][piece.row + 1] = True

      if not self.check_square_empty(piece.row + 1, piece.col + (1 * direction)):
        valid_moves.append((piece.row + 1, piece.col + (1 * direction)))
        
      if check_square_valid(piece.row - 1, piece.col + (1 * direction)):
        other_king_map[piece.col + (1 * direction)][piece.row - 1] = True    
    
      if not self.check_square_empty(piece.row - 1, piece.col + (1 * direction)):
        valid_moves.append((piece.row + - 1, piece.col + (1 * direction)))
    
    elif any(piece.get_type == t for t in (Piece_Type.BISHOP, Piece_Type.ROOK, Piece_Type.QUEEN)):
      valid_moves = piece.valid_moves()
      
      for moves_list in valid_moves:
        for move in moves_list:
          if not self.check_square_empty(move[0], move[1]):
            other_king_map[move[1]][move[0]] = True
            if self.get_piece_at_square(move[0], move[1]).get_type != Piece_Type.KING:
              break
          else:
            other_king_map[move[1]][move[0]] = True
            
      
      valid_moves = list(map(lambda x : self.get_moves_after_blocked(x, True), valid_moves))

      valid_moves = list(itertools.chain(*valid_moves))
    
    elif piece.get_type == Piece_Type.KNIGHT:
      valid_moves = piece.valid_moves()
      for row, col in valid_moves:
        if not self.check_square_empty(row, col):
          other_king_map[col][row] = True

    
    elif piece.get_type == Piece_Type.KING:
      current_king_map = self.pa_2_king_map if piece.player == 2 else self.pa_1_king_map
      valid_moves = set(piece.valid_moves())
      
      # for move in valid_moves:
      #   if check_square_valid(move[1], move[0]):
      #     other_king_map[move[1]][move[0]] = True
      
      
      for i in range(len(current_king_map)):
        for j in range(len(current_king_map)):
          if current_king_map[i][j]:
            if (j, i) in valid_moves:
              valid_moves.remove((j, i))
      
      valid_moves = list(valid_moves)
    
    valid_moves = list(filter(lambda x : not self.check_same_player(x[0], x[1], piece.player), valid_moves))

    return valid_moves
  
  def update_pinned_pieces(self) -> None:
    piece_t = None
    
    for p in self.pieces:
      if any(p.get_type == t for t in (Piece_Type.BISHOP, Piece_Type.ROOK, Piece_Type.QUEEN)):
        valid_moves = p.valid_moves()
        for move_list in valid_moves:
          move_list = self.get_moves_after_blocked_player(move_list, p.player)
          for move in move_list:
            if piece_t and not self.check_square_empty(move[0], move[1]):
              if self.get_piece_at_square(move[0], move[1]).get_type == Piece_Type.KING:
                temp = move_list + [(p.row, p.col)]
                temp = list(set(piece_t.current_moves).intersection(temp))
                piece_t.store_current_valid_moves(temp)
              else:
                break
            
            if not piece_t and not self.check_square_empty(move[0], move[1]):
              piece_t = self.get_piece_at_square(move[0], move[1])
          
          piece_t = None
    
  def scan_for_checks(self, kings) -> None:
    pass
    # TODO: During the valid pieces calculation a certain list
    # of the moves or lines that should be blocked by pieces and then those lines
    # will be intersected with all of those of the pieces of the checked player
    
    # for king in kings:
    #   current_king_map = self.pa_2_king_map if king.player == 2 else self.pa_1_king_map
      
    #   if current_king_map[king.col][king.row]:
    #     self.checked = True
        
    #     for piece in self.pieces:
    #       temp = list(set(piece_t.current_moves).intersection(temp))


  
  def create_board(self):
    for piece in self.pieces:
      self.board_map[piece.col][piece.row] = piece
    
    # do kings last
    kings = []
    for piece in self.pieces:
      if piece.get_type == Piece_Type.KING:
        kings.append(piece)
        continue
      
      piece.store_current_valid_moves(self.calculate_valid_moves(piece))
    
    for king in kings:
      king.store_current_valid_moves(self.calculate_valid_moves(king))
  
  def check_square_empty(self, row : int, col : int) -> bool:
    if row >= len(self.board_map) or col >= len(self.board_map[0]) or self.board_map[col][row] == None:
      return True
    
    return False

  def remove_piece_at(self, row : int, col : int) -> None:
    if row >= len(self.board_map) or col >= len(self.board_map[0]) or self.board_map[col][row] == None:
      return
    
    piece_to_remove = self.board_map[col][row]
    self.board_map[col][row] = None
    
    for piece in self.pieces:
      if piece == piece_to_remove:
        self.pieces.remove(piece)
  
  def get_piece_at_square(self, row : int, col : int) -> Piece:
    if row >= len(self.board_map) or col >= len(self.board_map[0]) or self.board_map[col][row] == None:
      return None
    
    return self.board_map[col][row]

  def check_same_player(self, row : int, col : int, player : int) -> bool:
    if row >= len(self.board_map) or col >= len(self.board_map[0]) or self.board_map[col][row] == None:
      return None
    
    return self.board_map[col][row].player == player
  
  def move_selected_piece(self, new_row, new_col):
    if new_row >= len(self.board_map) or new_col >= len(self.board_map[0]) or self.selected_piece == None:
      return
    
    self.board_map[self.selected_piece.col][self.selected_piece.row] = None
    self.selected_piece.move(new_row, new_col)
    self.board_map[new_col][new_row] = self.selected_piece
    
    # do kings last
    self.pa_1_king_map = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]
    self.pa_2_king_map = [[False] * BOARD_COLS for _ in range(BOARD_ROWS)]
    
    kings = []
    for piece in self.pieces:
      if piece.get_type == Piece_Type.KING:
        kings.append(piece)
        continue
      
      piece.store_current_valid_moves(self.calculate_valid_moves(piece))
    
    for king in kings:
      king.store_current_valid_moves(self.calculate_valid_moves(king))

    self.update_pinned_pieces() 
    
    intersection = set(kings[0].valid_moves()).intersection(kings[1].valid_moves())
    
    kings[0].store_current_valid_moves(list(set(kings[0].current_moves).difference(intersection)))
    kings[1].store_current_valid_moves(list(set(kings[1].current_moves).difference(intersection)))


    