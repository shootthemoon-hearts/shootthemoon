from .card import Card
from random import shuffle

class Deck():
    '''A deck of cards'''

    def populate_and_randomize(self):
        '''Populates the deck with a full set of cards and shuffles the 
        cards'''
        self.populate()
        self.randomize()

    def populate(self):
        '''Populates the deck with a full set of cards'''
        # Add each card
        self.cards = []
        for suit in Card.SUITS:
            for num in Card.NUMBERS:
                self.cards.append(Card(num, suit))

    def randomize(self):
        '''Shuffles the cards'''
        shuffle(self.cards)
