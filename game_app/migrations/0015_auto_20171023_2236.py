# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import game_app.models.player_type
import game_app.rules.pass_direction
import server_main.models.enum_field


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0014_auto_20170506_0545'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='time_turn_started',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='type',
            field=server_main.models.enum_field.EnumField(default=game_app.models.player_type.PlayerType(1)),
        ),
        migrations.AlterField(
            model_name='passround',
            name='direction',
            field=server_main.models.enum_field.EnumField(default=game_app.rules.pass_direction.PASS_DIRECTION(1)),
        ),
        migrations.AlterField(
            model_name='player',
            name='channel',
            field=models.CharField(default='', max_length=37),
        ),
    ]