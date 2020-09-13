from MAIN import *

# create the window
w = Window(500, 500, "Hello World")
# initialise the window
w.initScreen()

def tick(dt):
    print(f"tick {dt} since last")

def render(fps):
    print(f"render {fps}fps")

# bind events to the user functions
w.bindTick(tick)
w.bindRender(render)

# start the gameloop
w.startInternalGameLoop()
