from channels import Channel
from django.db import transaction

from game_app import message_constants
from game_app.card import Card
from game_app.deck import Deck
from game_app.models.pass_round import PassRound
from game_app.models.trick_turn import TrickTurn
from game_app.multiplex_transmit import game_transmit
from game_app.rules import game
from game_app.rules import pass_round
from game_app.rules import trick_turn
from game_app.rules.game_phases import GamePhases
from game_app.rules.pass_direction import PASS_DIRECTION

NUM_CARDS_TO_PASS_NORMAL = 3
NUM_CARDS_TO_PASS_NO_PASS = 0
NUM_CARDS_TO_PASS_DICT = {
    PASS_DIRECTION.LEFT: NUM_CARDS_TO_PASS_NORMAL,
    PASS_DIRECTION.RIGHT: NUM_CARDS_TO_PASS_NORMAL,
    PASS_DIRECTION.ACROSS: NUM_CARDS_TO_PASS_NORMAL,
    PASS_DIRECTION.NO_PASS: NUM_CARDS_TO_PASS_NO_PASS
}

def setup(game_round, game, number):
    '''Sets up the given GameRound object and adds it to the given game.
    
    This function guarantees a save of the GameRound object.
    
    Arguments:
        game_round: the GameRound database entry
        game: the Game database entry
        number: the 0 index number of the game round
    '''
    game_round.game = game
    game_round.number = number
    game_round.save()
    with transaction.atomic():
        for player in game_round.game.player_set.select_for_update().all():
            player.hand_points = 0
            player.save()

def start(gr):
    gr.active = True
    gr.save()
    deck = Deck()
    deck.populate_and_randomize()
    deal_cards(gr,deck)
    send_players_their_cards(gr)
    
    pass_direction = determine_passing(gr)
    if pass_direction != PASS_DIRECTION.NO_PASS:
        add_pass_phase(gr,pass_direction)
    else:
        bypass_pass_phase(gr)
        
def deal_cards(gr, deck):
    '''Deal the cards to each player'''
    print ("Deck length", len(deck.cards))
    player_list = list(gr.game.player_set.all())
    hand_size = int(len(deck.cards)/len(player_list))
    for ind in range(0,len(player_list)):
        card_offset = ind*hand_size
        player_list[ind].hand = deck.cards[card_offset:card_offset+hand_size]
        player_list[ind].hand.sort()
        player_list[ind].save()
        print ("player %s's hand: %s" % (player_list[ind].position ,player_list[ind].hand))
        
def send_players_their_cards(gr):
    '''Sends a message to each player telling them which cards are 
    theirs'''
    for player in gr.game.player_set.all():
        cards_str = Card.list_to_str(player.hand)
        game_transmit(Channel(player.channel),{"Cards":cards_str})
        
def send_players_initial_valid_cards(gr):
    for player in gr.game.player_set.all():
        valid_cards = player.hand
        send_player_valid_cards(gr,player, valid_cards)
        
def send_player_valid_cards(gr, player, valid_cards):
    cards_str = Card.list_to_str(valid_cards)
    game_transmit(Channel(player.channel),{"valid_cards":cards_str})
        
def determine_passing(gr):
    if (gr.number) % 4 == 0:
        direction = PASS_DIRECTION.LEFT
    elif (gr.number) % 4 == 1:
        direction = PASS_DIRECTION.RIGHT
    elif (gr.number) % 4 == 2:
        direction = PASS_DIRECTION.ACROSS
    else:
        direction = PASS_DIRECTION.NO_PASS
    return direction

def add_pass_phase(gr,pass_direction):
    gr.phase = GamePhases.PASS
    gr.save()
    pr = PassRound()
    pass_round.setup(pr, gr, pass_direction)
    send_players_initial_valid_cards(gr)
    pass_round.start(pr, NUM_CARDS_TO_PASS_DICT.get(pass_direction))
    
def bypass_pass_phase(gr):
    add_first_trick_phase(gr)
    
def add_first_trick_phase(gr):
    gr.phase = GamePhases.TRICK
    gr.save()
    add_trick_phase(gr,what_seat_has_two_of_clubs(gr))

def add_trick_phase(gr,seat_to_go_first):
    if len(gr.trickturn_set.all()) >=13:
        finish(gr)
    else:
        tr = TrickTurn()
        trick_turn.setup(tr, gr, len(gr.trickturn_set.all()), seat_to_go_first, gr.hearts_broken)
        trick_turn.start(tr)

def what_seat_has_two_of_clubs(gr):
    two_of_clubs = Card(2,'Clubs')
    for player in gr.game.player_set.all():
        if two_of_clubs in player.hand:
            return player.position

def get_time_info(now, base, bank=None):
    return {
        message_constants.KEY_START_TIME: now.timestamp() * 1000,
        message_constants.KEY_BASE_MS: base,
        message_constants.KEY_BANK_MS: bank
    }

def finish(gr):
    gr.active = False
    gr.save()
    players =  list(gr.game.player_set.all())
    for i in players:
        #checking if player shot the moon and if so applying exception#
        if i.hand_points == 26:
            for j in players:
                j.hand_points = 27
            i.hand_points = 0
    for i in players:
        if i.hand_points == 27:
            i.hand_points -= 1
    for i in players:
        i.game_points += i.hand_points
        i.save()
    game.add_round(gr.game)



