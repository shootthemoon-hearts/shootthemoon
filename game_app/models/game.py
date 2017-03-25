from channels import Group
from channels import Channel
from django.db import models 
from game_app.card import Card
from game_app.models.game_round import GameRound
from game_app.multiplex_transmit import game_transmit

class Game(models.Model):
    active = models.BooleanField(default=False)
    group_channel = models.CharField(max_length=16,default='')
    
    def setup(self,players):
        self.group_channel = "game_%s" % self.id
        for player in players:
            self.add_player(player,self.group)
        self.save()
    
    def add_player(self, player,group):
        game_transmit(Channel(player.channel),{'id':str(self.id)})
        player.enrolled_game = self
        player.position = len(self.player_set.all()) - 1
        game_transmit(Channel(player.channel),{"player_pos":player.position})
        print ('Game', self.id, 'has', len(self.player_set.all()), 'players')
        player.save()
        group.add(Channel(player.channel))
    
    def start(self):
        self.active = True
        self.save()
        self.add_round()
            
    def add_round(self):
        self.send_players_score()
        self.check_winning_conditions()
        new_round = GameRound()
        new_round.setup(self,len(self.gameround_set.all()))
        new_round.start()
    
    def pass_cards_selected(self, cards_str, channel):
        cards = []
        for card_str in cards_str:
            cards.append(Card.from_short_string(card_str))
        player = self.get_player_with_channel(channel)
        self.gameround_set.get(active=True).passround.received_passed_cards(player,cards)
    
    def trick_cards_selected(self,cards_str,channel):
        card = Card.from_short_string(cards_str[0])
        player = self.get_player_with_channel(channel)
        self.gameround_set.get(active=True).trickturn_set.get(active=True).card_discarded(player,card)
        
    def send_players_score(self):
        '''Sends a message to each player telling them the scores -- only
        updates after each hand'''
        score_list = []
        for player in self.player_set.all():
            score_list.append(player.game_points)
        game_transmit(Group(self.group),{"scores": {"player": player.position, "score_list": score_list}})
    
        
    def get_player_with_channel(self,channel):
        return self.player_set.get(channel=channel.name)
    
    def check_winning_conditions(self):
        for player in self.players:
            if player.game_points >= 100:
                self.self_jihad()
                
    
    def self_jihad(self):
        self.active = False
        self.save()

            
