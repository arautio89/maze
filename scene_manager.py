#import pyglet

#from main_menu import *
from Scenes.main_menu import MainMenu
from Scenes.game import Game

class SceneManager:
    def __init__(self, window):
        # Current Scene
        self.current = None
        self.window = window
        # Create Scenes here?
        self.scenes = {}
        self.create_scenes()
        #self.current = self.scenes['main menu']
        self.change_scene('main menu')
        print()

    def change_scene(self, scene_id):
        # Set Scene        
        #self.current.set_decorators()

        if self.current is not None:
            self.current.exit_scene()
            self.window.pop_handlers()
        
        #self.current_scene_id = scene_id
        scene = self.scenes[scene_id]
        self.current = scene
        
        self.window.push_handlers(scene)
        scene.enter_scene()
        

    def create_scenes(self):
        self.scenes['main menu'] = MainMenu(self)
        self.scenes['game'] = Game(self)
        

    def update(self, dt):
        self.current.update(dt)

        

