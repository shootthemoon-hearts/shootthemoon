from . import game_round as grrz

def setup(pr,parent_round,direction):
    pr.direction = direction
    pr.game_round = parent_round
    pr.save()

def start(pr):
    pr.active = True
    pr.save()
    
def received_passed_cards(pr, player, passed_cards):
    passed_cards_sorted = sorted(passed_cards)
    from_seat = player.position
    if not from_seat in pr.seats_received:
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

def set_hands_to_new_hands(pr):
    for from_seat in sorted(pr.seats_received):
        to_seat = (from_seat+pr.direction)%4
        
        start_index = from_seat*3
        end_index = from_seat*3+2
        
        from_player = pr.game_round.game.player_set.get(position=from_seat)
        from_player.hand = sorted(list(set(from_player.hand) - set(pr.passed_cards[start_index:end_index])))
        from_player.save()
        
        to_player = pr.game_round.game.player_set.get(position=to_seat)
        to_player.hand = sorted(to_player.hand + pr.passed_cards[start_index:end_index])
        to_player.save()
        
def self_jihad(pr):
    pr.active = False
    pr.save()
    grrz.send_players_their_cards(pr.game_round)
    grrz.add_first_trick_phase(pr.game_round)
    
        
        
        
        
        
        
        
        