from game_app.card import Card

class TrickTurn():
    
    def __init__(self, players, direction, first_turn, hearts_broken):
        self.first_turn = first_turn
        self.discards_per_player = {}
        self.players_new_hands = {}
        self.players = players
        self.player_order = []
        self.direction = direction
        self.hearts_broken = hearts_broken
        self.last_discarder = None
        for player in players:
            self.discards_per_player[player] = None
            
    def card_discarded(self, player, discard):
        discard = discard[0]
        self.player_order.append(player)
        self.discards_per_player[player] = discard
        new_hand = player.hand[:]
        for card in new_hand:
            if card == discard:
                del (new_hand[new_hand.index(card)]) 
        
        self.players_new_hands[player] = new_hand
        self.last_discarder = player
        
        return self.has_everyone_discarded()
        
    def has_everyone_discarded(self):
        for player in self.players:
            if not self.discards_per_player[player]:
                return False
        return True
    
    def set_hands_to_new_hands(self):
        for player in self.players:
            player.hand = self.players_new_hands[player]
            
            # +self.direction was changed to +1, because the play order doesn't
            # use self.direction, only the passing uses that
    def get_next_discarder(self):
        return self.players[(self.last_discarder.position+1)%4]
    
    def get_winner(self):
        first_discard = self.discards_per_player[self.player_order[0]]
        discards = []
        for player in self.player_order[1:]:
            if first_discard.suit == self.discards_per_player[player].suit:
                discards.append(self.discards_per_player[player])
        discards.append(first_discard)
        discards.sort()
        winning_card = discards[-1]
        for player, discard in self.discards_per_player.items():
            if discard == winning_card:
                return player
            
    def get_trick_points(self):
        points = 0
        discards = []
        for player in self.player_order[0:]:
            discards.append(self.discards_per_player[player])
        for i in discards:
            if i.suit == Card.HEARTS:
                points += 1
            if i.suit == Card.SPADES and i.number == 12:
                points += 13
        return points
        
    def what_was_lead(self):
        '''this check is run after the first guy discards'''
        first_discard = self.discards_per_player[self.player_order[0]]
        return first_discard.suit
    
    def are_hearts_broken(self):
        '''this check is run after everyone discarded in a trick'''
        discards = []
        counter = 0
        for player in self.player_order[0:]:
            discards.append(self.discards_per_player[player])
        for discard in discards:
            if discard.suit == Card.HEARTS:
                counter += 1
        if counter != 0:
            return True
        else:
            return False

    def valid_cards_follower(self, hand):
        lead_suit = self.what_was_lead()
        valid_cards = []
        counter = 0
        if self.first_turn == False:
            for card in hand:
                if card.suit == lead_suit:
                    counter += 1
            if counter != 0:
                for card in hand:
                    if card.suit == lead_suit:
                        valid_cards.append(card)
            else:
                for card in hand:
                    valid_cards.append(card)
        else:
            for card in hand:
                if card.suit == lead_suit:
                    counter += 1
            for card in hand:
                if counter != 0:
                    if card.suit == lead_suit:
                        valid_cards.append(card)
                else:     
                    for card in hand:
                        if card.suit != Card.HEARTS and card != Card(12,'Spades'):
                            valid_cards.append(card)
        return valid_cards 
        
    def valid_cards_leader(self, hand):
        valid_cards = []
        if self.first_turn == True:
            valid_cards.append(Card(2,'Clubs'))
        else:
            if self.hearts_broken == False:
                for card in hand:
                    if card.suit != Card.HEARTS:
                        valid_cards.append(card)
            else:
                for card in hand:
                    valid_cards.append(card)
        return valid_cards     
    