from src.requirements import *
from src.Text import *

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
