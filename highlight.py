import pygame

from pygame.sprite import Sprite

class Highlight(Sprite):

    def __init__(self, game, card):
        super().__init__()
        #Sets up screen and settings
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        self.create_attributes(card)

        #Converts the numerical value of the coordinates to rectangular coordinates
        self.rect.x = self.x
        self.rect.y = self.y

        #Value determines if highlight will be visible
        self.visible = True

    def create_attributes(self, card): #Sets image and loctation
        #Sets the image
        self.image = pygame.image.load(f"images/highlight.png")
        self.rect = self.image.get_rect()

        #Sets the y to the value that corrosponds with the card
        self.x = card.x
        self.y = card.y

    def blitme(self):
        #Copies the sprite image to the screen
        self.screen.blit(self.image, self.rect)