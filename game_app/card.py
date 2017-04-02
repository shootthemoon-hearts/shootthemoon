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
        
    @staticmethod
    def list_to_str_list(list_of_cards):
        out_str_list = []
        for card in list_of_cards:
            out_str_list.append(str(card))
        return out_str_list
        
    @staticmethod
    def list_to_str(list_of_cards):
        out_str = ""
        for card in list_of_cards:
            out_str += str(card)
        return out_str
    
    @classmethod
    def list_from_str_list(cls,in_str_list):
        card_list = []
        for in_str in in_str_list:
            card_list.extend(Card.list_from_str(in_str))
        return card_list
        
    @classmethod    
    def list_from_str(cls, in_str):
        single_card_regex = re.compile("([1-9a-d])([DCSH])")
        card_list = []
        for match in re.finditer(single_card_regex,in_str):
            if match:
                card_list.append(cls(
                    int(match.group(1),16),#16 is because number is hexidecimal
                    Card.SUITS[Card.SHORT_SUITS.index(match.group(2))]))
        return card_list

    def __repr__(self):
        short_suit = Card.SUIT_TO_SHORT_SUIT_DICT[self.suit]
        return '%x%c' % (self.number, short_suit)
    
    def __lt__(self, other):
        if self.suit != other.suit:
            if self.suit == 'Hearts' and other.suit == 'Spades':
                return False
            elif self.suit == 'Spades' and other.suit == 'Hearts':
                return True
            else:
                return self.suit < other.suit
        else:
            if self.number == 1 and other.number != 1:
                return False
            elif other.number == 1 and self.number != 1:
                return True
            else:
                return self.number < other.number
        
    def __gt__(self,other):
        if self.suit != other.suit:
            if self.suit == 'Hearts' and other.suit == 'Spades':
                return True
            elif self.suit == 'Spades' and other.suit == 'Hearts':
                return False
            else:
                return self.suit > other.suit
        else:
            if self.number == 1 and other.number != 1:
                return True
            elif other.number == 1 and self.number != 1:
                return False
            else:
                return self.number > other.number
        
    def __eq__(self,other):
        if self.suit != other.suit:
            return self.suit == other.suit
        else:
            return self.number == other.number
        
    def __le__(self, other):
        if self.suit != other.suit:
            if self.suit == 'Hearts' and other.suit == 'Spades':
                return False
            elif self.suit == 'Spades' and other.suit == 'Hearts':
                return True
            else:
                return self.suit <= other.suit
        else:
            if self.number == 1 and other.number != 1:
                return False
            elif other.number == 1 and self.number != 1:
                return True
            else:
                return self.number <= other.number
        
    def __ge__(self, other):
        if self.suit != other.suit:
            if self.suit == 'Hearts' and other.suit == 'Spades':
                return True
            elif self.suit == 'Spades' and other.suit == 'Hearts':
                return False
            else:
                return self.suit >= other.suit
        else:
            if self.number == 1 and other.number != 1:
                return True
            elif other.number == 1 and self.number != 1:
                return False
            else:
                return self.number >= other.number
 
    def __ne__(self, other):
        if self.suit != other.suit:
            return self.suit != other.suit
        else:
            return self.number != other.number
        
    def __hash__(self):
        return hash((self.number, self.suit))
        