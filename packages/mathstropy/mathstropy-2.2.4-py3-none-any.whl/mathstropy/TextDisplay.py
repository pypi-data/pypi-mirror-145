import pygame

pygame.font.init()

# display text on screen
class TextDisplay:
    def __init__(self, window):
        self.screen = window
    
    def display(self, size, text, colour, x, y):
        self.font = pygame.font.Font('freesansbold.ttf', size)  # specify the font and size
        self.textSurf = self.font.render(text, True, colour)    # create a surface for the text object
        self.textRect = self.textSurf.get_rect()  # get rect position of text on the screen
        self.textRect.topleft = (x, y)  # specify rect position of text on screen
        self.screen.blit(self.textSurf, self.textRect)