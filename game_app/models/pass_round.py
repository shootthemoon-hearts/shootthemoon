from django.db import models

from .game_round import GameRound
from .list_fields import CardListField,SmallIntListField

class PassRound(models.Model):
    active = models.BooleanField(default=False)
    game_round = models.OneToOneField(GameRound, on_delete=models.CASCADE)
    direction = models.IntegerField(default=0)
    passed_cards = CardListField(max_elements=12,default=[])
    seats_received = SmallIntListField(max_elements=4,default=[])
    
    def setup(self,direction):
        self.direction = direction
        self.save()
    
    def start(self):
        self.active = True
        self.save()
        
    def received_passed_cards(self, player, passed_cards):
        passed_cards_sorted = passed_cards.sorted
        from_seat = player.position
        if not from_seat in self.seats_received:
            self.seats_received.append(from_seat)
            seat_index_in_sort = self.seats_received.sorted.indexof(from_seat)
            starting_index = seat_index_in_sort*3
            for index_offset in range(0,3):
                self.passed_cards.insert(starting_index+index_offset, passed_cards_sorted[index_offset])
            self.save()
            if self.has_everyone_passed():
                self.set_hands_to_new_hands()
                self.self_jihad()
        
    def has_everyone_passed(self):
        for player in self.game_round.game.player_set.all():
            if not player.position in self.seats_received:
                return False
        return True
    
    def set_hands_to_new_hands(self):
        for from_seat in self.seats_received.sorted:
            to_seat = (from_seat+self.direction)%4
            
            start_index = from_seat*3
            end_index = from_seat*3+2
            
            from_player = self.game_round.game.player_set.get(position=from_seat)
            from_player.hand = sorted(list(set(from_player.hand) - set(self.passed_cards[start_index:end_index])))
            from_player.save()
            
            to_player = self.game_round.game.player_set.get(position=to_seat)
            to_player.hand = sorted(to_player.hand + self.passed_cards[start_index:end_index])
            to_player.save()
            
    def self_jihad(self):
        self.active = False
        self.save()
        self.game_round.send_players_their_cards()
        self.game_round.add_first_trick_phase()
        
            
            
            
            
            
            
            
            