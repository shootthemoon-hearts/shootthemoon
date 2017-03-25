from channels import Group
from channels import Channel
from django.db import models

from game_app.multiplex_transmit import game_transmit
from game_app.deck import Deck
from game_app.card import Card

from .game import *
from .trick_turn import *
from .pass_round import *

class RoundConstants():
    TRICK_PHASE = 'IN_TRICK'
    PASS_PHASE = 'PASS_PHASE'

class GameRound(models.Model):
    game = models.ForeignKey(Game, null = True, on_delete=models.CASCADE)
    
    active = models.BooleanField(default=False)
    number = models.IntegerField(default=-1)
    phase = models.CharField(max_length=10, default='')
    hearts_broken = models.BooleanField(default=False)
    
    def setup(self,parent_game,number):
        self.game = parent_game
        self.number = number
        for player in self.game.player_set.all():
            player.hand_points = 0
            player.save()
        self.save()
    
    def start(self):
        self.active = True
        self.save()
        deck = Deck()
        deck.populate_and_randomize()
        self.deal_cards(deck)
        self.send_players_their_cards()
        self.send_players_initial_valid_cards()
        
        pass_direction = self.determine_passing()
        if pass_direction != 0:
            self.add_pass_phase(pass_direction)
        else:
            self.bypass_pass_phase()
            
    def deal_cards(self, deck):
        '''Deal the cards to each player'''
        print ("Deck length", len(deck.cards))
        while len(deck.cards) > 0:
            for player in self.player_set.all():
                player.hand.append(deck.cards.pop())
        for player in self.player_set.all():
            player.hand.sort()
            player.save()
            print ("player %s's hand: %s" % (player.position ,player.hand))
            
    def send_players_their_cards(self):
        '''Sends a message to each player telling them which cards are 
        theirs'''
        for player in self.player_set.all():
            cards_str = ''
            for card in player.hand:
                cards_str += card.to_json()
            game_transmit(Channel(player.channel),{"Cards":cards_str})
            
    def send_players_initial_valid_cards(self):
        for player in self.player_set.all():
            valid_cards = player.hand
            self.send_player_valid_cards(player, valid_cards)
            
    def send_player_valid_cards(self, player, valid_cards):
        cards_str = ''
        for card in valid_cards:
                cards_str += card.to_json()
        game_transmit(Channel(player.channel),{"valid_cards":cards_str})
            
    def determine_passing(self):
        if (self.number)%4 == 0:
            direction = 1
        elif (self.number)%4 == 1:
            direction = -1
        elif (self.number)%4 == 2:
            direction = 2
        else:
            direction = 0
        return direction
    
    def add_pass_phase(self,pass_direction):
        self.phase = RoundConstants.PASS_PHASE
        self.save()
        self.send_group_the_phase()
        new_pass_round = PassRound()
        new_pass_round.setup(self,pass_direction)
        new_pass_round.start()
        
    def bypass_pass_phase(self):
        self.add_first_trick_phase()
        
    def add_first_trick_phase(self):
        self.phase = RoundConstants.TRICK_PHASE
        self.save()
        self.send_group_the_phase()
        self.add_trick_phase(self.what_seat_has_two_of_clubs())
    
    def add_trick_phase(self,seat_to_go_first):
        if len(self.trickturn_set.all()) >=13:
            self.self_jihad()
        else:
            new_trick_phase = TrickTurn()
            new_trick_phase.setup(self,len(self.trickturn_set.all()),seat_to_go_first,self.hearts_broken)
            new_trick_phase.start()
    
    def what_seat_has_two_of_clubs(self):
        two_of_clubs = Card(2,'Clubs')
        for player in self.game.player_set.all():
            if two_of_clubs in player.hand:
                return player.seat
    
    def send_group_the_phase(self):
        game_transmit(Group(self.game.group_channel),{"game_phase": self.phase})
        
    def self_jihad(self):
        self.active = False
        self.save()
        for i in self.game.player_set.all():
            #checking if player shot the moon and if so applying exception#
            if i.hand_points == 26:
                for j in self.game.player_set.all():
                    j.hand_points = 27
                i.hand_points = 0
        for i in self.game.player_set.all():
            if i.hand_points == 27:
                i.hand_points -= 1
        for i in self.game.player_set.all():
            i.game_points += i.hand_points

            

            