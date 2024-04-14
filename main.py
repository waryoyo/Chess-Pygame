import pygame
from pygame import gfxdraw
from config import *
from piece import Piece_sprite, Piece, Piece_Type
from typing import *
from util import create_pieces, remove_piece_empty, check_square_empty
import itertools

def draw_board(screen : pygame.Surface):
  for i in range(BOARD_ROWS):
    for j in range(BOARD_COLS):
      color = BOARD_COLORS[0]
      if (i + j) % 2:
        color = BOARD_COLORS[1]
      
      pygame.draw.rect(screen, color, 
        (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_labels(screen : pygame.Surface):
  font = pygame.font.SysFont(None, 24)
  
  for i in range(BOARD_ROWS):
    color = BOARD_COLORS[0]
    if i % 2 == 0:
      color = BOARD_COLORS[1]
    
    text = font.render(NUMBERS[i], True, color)
    screen.blit(text, (5, i * SQUARE_SIZE + 10))
    
    color = BOARD_COLORS[1]
    if i % 2 == 0:
      color = BOARD_COLORS[0]
    
    text = font.render(LETTERS[i], True, color)
    screen.blit(text, (i * SQUARE_SIZE + 63, HEIGHT - 20))

def get_moves_after_blocked(moves : List[Tuple[int, int]], pieces : List[Piece], keep_first = False):
  valid_moves = []
  for move in moves:
    if not check_square_empty(pieces, move[0], move[1]):
      if keep_first:
        valid_moves.append(move)
      break
    
    valid_moves.append(move)

  return valid_moves
  
def draw_available_moves(selected_piece : Piece, pieces: List[Piece], screen : pygame.Surface) -> List[Tuple[int,int]]:
  available_move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
  available_move_surface.fill((0,0,0,0))
  gfxdraw.filled_circle(available_move_surface, SQUARE_SIZE // 2, SQUARE_SIZE//2, 15 ,LIGHT_GREY_TRANSPARENT)
  
  valid_moves = []
  
  direction = 1
  
  if selected_piece.player == 1:
    direction *= -1
    
  if selected_piece.get_type == Piece_Type.PAWN:
    valid_moves = selected_piece.valid_moves()
    valid_moves = get_moves_after_blocked(valid_moves, pieces)
  
    if not check_square_empty(pieces, selected_piece.row + 1, selected_piece.col + (1 * direction)):
      valid_moves.append((selected_piece.row + 1, selected_piece.col + (1 * direction)))
  
    if not check_square_empty(pieces, selected_piece.row - 1, selected_piece.col + (1 * direction)):
      valid_moves.append((selected_piece.row + - 1, selected_piece.col + (1 * direction)))
  
  elif selected_piece.get_type == Piece_Type.BISHOP or selected_piece.get_type == Piece_Type.ROOK:
    valid_moves = selected_piece.valid_moves()
    valid_moves = list(map(lambda x : get_moves_after_blocked(x, pieces, True), valid_moves))

    valid_moves = list(itertools.chain(*valid_moves))
  
  elif selected_piece.get_type == Piece_Type.KNIGHT:
    valid_moves = selected_piece.valid_moves()
  

  valid_moves = list(filter(lambda x : x.player != selected_piece.player,valid_moves))
  
  for row, col in valid_moves:
    screen.blit(available_move_surface, 
      (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
  return valid_moves
  
def handle_event(event, pieces : List[Piece], selected_piece, valid_moves : List[Tuple[int,int]]):
    mouse_pos = pygame.mouse.get_pos()
  
    if event.type == pygame.MOUSEBUTTONUP:
        
      if selected_piece:
        for row, col in valid_moves:
          selected_rect = pygame.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
          if selected_rect.collidepoint(mouse_pos):
            remove_piece_empty(pieces, row, col)
            selected_piece.move(row, col)
            selected_piece = None
            valid_moves = []
            return selected_piece, valid_moves
          
          
      for piece in pieces:
          if piece.rect.collidepoint(mouse_pos):
            if selected_piece == piece:
              selected_piece = None
              valid_moves = []
            else:
              selected_piece = piece 
      
    return selected_piece, valid_moves 
       
  

def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  selected_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
  selected_surface.fill(YELLOW_TRANSPARENT)
  
  pieces = create_pieces()
  
  selected_piece = None  
  valid_moves = []
  
  while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      
      selected_piece, valid_moves = handle_event(event, pieces, selected_piece, valid_moves)
        
            
    screen.fill(BLACK)
    
    draw_board(screen)
    
    if selected_piece:
      screen.blit(selected_surface, 
        (selected_piece.row * SQUARE_SIZE, selected_piece.col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
      
    
    draw_labels(screen)
    
    for piece in pieces:
      piece.update(screen)
      
    if selected_piece:
      valid_moves = draw_available_moves(selected_piece, pieces, screen)
      
    hovered = False
    for piece in pieces:
      if piece.rect.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        hovered = True
        break

    if not hovered:
      pygame.mouse.set_cursor(*pygame.cursors.arrow)
     
  
    
    pygame.display.update()


  
if __name__ == "__main__":
  main()