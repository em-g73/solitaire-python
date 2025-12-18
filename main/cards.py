import pygame

from pygame.sprite import Sprite
from highlight import Highlight

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
        #Sets x and y based on pile/column and order
        if self.pile == 'draw_pile':
            self.x = 20
            self.y = 20
            self.image = pygame.image.load(f"images/reverse.png")
        else:
            self.x = game.columns_x_list[self.pile]
            self.y = game.columns_y_list[self.pile]
            game.columns_y_list[self.pile] += 75
            #Sets the image to the image corrosponding with the key and group
            self.image = pygame.image.load(f"images/{self.card}_{self.group}.png")

        self.rect = self.image.get_rect()
    
    def create_highlight(self, game): #Creates a highlight around the card to show it has been clicked on
        for column in game.columns_list:
            for card in column:
                try:
                    card.highlight.visible = False
                except AttributeError:
                    pass
        for card in game.draw_pile:
            try:
                card.highlight.visible = False
            except AttributeError:
                pass
        self.highlight = Highlight(game, self)

    def draw_pile_flip(self, game):
        self.y += 200
        #change layer
        game.draw_pile_list.pop()
        game.draw_pile_list.insert(0, game.current_card)
        self.image = pygame.image.load(f"images/{self.card}_{self.group}.png")
        self.rect = self.image.get_rect()
        #pygame.sprite.LayeredUpdates.move_to_front(self)

    def blitme(self):
        #Copies the sprite image to the screen
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)
        #Copies the highlight sprite's image to the screen if it exists and is visible
        try:
            if self.highlight.visible:
                self.highlight.blitme()
        except AttributeError:
            pass