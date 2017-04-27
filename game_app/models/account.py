from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    elo = models.IntegerField(default=1500)
    rank = models.IntegerField(default=-9)
    rank_points = models.IntegerField(default=0)
    rank_promote = models.IntegerField(default=45)