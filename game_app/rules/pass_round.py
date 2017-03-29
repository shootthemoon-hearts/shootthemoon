from . import game_round as grrz
from channels import Group, Channel
from game_app.multiplex_transmit import game_transmit
import random as rn

def setup(pr,parent_round,direction):
    pr.direction = direction
    pr.game_round = parent_round
    pr.save()

def start(pr):
    pr.active = True
    pr.save()
    send_turn_notification(pr)
    for i in pr.game_round.game.player_set.all():
        send_delay_message(pr, i, pr.id)
    
def send_delay_message(pr, player, turn_id):
    received_cards = []
    random_numbers = rn.sample(range(0,13),3)
    for i in range(0,2):
        received_cards.append(player.hand[random_numbers[i]])
    received_cards.sort()
    received_cards_str = ""
    for card in received_cards:
        received_cards_str += card.to_json()
    delay_message = {
        'channel':'game_command',
        'delay':2000,
        'content':{
            'command':'pass_cards_selected',
            'command_args':{
                'received_cards': received_cards_str,
                'turn_id': turn_id,
                'player_id': player.id
            }
        }
    }
    Channel('asgi.delay').send(delay_message)
    
def received_passed_cards(pr, player, passed_cards, turn_id):
    passed_cards_sorted = sorted(passed_cards)
    from_seat = player.position
    if not from_seat in pr.seats_received and pr.id == turn_id:
        pr.seats_received.append(from_seat)
        seats_received_sorted = sorted(pr.seats_received)
        seat_index_in_sort = seats_received_sorted.index(from_seat)
        starting_index = seat_index_in_sort*3
        for index_offset in range(0,3):
            pr.passed_cards.insert(starting_index+index_offset, passed_cards_sorted[index_offset])
        pr.save()
        if has_everyone_passed(pr):
            set_hands_to_new_hands(pr)
            self_jihad(pr)
    
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
        
def self_jihad(pr):
    pr.active = False
    pr.save()
    grrz.send_players_their_cards(pr.game_round)
    grrz.add_first_trick_phase(pr.game_round)
    
        
        
        
        
        
        
        