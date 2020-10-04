from src.requirements import *
from src.constants import colours, window_flags, alphabet

pygame.font.init() ## this is a kind of gapfill, there are better ways to do this

class Input_Handler():
    def __init__(self, window):
        self.window = window
        self.all_inputs = []
        self.check = False
    def tick(self):
        if self.check == True:
            mousepos = pygame.mouse.get_pos()
            for input_item in self.all_inputs:
                if input_item.check_mouse_click(mousepos) == True:
                    break
            self.check = False
            print("Check")
    def render(self):
        for i in range(len(self.all_inputs) - 1, -1, -1):
            self.all_inputs[i].render(self.window.windowSurface)


## Polar and Cartesian conversion functions in pure pygame ##

def cartesian(r, phi): # r is a length, phi is an angle measured from negative y (North)
    cartesian = pygame.math.Vector2()
    cartesian.from_polar((r, phi%360))
    return(cartesian.x, cartesian.y) # returned as tuple in form (x component, y component)

def polar(x, y): # x coord, y coord
    polar = pygame.math.Vector2(x, y) 
    return polar.as_polar() # returned as tuple in form (r, phi)