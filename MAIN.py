assert __name__ != "__main__", "This is a python module and should not be run directly"

# from pyfiglet import Figlet
# f = Figlet(font='big')
# print(f.renderText('PyGame Helper'))

startText = """
Thank You for using
 _____        _____                        _    _      _
|  __ \      / ____|                      | |  | |    | |
| |__) |   _| |  __  __ _ _ __ ___   ___  | |__| | ___| |_ __   ___ _ __
|  ___/ | | | | |_ |/ _` | '_ ` _ \ / _ \ |  __  |/ _ \ | '_ \ / _ \ '__|
| |   | |_| | |__| | (_| | | | | | |  __/ | |  | |  __/ | |_) |  __/ |
|_|    \__, |\_____|\__,_|_| |_| |_|\___| |_|  |_|\___|_| .__/ \___|_|
        __/ |                                           | |
       |___/                                            |_|
See our github at https://github.com/LordFarquhar/pygamehelper for documentation, to report bugs and suggest improvements
Thanks to LordFarquhar and royalJames99 our main developers
"""

endText = """
Thank You for using
 _____        _____                        _    _      _
|  __ \      / ____|                      | |  | |    | |
| |__) |   _| |  __  __ _ _ __ ___   ___  | |__| | ___| |_ __   ___ _ __
|  ___/ | | | | |_ |/ _` | '_ ` _ \ / _ \ |  __  |/ _ \ | '_ \ / _ \ '__|
| |   | |_| | |__| | (_| | | | | | |  __/ | |  | |  __/ | |_) |  __/ |
|_|    \__, |\_____|\__,_|_| |_| |_|\___| |_|  |_|\___|_| .__/ \___|_|
        __/ |                                           | |
       |___/                                            |_|
We hope you enjoyed the experience!
"""

import pygame
import pygame.locals as plocals
import sys
import time
from functools import reduce
import math


# Constant base class used to create Constants in python
class Const: 
    """
    forbids to overwrite existing variables 
    forbids to add new values if "locked" variable exists
    """ 
    def __setattr__(self,name,value):
        if("locked" in self.__dict__):    
            raise NameError("Class is locked can not add any attributes (%s)"%name)
        if (name in self.__dict__):
            raise NameError("Can't rebind const(%s)"%name)
        self.__dict__[name]=value

# constant class for alphabets
class ALPHABET(Const):
    def __init__(self):
        self.resAlphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
               "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]
        self.extAlphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
               ";", ":", ",", ".", "'", '"', "!", "£", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "@", "#", "~", "-", "_", "[", "]", "{", "}", "+", "=", "|", " ", "/", "`", "¬", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.locked = 1 # this will create lock for adding constants 
Alphabet = ALPHABET()

# constant class for colours
class COLOUR(Const):
    def __init__(self):
        self.White = (255, 255, 255)
        self.Black = (0, 0, 0)
        
        self.Red = (255, 0, 0)
        self.Green = (0, 0, 255)
        self.Blue = (0, 255, 0)
        
        # no locked attribute, means the user can add their own colours
Colour = COLOUR()

class WINDOW_FLAGS(Const):
    def __init__(self):
        self.fullscreen = plocals.FULLSCREEN | plocals.HWSURFACE
        self.resizable = plocals.RESIZABLE
        self.noframe = plocals.NOFRAME
Window_Flags = WINDOW_FLAGS()

# pygame.FULLSCREEN    create a fullscreen display
# pygame.RESIZABLE     display window should be sizeable
# pygame.NOFRAME       display window will have no border or controls
# pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN

##WINDOW CLASS##
class Window():
    def __init__(self, size: tuple, title: str, flags: list):
        self.width = size[0]  # screen width
        self.height = size[0]  # screen height
        self.title = title  # screen title displayed

        self.flags = flags #resizable  # whether the screen can be resized by the user
        self.bitflags = None
        if len(self.flags) != 0:
            self.bitflags = reduce(lambda x, y: x | y, self.flags) 

        # flags the user should be able to use
        
        self.frameCount = 0
        self.tickCount = 0

        # user bound methods
        self.boundTick = lambda delta, tps : None
        self.boundRender = lambda delta, fps : None

        self.boundKeyDown = lambda k : None
        self.boundKeyUp = lambda k : None

        self.boundMouseDown = lambda b, pos : None
        self.boundMouseUp = lambda b, pos : None

        self.boundEnd = lambda : None

    # user helper bind methods
    def bindTick(self, tick):
        self.boundTick = tick
    
    def bindRender(self, render):
        self.boundRender = render

    def bindKeyDown(self, keyDown):
        self.boundKeyDown = keyDown
    
    def bindKeyUp(self, keyUp):
        self.boundKeyUp = keyUp
    
    def bindMouseDown(self, mousedown):
        self.boundMouseDown = mousedown
    
    def bindMouseUp(self, mouseUp):
        self.boundMouseUp = mouseUp

    def bindEnd(self, end):
        self.boundEnd = end

    # user setup screen
    def initScreen(self):
        pygame.init()
        if self.bitflags:
            self.windowSurface = pygame.display.set_mode((self.width, self.height), self.bitflags, 32)
        else:
            self.windowSurface = pygame.display.set_mode((self.width, self.height), 32)
        pygame.display.set_caption(self.title)
        self.input_class = Input_Handler(self)

    # user start gameloop
    def startInternalGameLoop(self, targetFps, targetTps):
        print(startText)
        # setup default variables for timing
        SPT = 1.0/float(targetTps)  # seconds per tick
        SPR = 1.0/float(targetFps) # seconds per render
        last_time = 0
        accum_render_time = 0
        accum_tick_time = 0
        fps = 0
        # infinite loop
        while True:
            start_time = time.perf_counter() # start time of the loop
            delta = start_time - last_time # calculate the difference in time between each loop

            # tick
            accum_tick_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            while accum_tick_time >= SPT:
                tps = 1.0 / accum_tick_time
                self._tick(accum_tick_time, tps) # call the internal tick method
                accum_tick_time -= SPT # reduce the accumulated time by the intended seconds per tick

            # render
            accum_render_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            while accum_render_time >= SPR:
                fps = 1.0 / accum_render_time
                self._render(accum_render_time, fps) # call the internal render method
                accum_render_time -= SPR # reduce the accumulated time by the intended seconds per render

            last_time = start_time # set the last time of the loop so the next loop can access it

    # internal tick method
    def _tick(self, delta, tps):
        self.tickCount += 1 # increment the tick count
        for event in pygame.event.get():
            # detect screen close
            if event.type == plocals.QUIT:
                self._end()

            # detect screen resizing and places new dimensions
            # into resizeWidth/Height that is used in Window class
            if event.type == plocals.VIDEORESIZE:
                self.resizeWindow(event.w, event.h) # call the window resize event

            # detecting screen clicks
            if event.type == plocals.MOUSEBUTTONDOWN:
                self._mouseDown(event.button, pygame.mouse.get_pos()) # call the internal mousedown method
            if event.type == plocals.MOUSEBUTTONUP:
                self._mouseUp(event.button, pygame.mouse.get_pos()) # call the internal mouseup method

            # detecing keypresses
            if event.type == plocals.KEYDOWN:
                self._keyDown(event.key) # call the internal keydown method
            if event.type == plocals.KEYUP:
                self._keyUp(event.key) # call the internal keyup method

        self.input_class.tick()
        self.boundTick(delta, tps) # call the user defined tick method

    def _render(self, delta, fps):
        self.frameCount += 1 # increment the framecount
        self.windowSurface.fill(Colour.Black) # automatically blank the screen
        self.boundRender(delta, fps) # call the user defined render method
        self.input_class.render()
        pygame.display.flip() # refresh the necessary parts of the screen (more efficient than full update)

    def _mouseDown(self, button, pos):
        self.boundMouseDown(button, pos) # call the user defined mousedown method
    
    def _mouseUp(self, button, pos):
        self.boundMouseUp(button, pos) # call the user defined mouseup method
        self.input_class.check = True

    def _keyDown(self, key):
        self.boundKeyDown(key) # call the user defined keydown method

    def _keyUp(self, key):
        self.boundKeyUp(key) # call the user defined keyup method
    
    def _end(self):
        self.boundEnd()
        print(endText)
        pygame.quit()
        quit()

    def resizeWindow(self, width, height):
        self.width = width # set the window width
        self.height = height # set the window height
        self.windowSurface = pygame.display.set_mode(
            (self.width, self.height),plocals.RESIZABLE, 32) # redefine the surface
        pygame.display.update() # update the entire window



class Text():
    def __init__(self, font, fontsize, words, colourRGB):
        self.font = font  # the font
        self.fontsize = fontsize  # the size of the font
        self.words = words  # the actual text
        self.colour = colourRGB  # colour in form (R,G,B)

        self.font = pygame.font.SysFont(
            self.font, self.fontsize)  # gets the font
        # creates the text in the font required
        self.text = self.font.render(self.words, True, self.colour)
        self.textRect = self.text.get_rect()  # Draws box around text for alignment

    def render(self, window, x, y):
        self.textRect.left = x  # sets x coord
        self.textRect.top = y  # sets y coord
        # blits the text to the screen
        window.windowSurface.blit(self.text, self.textRect)
        
    def render_center(self, window, center):
        self.textRect.center = center
        # blits the text to the screen
        window.windowSurface.blit(self.text, self.textRect)
    
    def getDimensions(self) -> tuple:
        width, height = self.text.get_width(), self.text.get_height()
        return width, height


## Polar and Cartesian conversion functions in pure pygame ##

def cartesian(r, phi): # r is a length, phi is an angle measured from negative y (North)
    cartesian = pygame.math.Vector2()
    cartesian.from_polar((r, phi%360))
    return(cartesian.x, cartesian.y) # returned as tuple in form (x component, y component)

def polar(x, y): # x coord, y coord
    polar = pygame.math.Vector2(x, y) 
    return polar.as_polar() # returned as tuple in form (r, phi)

## Inputs ##
class Button_Circle():
    def __init__(self, pos, radius, window, name):
        self.pos = pos # pos as tuple
        self.radius = radius 
        self.state = False
        self.name = Text("calibri", 10, name, (0, 0, 0))
        self.window = window
        self.window.input_class.all_inputs.insert(0, self) # gives Input_Handle access to itself
        self.name.textRect.center = self.pos

        if math.dist(self.pos, self.name.textRect.topleft) > self.radius and math.dist(self.pos, self.name.textRect.bottomright) > self.radius:
            print(math.dist(self.pos, self.name.textRect.topleft))
            raise NameError("Name too big, truncate or reduce font size")

    def check_mouse_click(self, mouse_pos): # check if the button has been clicked
        if math.dist(self.pos, mouse_pos) < self.radius:
            self.state = not self.state
            return(True)

    def render(self, surface):
        if self.state == False:
            pygame.draw.circle(surface, (0, 255, 0), self.pos, self.radius)
        else:
            pygame.draw.circle(surface, (255, 0, 0), self.pos, self.radius)
        self.name.render_center(self.window, self.pos)

class Button_Square():
    def __init__(self, pos, size, window, name):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = pos
        self.rect.w = 2 * size
        self.rect.h = 2 * size
        self.state = False
        self.name = Text("Calibri", 10, name, (0, 0, 0))
        self.window = window
        self.window.input_class.all_inputs.insert(0, self)
        self.name.textRect.center = self.rect.center
        if self.rect.contains(self.name.textRect) != True:
            raise NameError("Name too big, truncate or reduce font size")        
    def check_mouse_click(self, mouse_pos):
        if self.rect.contains(pygame.Rect(mouse_pos, (0, 0))) == True:
            self.state = not self.state
            return(True)
    def render(self, surface):
        if self.state == False:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)
        self.name.render_center(self.window, self.rect.center)

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

class Circle(): # IT ALL NEEDS ANNOTATING
    def __init__(self, position, radius):
        self.position = pygame.math.Vector2(position)
        self.radius = radius
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "position":
            self.__dict__["x"] = self.__dict__[name].x
            self.__dict__["y"] = self.__dict__[name].y
            
        elif name == "x":
            self.__dict__["position"] = pygame.math.Vector2(self.x, self.y)

        elif name == "y":
            self.__dict__["position"] = pygame.math.Vector2(self.x, self.y)

        elif name == "radius":
            if 0 > value:
                self.normalize()
            self.__dict__["diameter"] = self.radius * 2
            self.__dict__["area"] = self.radius ** 2 * math.pi

        elif name == "diameter":
            self.__dict__["radius"] = self.diameter / 2
            self.__dict__["area"] = self.radius ** 2 * math.pi

        elif name == "area":
            self.__dict__["radius"] = math.sqrt(self.area / math.pi)
            self.__dict__["diameter"] = self.radius / 2
    def copy(self):
        return Circle(self.postition, self.radius)

    def move(self, x, y):
        return Circle((self.pos.x + x, self.pos.y + y, self.radius))

    def move_ip(self, x, y):
        self.x += x
        self.Y += y

    def inflate(self, factor):
        return Circle(self.position, self.radius + factor)

    def inflate_ip(self, factor):
        self.radius += factor

    def clamp(self, circle):
        return Circle(circle.position, self.radius)

    def clamp_ip(self, circle):
        self.position = circle.position

    def clip(self, circle): # needs math optimisation
        length = math.dist(self.position, circle.position)
        length2 = abs(length - (self.radius + circle.radius))
        newrad = length2 / 2
        newdist = self.radius - newrad
        newvec = pygame.math.Vector2(circle.x - self.x, circle.y - self.y)
        newvec.scale_to_length(newdist)
        return Circle((self.x + newvec.x, self.y + newvec.y), newrad)
        
    def clipline():
        pass # waiting for math

    def union(self, circle):
        pass # waiting for math

    def union_ip(self):
        pass # waiting for math

    def unionall(self):
        pass # waiting for math

    def unionall_ip(self):
        pass # waiting for math

    def normalize(self):
        self.radius = abs(self.radius)

    def contains(self, circle):
        return math.dist(self.position, circle.position) + circle.radius <= self.radius

    def collidepoint(self, v1, v2 = None):
        if v2 == None:
            test_for = v1
        else:
            test_for = (v1, v2)
        return math.dist(self.position, test_for) <= self.radius        
        
    def collidecircle(self, circle):
        return math.dist(self.position, circle.position) < self.radius + circle.radius
        
    def collidelist(self, circles):
        for i in range(len(circles)):
            if math.dist(self.position, circles[i].position) < self.radius + circles[i].radius:
                return(i)

    def collidelistall(self, circles):
        for i in range(len(circles)):
            if math.dist(self.position, circles[i].position) < self.radius + circles[i].radius:
                   yield int(i)

    def collidedict(self, circles, use_values = 0):
        if use_values ==0:
            for circle in circles:
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    return tuple(circle, circles[circle])
        else:
            for key in circles:
                circle = circles.get(key)
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    return tuple((key, circle))                    
            

    def collidedictall(self, circles, use_values = 0):
        if use_values == 0:
            for circle in circles:
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    yield tuple(circle, circles[circle])
        else:
            for key in circles:
                circle = circles.get(key)
                if math.dist(self.position, circle.position) < self.radius + circle.radius:
                    yield tuple((key, circle))
  
