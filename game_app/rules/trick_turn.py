from channels import Group
from channels import Channel

from game_app.multiplex_transmit import game_transmit
from game_app.card import Card

from . import game_round as grrz
    
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
    
    
def card_discarded(tt, player, discard):
    if player.position == tt.expected_seat:
        tt.discards.append(discard)
        tt.save()
        
        player.hand = sorted(list(set(player.hand) - set([discard])))
        player.save()
        
        send_players_discard(tt,player,discard)
        
        tt.expected_seat = get_next_expected_seat(tt)
        tt.save()
         
        if tt.expected_seat == tt.first_seat:
            self_jihad(tt)
        else:
            send_turn_notification(tt)
    
def send_turn_notification(tt):
    player = tt.game_round.game.player_set.get(position=tt.expected_seat)
    if tt.expected_seat == tt.first_seat:
        valid_cards = valid_cards_leader(tt,player.hand)
    else:
        valid_cards = valid_cards_follower(tt,player.hand)
        
    game_transmit(Channel(player.channel),{"your_turn": "true"})
    grrz.send_player_valid_cards(tt.game_round,player, valid_cards)
            
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
        if tt.hearts_broken:
            valid_cards = hand
        else:
            for card in hand:
                if card.suit != Card.HEARTS and card != Card(12,'Spades'):
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
                if card.suit != Card.HEARTS and card != Card(12,'Spades'):
                    valid_cards.append(card)
    return valid_cards

def send_players_discard(tt, player, discard):
    '''Sends a message to each player telling them which cards are 
    theirs'''
    discard_json = discard.to_json()
    game_transmit(Group(tt.game_round.game.group_channel),{"discard": {"player": player.position, "card": discard_json}})  
        
def self_jihad(tt):
    tt.active = False
    if tt.hearts_broken == False:
        tt.game_round.hearts_broken = are_hearts_now_broken(tt)
        tt.game_round.save()
    winning_player = get_winning_player(tt)
    winning_player.hand_points += get_trick_points(tt)
    winning_player.save()
    grrz.add_trick_phase(tt.game_round,winning_player.position)
