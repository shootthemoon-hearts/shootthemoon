from .round import Round
from .card import Card
from .deck import Deck
from .player import Player
from .trick_turn import TrickTurn
from .pass_round import PassRound
from . import game_event_manager 
from channels import Channel,Group
from game_app.models import GameRound,GameTrick,GamePassPhase

import logging

MAX_PLAYERS = 4
BEFORE_GAME = 'BEFORE_GAME'
IN_TRICK = 'IN_TRICK'
PASS_PHASE = 'PASS_PHASE'

def setup_game(game):
    game.active = True
    game.group_channel = 'game_%d'%game.id
    for player in game.player_set.all():
        Group(game.group_channel).add(player.channel)
    game_event_manager.multiplex_transmit(Group(game.group_channel),{'id':game.id})
    for player in game.player_set.all():
        game_event_manager.multiplex_transmit(Channel(player.channel),{"player_pos":player.seat})
    print ('Game',game.id,' has started')
    add_and_setup_round(game)

def add_and_setup_round(game):
    new_round = GameRound()
    new_round.game = game
    new_round.number = len(game.gameround_set.all())
    new_round.active = True
    new_round.phase = PASS_PHASE        
    add_and_setup_pass_phase(new_round)

def add_and_setup_pass_phase(game_round):
    new_pass = GamePassPhase()
    new_pass.game_round = game_round
    new_pass.active = True
    new_pass.direction = determine_passing(game_round.number)
    

def add_and_setup_trick_phase(game_round):
    pass
    
def determine_passing(round_number):
        if (round_number)%4 == 0:
            direction = 1
        elif (round_number)%4 == 1:
            direction = -1
        elif (round_number)%4 == 2:
            direction = 2
        else:
            direction = 0
        return direction   
    
def deal_cards(players, deck):
    #Deal the cards to each player
    print ("Deck length", len(deck.cards))
    while len(deck.cards) > 0:
        for player in players:
            player.hand.append(deck.cards.pop())
            
def send_players_their_cards(players):
    #Sends a message to each player telling them which cards are theirs
    for player in players:
        cards_str = ''
        for card in player.hand:
            cards_str += card.to_json()
        game_event_manager.multiplex_transmit(Channel(player.channel),{"Cards":cards_str})       

def send_player_valid_cards(player, valid_cards):
    cards_str = ""
    for card in valid_cards:
            cards_str += card.to_json()
    game_event_manager.multiplex_transmit(Channel(player.channel),{"valid_cards":cards_str})
    
def send_players_initial_valid_cards(players):
    for player in players:
        valid_cards = player.hand
        send_player_valid_cards(player, valid_cards)
        
def send_players_the_phase(players, phase):
    #Sends a message to each player telling them which cards are theirs
    for player in players:
        game_event_manager.multiplex_transmit(Channel(player.channel),{"game_phase": phase})
        
def send_players_discard(game_group, player, discard):
    #Sends a message to each player telling them which cards are theirs
    discard_json = ""
    for card in discard:
        discard_json += card.to_json()
    game_event_manager.multiplex_transmit(Group(game_group),{"discard": {"player": player.seat, "card": discard_json}})
    
def send_players_score(game_group, players):
    #Sends a message to each player telling them the scores -- only updates after each hand
    score_list = []
    for player in players:
        score_list.append(player.points)
    game_event_manager.multiplex_transmit(Group(game_group),{"scores": {"player": player.seat, "score_list": score_list}})
    
def organize_hand_and_begin_round(round,players,pass_direction):
    for i in range(0,len(players)):
        players[i].hand.sort()
        print ("player %s's hand: %s" % (i ,players[i].hand))
    send_players_their_cards(players)
    send_players_initial_valid_cards(players)
    if pass_direction != 0:
        pass_card_thing()
    else:
        self.phase = Game.IN_TRICK
        self.send_players_the_phase(self.phase)
        self.rounds[-1].phase = self.phase
        self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction))
        next_player = self.who_goes_first()
        game_event_manager.multiplex_transmit(next_player.channel,{"your_turn": "true"})
        
def pass_cards_selected(self, cards_str, channel):
    cards = []
    for card_str in cards_str:
        cards.append(Card.from_short_string(card_str))
    player = self.get_player_with_channel(channel)
    everyone_passed = self.pass_round.passed_cards(player, cards)
    if everyone_passed:
        self.pass_round.set_hands_to_new_hands()
        self.send_players_their_cards()
        self.tell_round_phase()
        self.phase = Game.IN_TRICK
        self.send_players_the_phase(self.phase)
        self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction, len(self.rounds[-1].tricks) == 0, self.hearts_broken))
        next_player = self.who_goes_first()
        #
        valid_cards = self.rounds[-1].tricks[-1].valid_cards_leader(next_player.hand)
        self.send_player_valid_cards(next_player.channel, valid_cards)
        #
        game_event_manager.multiplex_transmit(next_player.channel,{"your_turn": "true"})
  
def trick_cards_selected(self, cards_str, channel):
    cards = []
    for card_str in cards_str:
        cards.append(Card.from_short_string(card_str))
    player = self.get_player_with_channel(channel)
    self.send_players_discard(player, cards)
    everyone_discarded = self.rounds[-1].tricks[-1].card_discarded(player, cards)
    if everyone_discarded:
        if self.hearts_broken == False:
            self.hearts_broken = self.rounds[-1].tricks[-1].are_hearts_broken()
        self.tricks_this_hand += 1
        next_player = self.rounds[-1].tricks[-1].get_winner()
        next_player.hand_points += self.rounds[-1].tricks[-1].get_trick_points()
        for player in self.players:
            player.hand = self.rounds[-1].tricks[-1].players_new_hands[player]
        self.send_players_their_cards()
        self.phase = Game.IN_TRICK
        self.tell_round_phase()
        self.send_players_the_phase(self.phase)
        self.rounds[-1].tricks.append(TrickTurn(self.players, self.direction, len(self.rounds[-1].tricks) == 0, self.hearts_broken))
        #
        valid_cards = self.rounds[-1].tricks[-1].valid_cards_leader(next_player.hand)
        self.send_player_valid_cards(next_player.channel, valid_cards)
        #
        game_event_manager.multiplex_transmit(next_player.channel,{"your_turn": "true"})
        ###################################################
        ##### BELOW IF STATEMENT IS THE END OF A HAND #####
        ###################################################
        if self.tricks_this_hand == self.trick_count: #normally 13 (set lower for test)
            self.tricks_this_hand = 0
            ####
            for i in self.players:
                #checking if player shot the moon and if so applying exception#
                if i.hand_points == 26:
                    for j in self.players:
                        j.hand_points = 27
                    i.hand_points = 0
            for i in self.players:
                if i.hand_points == 27:
                    i.hand_points -= 1
            for i in self.players:
                i.game_points += i.hand_points
                    ####
            for i in self.players:
                i.hand_points = 0
            game_over = 0
            for i in self.players:
                if i.game_points >= 100:
                    game_over += 1
            if game_over == 0:
                self.send_players_score()
                self.setup_game()
            else:
                self.game_over()
    else:
        next_player = self.rounds[-1].tricks[-1].get_next_discarder()
        #
        valid_cards = self.rounds[-1].tricks[-1].valid_cards_follower(next_player.hand)
        self.send_player_valid_cards(next_player.channel, valid_cards)
        #
        game_event_manager.multiplex_transmit(next_player.channel,{"your_turn": "true"})
        
def pass_card_thing(game_round):
    game_round.phase = PASS_PHASE
    send_players_the_phase(game_round.phase)
    pass_round = GamePassPhase(players=self.players, direction=self.direction)
    #HERE
        
def who_goes_first(players):
    two_of_clubs = Card(2,'Clubs')
    for player in players:
        if two_of_clubs in player.hand:
            return player
        
def game_over(self):
    pass

'''
////////////////////////////////////
'''

        
        self.phase = Game.BEFORE_GAME
        self.send_players_the_phase(self.phase)
        deck = Deck()
        deck.populate_and_randomize()
        self.deal_cards(deck)
        ### deals with hand passing logic
        self.determine_passing()
        self.organize_hand()


        self.tricks_this_hand = 0
        self.game_winner = -1
        self.trick_count = 13 #13 normally
 
    
    def setup_game(self):
        self.phase = Game.BEFORE_GAME
        self.rounds.append(Round(len(self.rounds), self.phase))
        self.tell_round_phase()
        self.send_players_the_phase(self.phase)
        deck = Deck()
        deck.populate_and_randomize()
        self.deal_cards(deck)
        ### deals with hand passing logic
        self.determine_passing()
        self.organize_hand()


            


    

       
