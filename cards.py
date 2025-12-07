import pygame

from pygame.sprite import Sprite

class Cards(Sprite):

    def __init__(self, game, group, card, pile):
        super().__init__()
        #Sets up screen and settings
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        #Sets the card and group variables to the card and group values defined where the function is called
        self.group = group
        self.card = card
        self.pile = pile

        self.create_attributes(game)

        #Converts the numerical value of the coordinates to rectangular coordinates
        self.rect.x = self.x
        self.rect.y = self.y

    def create_attributes(self, game): #Sets image and location
        #Sets x and y (Change later)
        if self.pile == 'draw_pile':
            self.x = 20
            self.y = 20
        else:
            self.x = game.columns_x_list[self.pile]
            self.y = 20

        #Sets the image to the image corrosponding with the key and group
        self.image = pygame.image.load(f"images/{self.card}_{self.group}.png")
        self.rect = self.image.get_rect()
    
    def blitme(self):
        #Copies the sprite image to the screen
        self.screen.blit(self.image, self.rect)