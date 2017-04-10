from django.db import models 

import datetime

class Game(models.Model):
    active = models.BooleanField(default=False)
    group_channel = models.CharField(max_length=16,default='')
    date = models.DateField(default=datetime.date.today)