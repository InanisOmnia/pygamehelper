import src as pgh
from src.constants import colours, window_flags

# create the window
w = pgh.Window((500, 500), "Hello World", [window_flags.resizable])
# initialise the window
w.initScreen()

def tick(delta, tps):
    # print(f"{tps:.2f}tps {delta:.10f}delta")
    pass

def render(delta, fps):
    # print(f"{fps:.2f}fps {delta:.10f}delta")
    t.render(w, (w.width / 2) - (t.getDimensions()[0] / 2) + w.tickCount, (w.height / 2) - (t.getDimensions()[1] / 2))
    b.render(w.windowSurface)

def mousedown(key, pos):
    print(f"mousedown {key} at pos {pos}")

def mouseup(key, pos):
    print(f"mouseup {key} at pos {pos}")

def keydown(key):
    print(f"keydown {key}")

# bind events to the user functions
w.bindTick(tick)
w.bindRender(render)
w.bindMouseDown(mousedown)
w.bindMouseUp(mouseup)
w.bindKeyDown(keydown)

t = pgh.Text("comicsansms", 40, "Hello World", colours.Blue)
b = pgh.Button_Circle((80, 80), 50, w, "button")

# start the gameloop
w.startInternalGameLoop(60, 20)

