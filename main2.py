import pygame
from pygame import gfxdraw
from config import *
from typing import *
from board import Board

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

def get_moves_after_blocked(moves : List[Tuple[int, int]], board: Board, keep_first = False):
  valid_moves = []
  for move in moves:
    if not board.check_square_empty(move[0], move[1]):
      if keep_first:
        valid_moves.append(move)
      break
    
    valid_moves.append(move)

  return valid_moves
  
def draw_available_moves(board : Board, screen : pygame.Surface) -> List[Tuple[int,int]]:
  available_move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
  available_move_surface.fill((0,0,0,0))
  gfxdraw.filled_circle(available_move_surface, SQUARE_SIZE // 2, SQUARE_SIZE//2, 15, LIGHT_GREY_TRANSPARENT)

  valid_moves = board.selected_piece.current_moves
  for row, col in valid_moves:
    screen.blit(available_move_surface, 
      (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
def handle_event(event, board : Board, current_player : int) -> bool:
    mouse_pos = pygame.mouse.get_pos()
  
    if event.type == pygame.MOUSEBUTTONUP:
        
      if board.selected_piece and board.selected_piece.player == current_player:
        for row, col in board.selected_piece.current_moves:
          selected_rect = pygame.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
          
          if selected_rect.collidepoint(mouse_pos):
            
            board.remove_piece_at(row, col)
            board.move_selected_piece(row, col)
            current_player += 1
            board.selected_piece = None
            return True
          
          
      for piece in board.pieces:
          if piece.rect.collidepoint(mouse_pos):
            if board.selected_piece == piece:
              board.selected_piece = None
            elif piece.player == current_player:
              board.selected_piece = piece 
      
    return False
       
  

def main():
  
  # TODO: ADD turn based to game
  
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  selected_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
  selected_surface.fill(YELLOW_TRANSPARENT)
  
  board = Board()
  board.create_board()
  turn_counter = 0
    
  while True:
    current_player = 1 if turn_counter % 2 == 0 else 2
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      
      update_counter = handle_event(event, board, current_player)
      if update_counter: turn_counter += 1
        
            
    screen.fill(BLACK)
    
    draw_board(screen)
    
    if board.selected_piece:
      screen.blit(selected_surface, 
        (board.selected_piece.row * SQUARE_SIZE, board.selected_piece.col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
      
    
    draw_labels(screen)
    
    for piece in board.pieces:
      piece.update(screen)
      
    if board.selected_piece:
      draw_available_moves(board, screen)
      
    hovered = False
    for piece in board.pieces:
      if piece.rect.collidepoint(mouse_pos) and piece.player == current_player:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        hovered = True
        break

    if not hovered:
      pygame.mouse.set_cursor(*pygame.cursors.arrow)
     
  
    
    pygame.display.update()


  
if __name__ == "__main__":
  main()