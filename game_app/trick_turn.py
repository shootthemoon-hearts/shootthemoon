class TrickTurn():
    
    def __init__(self, players, direction):
        self.discards_per_player = {}
        
        self.players_new_hands = {}
        self.players = players
        self.player_order = []
        self.direction = direction
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
            
    def get_next_discarder(self):
        return self.players[(self.last_discarder.position+self.direction)%4]
    
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
        