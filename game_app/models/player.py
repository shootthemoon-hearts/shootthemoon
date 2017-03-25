from django.db import models

from .game import Game
from .match_making_queue import MatchMakingQueue
from .list_fields import CardListField


class Player(models.Model):
    disconnected = models.BooleanField(default=False)
    enrolled_queue = models.ForeignKey(MatchMakingQueue, null=True, on_delete=models.SET_NULL)
    enrolled_game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    channel = models.CharField(max_length=24,default='')
    position = models.IntegerField(null=True, default=None)
    hand = CardListField(max_elements=13,default=[])
    game_points = models.IntegerField(default=0)
    hand_points = models.IntegerField(default=0)
    