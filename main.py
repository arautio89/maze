# Maze
# main.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

#from config import *
from constants import *
from scene_manager import SceneManager

#FPS = 60
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 640

# 800 = 25*32, 640 = 20*32
window = pyglet.window.Window(width = SCREEN_WIDTH,
                              height = SCREEN_HEIGHT,
                              caption = "Maze")

scene_manager = SceneManager(window)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(scene_manager.update, 1/FPS)
    pyglet.app.run()
    #sys.exit() ???

