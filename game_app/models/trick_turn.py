from channels import Group
from channels import Channel
from django.db import models

from game_app.multiplex_transmit import game_transmit
from game_app.card import Card

from game_app.models import game_round
from .list_fields import CardListField

            
class TrickTurn(models.Model):
    active = models.BooleanField(default=False)
    game_round = models.ForeignKey(game_round.GameRound, on_delete=models.CASCADE)
    number = models.IntegerField(null=True,default=None)
    first_seat = models.IntegerField(default=None,null=True)
    discards = CardListField(max_elements=4,default=[])
    expected_seat = models.IntegerField(default=None,null=True)
    hearts_broken = models.BooleanField(default=False)
    
    def setup(self,parent_round,first_seat,number):
        self.game_round = parent_round
        self.first_seat = first_seat
        self.expected_seat = first_seat
        self.number = number
        self.save()
        
    def start(self):
        self.active = True
        self.save()
        self.send_turn_notification()
        
        
    def card_discarded(self, player, discard):
        if player.position == self.expected_seat:
            self.discards.append(discard)
            self.save()
            
            player.hand = sorted(list(set(player.hand) - set([discard])))
            player.save()
            
            self.send_players_discard(player,discard)
            
            self.expected_seat = self.get_next_expected_seat() 
            if self.expected_seat == self.first_seat:
                self.self_jihad()
            else:
                self.send_turn_notification()
        
    def send_turn_notification(self):
        player = self.game_round.game.player_set.get(position=self.expected_seat)
        if self.expected_seat == self.first_seat:
            valid_cards = self.valid_cards_leader(player.hand)
        else:
            valid_cards = self.valid_cards_follower(player.hand)
            
        game_transmit(Channel(player.channel),{"your_turn": "true"})
        self.game_round.send_player_valid_cards(player, valid_cards)
                
    def get_next_expected_seat(self):
        return (self.expected_seat+1)%4
    
    def get_winning_player(self):
        winning_discard = self.discards[0]
        winning_seat_offset = 0
        for seat_offset in range(1,4):
            discard = self.discards[seat_offset]
            if discard.suit == self.leading_suit() and discard > winning_discard:
                winning_discard = discard
                winning_seat_offset = seat_offset
        winning_seat = (self.first_seat+winning_seat_offset)%4
        return self.game_round.game.player_set.get(position=winning_seat)
            
    def get_trick_points(self):
        points = 0
        for discard in self.discards:
            if discard.suit == Card.HEARTS:
                points += 1
            if discard.suit == Card.SPADES and discard.number == 12:
                points += 13
        return points
        
    def leading_suit(self):
        '''this check is run after the first guy discards'''
        first_discard = self.discards[0]
        return first_discard.suit
    
    def are_hearts_now_broken(self):
        '''this check is run after everyone discarded in a trick'''
        return self.get_trick_points() > 0

    def valid_cards_follower(self, hand):
        valid_cards = []
        lead_suit = self.leading_suit()
        counter = 0
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
        return valid_cards 
        
    def valid_cards_leader(self, hand):
        valid_cards = []
        if self.number == 0:
            valid_cards.append(Card(2,'Clubs'))
        else:
            if self.hearts_broken:
                valid_cards = hand
            else:
                for card in hand:
                    if card.suit != Card.HEARTS and card != Card(12,'Spades'):
                        valid_cards.append(card)
        return valid_cards
    
    def send_players_discard(self, player, discard):
        '''Sends a message to each player telling them which cards are 
        theirs'''
        discard_json = ""
        for card in discard:
            discard_json += card.to_json()
        game_transmit(Group(self.game_round.game.group),{"discard": {"player": player.position, "card": discard_json}})  
            
    def self_jihad(self):
        self.active = False
        if self.hearts_broken == False:
            self.game_round.hearts_broken = self.are_hearts_broken()
            self.game_round.save()
        winning_player = self.get_winning_player()
        winning_player.hand_points += self.get_trick_points()
        winning_player.save()
        self.game_round.add_trick_phase()
    