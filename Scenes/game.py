# Scenes
# game.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

#from config import *
from constants import *
from Scenes.model import *

#from scene_manager import SceneManager

pyglet.resource.path = ['Images']
pyglet.resource.reindex()

#TILE_SIZE = 32
#TILES_HOR = 25
#TILES_VER = 20

# Game Scene
class Game:
    def __init__(self, scene_manager):
        self.scene_id = 'game'
        self.scene_manager = scene_manager
        self.window = scene_manager.window
        self.model = Model(self)

        #self.rect_batch = pyglet.graphics.Batch()
        #self.label_batch = pyglet.graphics.Batch()
        #self.bg_batch = pyglet.graphics.Batch() # Background Batch
        #self.sprite_batch = pyglet.graphics.Batch()

        #self.define_buttons()
        self.load_images()

        # Define My Batch
        self.my_batch = pyglet.graphics.Batch()
        # Define My Groups (Group for tiles, group for creatures)
        self.tiles_group = pyglet.graphics.OrderedGroup(0)
        self.cre_group = pyglet.graphics.OrderedGroup(1)

        # Field of View
        self.fov = True

        # Set Sprites, fill batches
        self.set_sprites()

        # Movement Delay (in frames)
        self.max_delay = MAX_DELAY
        self.delay = 0

        self.key_handler = pyglet.window.key.KeyStateHandler()

        #self.set_decorators()

    def enter_scene(self):
        self.window.push_handlers(self.key_handler)

    def exit_scene(self):
        self.window.pop_handlers() 
        
    def on_mouse_press(self, x,y, button, modifiers):
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            if button == mouse.LEFT:
                print('The left mouse button was pressed.')
                """
                for b in self.buttons:
                    if (b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h):
                        b.click()"""
              
    def on_key_press(self, symbol, modifiers):
        print("Key Pressed in Game Scene!")
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            if symbol == pyglet.window.key.ESCAPE:
                self.goto_main_menu()
                return pyglet.event.EVENT_HANDLED
            elif symbol == pyglet.window.key.SPACE:
                # Regenerate the Maze
                print("Regenerate Maze!")
                self.model.generate_maze()
                self.set_sprites()
            elif symbol == pyglet.window.key.TAB:
                self.fov = not self.fov
                print("Field of View:",self.fov)
                self.update_gfx()
                

    def on_draw(self):            
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            self.window.clear()
            self.my_batch.draw()
        
    def update(self, dt):
        
        player = self.model.player

        key_dict = {key.UP:(0,-1), key.DOWN:(0,1),
                    key.LEFT:(-1,0), key.RIGHT:(1,0)}
        
        if self.delay > 0:
            self.delay -= 1
        else:
            # Only move when exactly one arrow is pressed
            buttons_pressed = 0
            dx, dy = 0,0
            move = False
            for k in key_dict:
                if (self.key_handler[k]):
                    buttons_pressed += 1
                    if buttons_pressed == 1:
                        dx, dy = key_dict[k]
                        move = True
                    else:
                        dx, dy = 0,0
                        move = False

            if move:
                if player.direction == (dx,dy):
                    player.move_push(dx,dy)
                    self.delay = self.max_delay
                else:
                    player.change_direction((dx,dy))
                    self.delay = self.max_delay
                #self.update_gfx()

        if self.model.update_now:
            self.update_gfx()
            self.model.update_now = False


            

    def set_bg(self):
        #self.bg_batch.add()
        pass
        

    def load_images(self):
        self.bg_img = pyglet.resource.image('bg_forest_800x640.jpg')
        # Sprite Sheet
        sprite_sheet = pyglet.resource.image('spritesheet.png')
        sprite_sheet_seq = pyglet.image.ImageGrid(sprite_sheet, 10, 10)
        # Texture Sequence
        self.spritesheet = pyglet.image.TextureGrid(sprite_sheet_seq)
        
        print("Images Loaded!")

    def goto_main_menu(self):
        self.scene_manager.change_scene('main menu')

    def set_sprites(self):
        # Set sprites for entities
        # Add them to Batches

        my_batch = self.my_batch

        tiles_group = self.tiles_group
        cre_group = self.cre_group
        
        tiles = self.model.tiles

        player = self.model.player

        # First Tiles
        self.tex_dict = {}
        for k in sprite_dict:
            self.tex_dict[k] = self.spritesheet[sprite_dict[k]]

        """
        self.tex_dict['black'] black_tex = self.spritesheet[sprite_dict['black']]
        floor_tex = self.spritesheet[sprite_dict['floor']]
        """
        
        for x in range(TILES_HOR):
            for y in range(TILES_VER):
                tile = tiles[x][y]
                
                if tile.blocked == True:
                    sprite = pyglet.sprite.Sprite(self.tex_dict['wall'],
                                            batch = my_batch,
                                            group = self.tiles_group)
                else:
                    sprite = pyglet.sprite.Sprite(self.tex_dict['floor'],
                                            batch = my_batch,
                                            group = self.tiles_group)

                #sprite.visibe               
                
                tile.sprite = sprite
                #tile.sprite.x = TILE_SIZE * x + LEFT_MARGIN
                #tile.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (y + 1) + DOWN_MARGIN # Reverse!
                sx,sy = get_tile_coordinates(x, y)
                tile.sprite.x = sx
                tile.sprite.y = sy

        
        for cre in self.model.creatures:
            # ent_tex = self.spritesheet[sprite_dict[ent.ent_id]]
            sprite = pyglet.sprite.Sprite(self.tex_dict[cre.cre_id],
                                        batch = my_batch,
                                        group = self.cre_group)
            
            cre.sprite = sprite
            #cre.sprite.x = TILE_SIZE * ent.x
            #cre.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (ent.y + 1) # Reverse!

        self.update_gfx()

    def update_gfx(self):
        fov = self.model.player.vision.fov
        tiles = self.model.tiles
        # Field of View
        if self.fov:
            # Tiles
            for x in range(TILES_HOR):
                for y in range(TILES_VER):
                    tile = tiles[x][y]
                    # If Field of View is On
                    # Draw Black Squares to Tiles that are Not Seen
                    if fov[x][y] > 0:
                        tile.sprite.visible = True
                    else:
                        tile.sprite.visible = False

            # Creatures
            for cre in self.model.creatures:
                if fov[cre.x][cre.y] > 0:
                    cre.sprite.visible = True
                else:
                    cre.sprite.visible = False
        else:
            # Tiles
            for x in range(TILES_HOR):
                for y in range(TILES_VER):
                    tile = tiles[x][y]
                    tile.sprite.visible = True

            # Creatures
            for cre in self.model.creatures:
                cre.sprite.visible = True

        # Creature coordinates
        for cre in self.model.creatures:
            #cre.sprite.x = TILE_SIZE * cre.x
            #cre.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (cre.y + 1) # Reverse!
            sx,sy = get_tile_coordinates(cre.x, cre.y)
            cre.sprite.x = sx
            cre.sprite.y = sy

def get_tile_coordinates(tx,ty):
    """Given tile coordinates (tx,ty), give the screen coordinates of the sprite (lower left)
    """

    sx = TILE_SIZE * tx + LEFT_MARGIN
    sy = MAZE_SCREEN_HEIGHT - TILE_SIZE * (ty + 1) + DOWN_MARGIN  # Reverse !?!

    return(sx,sy)

"""
def set_sprite_xy(entities):
    # Set Sprite Coordinates
    # entities is a list
    for ent in entities:
        ent.sprite.x = TILE_SIZE * ent.x
        ent.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (ent.y + 1) # Reverse!
"""

"""
sprite_dict = {'player':(1,2), 'floor':(1,1),
               'wall':(2,1), 'boulder':(2,2)}
"""

sprite_dict = {'player':(1,2), 'floor':(1,3), 'wall':(1,5),
               'black':(1,6),
               'player up':(4,2), 'player down':(3,2),
               'player left':(3,1), 'player left':(3,3)}
