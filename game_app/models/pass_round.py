from django.db import models
from .game_round import GameRound
from .list_fields import CardListField
from django.contrib.postgres.fields import ArrayField


class PassRound(models.Model):
    active = models.BooleanField(default=False)
    game_round = models.OneToOneField(GameRound, on_delete=models.CASCADE)
    direction = models.IntegerField(default=0)
    passed_cards = CardListField(default=[])
    seats_received = ArrayField(models.IntegerField(default=0), size=4, default=list)