from __future__ import unicode_literals

from django.db import models

card_regex = '(\h[SCHD])+'
card_max_chars = 3;
card_validator = models.validators.RegexValidator(regex=card_regex, message=None, code=None, inverse_match=None, flags=0)
int_list_validator = models.validators.int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)

class Game(models.Model):
    active = models.BooleanField()
    group_channel = models.IntegerField()

class GameRound(models.Model):
    active = models.BooleanField()
    number = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    phase = models.CharField()
    
class GameTrick(models.Model):
    active = models.BooleanField()
    number = models.IntegerField()
    game_round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    discards = models.CharField(max_length=card_max_chars*4,validators=[card_validator])
    seat_order = models.CharField(max_length=card_max_chars*4,validators=[int_list_validator])

class MatchMakingQueue(models.Model):
    total_players = models.IntegerField()

class Player(models.Model):
    queue = models.ForeignKey(MatchMakingQueue, on_delete=models.SET_NULL)
    active_game = models.ForeignKey(Game, on_delete=models.SET_NULL)
    channel = models.IntegerField()
    seat = models.IntegerField()
    hand = models.CharField(max_length=card_max_chars*13,validators=[card_validator])
    points = models.IntegerField()  
    
    