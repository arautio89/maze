# Scenes
# items.py

from item_properties import ITEM_PROPERTIES

class Item:
    def __init__(self, item_name, model, x,y):
        self.name = item_name
        self.set_properties()

        self.model = model
        self.x = x
        self.y = y

        self.sprite = None
        self.sprite_dict = {}

    def set_properties():
        """Set item properties
        """
        item_props = ITEM_PROPERTIES[self.name]

        self.weight = item_props["weight"]

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