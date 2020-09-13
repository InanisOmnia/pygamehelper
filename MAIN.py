import pygame
import sys
from pygame.locals import *
import time

# Constant base class used to create Constats in python
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


##WINDOW CLASS##
class Window():
    def __init__(self, width, height, name, resizable=False):
        self.width = width  # screen width
        self.height = height  # screen height
        self.name = name  # screen title displayed

        self.resizable = resizable  # whether the screen can be resized by the user
        
        # flags the user should be able to use
        # pygame.FULLSCREEN    create a fullscreen display
        # pygame.RESIZABLE     display window should be sizeable
        # pygame.NOFRAME       display window will have no border or controls

        # flags we should consider
        # pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN

        # flags I think we should ignore
        # pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
        # pygame.OPENGL        create an opengl renderable display

        self.frameCount = 0
        self.tickCount = 0

        # user bound methods
        self.boundTick = lambda delta : None
        self.boundRender = lambda fps : None

        self.boundKeyDown = lambda k : None
        self.boundKeyUp = lambda k : None

        self.boundMouseDown = lambda b, pos : None
        self.boundMouseUp = lambda b, pos : None

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

    # user setup screen
    def initScreen(self):
        pygame.init()
        if self.resizable:
            self.windowSurface = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE, 32)
        else:
            self.windowSurface = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE, 32)
        pygame.display.set_caption(self.name)

    # user start gameloop
    def startInternalGameLoop(self):
        # setup default variables for timing
        SPT = 1.0/20.0  # seconds per tick
        SPR = 1.0/60 # seconds per render
        last_time = 0
        accum_render_time = 0
        accum_tick_time = 0
        fps = 0
        # infinite loop
        while True:
            start_time = time.time()  # start time of the loop
            end_time = time.perf_counter() # end time of the loop
            delta = end_time - last_time # calculate the difference in time between each loop
            last_time = end_time # set the last time of the loop so the next loop can access it

            # tick
            accum_tick_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            while accum_tick_time >= SPT:
                self._tick(delta) # call the internal tick method
                accum_tick_time -= SPT # reduce the accumulated time by the intended seconds per tick

            # render
            accum_render_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            while accum_render_time >= SPR:
                if (time.time() - start_time) > 0:
                    # FPS = 1 / time to process loop
                    fps = 1.0 / (time.time() - start_time)
                self._render(fps) # call the internal render method
                accum_render_time -= SPR # reduce the accumulated time by the intended seconds per render

    # internal tick method
    def _tick(self, delta):
        self.tickCount += 1 # increment the tick count
        for event in pygame.event.get():
            # detect screen close
            if event.type == QUIT:
                pygame.quit()
                quit()

            # detect screen resizing and places new dimensions
            # into resizeWidth/Height that is used in Window class
            if event.type == VIDEORESIZE:
                self.resizeWindow(event.w, event.h) # call the window resize event

            # detecting screen clicks
            if event.type == MOUSEBUTTONDOWN:
                self._mouseDown(event.button, pygame.mouse.get_pos()) # call the internal mousedown method
            if event.type == MOUSEBUTTONUP:
                self._mouseUp(event.button, pygame.mouse.get_pos()) # call the internal mouseup method

            # detecing keypresses
            if event.type == pygame.KEYDOWN:
                self._keyDown(event.key) # call the internal keydown method
            if event.type == pygame.KEYUP:
                self._keyUp(event.key) # call the internal keyup method

        self.boundTick(delta) # call the user defined tick method

    def _render(self, fps):
        self.frameCount += 1 # increment the framecount
        self.windowSurface.fill(Colour.White) # automatically blank the screen
        self.boundRender(fps) # call the user defined render method
        pygame.display.flip() # refresh the necessary parts of the screen (more efficient than full update)

    def _mouseDown(self, button, pos):
        self.boundMouseDown(button, pos) # call the user defined mousedown method
    
    def _mouseUp(self, button, pos):
        self.boundMouseUp(button, pos) # call the user defined mouseup method

    def _keyDown(self, key):
        self.boundKeyDown(key) # call the user defined keydown method

    def _keyUp(self, key):
        self.boundKeyUp(key) # call the user defined keyup method
    
    def resizeWindow(self, width, height):
        self.width = width # set the window width
        self.height = height # set the window height
        self.windowSurface = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE, 32) # redefine the surface
        pygame.display.update() # update the entire window



class Text():
    def __init__(self, font, fontsize, words, colourRGB, x, y):
        self.font = font  # the font
        self.fontsize = fontsize  # the size of the font
        self.words = words  # the actual text
        self.colour = colourRGB  # colour in form (R,G,B)
        self.x = x  # the x coordinate for the screen
        self.y = y  # the y coordinate for the screen

        self.font = pygame.font.SysFont(
            self.font, self.fontsize)  # gets the font
        # creates the text in the font required
        self.text = self.font.render(self.words, True, self.colour)
        self.textRect = self.text.get_rect()  # Draws box around text for alignment
        self.textRect.left = x  # sets x coord
        self.textRect.top = y  # sets y coord

    def showText(self, window):
        # blits the text to the screen
        window.windowSurface.blit(self.text, self.textRect)
