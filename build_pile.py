import pygame

from pygame.sprite import Sprite

class Build_Pile(Sprite):

    def __init__(self, game, key):
        super().__init__()
        #Sets up screen and settings
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        #Sets the key variable to the key that is defined where the function is called
        self.key = key

        self.create_attributes()

        #Converts the numerical value of the coordinates to rectangular coordinates
        self.rect.x = self.x
        self.rect.y = self.y

    def create_attributes(self): #Sets image and loctation
        #Assigns a y value to the pile based on the key
        y_coordinate = {
            "hearts": 20,
            "diamonds": 202,
            "clubs": 384,
            "spades": 566
        }

        #Sets the y to the value that corrosponds with the key
        self.y = y_coordinate[self.key]
        self.x = 1150

        #Sets the image to the image corrosponding with the key
        self.image = pygame.image.load(f"images/{self.key}_placeholder.png")
        self.rect = self.image.get_rect()

    def blitme(self):
        #Copies the sprite image to the screen
        self.screen.blit(self.image, self.rect)