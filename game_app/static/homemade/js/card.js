var Card = function(number, suit) {

    this.number = number;
    this.suit = suit;

};

Card.SPADES = 'Spades';
Card.CLUBS = 'Clubs';
Card.HEARTS = 'Hearts';
Card.DIAMONDS = 'Diamonds';
Card.BACK = 'Back';
Card.SUITS = [Card.BACK, Card.CLUBS, Card.DIAMONDS, Card.SPADES, Card.HEARTS];

Card.JACK = 'Jack';
Card.QUEEN = 'Queen';
Card.KING = 'King';
Card.ACE = 'Ace';

Card.NUMBER_STR_DICT = {
        1: Card.ACE,
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: Card.JACK,
        12: Card.QUEEN,
        13: Card.KING,
} ;

Card.NUMBERS = []; 
for (i = 1; i <= 13; i++) {
    Card.NUMBERS.push(i);
}

Card.SHORT_SPADES = 'S';
Card.SHORT_CLUBS = 'C';
Card.SHORT_HEARTS = 'H';
Card.SHORT_DIAMONDS = 'D';
Card.SHORT_BACK = 'B';
Card.SHORT_SUITS = [Card.SHORT_BACK, Card.SHORT_CLUBS, Card.SHORT_DIAMONDS, Card.SHORT_SPADES, Card.SHORT_HEARTS];

//Card.SUIT_TO_SHORT_SUIT_DICT = {
//    Card.SPADES: Card.SHORT_SPADES, 
//    Card.CLUBS: Card.SHORT_CLUBS,
//    Card.HEARTS: Card.SHORT_HEARTS,
//    Card.DIAMONDS: Card.SHORT_DIAMONDS,
//};

Card.CardFromShortSuit = function(number, short_suit) {
    // Ghetto backwards map logic
    i = Card.SHORT_SUITS.indexOf(short_suit);
    suit = Card.SUITS[i];
    return new Card(number, suit);
};

Card.CardsFromJSON = function(str) {
    cards = [];
    regex = /([1-9a-d][DCSH])/g;
    cards_str = str.match(regex);
    for (i in cards_str) {
        card_str = cards_str[i];
        regex = /[1-9a-d]/;
        number = card_str.match(regex).toString();
        number = parseInt(number,16);
        regex = /[DCSH]/;
        short_suit = card_str.match(regex).toString();
        cards.push(Card.CardFromShortSuit(number, short_suit));
    }
    return cards;
};

Card.prototype.toJSON = function() {
	var i = Card.SUITS.indexOf(this.suit);
	var short_suit = Card.SHORT_SUITS[i];
	return this.number.toString(16) + short_suit;
}

Card.prototype.equals = function(other) {
	return this.number == other.number && this.suit == other.suit;
}

Card.prototype.value = function(){
	return Card.SUITS.indexOf(this.suit)*100 + this.number;
}
