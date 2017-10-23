from django.db import models
from .game_round import GameRound
from .list_fields import CardListField
from django.contrib.postgres.fields import ArrayField
from server_main.models.enum_field import EnumField
from game_app.rules.pass_direction import PASS_DIRECTION


class PassRound(models.Model):
    active = models.BooleanField(default=False)
    game_round = models.OneToOneField(GameRound, on_delete=models.CASCADE)
    direction = EnumField(enum_class=PASS_DIRECTION, default=PASS_DIRECTION.LEFT)

    # Passed cards are stored in a single list
    # The list assumes three cards per player in seat order
    # If only some players have passed, the cards are placed in seat order,
    # but empty spaces are not kept for those who have not.
    # For example, if seat 0 and 2 have passed, but 1 has not, the list will
    # be 012678. Then when seat 1 passes, the list will be edited to
    # 012345678. seats_received is required to make this work.
    passed_cards = CardListField(default=[])
    seats_received = ArrayField(models.IntegerField(default=0), size=4, default=list)
