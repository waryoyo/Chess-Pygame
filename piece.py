import pygame
from enum import Enum
from config import *
from typing import *
from abc import ABC, abstractmethod

def check_square_valid(row : int, col : int) -> bool:
  if row < 0 or row >= 8:
    return False
  if col < 0 or col >= 8:
    return False
  
  return True


class Piece_Type(Enum):
  PAWN = 1
  BISHOP = 2
  KNIGHT = 3
  ROOK = 4
  QUEEN = 5
  KING = 6

class Piece_sprite(pygame.sprite.Sprite):
  def __init__(self, spritesheet) -> None:
    pygame.sprite.Sprite.__init__(self)
    self.spritesheet = pygame.image.load(spritesheet).convert_alpha()
    self.spritesheet = pygame.transform.smoothscale(self.spritesheet, (SQUARE_SIZE, SQUARE_SIZE))

class Piece(ABC):
  def __init__(self, base : Piece_sprite, row : int, col : int, player : int = 1) -> None:
    self.row = row
    self.col = col
    self.base = base
    self.player = player
    self.rect = base.spritesheet.get_rect()
    self.rect.x = row * SQUARE_SIZE
    self.rect.y = col * SQUARE_SIZE
    self.current_moves = None
    self.protected = False

  
  def update(self, surface):
    sprite = self.base.spritesheet
    surface.blit(sprite, (self.row * SQUARE_SIZE, self.col * SQUARE_SIZE))
  
  def move(self, row : int, col : int):
    self.row = row
    self.col = col
    self.rect.x = row * SQUARE_SIZE
    self.rect.y = col * SQUARE_SIZE
  
  def store_current_valid_moves(self, moves : List[Tuple[int, int]]) -> None:
    self.current_moves = moves
    
  @abstractmethod
  def valid_moves(self) -> List[Tuple[int, int]]:
    pass
  
  @property
  @abstractmethod
  def get_type(self) -> Piece_Type:
    pass

class Pawn(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)
        self.made_first_move = False

    def valid_moves(self):
        valid_moves = []  
        direction = -1 if self.player == 1 else 1 
        
        if self.made_first_move:
          valid_moves.append((self.row, self.col + direction))
        else:
          for i in range(1, 3):
            valid_moves.append((self.row, self.col + (i * direction) ))
        
        return valid_moves
    
    def move(self, row : int, col : int):
      self.made_first_move = True
      
      self.row = row
      self.col = col
      self.rect.x = row * SQUARE_SIZE
      self.rect.y = col * SQUARE_SIZE
  
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.PAWN
    
class King(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)

    def valid_moves(self) -> List[Tuple[int, int]]:
        valid_moves = []
        directions = [(1, -1), (-1, 1), (1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)] 
        
        for d_x, d_y in directions:
          x, y = self.row + d_x, self.col + d_y
          valid_moves.append((x, y))
           
        return valid_moves
  
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.KING

class Bishop(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)

    def valid_moves(self) -> List[Tuple[int, int]]:
        valid_moves = []
        directions = [(1, -1), (-1, 1), (1, 1), (-1, -1)]        
        
        for d_x, d_y in directions:
          x, y = self.row + d_x, self.col + d_y
          current_moves = []
          
          while check_square_valid(x, y):
            current_moves.append((x, y))
            x += d_x
            y += d_y

          if current_moves:
            valid_moves.append(current_moves)
        
        return valid_moves
  
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.BISHOP

class Knight(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)

    def valid_moves(self) -> List[Tuple[int, int]]:
        valid_moves = []
        
        directions = [(2, 1), (2, -1), (-1, 2), (1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2)]
        x, y = self.row, self.col
        
        for d_x, d_y in directions:
          if check_square_valid(x + d_x, y + d_y):
            valid_moves.append((x + d_x, y + d_y))
      
        return valid_moves
          
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.KNIGHT

class Rook(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)

    def valid_moves(self) -> List[Tuple[int, int]]:
        valid_moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]        
        
        for d_x, d_y in directions:
          x, y = self.row + d_x, self.col + d_y
          current_moves = []
          
          while check_square_valid(x, y):
            current_moves.append((x, y))
            x += d_x
            y += d_y

          if current_moves:
            valid_moves.append(current_moves)
        
        return valid_moves
    
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.ROOK

class Queen(Piece):
    def __init__(self, base: Piece_sprite, row: int, col: int, player: int = 1) -> None:
        super().__init__(base, row, col, player)

    def valid_moves(self) -> List[Tuple[int, int]]:
        valid_moves = []
        directions = [(1, -1), (-1, 1), (1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]        
        
        for d_x, d_y in directions:
          x, y = self.row + d_x, self.col + d_y
          current_moves = []
          
          while check_square_valid(x, y):
            current_moves.append((x, y))
            x += d_x
            y += d_y

          if current_moves:
            valid_moves.append(current_moves)
        
        return valid_moves
    @property
    def get_type(self) -> Piece_Type:
      return Piece_Type.QUEEN