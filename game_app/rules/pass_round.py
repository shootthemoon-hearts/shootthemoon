from . import game_round as grrz
from channels import Group, Channel
from enum import Enum
from game_app.multiplex_transmit import game_transmit
from game_app.card import Card
import random as rn
from django.utils import timezone
from game_app.models.pass_round import PassRound
from game_app.models.player import Player
from game_app.models.player_type import PlayerType
from game_app.rules import game_round
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

PASS_ROUND_TIMEOUT_MS = 10000

def setup(pr, parent_round, pass_direction):
    pr.direction = pass_direction
    pr.game_round = parent_round
    pr.save()

def start(pr, num_cards_to_pass):
    pr.active = True
    pr.save()
    send_turn_notification(pr)
    pr_id = pr.id
    send_pass_round_started(pr.game_round.game.group_channel, pr_id, num_cards_to_pass, pr.game_round.phase)
    for i in pr.game_round.game.player_set.all():
        send_delay_message(pr, i, pr_id)

def send_pass_round_started(group_channel, pass_round_id, num_cards_to_pass, phase):
    now = timezone.now()
    time_info = game_round.get_time_info(now, PASS_ROUND_TIMEOUT_MS)
    game_transmit(Group(group_channel), {
        "pass_round_started": {
            "id": pass_round_id,
            "cards_to_pass": num_cards_to_pass,
            "game_phase": phase,
            "time_info": time_info
        }
    })

def send_delay_message(pr, player, turn_id):
    received_cards = []
    random_numbers = rn.sample(range(0, 13), 3)
    for random_number in random_numbers:
        received_cards.append(player.hand[random_number])
    received_cards.sort()
    if player.type == PlayerType.DUMMY:
        delay = 100
    else:
        delay = PASS_ROUND_TIMEOUT_MS
    delay_message = {
        'channel':'game_command',
        'delay':delay,
        'content':{
            'command':'pass_cards_selected',
            'command_args':{
                'received_cards': Card.list_to_str_list(received_cards),
                'turn_id': turn_id,
                'player_id': player.id
            }
        }
    }
    Channel('asgi.delay').send(delay_message)

def received_passed_cards(passed_cards, player_id, turn_id):
    # If the pass is invalid this function will simply return and will not
    # make any changes
    try:
        with transaction.atomic():

            pr = PassRound.objects.select_for_update().get(id=turn_id)
            if not pr.active:
                return

            if len(passed_cards) != game_round.NUM_CARDS_TO_PASS_DICT.get(pr.direction):
                return

            player = Player.objects.get(id=player_id)
            from_seat = player.position

            if from_seat in pr.seats_received:
                return

            for card in passed_cards:
                if card not in player.hand:
                    return

            passed_cards_sorted = sorted(passed_cards)
            pr.seats_received.append(from_seat)
            pr.seats_received.sort()
            seats_received_sorted = sorted(pr.seats_received)
            seat_index_in_sort = seats_received_sorted.index(from_seat)
            starting_index = seat_index_in_sort * 3
            for index_offset in range(0, 3):
                pr.passed_cards.insert(starting_index + index_offset, passed_cards_sorted[index_offset])
            pr.save()


    except ObjectDoesNotExist:
        # If the query is invalid, the turn is invalid
        return

    if has_everyone_passed(pr):
        set_hands_to_new_hands(pr)
        finish(pr)

def has_everyone_passed(pr):
    for player in pr.game_round.game.player_set.all():
        if not player.position in pr.seats_received:
            return False
    return True

def send_turn_notification(pr):   
    game_transmit(Group(pr.game_round.game.group_channel),{"your_turn": pr.id})

def set_hands_to_new_hands(pr):
    for from_seat in sorted(pr.seats_received):
        to_seat = (from_seat+pr.direction.value)%4

        start_index = from_seat*3
        end_index = from_seat*3+3
        cards_to_pass = pr.passed_cards[start_index:end_index]

        with transaction.atomic():
            from_player = pr.game_round.game.player_set.select_for_update().get(position=from_seat)
            from_player.hand = sorted(list(set(from_player.hand) - set(cards_to_pass)))
            from_player.save()

        with transaction.atomic():
            to_player = pr.game_round.game.player_set.select_for_update().get(position=to_seat)
            to_player.hand = sorted(to_player.hand + cards_to_pass)
            to_player.save()

def finish(pr):
    pr.active = False
    pr.save()
    grrz.send_players_their_cards(pr.game_round)
    grrz.add_first_trick_phase(pr.game_round)
