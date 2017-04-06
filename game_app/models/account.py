from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    elo = models.IntegerField(default=800)
    rank = models.IntegerField(default=0)