from MAIN import *

# create the window
w = Window(500, 500, "Hello World")
# initialise the window
w.initScreen()

def tick(delta, tps):
    # print(f"{tps:.2f}tps {delta:.10f}delta")
    pass

def render(delta, fps):
    # print(f"{fps:.2f}fps {delta:.10f}delta")
    t.render(w, (w.width / 2) - (t.getDimensions()[0] / 2) + w.tickCount, (w.height / 2) - (t.getDimensions()[1] / 2))

# bind events to the user functions
w.bindTick(tick)
w.bindRender(render)


t = Text("comicsansms", 40, "Hello World", Colour.Blue)


# start the gameloop
w.startInternalGameLoop(100, 20)

