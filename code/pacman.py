### Just mucking about with pygame
### and using poetry
### and trying to store this in GitHub



##from scipy.spatial.transform import Rotation as R
import numpy as np
import pygame
import random
import sys


pygame.init()

#### G l o b a l   V a r s ####
NUM_TILES_WIDE = 25
NUM_TILES_HIGH = 25
TILE_WIDTH = 40
TILE_HEIGHT = 40
WIDTH = NUM_TILES_WIDE * TILE_WIDTH
HEIGHT = NUM_TILES_HIGH * TILE_HEIGHT
PLAYER_WIDTH = int(TILE_WIDTH *0.8)
PLAYER_HEIGHT = int(TILE_HEIGHT *0.8)
COUNTDOWN = 15 ### Length of game in seconds
PLAYER_NUM_LIVES = 3

def create_board(width, height):
    #create an array where every element is a number that signifies what kind of tile it is
    ### fill 2D array with ones, our default type for a barrier
    ## 0 = no barrier
    ## 1 = barrier
    ## 2 = point_ pill: if the player gets to this tile they get a point and the tile changes to 0
    ## 3 = exit: if the player gets here, they can go to the next level if they have enough points
    ## 4 = ghost_home: effectively type 0 but a different colour
    ## 5 = slime: players and ghosts will bounce off and change direction
    
    board_array = np.ones((height, width), int)
    for row in range(1, height-1):  #the top/first row is a border of 1's, so skip row zero
        if row == 1: ## special row where our first walls are created
            ## population = [' ', '1', 'o', 'X', 'h', 's']
            population = [0,1,2,3,4,5]
            weights =    [0,30, 60, 0, 0, 5]
            randomised_row = random.choices(population, weights, k=width)
            board_array[1] = randomised_row
            ### attempt to avoid two consecutive wall tiles
            for tile in range(2, width):  ### start at 2 since on this row we want 1 then 0
                if board_array[1][tile-1] == 1 and board_array[1][tile] == 1:
                    board_array[1][tile-1] = 2  ## change wall to point_pill
            board_array[1,0] = '1' ## left border
            board_array[1, width-1] = '1'  ## right border
        else:
            for col in range(1,width-1): ##don't change first and last memebers since they are the border
                population = [0,1,2,3,4,5]
                weights =    [0,30, 60, 0, 0, 5]
                randomised_tile = random.choices(population, weights, k=1)
                board_array[row][col] = randomised_tile[0]  ##hack: the above returns a one element array
                ### to avoid thick walls - if the tiles on 3 sides (not to the right) are a wall, make this a power pill
                if board_array[row][col] == 1 and board_array[row-1][col] == 1 and board_array[row-1][col-1] == 1 and board_array[row-1][col-1] == 1:
                    board_array[row][col] = 2
                ### swap out slime if there is one to the left
                if board_array[row][col] == 5 and board_array[row][col-1] == 5:
                    board_array[row][col] = 2
                ### swap out slime if there is one above
                if board_array[row][col] == 5 and board_array[row-1][col] == 5:
                    board_array[row][col] = 2

    ## Make the central 3x3 area into point_pills so player can start there and not be locked in
    board_array[-1 + height//2, -1+width//2] = 2
    board_array[-1 + height//2,    width//2] = 2
    board_array[-1 + height//2, 1+ width//2] = 2
    board_array[height//2, -1+width//2] = 2 ## set the middle tile to point_pill
    board_array[height//2,    width//2] = 2
    board_array[height//2,  1+width//2] = 2
    board_array[1 + height//2, -1 +width//2] = 2
    board_array[1 + height//2,     width//2] = 2
    board_array[1 + height//2,  1 +width//2] = 2

    return board_array

def draw_board(screen, board):
    """
    Draws a board on the given screen using the provided board array.

    Parameters:
        screen (pygame.Surface): The surface on which the board will be drawn.
        board (numpy.ndarray): The array representing the board. Each element in the array represents a tile on the board.
            The possible values are:
                0: Empty tile.
                1: Wall tile.
                2: Tile with a point pill.
                3: Unused tile.
                4: Unused tile.
                5: Green toxic blob tile.

    Returns:
        None

    Raises:
        SystemExit: If an unhandled tile type is encountered.
    """
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:  ## empty
                my_rectangle = (row*TILE_WIDTH, col*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(screen, (20,20,190),my_rectangle)
            elif board[row][col] == 1: ## walls
                my_rectangle = (row*TILE_WIDTH, col*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(screen, (200,215,255),my_rectangle)
            elif board[row][col] == 2:  ## like empty but with a point_pill
                scale = 5 ## scale by 1/scale
                my_ellipse_rectangle = (row*TILE_WIDTH+(TILE_WIDTH//2) -(TILE_WIDTH//(2*scale)), col*TILE_HEIGHT+(TILE_HEIGHT//2) -(TILE_HEIGHT//(2*scale)),
                                        TILE_WIDTH//scale, TILE_HEIGHT//scale)
                pygame.draw.ellipse(screen, (255,255,220),my_ellipse_rectangle)
            elif board[row][col] == 3:  ## unused
                my_rectangle = (row*TILE_WIDTH, col*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(screen, (100,150,0),my_rectangle)
            elif board[row][col] == 4:  ## unused
                my_rectangle = (row*TILE_WIDTH, col*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(screen, (0,150,100),my_rectangle)
            elif board[row][col] == 5: ## green toxic blobs
                my_rectangle = (row*TILE_WIDTH, col*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                pygame.draw.rect(screen, (50,190,50),my_rectangle, 0, int(TILE_WIDTH//10))  ## zero= fill; last values rounds corners
            else:
                print('EXITING: unhandled tile type: ', board[row][col])                                                            
                sys.exit()
    
                


def draw_player(screen, player_sprite, counter, player_x, player_y, direction):
    ## directions: 0=A=Left; 1=S=Down; 2=D=Right; 3=W=Up
    ## it always looks left unless it's going right
    if direction == 0:
        screen.blit(player_sprite[counter//5], (player_x, player_y))
    if direction == 1:
        screen.blit(player_sprite[counter//5], (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.flip(player_sprite[counter//5], True, False), (player_x, player_y))
    if direction == 3:
        screen.blit(player_sprite[counter//5], (player_x, player_y))
    

################################################################################################################
def draw_sprites_under_player(screen, sprites_under_player_list, player_x, player_y):
    for sprite in sprites_under_player_list:
        ## if sprite lifespan is zero, don't draw but instead remove from list
        ## temporary sprites will have lifespan reduced as time goes on
        if sprite.lifespan == 0:
            sprites_under_player_list.remove(sprite)
            continue
        ### draw the sprite from the sprite sheet and index it using lifespan
        sprite_x_in_sheet = sprite.get_curr_x(sprite.lifespan//sprite.life_multiplier)
        sprite_y_in_sheet = sprite.get_curr_y(sprite.lifespan//sprite.life_multiplier)
        sprite_x_in_board = PLAYER_WIDTH + sprite.initial_player_x - sprite.sprite_width_px//2
        sprite_y_in_board = sprite.initial_player_y - sprite.sprite_height_px//2
        screen.blit(sprite.sprite_sheet, (sprite_x_in_board,sprite_y_in_board), (sprite_x_in_sheet,sprite_y_in_sheet,sprite.sprite_width_px,sprite.sprite_height_px)) ##ignore x and y stored in sprite
        sprite.lifespan -= 1



################################################################################################################
class Sprite_list_item:
    def __init__(self,sprite_sheet, pos_x, pos_y, perm, lifespan, num_sprites_in_col, num_sprites_in_row, player_x, player_y, life_multiplier=1):
        self.sprite_sheet = sprite_sheet
        self.sprite_sheet.set_colorkey((0,0,0))
        self.x = pos_x
        self.y = pos_y
        self.perm = perm
        self.lifespan = lifespan * life_multiplier ##number of frames in sprite sheet, multiplied by multiplier to slow animations down
        self.num_sprites_in_col = num_sprites_in_col
        self.num_sprites_in_row = num_sprites_in_row
        self.sprite_width_px = self.sprite_sheet.get_width()//self.num_sprites_in_row
        self.sprite_height_px = self.sprite_sheet.get_height()//self.num_sprites_in_col
        self.initial_player_x = player_x
        self.initial_player_y = player_y
        self.life_multiplier = life_multiplier

    def get_curr_x(self, frame_num):
        return self.sprite_width_px*(frame_num%self.num_sprites_in_row)

    def get_curr_y(self, frame_num):
        return self.sprite_height_px*(frame_num//self.num_sprites_in_row)
    
################################################################################################################
class player:
    def __init__(self, sprite_sheet, pos_x, pos_y, direction = 'left', num_lives = PLAYER_NUM_LIVES,
                 width=PLAYER_WIDTH, height=PLAYER_HEIGHT, tile_width=TILE_WIDTH, tile_height=TILE_HEIGHT):
        self.sprite_sheet = sprite_sheet
        self.x = pos_x
        self.y = pos_y
        ###self.num_sprites_in_col = num_sprites_in_col  ###use if player images are in a single spritesheet
        ###self.num_sprites_in_row = num_sprites_in_row  ##current player anim is bunch of images
        self.direction = direction
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_center_x = int((pos_x+self.width/2)//self.tile_width)
        self.tile_center_y = int((pos_y+self.height/2)//self.tile_height)
        self.num_lives = num_lives

    def print(self):
        print(self.get_tile_x_left(), self.get_tile_x_right(), self.get_tile_y_top(), self.get_tile_y_bot(), self.x, self.y)
            

    def get_tile_x_left(self):
        return int((self.x)//self.tile_width)
    def get_tile_x_right(self):
        return int((self.x+self.width)//self.tile_width)
    def get_tile_y_top(self):
        return int((self.y)//self.tile_height)
    def get_tile_y_bot(self):
        return int((self.y+self.height)//self.tile_height)
    def get_tile_at_center_x(self):
        return int((self.x+self.width/2)//self.tile_width)
    def get_tile_at_center_y(self):
        return int((self.y+self.height/2)//self.tile_height)
    def lose_a_life(self):
        """
        Decrements the number of lives by one.
        This function is used to update the number of lives the player has. It subtracts one from the current number of lives.
        Parameters:
            self (object): The instance of the class.
        Returns:
            None
        """
        self.num_lives -= 1

    def new_tile_type_after_move(self, move_dist_in_px, direction):
        if direction == 'left':
            return int( (self.x-move_dist_in_px)//self.tile_width)
        elif direction == 'right':
            return int( (self.x+self.width+move_dist_in_px)//self.tile_width)
        elif direction == 'up':
            return int( (self.y-move_dist_in_px)//self.tile_height)
        elif direction == 'down':
            return int( (self.y+self.height+move_dist_in_px)//self.tile_height)
    def draw_player(self, screen, counter):
        ## player always looks left unless it's going right
        if self.direction == 'left':
            screen.blit(self.sprite_sheet[counter//5], (self.x, self.y))
        if self.direction == 'down':
            screen.blit(self.sprite_sheet[counter//5], (self.x, self.y))
        if self.direction == 'right':
            screen.blit(pygame.transform.flip(self.sprite_sheet[counter//5], True, False), (self.x, self.y))
        if self.direction == 'up':
            screen.blit(self.sprite_sheet[counter//5], (self.x, self.y))



####END OF PLAYER CLASS#########################################################################################
################################################################################################################
def draw_text(screen, text, size, x, y, colour=(255, 255, 255), mode=0):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    if mode == 1: ## draw same text as black background
        text_bg = font.render( text, True, (0, 0, 0) )
        screen.blit(text_bg, [int(x-text_bg.get_height()/20), int(y - text_bg.get_height()/20)])
    elif mode == 2: ## draw several bg versions of text as shifted drop shadows
        text_bg = font.render( text, True, (0, 0, 0) )
        offset = text_bg.get_height()/20
        screen.blit(text_bg, [int(x-offset*3), int(y - offset*3)])
        text_bg = font.render( text, True, (150, 0, 0) )
        screen.blit(text_bg, [int(x-offset*2), int(y - offset*2)])
        text_bg = font.render( text, True, (255, 0, 0) )
        screen.blit(text_bg, [int(x-offset*1), int(y - offset*1)])
    text2 = font.render( text, True, colour )
    screen.blit(text2, [x, y])



################################################################################################################
def main():
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    fps = 40
    score = 0
    high_score = 0
    high_score_beaten = False
    font = pygame.font.Font('freesansbold.ttf', 20)
    player_sprite = []
    for i in range(1,12):
        player_sprite.append(pygame.transform.scale(pygame.image.load(f'img/pikmon_sequence/pikmon-{i:03d}.png'),(PLAYER_WIDTH,PLAYER_HEIGHT)))
    points_pill_popped_sprite_sheet = pygame.image.load('img/Spritesheets/RocketFire2Sheet.png')

    pygame.display.set_caption("Terrible Pacman-Like Rehash by Malc")

    board = create_board(NUM_TILES_WIDE, NUM_TILES_HIGH)
    ##print(board) ### print the boards tiles to the console
    run = True
    player_x, player_y, player_direction = WIDTH//2, HEIGHT//2, 'left'  ## temp; 
    game_countdown, game_countdown_text = -2, str(COUNTDOWN).rjust(3) ## -2 is <0 so we show the P to PLAY text
    player_frame_counter=0
    player_movement_per_frame = TILE_WIDTH//5
    sprites_under_player_list = []

    player1 = player(player_sprite, WIDTH//2, HEIGHT//2, player_direction, num_lives = PLAYER_NUM_LIVES,
                 width=PLAYER_WIDTH, height=PLAYER_HEIGHT, tile_width=TILE_WIDTH, tile_height=TILE_HEIGHT)
 #### TODO: add player into while loop in parallel I guess
    while run:
        timer.tick(fps)
        if player_frame_counter < 19:
            player_frame_counter += 1
        else:
            player_frame_counter = 0
        screen.fill((20,20,190))
        draw_board(screen, board)
        ### draw the sprites on the board that are in the list. Each list entry is a sprite, a location and a time to live and a boolean
        ### whether the sprite should be taken off the list, that is, the sprite is now dead
        draw_sprites_under_player(screen, sprites_under_player_list, player_x, player_y)
        draw_player(screen, player_sprite, player_frame_counter, player_x, player_y, player_direction)
        player1.draw_player(screen, game_countdown)

        ### draw rectangle around player
        ##pygame.draw.rect(screen, (255,0,0), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT), 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT: 
                if game_countdown > 0: game_countdown -= 1
                game_countdown_text = str(game_countdown).rjust(3) if game_countdown > 0 else 'B O O M!'
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ## if we move in this direction and would change to the next tile
            if player1.get_tile_x_left() != int( (player1.x-player_movement_per_frame)//TILE_WIDTH):
                #### This if checks the tile type that top and bottom left corners of the player would move into
                if int(board[player1.get_tile_x_left()-1][player1.get_tile_y_top()]) == 1 or int(board[player1.get_tile_x_left()-1][player1.get_tile_y_bot()]) ==1:
                    ##if we're here, one hop left is a new tile but the new tile is a wall (block type 1) so don't move
                    pass
                elif int(board[player1.get_tile_x_left()-1][player1.get_tile_y_top()]) == 5 or int(board[player1.get_tile_x_left()-1][player1.get_tile_y_bot()]) == 5:
                    ### tile to the left is toxic, we moved into it so game over
                    game_countdown = -1
                else:
                    player1.x -= player_movement_per_frame
            else:
                player1.x -= player_movement_per_frame
        elif keys[pygame.K_DOWN]:
            ## if we move in this direction and the bottom edge of the player would change to the next tile
            if player1.get_tile_y_bot() != int( (player1.y+ PLAYER_HEIGHT+player_movement_per_frame)//TILE_HEIGHT):
                #### This if checks the tile type that left and right bottom corners of the player would move into
                if int(board[player1.get_tile_x_left()][player1.get_tile_y_bot()+1]) == 1 or int(board[player1.get_tile_x_right()][player1.get_tile_y_bot()+1]) ==1:
                    ##if we're here, one hop down is a new tile but the new tile is a wall (block type 1) so don't move
                    pass
                elif int(board[player1.get_tile_x_left()][player1.get_tile_y_bot()+1]) == 5 or int(board[player1.get_tile_x_right()][player1.get_tile_y_bot()+1]) == 5:
                    ### tile to the bottom is toxic, we moved into it so game over
                    game_countdown = -1
                else:
                    player1.y += player_movement_per_frame
            else:
                player1.y += player_movement_per_frame ##lower edge of player not entering a new tile via movement
        elif keys[pygame.K_RIGHT]: 
            ## if we move in this direction and would change to the next tile
            if player1.get_tile_x_right() != int( (player1.x+ PLAYER_WIDTH+player_movement_per_frame)//TILE_WIDTH):
                #### This if checks the tile type that top and bottom right cornersof the player would move into
                if int(board[player1.get_tile_x_right()+1][player1.get_tile_y_top()]) == 1 or int(board[player1.get_tile_x_right()+1][player1.get_tile_y_bot()]) ==1:
                    ##if we're here, one hop right is a new tile but the new tile is a wall (block type 1) so don't move
                    pass
                elif int(board[player1.get_tile_x_right()+1][player1.get_tile_y_top()]) == 5 or int(board[player1.get_tile_x_right()+1][player1.get_tile_y_bot()]) == 5:
                    ### tile to the right is toxic, we moved into it so game over
                    game_countdown = -1
                else:
                    player1.x += player_movement_per_frame
            else:
                player1.x += player_movement_per_frame
        elif keys[pygame.K_UP]:
            ## if we move in this direction and would change to the next tile
            if player1.get_tile_y_top() != int( (player1.y - player_movement_per_frame)//TILE_HEIGHT):
                #### This if checks the tile type that top and bottom right corners of the player would move into
                if int(board[player1.get_tile_x_left()][player1.get_tile_y_top()-1]) == 1 or int(board[player1.get_tile_x_right()][player1.get_tile_y_top()-1]) ==1:
                    ##if we're here, one hop up is a new tile but the new tile is a wall (block type 1) so don't move
                    pass
                elif int(board[player1.get_tile_x_left()][player1.get_tile_y_top()-1]) == 5 or int(board[player1.get_tile_x_right()][player1.get_tile_y_top()-1]) == 5:
                    ### tile to the top is toxic, we moved into it so game over
                    game_countdown = -1
                else:
                    player1.y -= player_movement_per_frame
            else:
                player1.y -= player_movement_per_frame
            ########## if current tile is a point pill, change to 0 (no barrier i.e. empty space) and play fire anim there
        if board[player1.get_tile_at_center_x()][player1.get_tile_at_center_y()] == 2:
            board[player1.get_tile_at_center_x()][player1.get_tile_at_center_y()] = 0
            tile_center_x = player1.get_tile_at_center_x()*TILE_WIDTH  ##TILE_WIDTH//2
            tile_center_y = player1.get_tile_at_center_y()*TILE_HEIGHT - TILE_HEIGHT//2
            ## create pill pop sprite to be added as a list item, nonpermanent for 25 frames, written to screen before player and under it
            pill_pop = Sprite_list_item(points_pill_popped_sprite_sheet, 0, 0, False, 25, 5,5, tile_center_x, tile_center_y, 2)
            sprites_under_player_list.append(pill_pop)
            if game_countdown > 0: score += 1 ## add 1 to score
        

        draw_text(screen, 'Score: ' + str(score), 40, 10, 10,(255, 0, 55),1) 
        draw_text(screen, 'Time remaining: ' + str(game_countdown_text), 40, WIDTH*5//10, 10, (255, 0, 55),1)
        draw_text(screen, 'High Score: ' + str(high_score), 40, WIDTH*2.1//10, 10, (255, 200, 55),1)
        if score > high_score:
            high_score = score
            high_score_beaten = True
        if game_countdown == 0:
            draw_text(screen, "OOF! GAME OVER DUDE!", 45, WIDTH//10, HEIGHT//2, (255, 0, 55),1)
            if not high_score_beaten:
                draw_text(screen, "My five year old could've done better", 40, WIDTH//10, HEIGHT*55//100, (255, 0, 55),1)
                draw_text(screen, "(and she's a Jack Russel Terrier)", 30, WIDTH//10, HEIGHT*65//100, (255, 0, 55),1)
        elif game_countdown == -1:
            draw_text(screen, "O U C H Y ! GAME OVER DUDE!", 45, WIDTH//10, HEIGHT//2, (255, 0, 55),1)
            draw_text(screen, "**you hit a toxic slime cube**", 45, WIDTH//10, HEIGHT*55//100, (255, 0, 55),1)
            draw_text(screen, "Are you alright? You're looking a wee bit green...", 40, WIDTH//10, HEIGHT*65//100, (255, 0, 55),1)
        if game_countdown < 1:
        ## wait for r key to be pressed to restart
            if high_score_beaten:
                draw_text(screen, "NEW HIGH SCORE! ", 40, WIDTH//10, HEIGHT//5, (255, 200, 255),2)
            draw_text(screen, 'HIT P TO PLAY --- OR Q TO QUIT', 40, WIDTH//10, HEIGHT//6, (255, 250, 215),2)
            draw_text(screen, 'USE ARROW KEYS TO MOVE PLAYER', 40, WIDTH//10, HEIGHT//4, (245, 250, 250),2)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:  ## Restart the game and try again
                game_countdown = COUNTDOWN
                score = 0
                board = create_board(NUM_TILES_WIDE, NUM_TILES_HIGH)
                high_score_beaten = False
                player1.x, player1.y = WIDTH//2, HEIGHT//2
            elif keys[pygame.K_q]: ## Quit the game
                run = False

        pygame.display.flip()  #### update screen
                
    pygame.quit()


########################################
if __name__ == '__main__':
    main()
