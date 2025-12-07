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

        for card in self.cards:
            for group in self.groups:
                card_0 = {'group': group, 'card': card}
                self.card_list.append(card_0)

        #Creates the four build piles using a base class
        self.hearts_pile = Build_Pile(self, "hearts")
        self.diamonds_pile = Build_Pile(self, "diamonds")
        self.clubs_pile = Build_Pile(self, "clubs")
        self.spades_pile = Build_Pile(self, "spades")

        self.create_draw_pile()
        self.create_columns()
        
    def create_draw_pile(self):
        #Creates a sprite group for cards in the draw pile
        self.draw_pile = pygame.sprite.Group()

        #Adds cards to the draw pile until there are 28 left
        while len(self.card_list) > 28:
            self.current_card = random.choice(self.card_list)
            self.current_card['pile'] = 'draw_pile'
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

        #Sets the initial x value to 20
        self.columns_x = 20

        self.columns_x_list = {
            'column_1': 0,
            'column_2': 0,
            'column_3': 0,
            'column_4': 0,
            'column_5': 0,
            'column_6': 0,
            'column_7': 0
        }

        #Adds 133 pixels of space between each pile
        for column in self.columns_x_list:
            self.columns_x += 133
            self.columns_x_list[column] = self.columns_x

        #Adds remaining cards to the columns (this doesn't work at the moment)
        while len(self.card_list) > 0:
            for column in self.columns_list:
                key = self.columns_list[column]
                while len(column) < key:
                    self.current_card = random.choice(self.card_list)
                    self.current_card['pile'] = f'column_{key}'
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

    def check_keydown_events(self, event):
        #Exits if the q key is pressed
        if event.key == pygame.K_q:
            sys.exit()
    
    def check_keyup_events(self, event):
        pass

    def update_screen(self):
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

    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)

if __name__ == '__main__':
    #Makes a game instance and runs the game.
    game = MainGame()
    game.run_game()

#Trace function: python -u -m trace -t main.py 