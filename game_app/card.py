import re

class Card():
    '''This class is meant to represent any card to be used during the game.

    Attributes:
        suit: The suit of the card
        number: The number representing the card.
            Ace is 1. 2 - 10 are the standard numbers. Jack is 11. Queen is 12.
            King is 13.
    '''

    SPADES = 'Spades'
    CLUBS = 'Clubs'
    HEARTS = 'Hearts'
    DIAMONDS = 'Diamonds'
    SUITS = [SPADES, CLUBS, HEARTS, DIAMONDS]

    JACK = 'Jack'
    QUEEN = 'Queen'
    KING = 'King'
    ACE = 'Ace'

    NUMBER_STR_DICT = {
            1: ACE,
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: JACK,
            12: QUEEN,
            13: KING,
    } 

    NUMBERS = NUMBER_STR_DICT.keys()

    SHORT_SPADES = 'S'
    SHORT_CLUBS = 'C'
    SHORT_HEARTS = 'H'
    SHORT_DIAMONDS = 'D'
    SHORT_SUITS = [SHORT_SPADES, SHORT_CLUBS, SHORT_HEARTS, SHORT_DIAMONDS]

    SUIT_TO_SHORT_SUIT_DICT = {
            SPADES: SHORT_SPADES, 
            CLUBS: SHORT_CLUBS,
            HEARTS: SHORT_HEARTS,
            DIAMONDS: SHORT_DIAMONDS,
    }

    def __init__(self, number, suit):
        '''Constructor

        Args:
            number: The number representing the card. Must be an integer.
                Ace is 1. 2 - 10 are the standard numbers. Jack is 11. Queen is
                12. King is 13.
            suit: The suit of the card
        '''
        self.suit = suit
        self.number = number
        
    @classmethod    
    def from_short_string(cls, short):
        regex = r"[0-9]{1,2}"
        number = re.match(regex, short).group()
        number = int(number)
        regex = r"[DCSH]"
        short_suit = re.search(regex, short).group()
        return cls(number, Card.SUITS[Card.SHORT_SUITS.index(short_suit)])

    def __repr__(self):
        '''Returns a string representation of the card to help with 
        debugging'''
        number_str = Card.NUMBER_STR_DICT[self.number]
        return '%s of %s' % (number_str, self.suit)

    def to_json(self):
        '''Returns a json representation of this card'''
        short_suit = Card.SUIT_TO_SHORT_SUIT_DICT[self.suit]
        return '%s%s' % (self.number, short_suit)
    
    def __lt__(self, other):
        if self.suit != other.suit:
            return self.suit < other.suit
        else:
            return self.number < other.number
        
    def __gt__(self,other):
        if self.suit != other.suit:
            return self.suit > other.suit
        else:
            return self.number > other.number
        
    def __eq__(self,other):
        if self.suit != other.suit:
            return self.suit == other.suit
        else:
            return self.number == other.number
        
    def __le__(self, other):
        if self.suit != other.suit:
            return self.suit <= other.suit
        else:
            return self.number <= other.number
        
    def __ge__(self, other):
        if self.suit != other.suit:
            return self.suit >= other.suit
        else:
            return self.number >= other.number
 
    def __ne__(self, other):
        if self.suit != other.suit:
            return self.suit != other.suit
        else:
            return self.number != other.number
        
    def __hash__(self):
        return hash((self.number, self.suit))
        