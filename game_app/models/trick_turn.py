from django.db import models
from .game_round import GameRound
from .list_fields import CardListField

            
class TrickTurn(models.Model):
    active = models.BooleanField(default=False)
    game_round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    number = models.IntegerField(null=True,default=None)
    first_seat = models.IntegerField(default=None,null=True)
    discards = CardListField(default=[])
    expected_seat = models.IntegerField(default=None,null=True)
    hearts_broken = models.BooleanField(default=False)