from src.requirements import *
from src.constants import colours, window_flags
from src.constants.text import *
from src.main import Input_Handler

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

            ## tick
            accum_tick_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            while accum_tick_time >= SPT:
                tps = 1.0 / accum_tick_time
                self._tick(accum_tick_time, tps) # call the internal tick method
                accum_tick_time -= SPT # reduce the accumulated time by the intended seconds per tick

            ## render
            # accum_render_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            # while accum_render_time >= SPR:
            #     fps = 1.0 / accum_render_time
            #     self._render(accum_render_time, fps) # call the internal render method
            #     accum_render_time -= SPR # reduce the accumulated time by the intended seconds per render
            
            accum_render_time += delta # if the difference in time between the two loops was more than the number of ticks per second then call multiple ticks
            if accum_render_time >= SPR:
                fps = 1.0 / accum_render_time
                self._render(accum_render_time, fps) # call the internal render method
                accum_render_time -= SPR # set the accumulated time to zero as the render does not need calling multiple times per loop

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
        self.windowSurface.fill(colours.Black) # automatically blank the screen
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
