class PassRound():
    
    def __init__(self, players, direction):
        self.players_pass_dict = {}
        self.players_new_hands = {}
        self.players = players
        self.direction = direction
        
        for player in players:
            self.players_pass_dict[player] = False
            self.players_new_hands[player] = player.hand
        
    def passed_cards(self, player, passed_cards):
        i = player.position
        receiving_player = self.players[(i+self.direction)%4]
        receiving_new_hand = sorted(self.players_new_hands[receiving_player] + passed_cards)
        giving_new_hand = sorted(list(set(self.players_new_hands[player]) - set(passed_cards)))
        
        self.players_new_hands[receiving_player] = receiving_new_hand
        self.players_new_hands[player] = giving_new_hand
        self.players_pass_dict[player] = True
        
        return self.has_everyone_passed()
        
    def has_everyone_passed(self):
        for player in self.players:
            if not self.players_pass_dict[player]:
                return False
        return True
    
    def set_hands_to_new_hands(self):
        for player in self.players:
            player.hand = self.players_new_hands[player]
            
            
            
            
            
            
            
            