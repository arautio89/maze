# Scenes
# game.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

#from config import *
from constants import *
from Scenes.maze_generator import *
from Scenes.vision import *

#from scene_manager import SceneManager

pyglet.resource.path = ['Images']
pyglet.resource.reindex()

#TILE_SIZE = 32
#TILES_HOR = 25
#TILES_VER = 20

class Model:
    def __init__(self, game_scene):
        # Game Scene
        self.game_scene = game_scene

        self.tiles = [[Tile() for y in range(TILES_VER)]
                      for x in range(TILES_HOR)]
        #self.entities = []
        self.creatures = []
        self.items = []

        # Test Level Content
        self.generate_maze()        

        self.player = Creature('player', self, TILES_HOR//2, TILES_VER - 1)

        self.player.vision = Vision(self.player)
        #self.player.vision.owner = self.player
        #Entity('boulder', self.curr_level, 5,10)
        #Entity('boulder', self.curr_level, 7,10)

        # Update the Graphics because the game state has changed visibly
        self.update_now = False

    def generate_maze(self):
        maze = maze_generator()
        for x in range(TILES_HOR):
            for y in range(TILES_VER):
                self.tiles[x][y].blocked = maze[x][y]
        self.update_now = True



class Tile:
    def __init__(self, blocked = False):
        self.blocked = blocked

        # Occupying Creature
        self.occupant = None
        # List of items on the floor
        self.items = []
        # Stains and puddles (liquid), footprints?
        #self.stains ?
        # Scents, smells (list?)
        #self.smells = []
        self.sprite = None

class Creature:
    def __init__(self, cre_id, model, x,y):
        self.cre_id = cre_id # Creature ID
        self.model = model
        self.x = x
        self.y = y
        self.direction = (0,-1) # 'up', 'down', 'left', 'right'
        self.delay = 0
        self.sprite = None
        self.sprite_dict = {}

        self.inventory = []

        # Add Entity as Occupant
        model.tiles[x][y].occupant = self
        model.creatures.append(self)

    def move(self, dx,dy): # TODO!!!
        tiles = self.model.tiles
        # Move Entity
        # Limit to TILES_HOR, TILES_VER
        nx = max(0, min(self.x + dx, TILES_HOR - 1))
        ny = max(0, min(self.y + dy, TILES_VER - 1))
        
        new_tile = tiles[nx][ny]
        free_move = not new_tile.blocked and new_tile.occupant == None
               
        # If move possible, remove the moving Entity (self)
        # from its old tile and set it to the new one
        if free_move:
            tiles[self.x][self.y].occupant = None
            #self.level.tiles[self.x][self.y].occupant = None
            # Set new coordinates to Entity Coordinates
            
            self.x = nx
            self.y = ny

            tiles[self.x][self.y].occupant = self

            self.model.update_now = True
            
            # Change Sprite Coordinates
            #self.sprite.x = TILE_SIZE * self.x
            #self.sprite.y = TILE_SIZE * self.y # Reverse!!!
            #set_sprite_xy([self])
            #self.model.game_scene.update_gfx()

    def move_attack(self, dx,dy):
        pass

    def move_push(self, dx,dy): # <<<===!!!!!
        # Entity moves and possibly pushes a boulder
        model = self.model
        # Move Entity
        # Limit to TILES_HOR, TILES_VER
        nx = max(0, min(self.x + dx, TILES_HOR - 1))
        ny = max(0, min(self.y + dy, TILES_VER - 1))
        # New coordinates for pushed boulder
        nnx = nx + dx
        nny = ny + dy

        # Is the move a free move (move to empty space)
        # or a boulder push (move to boulder, boulder to empty)
        new_tile = model.tiles[nx][ny]
        free_move = not new_tile.blocked and new_tile.occupant == None
        if new_tile.occupant != None:
            boulder_push = (new_tile.occupant.ent_id == 'boulder'
                            and not model.tiles[nnx][nny].blocked
                            and model.tiles[nnx][nny].occupant == None
                            and 0 <= nnx < TILES_HOR
                            and 0 <= nny < TILES_VER)
        else:
            boulder_push = False

        boulder = None
        if boulder_push:
            boulder = new_tile.occupant
            boulder.move(dx,dy)

        if free_move or boulder_push:
            self.move(dx,dy)
            if self.vision != None:
                self.vision.update_fov()
            #level.moves.append(("Move", dx, dy, boulder))

    def change_direction(self, direction):
        self.direction = direction
        if self.vision != None:
            self.vision.update_fov()

        self.model.update_now = True

    def get_item(self, item):
        # Put item into the inventory
        # if it is on the same tile as the creature

        if (self.x == item.x and self.y == item.y):
            # Check if the creature can pick up items?
            self.inventory.append(item)
            item.owner == self
            # Remove the item from the tile
            self.model.tiles[self.x][self.y].items.remove(item)

    def drop_item(self, item):
        # Put an item in the creature's inventory
        # on the ground on the same tile

        if item in self.inventory:
            item.owner = None
            self.inventory.remove(item)
            item.x = self.x
            item.y = self.y
            # Add the item to the tile
            self.model.tiles[self.x][self.y].items.append(item)

    def death(self):
        # Remove creature from the list of creatures
        self.model.creatures.remove(self)
        # Creature no longer occupies its tile
        self.model.tiles[self.x][self.y].occupant = None
        # Creature drops all items in its inventory
        #self.model.tiles[self.x][self.y].items += self.inventory
        for item in self.inventory:
            self.drop_item(item)

"""
class Item:
    def __init__(self, item_id, model, x,y, owner = None):
        self.item_id = item_id # Item ID
        self.model = model
        self.x = x
        self.y = y

        self.owner = owner
        
        #self.direction = (0,-1) # 'up', 'down', 'left', 'right'
        #self.delay = 0
        self.sprite = None
        self.sprite_dict = {}

        self.owner = None # Who owns the object?

        # Item Properties
        self.weight = 0 # grams?
        

        # Add Entity as Occupant
        model.tiles[x][y].items.append(self)
        model.items.append(self)

    def destroy(self):
        # Remove item from the list of items
        self.model.items.remove(self)
        # Item is no longer on the tile
        self.model.tiles[self.x][self.y].items.remove(self)
        # Item no longer has an owner
        if self.owner != None: # if self in self.owner.inventory?
            self.owner.inventory.remove(self)
        self.owner = None
"""

"""
def set_sprite_xy(entities):
    # Set Sprite Coordinates
    # entities is a list
    for ent in entities:
        ent.sprite.x = TILE_SIZE * ent.x
        ent.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (ent.y + 1) # Reverse!
"""       


sprite_dict = {'player':(1,2), 'floor':(1,3),
               'plate on':(2,5), 'plate off':(2,6),
               'wall':(1,5), 'black':(1,6), 'boulder':(4,2)}
