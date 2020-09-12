from MAIN import *

def tick(dt):
    #dt equals the delta time so movement specific calculations on the user side can be made
    print(dt)

def render(fps):
    print(f"render {fps}")

w = Window(500, 500, "Hello World")
w.initScreen()
w.startLoop(tick, render)

