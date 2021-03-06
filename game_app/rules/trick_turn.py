from channels import Group
from channels import Channel
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from game_app.multiplex_transmit import game_transmit
from game_app.card import Card
from game_app.models.trick_turn import TrickTurn
from game_app.models.player import Player
from game_app.models.player_type import PlayerType

from . import game_round as grrz

import random as rn

TRICK_BASE_MS = 5000

def setup(tt,parent_round,number,first_seat,hearts_broken):
    tt.game_round = parent_round
    tt.first_seat = first_seat
    tt.expected_seat = first_seat
    tt.number = number
    tt.hearts_broken = hearts_broken
    tt.save()
    
def start(tt):
    tt.active = True
    tt.save()
    send_turn_notification(tt)

def card_discarded(discard, player_id, turn_id, move_time):
    # If the move is invalid this function will simply return and will not
    # make any changes
    try:
        with transaction.atomic():

            tt = TrickTurn.objects.select_for_update().get(id=turn_id)
            if not tt.active:
                return

            player = Player.objects.select_for_update().get(id=player_id)


            if player.position == tt.expected_seat:
                if tt.expected_seat == tt.first_seat:
                    valid_cards = valid_cards_leader(tt, player.hand)
                else:
                    valid_cards = valid_cards_follower(tt, player.hand)

                if not discard in valid_cards:
                    return
            else:
                return

            tt.discards.append(discard)
            tt.expected_seat = get_next_expected_seat(tt)
            tt.save()

            player.hand.remove(discard)
            player.bank_ms = get_updated_bank_ms(player.bank_ms, move_time, player.time_turn_started)
            player.save()

    except ObjectDoesNotExist:
        # If the query is invalid, the turn is invalid, so don't make it
        return

    send_players_discard(tt, player, discard)

    if tt.expected_seat == tt.first_seat:
        finish(tt)
    else:
        send_turn_notification(tt)

def send_turn_notification(tt):
    player = tt.game_round.game.player_set.get(position=tt.expected_seat)
    if tt.expected_seat == tt.first_seat:
        valid_cards = valid_cards_leader(tt,player.hand)
    else:
        valid_cards = valid_cards_follower(tt,player.hand)
    grrz.send_player_valid_cards(tt.game_round, player, valid_cards)

    now = timezone.now()
    time_info = grrz.get_time_info(now, TRICK_BASE_MS, player.bank_ms)
    game_transmit(Group(tt.game_round.game.group_channel), {
        'trick':{
            'id':tt.id,
            'player':player.position,
            'time_info':time_info,
            'game_phase':tt.game_round.phase
        }
    })

    player.time_turn_started = now
    player.save()

    send_delay_message(tt, player, tt.id, valid_cards)
    
def send_delay_message(tt, player, turn_id, valid_cards):
    received_cards = []
    random_number = rn.randint(0,len(valid_cards)-1)
    received_cards.append(valid_cards[random_number])
    if player.type == PlayerType.DUMMY:
        delay = 300
    else:
        delay = player.bank_ms + TRICK_BASE_MS
    delay_message = {
        'channel':'game_command',
        'delay':delay,
        'content':{
            'command':'trick_card_selected',
            'command_args':{
                'received_cards': Card.list_to_str_list(received_cards),
                'turn_id': turn_id,
                'player_id': player.id
            }
        }
    }
    Channel('asgi.delay').send(delay_message)
            
def get_next_expected_seat(tt):
    return (tt.expected_seat+1)%4

def get_winning_player(tt):
    winning_discard = tt.discards[0]
    winning_seat_offset = 0
    for seat_offset in range(1,4):
        discard = tt.discards[seat_offset]
        if discard.suit == leading_suit(tt) and discard > winning_discard:
            winning_discard = discard
            winning_seat_offset = seat_offset
    winning_seat = (tt.first_seat+winning_seat_offset)%4
    return tt.game_round.game.player_set.get(position=winning_seat)
        
def get_trick_points(tt):
    points = 0
    for discard in tt.discards:
        if discard.suit == Card.HEARTS:
            points += 1
        if discard.suit == Card.SPADES and discard.number == 12:
            points += 13
    return points
    
def leading_suit(tt):
    '''this check is run after the first guy discards'''
    first_discard = tt.discards[0]
    return first_discard.suit

def are_hearts_now_broken(tt):
    '''this check is run after everyone discarded in a trick'''
    return get_trick_points(tt) > 0

def valid_cards_follower(tt, hand):
    valid_cards = []
    lead_suit = leading_suit(tt)
    in_suit_cards = 0
    for card in hand:
        if card.suit == lead_suit:
            in_suit_cards += 1
    if in_suit_cards != 0:
        for card in hand:
            if card.suit == lead_suit:
                valid_cards.append(card)
    else:
        if tt.number>0:
            valid_cards = hand
        else:
            for card in hand:
                if card.suit != Card.HEARTS and not (card.suit == Card.SPADES and card.number == 12):
                    valid_cards.append(card)
            if len(valid_cards)==0:
                valid_cards = hand
    return valid_cards 
    
def valid_cards_leader(tt, hand):
    valid_cards = []
    if tt.number == 0:
        valid_cards.append(Card(2,'Clubs'))
    else:
        if tt.hearts_broken:
            valid_cards = hand
        else:
            for card in hand:
                if card.suit != Card.HEARTS:
                    valid_cards.append(card)
            if len(valid_cards)==0:
                valid_cards = hand
    return valid_cards

def get_updated_bank_ms(bank_ms, time_this_move, time_turn_started):
    time_took = (time_this_move - time_turn_started).total_seconds() * 1000
    if not time_took > TRICK_BASE_MS:
        # the player didn't eat into their bank
        return bank_ms

    new_bank_ms = bank_ms - (time_took - TRICK_BASE_MS)
    if new_bank_ms < 0:
        new_bank_ms = 0
    return new_bank_ms

def send_players_discard(tt, player, discard):
    '''Sends a message to each player telling them which cards are 
    theirs'''
    discard_json = str(discard)
    game_transmit(Group(tt.game_round.game.group_channel),
                  {"discard": {"id":tt.id, "player": player.position, "card": discard_json}})  
        
def finish(tt):
    tt.active = False
    tt.save()
    if tt.hearts_broken == False:
        tt.game_round.hearts_broken = are_hearts_now_broken(tt)
        tt.game_round.save()
    winning_player = get_winning_player(tt)
    winning_player.hand_points += get_trick_points(tt)
    winning_player.save()
    grrz.send_players_their_cards(tt.game_round)
    grrz.add_trick_phase(tt.game_round,winning_player.position)
