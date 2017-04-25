from . import game_round as grrz
from channels import Group, Channel
from game_app.multiplex_transmit import game_transmit
from game_app.card import Card
import random as rn
from game_app.models.pass_round import PassRound
from game_app import game_sched
from django.db import transaction
from game_app.rules import game

TIME_TO_SELECT_PASS_CARDS = 1

def setup(pr,parent_round,direction):
    pr.direction = direction
    pr.game_round = parent_round
    pr.save()

def start(pr):
    pr.active = True
    pr.save()
    send_turn_notification(pr)
    for i in pr.game_round.game.player_set.all():
        start_pass_timer(pr, i, pr.id)
    
def start_pass_timer(pr, player, turn_id):
    received_cards = []
    random_numbers = rn.sample(range(0,13),3)
    for random_number in random_numbers:
        received_cards.append(player.hand[random_number])
    received_cards.sort()

    game_sched.scheduler.enter(TIME_TO_SELECT_PASS_CARDS, 1, game.pass_cards_selected, (pr.game_round.game, Card.list_to_str_list(received_cards), player, turn_id))

def received_passed_cards(pr, player, passed_cards, turn_id):
    passed_cards_sorted = sorted(passed_cards)
    from_seat = player.position
    if not from_seat in pr.seats_received and pr.id == turn_id:
        with transaction.atomic():
            pr = PassRound.objects.select_for_update().get(id=pr.id)
            pr.seats_received.append(from_seat)
            seats_received_sorted = sorted(pr.seats_received)
            seat_index_in_sort = seats_received_sorted.index(from_seat)
            starting_index = seat_index_in_sort*3
            for index_offset in range(0,3):
                pr.passed_cards.insert(starting_index+index_offset, passed_cards_sorted[index_offset])
            pr.save()
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
        to_seat = (from_seat+pr.direction)%4
        
        start_index = from_seat*3
        end_index = from_seat*3+3
        cards_to_pass = pr.passed_cards[start_index:end_index]
        
        from_player = pr.game_round.game.player_set.get(position=from_seat)
        from_player.hand = sorted(list(set(from_player.hand) - set(cards_to_pass)))
        from_player.save()
        
        to_player = pr.game_round.game.player_set.get(position=to_seat)
        to_player.hand = sorted(to_player.hand + cards_to_pass)
        to_player.save()
        
def finish(pr):
    pr.active = False
    pr.save()
    grrz.send_players_their_cards(pr.game_round)
    grrz.add_first_trick_phase(pr.game_round)
    
        
        
        
        
        
        
        