# Maze
# vision.py

#from config import *
from constants import *

class Vision:
    def __init__(self, owner):
        # Field of View
        # 0 = Not seen
        # 1 = Partial Visibility
        # 2 = Peripheral Visibility
        # 3 = Full Visibility
        self.fov = [[0 for y in range(TILES_VER)]
                    for x in range(TILES_HOR)]

        self.owner = owner # Reference to the owner
        
        #self.curr_level.generate_maze()

        self.update_fov()
        
        

    def update_fov(self):
        # Update Field of View
        owner = self.owner
        vx,vy = owner.x, owner.y
        dx, dy = owner.direction
        tiles = owner.model.tiles
        max_d = max(TILES_HOR, TILES_VER)

        # Clear FoV
        for x in range(TILES_HOR):
            for y in range(TILES_VER):
                self.fov[x][y] = 0

        #self.fov[vx][vy] = 3

        # Offset
        offx, offy = dy, dx
        
        for d in range(max_d): #range(1,max_d)
            # Current Cell (to be Checked)
            cx = vx + d*dx
            cy = vy + d*dy
            if not (0 <= cx < TILES_HOR and 0 <= cy < TILES_VER):
                break

            # Neighboring Cells for Current Cell
            self.fov[cx][cy] = 3
            
            if 0 <= cx + offx < TILES_HOR and 0 <= cy + offy < TILES_VER:
                self.fov[cx + offx][cy + offy] = 1
            if 0 <= cx - offx < TILES_HOR and 0 <= cy - offy < TILES_VER:
                self.fov[cx - offx][cy - offy] = 1
            
            if tiles[cx][cy].blocked:
                break


