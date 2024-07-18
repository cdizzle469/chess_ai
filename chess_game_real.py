import pygame
import chess
import sys
import the_ai
from tkinter import *

letter_index = {0: 'a', 1: 'b', 2:'c', 3:'d', 4:'e', 5: 'f', 6:'g', 7:'h'}
letter_index2 = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
castle_map = {'g1': 'h1', 'c1': 'a1', 'g8': 'h8', 'c8': 'a8'}

castle_moves = {
    "h1": "f1",  # White kingside castle
    "a1": "d1",  # White queenside castle
    "h8": "f8",  # Black kingside castle
    "a8": "d8"   # Black queenside castle
} 

board = chess.Board()

def ai_move(board):
    move = the_ai.get_move(board)
    for sprite in all_sprites:
        if sprite.square==move[0:2]:
            sprite.move_for_comp(move)
        
class piece(pygame.sprite.Sprite):
    def __init__(self, image, coords, team, pos, color):
        super().__init__()
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect() 
        self.rect.topleft = (
            (coords[1] + 0.5) * SQUARE_SIZE - self.rect.width / 2,
            (coords[0] + 0.5) * SQUARE_SIZE - self.rect.height / 2
        )
        self.team = team
        self.initial_mouse = True
        self.initial_pos = pos
        self.dragging = False
        self.color = color
        # self.pos = convert_to_coords(self.rect.x, self.rect.y, self.team)
    def update(self):
        if self.dragging:
            if self.initial_mouse:
                initial_mouse = False
            self.rect.x, self.rect.y = pygame.mouse.get_pos()
            self.initial_mouse = False
        else:
            if not self.initial_mouse:
                self.initial_mouse = True
                new_square = convert_to_coords(self.rect.x, self.rect.y, self.team)
                prev_pos = convert_to_coords(self.initial_pos[0], self.initial_pos[1], self.team)
                move = f'{self.initial_pos}{new_square}'
                print(move)
                legal = False
                for i in board.legal_moves:
                    if str(i) == move:
                        print('hi')
                        move = chess.Move.from_uci(move)
                        
                        
                        last_move = str(board.san(move))
                        
                        print(last_move)
                        for sprite in all_sprites:
                            if sprite.initial_pos==new_square:
                                sprite.kill()
                        board.push(move)
                        self.initial_pos = new_square
                        if last_move[0]=='O':
                            print('castle')
                            self.castle(str(move))
                        
                        ai_move(board)
                        legal = True
                    elif str(i)[::4] == move:
                        self.premote()
                if not legal:
                    self.rect.topleft = prev_pos[0]+20, prev_pos[1]+20
    def move_for_comp(self, move):
        self.rect.topleft = convert_to_coords(move[2], move[3], self.team)
        print(move)
        for sprite in all_sprites:
            if sprite.initial_pos == move[2::]:
                sprite.kill()
        self.initial_pos = move[2::]
        board.push(chess.Move.from_uci(move))
    def castle(self, move):
        square = castle_map[move[2::]]
        print(square)
        for sprite in all_sprites:
            if sprite.initial_pos == square:
                sprite.move_for_castle(square)
    def move_for_castle(self, square):
        print(square)
        dest = castle_moves[square]
        self.rect.topleft = convert_to_coords(dest[0], dest[1], self.team)
        self.initial_pos = dest
    def premote(self):
        premotion_type = create_premote_window(self.color)
        self.change_to_premotion(premotion_type)
        
    def change_to_premotion(self, piecetype):
        my_image = f'{self.color}{piecetype}.png'
        
        image = pygame.image.load(my_image)
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect() 
    
        
    
        


def create_premote_window(side):
    options = ['q', 'r', 'n', 'b']
    wn = Tk()
    wn.geometry('200x500')
    option_images = []
    result = None
    def on_choice(choice):
        nonlocal result
        wn.destroy()
        result = choice
       


   
    for i in options:
        image_path = "{}{}.png".format(side, i)
        option_image = PhotoImage(file=image_path)
       
        resize = option_image.subsample(4, 4)
        option_images.append(resize)


        btn = Button(wn, image=resize, command=lambda button_name = i: on_choice(button_name))
       
        btn.pack()


    wn.mainloop()
    return result

        
# Initialize pygame
pygame.init()

# Constants
width, height = 720, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = 92, 96, 97
SQUARE_SIZE = width // 8

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Board")

def convert_to_coords(x, y, team):
    
    if isinstance(x, int):
        if team==0:
            return f'{letter_index[x//SQUARE_SIZE]}{abs((y//SQUARE_SIZE)-8)}'
        else:
            x = abs((x//SQUARE_SIZE)-7)
            return f'{letter_index[x]}{(y//SQUARE_SIZE)+1}'
    else:
        if team==0:
            return (letter_index2[x]*SQUARE_SIZE, abs(int(y)-8)*SQUARE_SIZE)
        else:
            return (abs(letter_index2[x]-7)*SQUARE_SIZE, (int(y)-1)*SQUARE_SIZE)

def ai_move(board):
    move = the_ai.get_move(board)
    move = str(move)
    print(move)
    print(move[0:2])
    for sprite in all_sprites:
        if sprite.initial_pos==move[0:2]:
            
            sprite.move_for_comp(move)
            
def start_game(team):
    board = chess.Board()
    square = 0
    if team == 1:
        board.apply_transform(chess.flip_horizontal)
    
    pieces = board.piece_map()
    
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if square in pieces:
                if team==1:
                    if pieces[square].color:
                        team_col = 'w'
                    else:
                        team_col = 'b'
                else:
                    if pieces[chess.square_mirror(square)].color:
                        team_col = 'w'
                    else:
                        team_col = 'b'
                if team==1:
                    imp = piece('{}{}.png'.format(team_col, str(pieces[square]).lower()), [row, col], team, f'{letter_index[abs(col-7)]}{row+1}', team_col)
                else:
                    imp = piece('{}{}.png'.format(team_col, str(pieces[square]).lower()), [row, col], team, f'{letter_index[col]}{abs(row-8)}', team_col)
                all_sprites.add(imp)
            square+=1
            
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

all_sprites = pygame.sprite.Group()

smallfont = pygame.font.SysFont('Corbel',35) 
  
# rendering a text written in 
# this font 
text = smallfont.render('play' , True , (110, 111, 50)) 

# this font 
white_pick = smallfont.render('White' , True , (0, 0, 0)) 

black_pick = smallfont.render('Black' , True , (0, 0, 0)) 
game_start = 0
team = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if event.button == 1:  # Left mouse button
                # Check if the mouse is over any draggable sprite in the group
                for sprite in all_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.dragging = True
            if game_start<1:
                if width/2-40 <= mouse[0] <= width/2+90 and height/2 <= mouse[1] <= height/2+40: 
                   start_game(team)
                   game_start+=1
                   if team==1:
                       ai_move(board)

                if width/2-150 <= mouse[0] <= width/2-10 and height/2-50 <= mouse[1] <= height/2-10: 
                   team=0
                   print(team)

                if width/2+50 <= mouse[0] <= width/2+180 and height/2-50 <= mouse[1] <= height/2-10: 
                   team=1
                   print(team)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for sprite in all_sprites:
                    sprite.dragging = False
    mouse = pygame.mouse.get_pos()

    if game_start<1:
        screen.fill(WHITE)
    
        
        if width/2-50 <= mouse[0] <= width/2+90 and height/2 <= mouse[1] <= height/2+40: 

            pygame.draw.rect(screen,WHITE,[width/2-40,height/2,140,40]) 
          
        else:

            pygame.draw.rect(screen,BLACK,[width/2-40,height/2,140,40]) 
        # if width/2 <= mouse[0] <= width/2+40 and height/2 <= mouse[1] <= height/2-50: 
        #     pygame.draw.rect(screen,WHITE,[width/2,height/2,140,40])
            
        # else: 
        #     pygame.draw.rect(screen,BLACK,[width/2,height/2,140,50])
        if team == 1:
            pygame.draw.rect(screen,GREY,[width/2+50,height/2-50,140,40])
        else:
            
            pygame.draw.rect(screen,GREY,[width/2-100,height/2-50,140,40])
        
            
        screen.blit(text, (width/2,height/2))
        
        screen.blit(white_pick, (width/2-100,height/2-50))
        
        screen.blit(black_pick, (width/2+100,height/2-50))
        
    else:
        draw_board()
        all_sprites.draw(screen)
        all_sprites.update()
        
    pygame.display.flip()