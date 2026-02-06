##import pygame


################################################################################################################
## this is a class for an animated character that can move around the screen
## and can hold a number of sprite animations depending on state e.g. on fire, activated, dead, on alert
################################################################################################################

class mobile_character:
    def __init__(self, default_sprite_sheet, pos_x, pos_y, default_sprite_num_frames,
                 def_char_width, def_char_height, sprite_sheet_width, sprite_sheet_height,
                   tile_width, tile_height, num_lives=1):
        ##initialise the list with one item, a tuple with the sprite sheet, width, height, number of frames
        self.state_sprite_sheet_list = [(default_sprite_sheet, def_char_width, def_char_height, default_sprite_num_frames)]
        self.character_state = 0  ##the default state, indicating the default anim for this character
        self.curr_sprite = self.state_sprite_sheet_list[self.character_state] ##which sprite depending on state
        self.x = pos_x ## where on screen to draw character
        self.y = pos_y ## where on screen to draw character
        self.width = def_char_width ## on screen width of character
        self.height = def_char_height ## on screen height of character
        ###self.sprite_sheet_width = sprite_sheet_width  ## width of one character on sprite sheet (1 char per frame)
        ###self.sprite_sheet_height = sprite_sheet_height  ## height of one character on sprite sheet
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
        """
        Given a direction and a move distance in pixels, this function returns the new column or row of the tile the player
        would be on if they moved that distance in that direction.
        If the direction is left or right, it calculates the new column. If the direction is up or down, it calculates the new row.
        If we know what the new tile is, we can check if it's, e.g. a wall or not and then allow/disallow the movement.
        Parameters:
            self (object): The instance of the class.
            move_dist_in_px (int): The distance in pixels the player has moved.
            direction (str): The direction the player is moving. Can be 'left', 'right', 'up', or 'down'.
        Returns:
            int: The new column or row of the tile the player WOULD be  on if they moved that distance in that direction.
        """
        if direction == 'left':
            return int( (self.x-move_dist_in_px)//self.tile_width)
        elif direction == 'right':
            return int( (self.x+self.width+move_dist_in_px)//self.tile_width)
        elif direction == 'up':
            return int( (self.y-move_dist_in_px)//self.tile_height)
        elif direction == 'down':
            return int( (self.y+self.height+move_dist_in_px)//self.tile_height)
        
  ############################      
    def draw(self, screen, counter):
        state = self.character_state
        ## draw the right frame of the sprite animation associated with this character state
        frames_per_sprite = self.curr_sprite[3]
        frame_x_in_sheet = (counter%frames_per_sprite)*self.width
        frame_y_in_sheet = 0  ##(counter//frames_per_sprite)*self.sprite_sheet_height
        ##DEBUG
        print(frame_x_in_sheet, frame_y_in_sheet)
        screen.blit(self.curr_sprite[0], (self.x, self.y),
                    (frame_x_in_sheet,frame_y_in_sheet,self.width,self.height))
       


#### END OF CLASS #########################################################################################
