from django.db import models
from django.contrib.auth.models import User

from .game import Game
from .match_making_queue import MatchMakingQueue
from .list_fields import CardListField


class Player(models.Model):
    disconnected = models.BooleanField(default=False)
    enrolled_queue = models.ForeignKey(MatchMakingQueue, null=True, on_delete=models.SET_NULL)
    enrolled_game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    channel = models.CharField(max_length=27,default='')
    position = models.IntegerField(null=True, default=None)
    hand = CardListField(default=[])
    game_points = models.IntegerField(default=0)
    hand_points = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True)
    
    #self.accounts = None
        
    ''' these are supposed to get sent to update the account in some way after the game '''
    new_elo = models.IntegerField(default=0)
    new_rank = models.IntegerField(default=0)
    new_rank_progress = models.IntegerField(default=0)
    place_this_game = models.IntegerField(default=0)
    