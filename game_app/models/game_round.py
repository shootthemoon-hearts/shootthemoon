from django.db import models
from .game import Game

class GameRound(models.Model):
    game = models.ForeignKey(Game, null = True, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    number = models.IntegerField(default=-1)
    phase = models.CharField(max_length=10, default='')
    hearts_broken = models.BooleanField(default=False)