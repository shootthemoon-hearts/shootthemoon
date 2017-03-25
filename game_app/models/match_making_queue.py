from django.db import models

class MatchMakingQueue(models.Model):
    name = models.CharField(max_length=12,default='default')
    total_players = models.IntegerField()