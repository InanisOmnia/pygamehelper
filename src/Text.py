from src.requirements import *
from src.constants import colours, window_flags, alphabet

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

