# Scenes
# main_menu.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

#from scene_manager import SceneManager

"""
print("Fonts")
pyglet.font.add_file('Old English Five.ttf')
pyglet.font.load('Old English Five')
"""

# Main Menu Scene
class MainMenu:
    def __init__(self, scene_manager):
        self.scene_id = 'main menu'
        self.scene_manager = scene_manager
        self.window = scene_manager.window

        self.key_handler = key.KeyStateHandler()

        self.rect_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        load_fonts()

        self.define_buttons()
        
        #self.set_decorators()

    def enter_scene(self):
        self.window.push_handlers(self.key_handler)

    def exit_scene(self):
        self.window.pop_handlers() 

    def on_mouse_press(self, x,y, button, modifiers):
        #if self.scene_manager.current_scene_id == 'main menu':
        if self.scene_manager.current == self:
            if button == mouse.LEFT:
                print('The left mouse button was pressed.')
                for b in self.buttons:
                    if (b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h):
                        b.click()
        
    def on_key_press(self, symbol, modifiers):
        print("Key Pressed in Main Menu!")
        #if self.scene_manager.current_scene_id == 'main menu':
        if self.scene_manager.current == self:
            if symbol == pyglet.window.key.ESCAPE:
                self.quit_game()
                return pyglet.event.EVENT_HANDLED

        if symbol == pyglet.window.key.SPACE:
            print(self)

        if symbol == pyglet.window.key.ENTER:
            self.go_play()

    def on_draw(self):
        #if self.scene_manager.current_scene_id == 'main menu':
        if self.scene_manager.current == self:
            self.window.clear()
            self.rect_batch.draw()
            self.label_batch.draw()
        
    def update(self, dt):
        pass

    def define_buttons(self):
        # Define buttons
        self.buttons = []

        play_button = Button("Play!", 100, 500, 200, 50,
                             (0,255,0), (255,255,255,255),
                             self.rect_batch, self.label_batch,
                             self.go_play) #print_play

        quit_button = Button("Quit!", 100, 300, 200, 50,
                             (255,0,0), (255,255,255,255),
                             self.rect_batch, self.label_batch,
                             self.quit_game)

        self.buttons += [play_button, quit_button]

        print("Buttons defined!")

    def go_play(self):
        self.scene_manager.change_scene('game')

    def quit_game(self):
        print("Quitting game!")
        pyglet.app.exit()
        
class Button:
    def __init__(self, label, x,y, w,h,
                 rect_color, font_color,
                 rect_batch, label_batch,
                 func):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func

        u1,v1, u2,v2 = x, y,  x + w, y + h
        u = (u1 + u2)//2
        v = (v1 + v2)//2

        font = 'Old English Five'
        # font = 'Times New Roman'

        # Add Rectangle to Batch
        rect_batch.add(4, pyglet.gl.GL_QUADS, None,
                             ('v2f', [u2,v2, u1,v2, u1,v1, u2,v1]),
                             ('c3B', rect_color*4) )

        # Add Label to Batch
        pyglet.text.Label(label,
                          font_name=font,
                          font_size=24, color = font_color,
                          x=u, y=v,
                          batch = label_batch,
                          anchor_x='center', anchor_y='center')

    def click(self):
        self.func()

def print_message(message):
    print(message)

def print_play():
    print("Play!")

def print_quit():
    print("Quit!")

def load_fonts():
    print("Fonts")
    pyglet.font.add_file('Old English Five.ttf')
    pyglet.font.load('Old English Five')
