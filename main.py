import sys
import random
import pygame

from settings import Settings
from build_pile import Build_Pile
from cards import Cards

class MainGame:

    def __init__(self):
        #Sets up basic settings
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        #Sets up screen
        self.fullscreen = True
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.cursor = pygame.mouse.set_cursor(*pygame.cursors.arrow)
        pygame.display.set_caption("Solitaire")

        self.set_up()

    def set_up(self): #Creates build piles, draw pile, and card columns
        #Lists card categories
        self.groups = [
            "hearts", 
            "diamonds", 
            "spades", 
            "clubs"
            ]

        #Lists types of cards
        self.cards = [
            'ace',
            'two',
            'three',
            'four',
            'five',
            'six',
            'seven',
            'eight',
            'nine',
            'ten',
            'jack',
            'queen',
            'king'
        ]
        
        #Creates a list of all 52 cards
        self.card_list = []

        #Adds each card to card_list with the card and group as attributes
        for card in self.cards:
            for group in self.groups:
                card_0 = {'group': group, 'card': card}
                self.card_list.append(card_0)

        #Creates the four build piles using a base class
        self.hearts_pile = Build_Pile(self, "hearts")
        self.diamonds_pile = Build_Pile(self, "diamonds")
        self.clubs_pile = Build_Pile(self, "clubs")
        self.spades_pile = Build_Pile(self, "spades")

        #Creates the draw pile and columns
        self.create_draw_pile()
        self.create_columns()
        
    def create_draw_pile(self):
        #Creates a sprite group for cards in the draw pile
        self.draw_pile = pygame.sprite.Group()
        #Creates a list of cards in the draw pile
        self.draw_pile_list = []

        #Adds cards to the draw pile until there are 28 left
        while len(self.card_list) > 28:
            self.current_card = random.choice(self.card_list)
            self.current_card['pile'] = 'draw_pile'
            self.draw_pile_list.append(self.current_card)
            self.card = Cards(self, self.current_card['group'], self.current_card['card'], self.current_card['pile'])
            self.draw_pile.add(self.card)
            self.card_list.remove(self.current_card)

    def create_columns(self):
        #Creates a sprite group for each column
        self.column_1 = pygame.sprite.Group()
        self.column_2 = pygame.sprite.Group()
        self.column_3 = pygame.sprite.Group()
        self.column_4 = pygame.sprite.Group()
        self.column_5 = pygame.sprite.Group()
        self.column_6 = pygame.sprite.Group()
        self.column_7 = pygame.sprite.Group()

        #Creates a dictionary of the columns
        self.columns_list = {
            self.column_1: 1,
            self.column_2: 2,
            self.column_3: 3,
            self.column_4: 4,
            self.column_5: 5,
            self.column_6: 6,
            self.column_7: 7
        }

        self.column_cards_list = []

        #Sets the initial x value to 20
        self.columns_x = 50

        #Creates a list of the x value of each column (the number changes later)
        self.columns_x_list = {
            'column_1': 0,
            'column_2': 0,
            'column_3': 0,
            'column_4': 0,
            'column_5': 0,
            'column_6': 0,
            'column_7': 0
        }

        #Creates a list of the current y value of the top card in each column (the number changes later)
        self.columns_y_list = {
            'column_1': 20,
            'column_2': 20,
            'column_3': 20,
            'column_4': 20,
            'column_5': 20,
            'column_6': 20,
            'column_7': 20
        }

        #Adds 133 pixels of space between each pile
        for column in self.columns_x_list:
            self.columns_x += 133
            self.columns_x_list[column] = self.columns_x

        #Adds remaining cards to the columns
        while len(self.card_list) > 0:
            for column in self.columns_list:
                key = self.columns_list[column]
                while len(column) < key:
                    self.current_card = random.choice(self.card_list)
                    self.current_card['pile'] = f'column_{key}'
                    self.column_cards_list.append(self.current_card)
                    self.card = Cards(self, self.current_card['group'], self.current_card['card'], self.current_card['pile'])
                    column.add(self.card)
                    self.card_list.remove(self.current_card)

    def check_events(self):
        for event in pygame.event.get():
            #Checks if the exit button is pressed
            if event.type == pygame.QUIT:
                sys.exit()
            #Checks for buttons pressed
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            #Checks for buttons unpressed
            elif event.type == pygame.KEYUP:
               self.check_keyup_events(event)
            #Checks if the mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_mouse_events()

    def check_keydown_events(self, event):
        #Exits if the q key is pressed
        if event.key == pygame.K_q:
            sys.exit()
    
    def check_keyup_events(self, event):
        pass

    def check_mouse_events(self):
        self.mouse_pos_x, self.mouse_pos_y = pygame.mouse.get_pos()
        self.mouse_collisions = []
        #Creates a highlight around the column card being clicked
        for column in (self.columns_list):
            for card in column: 
                if card.rect.collidepoint(self.mouse_pos_x, self.mouse_pos_y):
                    self.mouse_collisions.append(card)
            if len(self.mouse_collisions) > 1:
                for card in self.mouse_collisions:
                    if self.mouse_pos_y in range(card.y, card.y + 75):
                        card.create_highlight(self)
            elif len(self.mouse_collisions) == 1:
                self.current_card = self.mouse_collisions[0]
                self.current_card.create_highlight(self)
        #Creates a highlight around the top card of the draw pile on click
        for card in self.draw_pile:
            self.current_card = self.draw_pile_list[-1]
            if card.rect.collidepoint(self.mouse_pos_x, self.mouse_pos_y) and (self.current_card['card'] == card.card and self.current_card['group'] == card.group):
                card.create_highlight(self)            

    def update_screen(self): #Sets the background color and copies all of the sprites to the screen
        self.screen.fill(self.settings.bg_color)
        self.hearts_pile.blitme()
        self.diamonds_pile.blitme()
        self.clubs_pile.blitme()
        self.spades_pile.blitme()
        for card in self.draw_pile:
            card.blitme()
        for column in self.columns_list:
            for card in column:
                card.blitme()
        pygame.display.flip()

    def run_game(self): #Checks events, updates screen, and tracks time while running the game
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)

if __name__ == '__main__':
    #Makes a game instance and runs the game.
    game = MainGame()
    game.run_game()

#Trace function: python -u -m trace -t main.py 